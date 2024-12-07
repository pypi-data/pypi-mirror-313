# 开发于 python3，仅需要下面两个第三方依赖，训练的数据为 labelimg 标注型的数据。
# 依赖 pytorch：（官网找安装方式）开发使用版本为 torch-1.4.0-cp36-cp36m-win_amd64.whl
# 依赖 opencv： （pip install opencv-contrib-python==3.4.1.15）
#     其实这里的 opencv 版本不重要，py3能用就行，只是个人喜欢这个版本，因为能用sift图像检测，稳。


import cv2
import numpy as np
import torch

import os
import math
import xml.dom.minidom

def read_image_meta(f):
    if f.endswith('.gif'):
        gif = cv2.VideoCapture(f)
        ret, frame = gif.read()
        return frame
    else:
        return cv2.imread(f)

# 读取voc格式文件
def read_voc_xml(file, islist=True):
    d = xml.dom.minidom.parse(file)
    v = d.getElementsByTagName('annotation')[0]
    f = v.getElementsByTagName('path')[0].firstChild.data
    if not os.path.isfile(f):
        # 如果读取 xml 内的图片文件地址失败，则会在 xml 地址寻对应名字的图片文件再试一次
        # 所以打标的图片文件应该尽量和 voc 格式的xml文件地址放在一起，增加便利
        imgname = os.path.split(f)[-1]
        xmlpath = os.path.split(file)[0]
        f = os.path.join(xmlpath, imgname)
        if not os.path.isfile(f):
            raise 'fail load img: {}'.format(f)
    size = v.getElementsByTagName('size')[0]
    npimg = read_image_meta(f)
    npimg = cv2.cvtColor(npimg, cv2.COLOR_BGR2RGB) # [y,x,c]
    npimg = cv2.resize(npimg, (416, 416))
    npimg_ = np.transpose(npimg, (2,1,0)) # [c,x,y]
    def readobj(obj):
        d = {}
        bbox = obj.getElementsByTagName('bndbox')[0]
        d['width']  = int(size.getElementsByTagName('width')[0].firstChild.data)
        d['height'] = int(size.getElementsByTagName('height')[0].firstChild.data)
        d['ratew']  = rw = d['width']/416
        d['rateh']  = rh = d['height']/416
        d['depth']  = int(size.getElementsByTagName('depth')[0].firstChild.data)
        d['cate']   = obj.getElementsByTagName('name')[0].firstChild.data
        d['xmin']   = int(bbox.getElementsByTagName('xmin')[0].firstChild.data)/rw
        d['ymin']   = int(bbox.getElementsByTagName('ymin')[0].firstChild.data)/rh
        d['xmax']   = int(bbox.getElementsByTagName('xmax')[0].firstChild.data)/rw
        d['ymax']   = int(bbox.getElementsByTagName('ymax')[0].firstChild.data)/rh
        d['w']      = d['xmax'] - d['xmin']
        d['h']      = d['ymax'] - d['ymin']
        d['rect']   = d['xmin'],d['ymin'],d['xmax'],d['ymax']
        d['centerx'] = (d['xmin'] + d['xmax'])/2.
        d['centery'] = (d['ymin'] + d['ymax'])/2.
        d['numpy']  = npimg_
        d['file'] = f
        return d
    if islist:  r = [readobj(obj) for obj in v.getElementsByTagName('object')]
    else:       r = readobj(v.getElementsByTagName('object')[0])
    return r

