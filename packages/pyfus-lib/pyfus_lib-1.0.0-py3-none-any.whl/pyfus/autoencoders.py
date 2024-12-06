import torch
import os
import numpy as np
import torch.nn.functional as F
import time, copy, math
#from torchvision import transforms, utils#, models
from torch.utils.data import Dataset, DataLoader
from torch import nn, optim
from collections import OrderedDict
from sklearn.metrics import confusion_matrix
from sklearn.decomposition import PCA, FastICA
from sklearn.manifold import TSNE
from scipy.io import loadmat
import h5py, pickle
import matplotlib.pyplot as plt



class DatasetCAE(Dataset):

    def __init__(self, data, add_noise=False):
        """
        @args:
            images_list (string): path to the txt file containing the list of images (without extension) in the dataset
            root_dir (string): directory with all the images
            :bool add_noise: whether or not to add noise to sample data.
        """
        self.dataset = data
        self.add_noise = add_noise

    def __len__(self):
        return(len(self.dataset))

    def __getitem__(self, idx):

        signal = np.array([self.dataset[idx]])
        sample = {'signal': torch.from_numpy(signal).float()}

        return(sample)



class CAE_model(nn.Module):


    def __init__(self, code_length, n_frames):

        super(CAE_model, self).__init__()

        self.code_length = code_length
        self.n_frames = n_frames

        self.conv_params = {'in_channels':  [1, 32, 64, 128],
                 'out_channels': [32, 64, 128, 256],
                 'kernel_size':  [3, 3, 5, 7],
                 'stride':       [1, 2, 2, 2]}
        self.signal_size_postconv, self.last_out = self.output_size_calculator()
        self.compute_output_padding()

        self.convs, self.t_convs = [], []
        for i, o, k, s, p in zip(self.conv_params['in_channels'],
                              self.conv_params['out_channels'],
                              self.conv_params['kernel_size'],
                              self.conv_params['stride'],
                              self.conv_params['t_output_padding']):
            self.convs.append(nn.Conv1d(i, o, k, stride=s))
            self.convs.append(nn.ReLU())
            #self.convs.append(nn.BatchNorm1d(o))
            self.t_convs.append(nn.ReLU())
            self.t_convs.append(nn.ConvTranspose1d(o, i, k, stride=s, output_padding=p))
        self.t_convs.reverse()

        self.convs = nn.ModuleList(self.convs)
        self.fc = nn.Linear(self.signal_size_postconv*self.last_out, code_length)
        self.t_fc = nn.Linear(code_length, self.signal_size_postconv*self.last_out)
        self.t_convs = nn.ModuleList(self.t_convs)


    def output_size_calculator(self):

        size_ = self.n_frames
        for k, s in zip(self.conv_params['kernel_size'], self.conv_params['stride']):
            size_ = int((size_ - k) / s) + 1
        return(size_, self.conv_params['out_channels'][-1])


    def compute_output_padding(self):

        out_conv_shape = lambda i, k, s: math.floor((i - k)/s + 1)
        out_t_conv_shape = lambda i, k, s, o: (i - 1) * s + k + o
        res = []

        out, t_out = [self.n_frames], [self.signal_size_postconv]
        i, t_i = self.n_frames, self.signal_size_postconv

        for k, s in zip(self.conv_params['kernel_size'],
                        self.conv_params['stride']):
            new_i = out_conv_shape(i, k, s)
            out.append(new_i)
            i = new_i
        out.reverse()

        padding = []
        for idx, (k, s) in enumerate(zip(np.flip(self.conv_params['kernel_size']),
                                         np.flip(self.conv_params['stride']))):
            padding.append(out[idx+1] - out_t_conv_shape(t_i, k, s, 0))
            new_t_i = out_t_conv_shape(t_i, k, s, padding[idx])
            #print(t_i, k, s, padding[idx])
            t_i = new_t_i
            t_out.append(new_t_i)

        padding.reverse()
        self.conv_params['t_output_padding'] = padding


    def forward(self, x):

        # encoding
        for conv in self.convs:
            x = conv(x)
        z = F.relu(self.fc(x.view(-1, self.signal_size_postconv*self.last_out)))
        #z = torch.squeeze(z)

        # decoding
        x = F.relu(self.t_fc(z))
        x = x.view([-1, self.last_out, self.signal_size_postconv])
        for t_conv in self.t_convs:
            x = t_conv(x)

        return(x, z)


    def encode(self, x):

        #encoding
        for conv in self.convs:
            x = conv(x)
        z = F.relu(self.fc(x.view(-1, self.signal_size_postconv*self.last_out)))

        return(z)



