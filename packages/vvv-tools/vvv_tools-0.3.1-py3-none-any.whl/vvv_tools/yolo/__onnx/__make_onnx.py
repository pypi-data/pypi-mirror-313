import os
import math
import json
import base64
import inspect
import cv2
import numpy as np
import torch
import torch.nn as nn
import torch.onnx
import torch.nn.functional as F
import torch.utils.data as Data
from torch.autograd import Variable
from collections import OrderedDict

USE_CUDA = True if torch.cuda.is_available() else False
DEVICE = 'cuda' if USE_CUDA else 'cpu'
torch.set_printoptions(precision=2, sci_mode=False, linewidth=120, profile='full')
DEVICE = 'cpu'

def load_predict_func(mod_filename):
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
    return load_state(mod_filename)

def load_predict_yolo_func(mod_filename):
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
    return load_net(mod_filename)

g_code_clz = None
g_code_yolo = None
g_code_clz_tail = None
g_code_yolo_tail = None

def make_p_clz_code(mod):
    global g_code_clz, g_code_yolo, g_code_clz_tail, g_code_yolo_tail
    g_code_clz = ('''
def load_mod_predict_clz(model_path, class_types):
    ort_session = ort.InferenceSession(model_path)
    input_name = ort_session.get_inputs()[0].name
    class_types = [i[0] for i in sorted(class_types.items(), key=lambda e:e[1])]
    def _(filepath):
        if type(filepath) == str:
            img = cv2.imdecode(np.fromfile(filepath, dtype=np.uint8), 1)
        else:
            img = filepath
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (40, 40))
        img = np.transpose(img, (2,1,0))
        x = np.expand_dims(img.astype(np.float32), axis=0)
        result = ort_session.run(None, {input_name: x})
        v = result[0][0].tolist()
        r = unquote(class_types[v.index(max(v))])
        return r
    return _
    ''').strip()
    g_code_clz_tail = ('''predict_clz_func = load_mod_predict_clz('predict_clz.onnx', class_types='''+json.dumps(mod['class_types'])+r''')''').strip()
    return g_code_clz, g_code_clz_tail

def make_p_yolo_code(mod):
    global g_code_clz, g_code_yolo, g_code_clz_tail, g_code_yolo_tail
    g_code_yolo = ('''
def load_mod_predict_yolo(model_path, anchors=None, class_types=None):
    ort_session = ort.InferenceSession(model_path)
    input_name = ort_session.get_inputs()[0].name
    def _(filepath, predict_clz=None, pre_deal_img=None, filter_by_rect=None, threshold=0.2, nms_threshold=0.2):
        def parse_y_pred(ypred, threshold, nms_threshold):
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
                xx = 0 if xx < 0 else xx
                _x = 0 if _x < 0 else _x
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
            v = [get_xyxy_clz_con(i) for i in infos if i[3] > threshold]
            if nms_threshold:
                return nms(v)
            else:
                return v
        if type(filepath) == str:
            img = cv2.imdecode(np.fromfile(filepath, dtype=np.uint8), 1)
        else:
            img = filepath
        bkimg = pre_deal_img(img) if pre_deal_img else img.copy()
        height, width = bkimg.shape[:2]
        npimg = cv2.cvtColor(bkimg, cv2.COLOR_BGR2RGB)
        npimg = cv2.resize(npimg, (416, 416))
        npimg = np.transpose(npimg, (2,1,0))
        x = np.expand_dims(npimg.astype(np.float32), axis=0)
        y_pred = ort_session.run(None, {input_name: x})[0]
        v = parse_y_pred(y_pred, threshold, nms_threshold)
        r = []
        for i in v:
            rect, clz, con, log_cons = i
            rw, rh = width/416, height/416
            rect[0],rect[2] = int(rect[0]*rw),int(rect[2]*rw)
            rect[1],rect[3] = int(rect[1]*rh),int(rect[3]*rh)
            if filter_by_rect and filter_by_rect(rect):
                continue
            if predict_clz:
                clz = predict_clz(bkimg[rect[1]:rect[3], rect[0]:rect[2]])
            r.append([rect, clz, con, log_cons])
        r = sorted(r, key=lambda v:v[0][0])
        return [[rect, clz, con] for rect, clz, con, log_cons in r]
    return _
    ''').strip()
    g_code_yolo_tail = ('''predict_yolo_func = load_mod_predict_yolo('predict_yolo.onnx', class_types='''+json.dumps(mod['class_types'])+r''', anchors='''+json.dumps(mod['anchors'])+r''')''').strip()
    return g_code_yolo, g_code_yolo_tail

