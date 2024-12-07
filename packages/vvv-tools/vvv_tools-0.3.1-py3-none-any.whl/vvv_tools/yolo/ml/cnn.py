# coding=utf-8
# pip install opencv-contrib-python torch torchvision torchaudio -i https://pypi.tuna.tsinghua.edu.cn/simple/

import os
import base64
import inspect
import cv2
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.data as Data
from torch.autograd import Variable
from collections import OrderedDict

USE_CUDA = True if torch.cuda.is_available() else False
DEVICE = 'cuda' if USE_CUDA else 'cpu'
torch.set_printoptions(precision=2, sci_mode=False, linewidth=120, profile='full')

def read_imginfos(file, class_types_list):
    class_types = set()
    imginfos = []
    if class_types_list:
        class_types = list(class_types_list)
    else:
        for name in os.listdir(file):
            class_types.add(name)
        class_types = sorted(class_types)
    for clazz in os.listdir(file):
        clazzfilepath = os.path.join(file, clazz)
        for imgfile in os.listdir(clazzfilepath):
            imgfile = os.path.join(clazzfilepath, imgfile)
            fil = imgfile
            img = cv2.imdecode(np.fromfile(fil, dtype=np.uint8), 1)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # [y,x,c]
            img = cv2.resize(img, (40, 40))
            img = np.transpose(img, (2,1,0)) # [c,x,y]
            imginfo = {}
            imginfo['class'] = clazz
            imginfo['img'] = img
            imginfos.append(imginfo)
            # cv2.imshow('test', img)
            # cv2.waitKey(0)
    class_types = {tp: idx for idx, tp in enumerate(class_types)}
    return imginfos, class_types

def make_y_true(imginfo, class_types):
    img = imginfo['img']
    class_types.get(imginfo['class'])
    clz = [0.]*len(class_types)
    clz[class_types.get(imginfo['class'])] = 1.
    return torch.FloatTensor(clz)

def load_data(filepath, class_types_list=None):
    imginfos, class_types = read_imginfos(filepath, class_types_list)
    train_data = []
    print(len(imginfos))
    for imginfo in imginfos:
        train_data.append([torch.FloatTensor(imginfo['img']), make_y_true(imginfo, class_types)])
    return train_data, class_types

class MiniCNN(nn.Module):
    class ConvBN(nn.Module):
        def __init__(self, cin, cout, kernel_size=3, stride=1, padding=None):
            super().__init__()
            padding   = (kernel_size - 1) // 2 if not padding else padding
            self.conv = nn.Conv2d(cin, cout, kernel_size, stride, padding, bias=False)
            self.bn   = nn.BatchNorm2d(cout, momentum=0.01)
            self.relu = nn.LeakyReLU(0.1, inplace=True)
        def forward(self, x): 
            return self.relu(self.bn(self.conv(x)))
    def __init__(self, class_types, inchennel=3):
        super().__init__()
        self.oceil = len(class_types)
        self.model = nn.Sequential(
            OrderedDict([
                # ('ConvBN_0',  self.ConvBN(inchennel, 32)),
                # ('Pool_0',    nn.MaxPool2d(2, 2)),
                # ('ConvBN_1',  self.ConvBN(32, 64)),
                # ('Pool_1',    nn.MaxPool2d(2, 2)),
                # ('ConvBN_2',  self.ConvBN(64, 32)),
                # ('Pool_2',    nn.MaxPool2d(2, 2)),
                # ('ConvBN_3',  self.ConvBN(32, 8)),
                # ('Flatten',   nn.Flatten()),
                # ('Linear1',    nn.Linear(200, 64)),
                # ('Linear2',    nn.Linear(64, self.oceil)),
                ('ConvBN_0',  self.ConvBN(inchennel, 32)),
                ('Pool_0',    nn.MaxPool2d(2, 2)),
                ('ConvBN_1',  self.ConvBN(32, 64)),
                ('Pool_1',    nn.MaxPool2d(2, 2)),
                ('ConvBN_2',  self.ConvBN(64, 128)),
                ('Pool_2',    nn.MaxPool2d(2, 2)),
                ('ConvBN_3',  self.ConvBN(128, 256)),
                ('Flatten',   nn.Flatten()),
                ('Linear1',    nn.Linear(6400, 128)),
                ('Linear2',    nn.Linear(128, self.oceil)),
            ])
        )
    def forward(self, x):
        x = torch.sigmoid(self.model(x))
        return x

def train(mod_filename, train_data, class_types, batch_size=1000):
    EPOCH = 10000
    LR = 0.0001
    try:
        state = torch.load(mod_filename, map_location=torch.device(DEVICE))
        net = MiniCNN(class_types)
        net.load_state_dict(state['net'])
        net.to(DEVICE)
        optimizer = state['optimizer']
        epoch = state['epoch']
        print('load train.')
    except:
        import traceback
        excp = traceback.format_exc()
        if 'FileNotFoundError' not in excp:
            print(traceback.format_exc())
        net = MiniCNN(class_types)
        net.to(DEVICE)
        optimizer = torch.optim.Adam(net.parameters(), lr=LR)
        epoch = 0
        print('new train.')
    mloss = miniloss(class_types).to(DEVICE)
    optimizer = torch.optim.Adam(net.parameters(), lr=LR)
    train_loader = Data.DataLoader(
        dataset=train_data,
        batch_size=batch_size,
        shuffle=True,
    )
    for epoch in range(epoch, epoch+EPOCH):
        print('epoch', epoch)
        for step, (b_x, b_y) in enumerate(train_loader):
            b_x = Variable(b_x).to(DEVICE)
            b_y = Variable(b_y).to(DEVICE)
            print(b_y.shape)
            loss = mloss(net(b_x), b_y)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        state = {'net':net.state_dict(), 'MiniCNNcode': inspect.getsource(MiniCNN), 'optimizer':optimizer, 'epoch':epoch+1, 'class_types':class_types}
        torch.save(state, mod_filename)
        print('save.')
    print('end.')

class miniloss(nn.Module):
    def __init__(self, class_types):
        super().__init__()
        self.clazlen = len(class_types)

    def forward(self, pred, targ, callback=None):
        loss = F.mse_loss(pred,targ,reduction='sum')
        global print
        print = callback if callback else print
        print(loss)
        return loss



