class CAE:


    def __init__(self, params, weights=None):

        self.params = params
        self.loss_func = nn.MSELoss()

        model = CAE_model(self.params['code_length'], self.params['n_frames'])
        if weights:
            model.load_state_dict(torch.load(weights, weights_only=True))

        #print(model)

        dev = torch.device(F"cuda:{self.params['gpu_id']}") if torch.cuda.is_available() else torch.device("cpu")

        self.model = model.to(dev)
        self.dev = dev

        self.opt = optim.Adam(self.model.parameters(), lr=self.params['lr'],
                             weight_decay=self.params['wd'])


    def load_weights(self, path, convert=False):
        if convert:
            weights = convert_weights(path)
        else:
            weights = torch.load(path, weights_only=True)
        self.model.load_state_dict(weights)


    def create_batches(self):

        pass


    def fit(self, data):

        #data = data[np.random.choice(data.shape[0], int(data.shape[0]*0.5), replace=False), :]
        dataset = DatasetCAE(data+1)
        ds_size = len(dataset)
        self.data_loader = torch.utils.data.DataLoader(dataset, batch_size=self.params['bs'], shuffle=True)

        print("MODEL : {}\n".format(self.params['model']))
        print("BATCH_SIZE : {}\n".format(self.params['bs']))

        file = "{}_BS{}_LR{}.txt".format(self.params['model'],
                self.params['bs'], self.params['lr'])

        with open('records\\'+file, 'w') as infos:
            infos.write("MODEL {}\n".format(self.params['model']))
            infos.write("EPOCHS {}\n".format(self.params['e']))
            infos.write("BATCH_SIZE {}\n".format(self.params['bs']))
            infos.write("LEARNING_RATE {}\n".format(self.params['lr']))
            infos.write("MOMENTUM {}\n".format(self.params['m']))
            infos.write("WEIGHT_DECAY {}\n".format(self.params['wd']))

        for epoch in range(self.params['e']):

            print("EPOCH : {}".format(epoch+1))
            timestamp = time.time()

            self.model.train()
            total_loss = 0

            for dic in self.data_loader:

                xb = dic['signal'].to(self.dev)
                with torch.set_grad_enabled(True):
                    y, _ = self.model(xb)
                    #print(xb.size(), y.size(), yb.size())
                    #print(y)
                    #print(y, yb)
                    loss = self.loss_func(y, xb)
                    #print(loss)
                    loss.backward()
                    #print(self.model.conv1.weight.grad)
                    self.opt.step()
                    self.opt.zero_grad()
                    total_loss += loss.item() * xb.size(0)
                #print(loss)
            #print(self.model.conv1.weight, self.model.t_conv1.weight)

            val_loss = total_loss / ds_size
            #### conversion to % of signal
            val_loss = np.sqrt(val_loss)*100

            print("{} :   Loss = {}%".format("training", val_loss))

            with open("records\\"+file, 'a') as dst:
                    dst.write("{} {}\n".format(epoch+1, val_loss))

            timestamp = time.time() - timestamp
            h = timestamp//3600
            timestamp %= 3600
            m = timestamp//60
            timestamp %= 60
            s = timestamp

            print("EXECUTION TIME : {}h{}m{}s\n\n".format(int(h), int(m), int(s)))
            torch.save(self.model.state_dict(), ".\\weights\\weights_{}_BS{}_LR{}_{}.pt".format(self.params['model'], self.params['bs'], self.params['lr'], epoch+1))


    def test_reconstruction(self, data):

        dataset = DatasetCAE(data+1)
        ds_size = len(dataset)
        self.data_loader = torch.utils.data.DataLoader(dataset, batch_size=1, shuffle=False)

        self.model.eval()
        for dic in self.data_loader:
            x = dic["signal"].to(m.dev)
            if torch.max(torch.abs(x)).item() > 1.2 or torch.min(torch.abs(x)).item() < 0.8:
                y, _ = m.model(x)
            #c = m.model.encode(x)
            #print(c)
            #print(y)
                x, y = np.squeeze(x.detach().cpu().numpy()), np.squeeze(y.detach().cpu().numpy())
                plt.figure()
                #plt.subplot(1,2,1)
                plt.plot(x, color='blue')
                plt.plot(y, color='red')
                plt.ylim(0.5, 1.5)
                #plt.subplot(1,2,2)
                plt.show()


    def encode_dataset(self, data):

        print("Encoding with model : {}\n".format(self.params['model']))

        dataset = DatasetCAE(data+1)
        ds_size = len(dataset)
        self.data_loader = torch.utils.data.DataLoader(dataset, batch_size=self.params['bs'], shuffle=False)

        self.model.eval()

        for i, dic in enumerate(self.data_loader):

            xb = dic['signal'].to(self.dev)
            with torch.set_grad_enabled(False):
                c = self.model.encode(xb)

            c = np.squeeze(c.detach().cpu().numpy())
            if i == 0:
                codes_array = c
            else:
                codes_array = np.vstack((codes_array, c))

        name = self.params['model']
        np.save(F'codes_{name}.npy', codes_array)


    def predict(self, data):

        dataset = DatasetCAE(data+1)
        ds_size = len(dataset)
        self.data_loader = torch.utils.data.DataLoader(dataset, batch_size=self.params['bs'], shuffle=False)

        self.model.eval()

        for i, dic in enumerate(self.data_loader):

            xb = dic['signal'].to(self.dev)
            with torch.set_grad_enabled(False):
                c = self.model.encode(xb)

            c = np.squeeze(c.detach().cpu().numpy())
            if i == 0:
                codes_array = c
            else:
                codes_array = np.vstack((codes_array, c))

        return(codes_array)



