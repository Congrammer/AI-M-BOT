import cv2
import os
import numpy as np
from tqdm import tqdm
from sys import exit

source_path = './游戏截图/'  # 源文件路径
target_path = './预先处理/'  # 输出目标文件路径

if not os.path.isdir(source_path):
    os.makedirs(source_path)
    exit(0)

if not os.path.isdir(target_path):
    os.makedirs(target_path)

if __name__ == '__main__':
    if not os.listdir(source_path):
        exit(0)
    for file in tqdm(os.listdir(source_path)):
        image_source = cv2.imdecode(np.fromfile(source_path + file, dtype=np.uint8), -1)  # 读取图片
        image_size_h, image_size_w = image_source.shape[:2]  # 设定长宽
        if round(3 * image_size_w / 4 / image_size_h, 2) == 1.00:
            image_size_w = image_size_h
        image = cv2.resize(image_source, (image_size_w, image_size_h), 0, 0, cv2.INTER_LINEAR)  # 修改尺寸
        cv2.imencode('.jpg', image)[1].tofile(target_path + file[0:file.find('.')] + '.jpg')  # 重命名并且保存

    print('批量处理完成')
