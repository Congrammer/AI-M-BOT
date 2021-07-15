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


def prep_box(layerOutputs, frame_width, frame_height):
    boxes1 = []
    boxes2 = []
    confidences1 = []
    confidences2 = []
    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]
            if confidence > 0.1 and classID == 0:
                box = detection[:4] * np.array([frame_width, frame_height, frame_width, frame_height])
                (centerX, centerY, width, height) = box.astype("int")
                box = [int(centerX), int(centerY), int(width), int(height)]
                boxes1.append(box)
                confidences1.append(float(confidence))
            elif confidence > 0.1 and classID == 1:
                box = detection[:4] * np.array([frame_width, frame_height, frame_width, frame_height])
                (centerX, centerY, width, height) = box.astype("int")
                box = [int(centerX), int(centerY), int(width), int(height)]
                boxes2.append(box)
                confidences2.append(float(confidence))

    indices1 = cv2.dnn.NMSBoxes(boxes1, confidences1, 0.5, 0.4)
    indices2 = cv2.dnn.NMSBoxes(boxes2, confidences2, 0.5, 0.4)

    return indices1, indices2, boxes1, boxes2


if __name__ == '__main__':
    if not os.listdir(pics_path):
        exit(0)

    CONFIG_FILE = './yolov4-tiny-cf02.cfg'
    WEIGHT_FILE = './yolov4-tiny-cf02.weights'

    net = cv2.dnn.readNetFromDarknet(CONFIG_FILE, WEIGHT_FILE)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    start_time = time()

    for pics in tqdm(os.listdir(pics_path)):
        pic_names = pics.replace('.jpg', '')
        file_create = open(prep_label_path + pic_names + '.txt', 'w')
        pictures = cv2.imdecode(np.fromfile(pics_path + pics, dtype=np.uint8), -1)
        # cv2.imshow('Show frame', pictures)
        # cv2.waitKey(1)

        frame_height, frame_width = pictures.shape[:2]
        blob = cv2.dnn.blobFromImage(pictures, 1 / 255.0, (608, 608), swapRB=False, crop=False)
        net.setInput(blob)
        layerOutputs = net.forward(ln)

        indices1, indices2, boxes1, boxes2 = prep_box(layerOutputs, frame_width, frame_height)
        if len(indices1) > 0:
            for i in indices1.flatten():
                (x, y) = (boxes1[i][0], boxes1[i][1])
                (w, h) = (boxes1[i][2], boxes1[i][3])
                file_create.write(f'0 {(x/frame_width):.6f} {(y/frame_height):.6f} {(w/frame_width):.6f} {(h/frame_height):.6f}\n')

        if len(indices2) > 0:
            for i in indices2.flatten():
                (x, y) = (boxes2[i][0], boxes2[i][1])
                (w, h) = (boxes2[i][2], boxes2[i][3])
                file_create.write(f'1 {(x/frame_width):.6f} {(y/frame_height):.6f} {(w/frame_width):.6f} {(h/frame_height):.6f}\n')

        file_create.close()

    end_time = time() - start_time

    print(f'Time used: {end_time:.3f} s')
    sleep(3)
