from ml import cnn

load_data = cnn.load_data
train = cnn.train

root = './imgs/cnn_clz'
mod_filename = './mods/clz_net.pkl'
train_data, class_types = load_data(root)
train_data = train_data * 10
train(mod_filename, train_data, class_types)