# 生成 y_true 用于误差计算
def make_y_true(imginfo, S, anchors, class_types, z=None):
    def get_max_match_anchor_idx(anchors, bw, bh):
        ious = []
        for aw, ah in anchors:
            mi = min(aw,bw)*min(ah,bh)
            ma = max(aw,bw)*max(ah,bh)
            ious.append(mi/(aw*ah + bw*bh - mi))
        return ious.index(max(ious))
    cx = imginfo['centerx']
    cy = imginfo['centery']
    bw = imginfo['w']
    bh = imginfo['h']
    gap = int(416/S)
    ww = list(range(416))[::int(gap)]
    for wi in range(len(ww)):
        if ww[wi] > cx: 
            break
    hh = list(range(416))[::int(gap)]
    for hi in range(len(hh)):
        if hh[hi] > cy: 
            break
    wi, hi = wi - 1, hi - 1
    sx, sy = (cx-ww[wi])/gap, (cy-hh[hi])/gap # 用ceil左上角做坐标并进行归一化
    ceillen = (5+len(class_types))
    log = math.log
    z = torch.zeros((S, S, len(anchors)*ceillen)) if z is None else z
    indx = get_max_match_anchor_idx(anchors, bw, bh)
    for i, (aw, ah) in enumerate(anchors):
        if i == indx:
            left = i*ceillen
            clz = [0.]*len(class_types)
            clz[class_types.get(imginfo['cate'])] = 1.
            v = torch.FloatTensor([sx, sy, log(bw/aw), log(bh/ah), 1.] + clz)
            z[wi, hi, left:left+ceillen] = v
    return z

def load_voc_data(xmlpath, anchors, start=0, limit=1000, file_filter=None):
    files = [os.path.join(xmlpath, path) for path in os.listdir(xmlpath) if path.endswith('.xml')][start:start+limit]
    imginfos = []
    print('use anchors:', anchors)
    print('load xml file number:{}, start.'.format(len(files)))
    for idx, file in enumerate(files):
        if file_filter and not file_filter(file): continue
        if idx % 1000 == 0: print('loading {}/{}'.format(idx, len(files)))
        xmlfiles = read_voc_xml(file, islist=True)
        imginfos.append(xmlfiles)
    print('load all file. ok.')
    for i in imginfos:
        for j in i:
            j['cate'] = 'v'
    class_types = []
    for i in imginfos:
        for j in i:
            class_types.append(j['cate'])
    print('load class types. start.')
    class_types = {typ:idx for idx,typ in enumerate(sorted(list(set(class_types))))}
    print('load class types. ok.')
    print('class_types:', class_types)
    train_data = []
    print('make x_true,y_true. start.')
    for idx, imginfo in enumerate(imginfos):
        if idx % 200 == 0: print('makeing x_true,y_true. {}/{}'.format(idx, len(files)))
        x_true = torch.FloatTensor(imginfo[0]['numpy'])
        y_true = None
        for imgy in imginfo:
            y_true = make_y_true(imgy, 13, anchors, class_types, y_true)
        train_data.append([x_true, y_true])
        # if idx % 200 == 0: print('makeing x_true,y_true. {}/{}'.format(idx, len(files)))
        # for imgy in imginfo:
        #     x_true = torch.FloatTensor(imgy['numpy'])
        #     y_true = make_y_true(imgy, 13, anchors, class_types)
        #     train_data.append([x_true, y_true])
    print('make x_true,y_true. ok.')
    return train_data, imginfos, class_types












import base64
import inspect

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.data as Data
from torch.autograd import Variable
from collections import OrderedDict

USE_CUDA = True if torch.cuda.is_available() else False
DEVICE = 'cuda' if USE_CUDA else 'cpu'
torch.set_printoptions(precision=2, sci_mode=False, linewidth=120, profile='full')

