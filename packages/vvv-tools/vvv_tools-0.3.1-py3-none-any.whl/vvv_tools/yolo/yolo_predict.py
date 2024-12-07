# coding=utf-8
# pip install opencv-contrib-python torch torchvision torchaudio -i https://pypi.tuna.tsinghua.edu.cn/simple/

import os
import math
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

def make_predict_yolo_func(mod_filename):
    def load_net(filename=None):
        state = torch.load(filename, map_location=torch.device(DEVICE))
        anchors = state['anchors']
        class_types = state['class_types']
        vars = {}
        exec(state['MiniYolo'], globals(), vars)
        MiniYolo = vars['MiniYolo']
        net = MiniYolo(anchors, class_types)
        net.load_state_dict(state['net'])
        net.to(DEVICE)
        net.eval()
        state['net'] = net
        return state
    def make_get_model_func(state):
        net = state['net'].to(DEVICE)
        # 将经过 backbone 的矩阵数据转换成坐标和分类名字
        def parse_y_pred(ypred, anchors, class_types, islist=False, threshold=0.2, nms_threshold=0.6):
            ceillen = 5+len(class_types)
            sigmoid = lambda x:1/(1+np.exp(-x))
            infos = []
            for idx in range(len(anchors)):
                a = ypred[:,:,:,4+idx*ceillen]
                for ii,i in enumerate(a[0]):
                    for jj,j in enumerate(i):
                        infos.append((ii,jj,idx,sigmoid(j)))
            infos = sorted(infos, key=lambda i:-i[3])
            def get_xyxy_clz_con(info):
                gap = 416/ypred.shape[1]
                x,y,idx,con = info
                gp = idx*ceillen
                contain = sigmoid(ypred[0,x,y,gp+4])
                pred_xy = sigmoid(ypred[0,x,y,gp+0:gp+2])
                pred_wh = ypred[0,x,y,gp+2:gp+4]
                pred_clz = ypred[0,x,y,gp+5:gp+5+len(class_types)]
                exp = math.exp
                cx, cy = map(float, pred_xy)
                rx, ry = (cx + x)*gap, (cy + y)*gap
                rw, rh = map(float, pred_wh)
                rw, rh = exp(rw)*anchors[idx][0], exp(rh)*anchors[idx][1]
                clz_   = list(map(float, pred_clz))
                xx = rx - rw/2
                _x = rx + rw/2
                yy = ry - rh/2
                _y = ry + rh/2
                np.set_printoptions(precision=2, linewidth=200, suppress=True)
                log_cons = sigmoid(ypred[:,:,:,gp+4])
                log_cons = np.transpose(log_cons, (0, 2, 1))
                for key in class_types:
                    if clz_.index(max(clz_)) == class_types[key]:
                        clz = key
                        break
                return [xx, yy, _x, _y], clz, con, log_cons
            def nms(infos):
                if not infos: return infos
                def iou(xyxyA,xyxyB):
                    ax1,ay1,ax2,ay2 = xyxyA
                    bx1,by1,bx2,by2 = xyxyB
                    minx, miny = max(ax1,bx1), max(ay1, by1)
                    maxx, maxy = min(ax2,bx2), min(ay2, by2)
                    intw, inth = max(maxx-minx, 0), max(maxy-miny, 0)
                    areaA = (ax2-ax1)*(ay2-ay1)
                    areaB = (bx2-bx1)*(by2-by1)
                    areaI = intw*inth
                    return areaI/(areaA+areaB-areaI)
                rets = []
                infos = infos[::-1]
                while infos:
                    curr = infos.pop()
                    if rets and any([iou(r[0], curr[0]) > nms_threshold for r in rets]):
                        continue
                    rets.append(curr)
                return rets
            if islist:
                v = [get_xyxy_clz_con(i) for i in infos if i[3] > threshold]
                if nms_threshold:
                    return nms(v)
                else:
                    return v
            else:
                return get_xyxy_clz_con(infos[0])
        def get_predict(filepath, predict_clz=None, pre_deal_img=pre_deal_img):
            net = state['net']
            anchors = state['anchors']
            class_types = state['class_types']
            if type(filepath) == str:
                npimg = read_image_meta(filepath)
            else:
                npimg = filepath
            bkimg = pre_deal_img(npimg) if pre_deal_img else npimg.copy()
            height, width = bkimg.shape[:2]
            npimg = cv2.cvtColor(bkimg, cv2.COLOR_BGR2RGB) # [y,x,c]
            npimg = cv2.resize(npimg, (416, 416))
            npimg_ = np.transpose(npimg, (2,1,0)) # [c,x,y]
            y_pred = net(torch.FloatTensor(npimg_).unsqueeze(0).to(DEVICE))
            if USE_CUDA:
                y_pred = y_pred.cpu().detach().numpy()
            else:
                y_pred = y_pred.detach().numpy()
            v = parse_y_pred(y_pred, anchors, class_types, islist=True, threshold=0.2, nms_threshold=0.1)
            r = []
            for i in v:
                rect, clz, con, log_cons = i
                rw, rh = width/416, height/416
                rect[0],rect[2] = int(rect[0]*rw),int(rect[2]*rw)
                rect[1],rect[3] = int(rect[1]*rh),int(rect[3]*rh)
                x = (rect[0] + rect[2])/2.
                y = (rect[1] + rect[3])/2.
                if y < 35 or y > 45: continue
                print(y)
                area = (rect[3]-rect[1]) * (rect[2]-rect[0])
                _img = bkimg[rect[1]:rect[3], rect[0]:rect[2]]
                if predict_clz:
                    clz = predict_clz(_img)
                r.append([rect, clz, con, log_cons, area])
            r = sorted(r, key=lambda v:v[0][0])
            def insert_(x):
                p = None
                r = []
                for i in x:
                    rect, clz, con, log_cons, area = i
                    c = (rect[0], rect[1], rect[2], rect[3])
                    if not p:
                        if c[0] > 30:
                            pass
                    else:
                        if c[0] - p[2]>20:
                            if p[3] - p[1] < 28:
                                rect = (p[2], p[1]-10, c[0], p[3]+10)
                            else:
                                rect = (p[2], p[1], c[0], p[3])
                            _img = bkimg[rect[1]:rect[3], rect[0]:rect[2]]
                            if predict_clz:
                                clz = predict_clz(_img)
                            print('插入')
                            r.append([rect, clz, con, log_cons, area])
                    p = c
                    r.append(i)
                return r
            r = insert_(r)
            return [[rect, clz, con, area] for rect, clz, con, log_cons, area in r]
        return get_predict
    try:
        return make_get_model_func(load_net(mod_filename))
    except:
        import traceback
        excp = traceback.format_exc()
        print(excp)