def save_mod_predict_clz(mod_filename):
    tarp = '.'
    name = 'predict_clz'
    mod = load_predict_func(mod_filename)
    dummy_input = torch.randn(1, 3, 40, 40, requires_grad=True)
    print(f"Model exported to {name}")
    tarf = os.path.join(tarp, name+'.onnx')
    torch.onnx.export(mod['net'], dummy_input, tarf, verbose=False, input_names=['input'], output_names=['output'])
    code = '''
from urllib.parse import unquote
import cv2
import numpy as np
import onnxruntime as ort

'''+make_p_clz_code(mod)[0]+'''

'''+make_p_clz_code(mod)[1]+'''
r = predict_clz_func('../imgs/cnn_clz/0/1057_7bf7479a8c584ecd8f3dd83f51a5daf5_2.jpg')
print(r)
    '''
    tarf = os.path.join(tarp, name+'_onnx.py')
    with open(tarf, 'w', encoding='utf8') as f:
        f.write(code.strip())
    print(f"code: {tarf}")

def save_mod_predict_yolo(mod_filename):
    tarp = '.'
    name = 'predict_yolo'
    mod = load_predict_yolo_func(mod_filename)
    dummy_input = torch.randn(1, 3, 416, 416, requires_grad=True)
    print(f"Model exported to {name}")
    tarf = os.path.join(tarp, name+'.onnx')
    torch.onnx.export(mod['net'], dummy_input, tarf, verbose=False, input_names=['input'], output_names=['output'])
    code = '''
import math

import cv2
import numpy as np
import onnxruntime as ort

'''+make_p_yolo_code(mod)[0]+'''

'''+make_p_yolo_code(mod)[1]+'''
r = predict_yolo_func('../imgs/Fatea_3/10af55e1bc914bae9ab9f07a9f337075_2_2.jpg')
print(r)
    '''
    tarf = os.path.join(tarp, name+'_onnx.py')
    with open(tarf, 'w', encoding='utf8') as f:
        f.write(code.strip())
    print(f"code: {tarf}")

def save_mod_preimage():
    tarp = '.'
    if not (g_code_clz and g_code_yolo):
        raise Exception('not init')
    title = '''
import math
from urllib.parse import unquote
import cv2
import numpy as np
import onnxruntime as ort
    '''.strip()
    tail = (r'''
''' + g_code_clz_tail + r'''
''' + g_code_yolo_tail + r'''

def pre_deal_img(img):
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

r = predict_yolo_func('../imgs/Fatea_3/10af55e1bc914bae9ab9f07a9f337075_2_2.jpg', predict_clz_func, pre_deal_img)
print(r)










# 以下仅用于测试，可以直接删掉
import os
import cv2
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
def filter_by_rect(rect):
    y = (rect[1] + rect[3])/2.
    return y < 35 or y > 45
tarp = '../imgs/Fatea/'
for i in os.listdir(tarp):
    if i.endswith('.jpg') or i.endswith('.png'):
        img = read_image_meta(tarp + i)
        r = predict_yolo_func(img, predict_clz_func, pre_deal_img=pre_deal_img, filter_by_rect=filter_by_rect)
        for ii in r:
            _rect, clz, con = ii
            img = drawrect(img, _rect, '{}'.format(clz, con))
            # img = drawrect(img, _rect, '{}|{:<.2f}'.format(clz, con))
        cv2.imshow('test', img)
        cv2.waitKey(0)
    ''').strip()
    code = '\n'.join([title, g_code_clz, g_code_yolo, tail])
    name = 'predict_image_all'
    tarf = os.path.join(tarp, name + '.py')
    with open(tarf, 'w', encoding='utf8') as f:
        f.write(code)

save_mod_predict_clz('../mods/clz_net.pkl')
save_mod_predict_yolo('../mods/yolo_net.pkl')
save_mod_preimage()