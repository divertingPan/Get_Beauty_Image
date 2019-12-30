# -*- coding: utf-8 -*-

import requests
from json import JSONDecoder
from PIL import Image
import os
import shutil
import time

# 这里用了一个API
http_url = "https://api-cn.faceplusplus.com/humanbodypp/v1/detect"
data = {"api_key": "_xdd7OMPd5rsHSsqwNaFTi-j-U_4T2HG",
        "api_secret": "fnGuZLo26p2vn0MWh6MCRgIdg5p_sESp",
        "return_attributes": "gender"}
#HumanBody Detect API（V1）

testing_dir = '女装大佬/'; # 准备分类的图
done_path = 'done/';      # 包含女装大佬的照片会放进这里
temp_path = 'temp/';      # 没有女装大佬的图会扔进这里

for maindir, subdir, file_name_list in os.walk(testing_dir):
    print("testing directory:", maindir); #当前目录
    print("file list:", file_name_list);  #当前目录下的所有文件名

for file in file_name_list:
    file_path = maindir + file;
    img = Image.open(file_path).convert('RGB').resize((512, 512), Image.BILINEAR) # 原图可能太大，所以先压缩一下大小再传给API
    img.save(temp_path + "human_temp.jpg")  # 其实没必要存一下再读取，但是懒得改了就这样吧
    files = {"image_file": open(temp_path + "human_temp.jpg", "rb")}
    #以二进制读入图像，这个字典中open(filepath1, "rb")返回的是二进制的图像文件，所以"image_file"是二进制文件，符合官网要求

    response = requests.post(http_url, data=data, files=files)
    #POTS上传
    
    req_con = response.content.decode('utf-8')
    #response的内容是JSON格式
    
    req_dict = JSONDecoder().decode(req_con)
    #对其解码成字典格式
    
    if len(req_dict['humanbodies']):
        if req_dict['humanbodies'][0]['attributes']['gender']['female'] > req_dict['humanbodies'][0]['attributes']['gender']['male']:
            new_path = done_path + file;
            path = shutil.copy(file_path, new_path);
            print('select: ' + path);
        else:
            new_path = temp_path + file;
            path = shutil.copy(file_path, new_path);
            print('out: ' + path);
    else:
        new_path = temp_path + file;
        path = shutil.copy(file_path, new_path);
        print('out: ' + path);

    time.sleep(1) # 运行太快会卡死，手动降速
    