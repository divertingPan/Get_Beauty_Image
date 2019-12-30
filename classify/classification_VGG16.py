# -*- coding: utf-8 -*-
from keras.applications.vgg16 import VGG16
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input, decode_predictions
import numpy as np
import matplotlib.pyplot as plt

model = VGG16(weights='imagenet', include_top=True)

img_path = 'test/186.jpg'
img = image.load_img(img_path, target_size=(224, 224))
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = preprocess_input(x)

preds = model.predict(x)
# decode the results into a list of tuples (class, description, probability)
# (one such list for each sample in the batch)

print('Path:', img_path, '\nPredicted:', decode_predictions(preds, top=8)[0])
plt.figure(figsize=(8,8));
plt.subplot(2,1,1);
plt.axis('off');
plt.imshow(plt.imread(img_path));
name_list = [decode_predictions(preds)[0][i][1] for i in range (0, 5)]; 
num_list = [decode_predictions(preds)[0][i][2] for i in range (0, 5)];
plt.subplot(2,1,2);
plt.barh(range(len(num_list)), num_list, tick_label = name_list);
plt.show();
