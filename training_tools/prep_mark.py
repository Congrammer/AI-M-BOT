from time import time, sleep
from tqdm import tqdm
from sys import exit
import numpy as np
import os
import cv2


prep_label_path = './测试标注/'
if not os.path.isdir(prep_label_path):
    os.makedirs(prep_label_path)

pics_path = './预先处理/'
if not os.path.isdir(pics_path):
    os.makedirs(pics_path)


if __name__ == '__main__':
    if not os.listdir(pics_path):
        exit(0)

    CONFIG_FILE = './yolov4-tiny.cfg'
    WEIGHT_FILE = './yolov4-tiny.weights'

    net = cv2.dnn.readNet(CONFIG_FILE, WEIGHT_FILE)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
    model = cv2.dnn_DetectionModel(net)
    model.setInputParams(size=(512, 320), scale=1/255, swapRB=False)

    start_time = time()

    for pics in tqdm(os.listdir(pics_path)):
        pic_names, pic_ext = os.path.splitext(pics)
        file_create = open(prep_label_path + pic_names + '.txt', 'w')
        pictures = cv2.imdecode(np.fromfile(pics_path + pics, dtype=np.uint8), -1)
        pictures = pictures[..., :3]
        # cv2.imshow('Show frame', pictures)
        # cv2.waitKey(1)

        frame_height, frame_width = pictures.shape[:2]
        classes, scores, boxes = model.detect(pictures, 0.2, 0.3)

        for (classid, score, box) in zip(classes, scores, boxes):
            x, y, w, h = box
            x = x + w/2
            y = y + h/2
            if classid == 0:
                file_create.write(f'0 {(x/frame_width):.6f} {(y/frame_height):.6f} {(w/frame_width):.6f} {(h/frame_height):.6f}\n')
            if classid == 1:
                file_create.write(f'1 {(x/frame_width):.6f} {(y/frame_height):.6f} {(w/frame_width):.6f} {(h/frame_height):.6f}\n')

        file_create.close()

    end_time = time() - start_time

    print(f'Time used: {end_time:.3f} s')
    sleep(3)