def visualize_encoding(code_file_cae, code_file_pca):

    data = np.load(code_file_cae)
    print(data.shape)
    data = data[np.random.choice(data.shape[0], int(data.shape[0]*0.1), replace=False), :]
    print(data.shape)

    fig = plt.figure()
    plt.title("CAE")
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(data[:,0], data[:,1], data[:,2], s=0.1)

    data = np.load(code_file_pca)
    data = data[np.random.choice(data.shape[0], int(data.shape[0]*0.1), replace=False), :]

    fig = plt.figure()
    plt.title("PCA")
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(data[:,0], data[:,1], data[:,2], s=0.1)

    plt.show()


if __name__ == '__main__':


    n_frames = 206
    epochs = 20
    bs = 4096 #131072 #32768 #65536

    lr = 0.00025 #0.01
    momentum = 0.9
    weight_decay = 0.00005

    code_length = 20
    gpu_id = 1

    model_name = F"CAE_CL{code_length}_test_deep2"

    params = {'model':model_name, 'e':epochs, 'bs':bs, 'lr':lr, 'm':momentum, 'n_frames':n_frames,
              'wd':weight_decay, 'code_length':code_length, 'gpu_id':gpu_id}

    data = np.load('E:/17-brainpain/test_cae.npy')

    m = CAE(params)#, weights="weights/weights_CAE_CL3_test_deep_BS4096_LR0.00025_30.pt")
    #pickle.dump(m, open('cae_test.p', 'wb'))
    m.fit(data)
    #m.load_weights("weights/weights_CAE_CL3_test_BS1024_LR0.00025_20.pt")
    m.test_reconstruction(data)
    m.encode_dataset(data)


    #model = PCA(code_length)
    #X = model.fit_transform(data)
    #np.save(F'codes_PCA_{code_length}.npy', X)

    visualize_encoding("codes_CAE_CL3_test_deep.npy", "codes_PCA_3.npy")