def pre_deal_img(img):
    # 如果图片存在预处理，那么这里需要根据图片的预处理提前处理了图片才好做识别
    npimg = img.copy()
    npimg = cv2.addWeighted(npimg, 1.5, npimg, -0.5, 0)
    _, npimg = cv2.threshold(npimg, 178, 255, cv2.THRESH_BINARY)
    npimg[np.logical_not(np.all(npimg < 150, axis=2))] = 255
    return npimg

def read_image_meta(f):
    if f.endswith('.gif'):
        gif = cv2.VideoCapture(f)
        ret, frame = gif.read()
        return frame
    else:
        return cv2.imread(f)

def drawrect(img, rect, text):
    cv2.rectangle(img, tuple(rect[:2]), tuple(rect[2:]), (10,250,10), 2, 1)
    x, y = rect[:2]
    def cv2ImgAddText(img, text, left, top, textColor=(0, 255, 0), textSize=20):
        from PIL import Image, ImageDraw, ImageFont
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img)
        fontText = ImageFont.truetype( "font/simsun.ttc", textSize, encoding="utf-8")
        draw.text((left, top), text, textColor, font=fontText)
        return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
    import re
    if re.findall('[\u4e00-\u9fa5]', text):
        img = cv2ImgAddText(img, text, x, y, (10,10,250), 12) # 如果存在中文则使用这种方式绘制文字
        # img = cv2ImgAddText(img, text, x, y-12, (10,10,250), 12) # 如果存在中文则使用这种方式绘制文字
    else:
        cv2.putText(img, text, (x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (10,10,250), 1)
    return img

def file_filter(filename):
    return True
    fls = ['10d3b8dc4b074cfdb31db59c2260642c_28.jpg',]
    print(filename)
    for i in fls:
        if i.split('.')[0] in filename:
            return True

predict_yolo = make_predict_yolo_func('./mods/yolo_net.pkl')

testpath = './imgs/data_4'
v = [os.path.join(testpath, i) for i in os.listdir(testpath) if i.lower().endswith('.jpg') or i.lower().endswith('.png') or i.lower().endswith('.gif')]
# v = v[::-1]
for i in v:
    print(i)
    if not file_filter(i): continue
    r = predict_yolo(i, pre_deal_img=pre_deal_img)
    img = pre_deal_img(read_image_meta(i))
    for i in r:
        _rect, clz, con, area = i
        print(_rect, area)
        img = drawrect(img, _rect, '{}|{:<.2f}'.format('x', con))
    cv2.imshow('test', img)
    cv2.waitKey(0)