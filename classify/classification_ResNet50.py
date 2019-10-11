# -*- coding: utf-8 -*-
from keras.applications.resnet50 import ResNet50
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np
import matplotlib.pyplot as plt


model = ResNet50(weights='imagenet', include_top=True);

'''
#单个图像识别结果测试

img_path = 'test/15.jpg';
img = image.load_img(img_path, target_size=(224, 224));
x = image.img_to_array(img);
x = np.expand_dims(x, axis=0);
x = preprocess_input(x);
preds = model.predict(x);
# decode the results into a list of tuples (class, description, probability)
# (one such list for each sample in the batch)

print('Path:', img_path, '\nPredicted:', decode_predictions(preds, top=8)[0]);
plt.figure(figsize=(8,8));
plt.subplot(2,1,1);
plt.axis('off');
plt.imshow(plt.imread(img_path));
name_list = [decode_predictions(preds)[0][i][1] for i in range (0, 5)]; 
num_list = [decode_predictions(preds)[0][i][2] for i in range (0, 5)];
plt.subplot(2,1,2);
plt.barh(range(len(num_list)), num_list, tick_label = name_list);
plt.show();


import shutil
new_path = 'done/13.jpg';
path = shutil.copy(img_path, new_path);
print(path);

'''

import os
import shutil

testing_dir = '火车迷/';
done_dir = 'done/';
temp_dir = 'temp/';
target_list = ['steam_locomotive', 'passenger_car', 'freight_car', 'electric_locomotive', 'bullet_train'];

for maindir, subdir, file_name_list in os.walk(testing_dir):
    print("testing directory:", maindir); #当前目录
    print("file list:", file_name_list);  #当前目录下的所有文件名

for file in file_name_list:
    img_path = maindir + file;
    img = image.load_img(img_path, target_size=(224, 224));
    x = image.img_to_array(img);
    x = np.expand_dims(x, axis=0);
    x = preprocess_input(x);
    preds = model.predict(x);
    if decode_predictions(preds)[0][0][1] in target_list:
        new_path = done_dir + file;
        path = shutil.copy(img_path, new_path);
        print('select: ' + path);
    else:
        new_path = temp_dir + file;
        path = shutil.copy(img_path, new_path);
        print('out: ' + path);
    