from ml import yolo
load_voc_data = yolo.load_voc_data
train = yolo.train

xmlpath = './imgs/data_3'
mod_filename = './mods/yolo_net.pkl'
anchors = [[40, 40]]
start = 0
limitnum = 1000

def file_filter(filename):
    return True
    fls = ['ce32887f1abb41419469c1cd14e3dbd0_13.jpg']
    print(filename)
    for i in fls:
        if i.split('.')[0] in filename:
            return True

train_data, _, class_types = load_voc_data(xmlpath, anchors, start, limitnum, file_filter=file_filter)
train_data = train_data * 50
train(mod_filename, train_data, anchors, class_types, batch_size=15, LR=0.0001)