import cv2
import numpy as np
import torch

import os
import math
import xml.dom.minidom
import urllib.parse

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
    imgname = os.path.split(f)[-1]
    xmlpath = os.path.split(file)[0]
    f = os.path.join(xmlpath, imgname)
    if not os.path.isfile(f):
        raise 'fail load img: {}'.format(f)
    size = v.getElementsByTagName('size')[0]
    npimg = read_image_meta(f)
    def readobj(obj):
        d = {}
        bbox = obj.getElementsByTagName('bndbox')[0]
        d['width']  = int(size.getElementsByTagName('width')[0].firstChild.data)
        d['height'] = int(size.getElementsByTagName('height')[0].firstChild.data)
        d['cate']   = obj.getElementsByTagName('name')[0].firstChild.data
        d['xmin']   = int(bbox.getElementsByTagName('xmin')[0].firstChild.data)
        d['ymin']   = int(bbox.getElementsByTagName('ymin')[0].firstChild.data)
        d['xmax']   = int(bbox.getElementsByTagName('xmax')[0].firstChild.data)
        d['ymax']   = int(bbox.getElementsByTagName('ymax')[0].firstChild.data)
        d['numpy']  = npimg[d['ymin']:d['ymax'],d['xmin']:d['xmax']]
        d['file'] = f
        d['imgname'] = imgname
        return d
    if islist:  r = [readobj(obj) for obj in v.getElementsByTagName('object')]
    else:       r = readobj(v.getElementsByTagName('object')[0])
    return r

def load_voc_data(xmlpath, start=0, limit=1000):
    files = [os.path.join(xmlpath, path) for path in os.listdir(xmlpath) if path.endswith('.xml')][start:start+limit]
    imginfos = []
    print('load xml file number:{}, start.'.format(len(files)))
    for idx, file in enumerate(files):
        if idx % 1000 == 0: print('loading {}/{}'.format(idx, len(files)))
        xmlfiles = read_voc_xml(file, islist=True)
        imginfos.extend(xmlfiles)
    print('load all file. ok.')
    return imginfos

def safe_name(name):
    return ''.join([urllib.parse.quote(i) if ord(i) < 256 else i for i in name])


tarp = './cnn_clz'
if not os.path.isdir(tarp):
	os.mkdir(tarp)
imginfos = load_voc_data('./data_2')
for idx, i in enumerate(imginfos):
	print(i['cate'])
	tarclzp = os.path.join(tarp, safe_name(i['cate']))
	if not os.path.isdir(tarclzp):
		os.mkdir(tarclzp)
	tarf = os.path.join(tarclzp, str(idx) + '_' + i['imgname'])
	print(tarf)
	cv2.imwrite(tarf, i['numpy'])