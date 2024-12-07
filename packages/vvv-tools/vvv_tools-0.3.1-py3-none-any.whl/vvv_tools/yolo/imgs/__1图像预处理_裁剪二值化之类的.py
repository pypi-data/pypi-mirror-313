import re
import shutil
import cv2
import numpy as np

def read_image_meta(f):
    if f.endswith('.gif'):
        gif = cv2.VideoCapture(f)
        ret, frame = gif.read()
        return frame
    else:
        return cv2.imread(f)

def dd(npimg):
    npimg = cv2.addWeighted(npimg, 1.5, npimg, -0.5, 0)
    _, npimg = cv2.threshold(npimg, 178, 255, cv2.THRESH_BINARY)
    npimg[np.logical_not(np.all(npimg < 150, axis=2))] = 255
    return npimg

import os
srcp = './data/'
tarp = './data_2/'

if not os.path.isdir(tarp):
    os.makedirs(tarp)

def reptype(e):
    return e.rsplit('.',1)[0]+'.png'

ls = os.listdir(srcp)
for i in ls:
    sr = os.path.join(srcp, i)
    tr = os.path.join(tarp, i)
    if i.endswith('.jpg') or i.endswith('.png') or i.endswith('.gif'):
        print(i)
        imgsr = read_image_meta(sr)
        imgsr = dd(imgsr)
        tr = reptype(tr)
        print(tr)
        cv2.imwrite(tr, imgsr)
    else:
        if i.endswith('xml'):
            def repfunc(e):
                a = e.group(1)
                b = reptype(e.group(2))
                c = e.group(3)
                return a + b + c
            with open(sr, encoding='utf8') as f:
                code = f.read()
                code = re.sub('(<filename>)(.*?)(</filename>)', repfunc, code)
                filename = re.findall('(<filename>)(.*?)(</filename>)', code)[0][1]
                code = re.sub('(<path>)(.*?)(</path>)', f'<path>{filename}</path>', code)
            with open(tr, 'w', encoding='utf8') as f:
                f.write(code)
        else:
            print('error file', i)


