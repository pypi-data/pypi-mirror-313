# 图像预处理

import os
import cv2
import numpy as np
import random

def rand_line(image):
    # 随机绘制干扰细线
    h, w = image.shape[:2]
    for _ in range(random.randint(7, 15)):
        pt1 = (random.randint(0, w//3), random.randint(0, h//3))
        pt2 = (random.randint(w//3, w), random.randint(h//3, h))
        c1 = random.randint(10,240)
        c2 = random.randint(10,240)
        c3 = random.randint(10,240)
        color = (c1, c2, c3)
        if random.random() < 0.5:
            thickness = random.randint(1, 1)
            cv2.line(image, pt1, pt2, color, thickness)
        else:
            a = random.randint(100, 180)
            b = random.randint(50, 100)
            k = 1 if random.random() < 0.5 else -1
            sa = 30 * k
            ea = 150 * k
            center = ((pt1[0] + pt2[0]) // 2, (pt1[1] + pt2[1]) // 2)
            rotate = random.randint(0, 180)
            cv2.ellipse(image, center, (a, b), 45, sa, ea, color, 1)

def rand_light(image):
    # 随机改变亮度和对比度
    brightness = random.randint(-40, 40)
    contrast = random.uniform(0.8, 1.2)
    image = cv2.convertScaleAbs(image, alpha=contrast, beta=brightness)
    return image

def rand_rotate(image):
    # 随机旋转
    ag = 3
    angle = random.randint(-ag, ag)
    h, w = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    fill_color = (255,255,255) # 填充颜色
    image = cv2.warpAffine(image, M, (w, h), borderValue=fill_color)
    return image

def rand_cut(image):
    # 随机裁剪
    cutl, cutr = 3, 3
    cutt, cutb = 3, 3
    l = random.randint(0, cutl)
    r = random.randint(0, cutr)
    t = random.randint(0, cutt)
    b = random.randint(0, cutb)
    h, w = image.shape[:2]
    image = image[0+t:h-b, 0+l:w-r]
    return image

def rand_pad(image):
    # 随机边缘填充
    a = random.randint(0, 2)
    b = random.randint(0, 2)
    c = random.randint(0, 2)
    d = random.randint(0, 2)
    image = cv2.copyMakeBorder(image, a, b, c, d, cv2.BORDER_REPLICATE)
    return image

def add_gaussian_noise(image, mean=0):
    sigma = (random.random() * 0.4 + 0.1)
    gauss = np.random.normal(mean, sigma, image.shape).astype('uint8')
    noisy_image = cv2.add(image, gauss)
    return noisy_image

def random_blur(image):
    ksize = random.choice([1, 3])  # 随机选择模糊核大小
    return cv2.GaussianBlur(image, (ksize, ksize), 0)

def transform_v1(image):
    # 用于分类
    # image = rand_rotate(image)
    # image = rand_light(image)
    image = rand_cut(image)
    image = rand_pad(image)
    rand_line(image)
    image = random_blur(image)
    image = add_gaussian_noise(image)
    return image

def transform_v2(image):
    # 用于yolo
    image = rand_light(image)
    rand_line(image)
    image = random_blur(image)
    image = add_gaussian_noise(image)
    return image

def test_show(image_path):
    import matplotlib.pyplot as plt
    image = cv2.imread(image_path)
    augmented_image = transform_v2(image)
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.title('Original Image')
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.subplot(1, 2, 2)
    plt.title('Augmented Image')
    plt.imshow(cv2.cvtColor(augmented_image, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()


# image_path = './cnn_clz/1/105_02af84aa4c494aa58e9a876d40b29493_11.png'  # 替换为你的图片路径
# test_show(image_path)

root = './cnn_clz/'
for _root in os.listdir(root):
    _root = os.path.join(root, _root)
    for i in os.listdir(_root):
        if i.startswith('rd_'): continue
        tfile = os.path.join(_root, i)
        print(tfile)
        image = cv2.imread(tfile)
        for idx in range(3):
            _image = rand_cut(image)
            tsavefile = os.path.join(_root, f'rd_cut_{idx}_' + i)
            cv2.imwrite(tsavefile, _image)
        for idx in range(3):
            _image = rand_pad(image)
            tsavefile = os.path.join(_root, f'rd_pad_{idx}_' + i)
            cv2.imwrite(tsavefile, _image)