# coding=utf-8

import io
import base64
import os
import cv2
import numpy as np
import torch
import torch.nn as nn
from collections import OrderedDict

USE_CUDA = True if torch.cuda.is_available() else False
DEVICE = 'cuda' if USE_CUDA else 'cpu'
torch.set_printoptions(precision=2, sci_mode=False, linewidth=120, profile='full')

def read_img_by_base64(b64img, readtype=1):
    img = base64.b64decode(b64img.encode())
    image = cv2.imdecode(np.frombuffer(img, np.uint8), readtype)
    return image

def make_predict_func():
    def load_state(filename=None):
        state = torch.load(filename, map_location=torch.device('cpu'))

        class_types = state['class_types']
        vars = {}
        exec(state['MiniCNNcode'], globals(), vars)
        MiniCNN = vars['MiniCNN']
        net = MiniCNN(class_types)
        net.load_state_dict(state['net'])
        net.to(DEVICE)
        net.eval()
        state['net'] = net
        return state
    def make_get_class_func(state):
        net = state['net'].to(DEVICE)
        def get_class(filepath):
            class_types = state['class_types']
            class_types = [i[0] for i in sorted(class_types.items(), key=lambda e:e[1])]
            if type(filepath) == str:
                img = cv2.imdecode(np.fromfile(filepath, dtype=np.uint8), 1)
            else:
                img = filepath
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # [y,x,c]
            img = cv2.resize(img, (40, 40))
            img = np.transpose(img, (2,1,0)) # [c,x,y]
            x = torch.FloatTensor(img).unsqueeze(0).to(DEVICE)
            v = net(x)
            if USE_CUDA:
                v = v.cpu().detach().numpy()
            else:
                v = v.detach().numpy()
            v = v[0].tolist()
            r = class_types[v.index(max(v))]
            return r
        return get_class
    return make_get_class_func(load_state('./mods/clz_net.pkl'))


root = './imgs/cnn_clz'

get_clazz = make_predict_func()

p = 0
q = 0
for clazz in os.listdir(root):
    filepath = os.path.join(root, clazz)
    for j in os.listdir(filepath):
        imgpath = os.path.join(filepath, j)
        t = get_clazz(imgpath)
        if t == clazz:
            p += 1
        else:
            print('    ', t, imgpath)
            # img = cv2.imdecode(np.fromfile(imgpath, dtype=np.uint8), 1)
            # cv2.imshow('test', img)
            # cv2.waitKey(0)
            q += 1
        # print(t)
        # break
        if (p + q) % 100 == 0:
            print('aaa', p, 'bbb', q, 'ccc', p/(p+q))