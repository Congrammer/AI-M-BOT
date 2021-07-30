from tqdm import tqdm
import numpy as np
import cv2
import os

source_path = './完成/'  # 源文件路径
target_path = './转换宽高/'  # 输出目标文件路径
txt_path = './转换标注/'

if not os.path.isdir(source_path):
    os.makedirs(source_path)
    exit(0)

if not os.path.isdir(target_path):
    os.makedirs(target_path)

if not os.path.isdir(txt_path):
    os.makedirs(txt_path)

if __name__ == '__main__':
    if not os.listdir(source_path):
        exit(0)
    for files in tqdm(os.listdir(source_path)):
        file_names, file_ext = os.path.splitext(files)
        if file_ext == '.txt':
            file_create = open(txt_path + files, 'w')
            if not os.path.getsize(source_path + files):
                file_create.close()
                continue

            file_data = []

            with open(source_path + files, 'r') as myfile:
                # 读取数据
                for line in myfile:
                    currentLine = line[:-1]
                    data = currentLine.split(' ')
                    if float(data[2]) + float(data[4]) / 2 > 0.25 and float(data[2]) - float(data[4]) / 2 < 0.75:
                        file_data.append(data)

                # 处理转换数据
                for i in file_data:
                    h1, h2 = float(i[2]) - float(i[4]) / 2, float(i[2]) + float(i[4]) / 2
                    h1 = 0.5 + ((0.25 if h1 < 0.25 else h1) - 0.5) * 2
                    h2 = 0.5 + ((0.75 if h2 > 0.75 else h2) - 0.5) * 2
                    i[4] = str('{:.6f}'.format(h2 - h1))
                    i[2] = str('{:.6f}'.format((h2 + h1) / 2))

                # 写入数据
                for j in file_data:
                    content = ''
                    for k in j:
                        content += k + ' '
                    file_create.write(content)
                    file_create.write('\n')

            file_create.close()

        else:
            pics = cv2.imdecode(np.fromfile(source_path + files, dtype=np.uint8), -1)
            crop_img = pics[int(pics.shape[1] / 4):int(pics.shape[1] * 3 / 4), 0:pics.shape[0]]
            cv2.imencode('.jpg', crop_img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])[1].tofile(target_path + files[0:files.find('.')] + '.jpg')  # 重命名并且保存
