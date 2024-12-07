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

def make_predict_func(mod_filename):
    def load_state(filename=None):
        state = torch.load(filename, map_location=torch.device(DEVICE))
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
    return make_get_class_func(load_state(mod_filename))

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
        def parse_y_pred(ypred, anchors, class_types, islist=False, threshold=0.2, nms_threshold=None):
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
        def get_predict(filepath, predict_clz=None):
            net = state['net']
            anchors = state['anchors']
            class_types = state['class_types']
            if type(filepath) == str:
                npimg = read_image_meta(filepath)
            else:
                npimg = filepath
            img = npimg.copy()
            height, width = npimg.shape[:2]
            npimg = cv2.cvtColor(npimg, cv2.COLOR_BGR2RGB) # [y,x,c]
            npimg = cv2.resize(npimg, (416, 416))
            npimg_ = np.transpose(npimg, (2,1,0)) # [c,x,y]
            y_pred = net(torch.FloatTensor(npimg_).unsqueeze(0).to(DEVICE))
            if USE_CUDA:
                y_pred = y_pred.cpu().detach().numpy()
            else:
                y_pred = y_pred.detach().numpy()
            v = parse_y_pred(y_pred, anchors, class_types, islist=True, threshold=0.2, nms_threshold=0.2)
            r = []
            for i in v:
                rect, clz, con, log_cons = i
                rw, rh = width/416, height/416
                rect[0],rect[2] = int(rect[0]*rw),int(rect[2]*rw)
                rect[1],rect[3] = int(rect[1]*rh),int(rect[3]*rh)
                _img = img[rect[1]:rect[3], rect[0]:rect[2]]
                if predict_clz:
                    clz = predict_clz(_img)
                r.append([rect, clz, con, log_cons])
            r = sorted(r, key=lambda v:v[0][0])
            return [[rect, clz, con] for rect, clz, con, log_cons in r]
        return get_predict
    try:
        return make_get_model_func(load_net(mod_filename))
    except:
        import traceback
        excp = traceback.format_exc()
        print(excp)

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

def make_pre_files(fname, shape, r):
    f = []
    for _rect, clz, con in r:
        f.append(('''
  <object>
      <name>%s</name>
      <bndbox>
          <xmin>%s</xmin>
          <ymin>%s</ymin>
          <xmax>%s</xmax>
          <ymax>%s</ymax>
      </bndbox>
  </object>
    ''' % (urllib.parse.unquote(clz), *_rect)).strip())
    return '''
<annotation>
  <filename>%s</filename>
  <path>%s</path>
  <size>
      <width>%s</width>
      <height>%s</height>
      <depth>%s</depth>
  </size>
  %s
</annotation>
''' % (fname, fname, shape[1], shape[0], shape[2], '\n'.join(f))

import shutil
import urllib.parse
get_clazz = make_predict_func('../mods/clz_net.pkl')
predict_yolo = make_predict_yolo_func('../mods/yolo_net.pkl')

srcp = './data_2'
tarp = './data_3'
if not os.path.isdir(tarp):
    os.mkdir(tarp)

for i in os.listdir(srcp):
    sf = os.path.join(srcp, i)
    tf = os.path.join(tarp, i)
    if i.endswith('.jpg') or i.endswith('.png') or i.endswith('.gif'):
        r = predict_yolo(sf, get_clazz)
        img = read_image_meta(sf)
        f =''
        for ii in r:
            _rect, clz, con = ii
            clz = urllib.parse.unquote(clz)
            print(_rect, clz)
            f += clz
            img = drawrect(img, _rect, '{}|{:<.2f}'.format(clz, con))

        # pfile = make_pre_files(i, img.shape, r)
        # tf2 = tf.rsplit('.', 1)[0] + '.xml'
        # with open(tf2, 'w', encoding='utf-8') as f:
        #     f.write(pfile)
        # print(tf2)
        print(f)
        cv2.imshow('test', img)
        cv2.waitKey(0)

    # shutil.copy2(sf, tf)