class MiniYolo(nn.Module):
    class ConvBN(nn.Module):
        def __init__(self, cin, cout, kernel_size=3, stride=1, padding=None):
            super().__init__()
            padding   = (kernel_size - 1) // 2 if not padding else padding
            self.conv = nn.Conv2d(cin, cout, kernel_size, stride, padding, bias=False)
            self.bn   = nn.BatchNorm2d(cout, momentum=0.01)
            self.relu = nn.LeakyReLU(0.01, inplace=True)
        def forward(self, x): 
            return self.relu(self.bn(self.conv(x)))
    def __init__(self, anchors, class_types, inchennel=3):
        super().__init__()
        self.oceil = len(anchors)*(5+len(class_types))
        self.model = nn.Sequential(
            OrderedDict([
                # ('ConvBN_0',  self.ConvBN(inchennel, 32)),
                # ('Pool_0',    nn.MaxPool2d(2, 2)),
                # ('ConvBN_1',  self.ConvBN(32, 48)),
                # ('Pool_1',    nn.MaxPool2d(2, 2)),
                # ('ConvBN_2',  self.ConvBN(48, 64)),
                # ('Pool_2',    nn.MaxPool2d(2, 2)),
                # ('ConvBN_3',  self.ConvBN(64, 80)),
                # ('Pool_3',    nn.MaxPool2d(2, 2)),
                # ('ConvBN_4',  self.ConvBN(80, 96)),
                # ('Pool_4',    nn.MaxPool2d(2, 2)),
                # ('ConvBN_5',  self.ConvBN(96, 102)),
                # ('ConvEND',   nn.Conv2d(102, self.oceil, 1)),
                ('ConvBN_0',  self.ConvBN(inchennel, 32)),
                ('Pool_0',    nn.MaxPool2d(2, 2)),
                ('ConvBN_1',  self.ConvBN(32, 128)),
                ('Pool_1',    nn.MaxPool2d(2, 2)),
                ('ConvBN_2',  self.ConvBN(128, 128)),
                ('Pool_2',    nn.MaxPool2d(2, 2)),
                ('ConvBN_3',  self.ConvBN(128, 128)),
                ('Pool_3',    nn.MaxPool2d(2, 2)),
                ('ConvBN_4',  self.ConvBN(128, 128)),
                ('Pool_4',    nn.MaxPool2d(2, 2)),
                ('ConvBN_5',  self.ConvBN(128, 128)),
                ('ConvEND',   nn.Conv2d(128, self.oceil, 1)),
            ])
        )
    def forward(self, x):
        return self.model(x).permute(0,2,3,1)

class yoloLoss(nn.Module):
    def __init__(self, S, anchors, class_types):
        super(yoloLoss,self).__init__()
        self.S = S
        self.B = len(anchors)
        self.clazlen = len(class_types)
        self.ceillen = (5+self.clazlen)
        self.anchors = torch.FloatTensor(anchors).to(DEVICE)

    def get_iou(self,box_pred,box_targ,anchor_idx):
        rate = 416/self.S
        pre_xy = box_pred[...,:2] * rate
        pre_wh_half = torch.exp(box_pred[...,2:4])*self.anchors[anchor_idx]/2
        pre_mins = pre_xy - pre_wh_half
        pre_maxs = pre_xy + pre_wh_half
        true_xy = box_targ[...,:2] * rate
        true_wh_half = torch.exp(box_targ[...,2:4])*self.anchors[anchor_idx]/2
        true_mins = true_xy - true_wh_half
        true_maxs = true_xy + true_wh_half

        inter_mins = torch.max(true_mins, pre_mins)
        inter_maxs = torch.min(true_maxs, pre_maxs)
        inter_wh   = torch.max(inter_maxs - inter_mins, torch.FloatTensor([0.]).to(DEVICE))
        inter_area = inter_wh[...,0] * inter_wh[...,1]
        ture_area = torch.exp(box_pred[...,2])*self.anchors[anchor_idx][0] * torch.exp(box_pred[...,3])*self.anchors[anchor_idx][1]
        pred_area = torch.exp(box_targ[...,2])*self.anchors[anchor_idx][0] * torch.exp(box_targ[...,3])*self.anchors[anchor_idx][1]
        ious = inter_area/(ture_area+pred_area-inter_area)
        return ious

    def forward(self,predict_tensor,target_tensor,callback=None):
        N = predict_tensor.size()[0]
        box_contain_loss = 0
        noo_contain_loss = 0
        locxy_loss       = 0
        locwh_loss       = 0
        loc_loss         = 0
        class_loss       = 0
        for idx in range(self.B):
            targ_tensor = target_tensor [:,:,:,idx*self.ceillen:(idx+1)*self.ceillen]
            pred_tensor = predict_tensor[:,:,:,idx*self.ceillen:(idx+1)*self.ceillen]
            coo_mask = (targ_tensor[:,:,:,4] >  0).unsqueeze(-1).expand_as(targ_tensor)
            noo_mask = (targ_tensor[:,:,:,4] == 0).unsqueeze(-1).expand_as(targ_tensor)
            if not torch.any(coo_mask): 
                noo_pred = pred_tensor[noo_mask].view(-1,self.ceillen)
                noo_targ = targ_tensor[noo_mask].view(-1,self.ceillen)
                noo_contain_loss += F.mse_loss(torch.sigmoid(noo_pred[...,4]),   noo_targ[...,4],reduction='sum')*.1
            else:
                coo_pred = pred_tensor[coo_mask].view(-1,self.ceillen)
                coo_targ = targ_tensor[coo_mask].view(-1,self.ceillen)
                noo_pred = pred_tensor[noo_mask].view(-1,self.ceillen)
                noo_targ = targ_tensor[noo_mask].view(-1,self.ceillen)

                box_pred = coo_pred[...,0:5].contiguous().view(-1,5)
                box_targ = coo_targ[...,0:5].contiguous().view(-1,5)
                class_pred = coo_pred[...,5:5+self.clazlen]
                class_targ = coo_targ[...,5:5+self.clazlen]

                box_pred[...,:2] = torch.sigmoid(box_pred[...,:2])
                ious = self.get_iou(box_pred,box_targ,idx)
                box_contain_loss += F.mse_loss(torch.sigmoid(box_pred[...,4])*ious, box_targ[...,4],reduction='sum')
                noo_contain_loss += F.mse_loss(torch.sigmoid(noo_pred[...,4]),      noo_targ[...,4],reduction='sum')*.1
                locxy_loss       += F.mse_loss(box_pred[...,0:2], box_targ[...,0:2],reduction='sum')
                locwh_loss       += F.mse_loss(box_pred[...,2:4], box_targ[...,2:4],reduction='sum')
                loc_loss         += locxy_loss + locwh_loss
                class_loss       += F.mse_loss(class_pred,class_targ,reduction='sum')
                # print('[ ious ] :', ious)
        all_loss = (box_contain_loss + noo_contain_loss + loc_loss + class_loss)/N/self.B
        global print
        print = callback if callback else print
        print(
            '[ loss ] (con|non){:>.3f}|{:>.3f},(xy|wh){:>.3f}|{:>.3f},(class){:>.3f},(all){:>.3f}.'.format(
                box_contain_loss.item(),    noo_contain_loss.item(),    locxy_loss.item(),
                locwh_loss.item(),          class_loss.item(),          all_loss.item(),
            )
        )
        return all_loss

def train(mod_filename, train_data, anchors, class_types, batch_size=10, LR=0.001):
    EPOCH = 100
    train_loader = Data.DataLoader(
        dataset    = train_data,
        batch_size = batch_size,
        shuffle    = True,
    )
    total_length = (int(len(train_data) / batch_size))
    try:
        state = torch.load(mod_filename, map_location=torch.device(DEVICE))
        net = MiniYolo(anchors, class_types)
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
        net = MiniYolo(anchors, class_types)
        net.to(DEVICE)
        optimizer = torch.optim.Adam(net.parameters(), lr=LR)
        epoch = 0
        print('new train.')
    yloss = yoloLoss(13, anchors=anchors, class_types=class_types, )
    net.train()
    for epoch in range(epoch, epoch+EPOCH):
        print('epoch', epoch)
        for step, (x_true_, y_true_) in enumerate(train_loader):
            print('[{:<3}/{}]'.format(step, total_length), end='')
            x_true = Variable(x_true_).to(DEVICE)
            y_true = Variable(y_true_).to(DEVICE)
            output = net(x_true)
            loss = yloss(output, y_true)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        state = {'net':net.state_dict(), 'optimizer':optimizer, 'epoch':epoch+1, 'MiniYolo': inspect.getsource(MiniYolo), 
                 'anchors':anchors, 'class_types':class_types}
        torch.save(state, mod_filename)
        print('save.')
    print('end.')














