from time import sleep
from tqdm import tqdm
from sys import exit
import os


final_path = './标注完成/'  # 标注好的图片路径
label_path = './素材标注/'
train_txt = 'train.txt'  # 标注好的图片txt

if not os.path.isdir(final_path):
    os.makedirs(final_path)


if __name__ == '__main__':
    if not os.listdir(final_path):
        exit(0)

    txtfile = open(train_txt, 'w')
    label_list = []
    marked = 0
    totals = 0
    for labels in (os.listdir(label_path)):
        label_list.append(labels.replace('.txt', ''))
        if labels != 'classes.txt' and os.path.getsize(label_path + labels):
            marked += 1

    for files in tqdm(os.listdir(final_path)):
        file_names = files.replace('.jpg', '')
        txtfile.write(file_names + '\n')  # 录入文件名
        totals += 1
        if not file_names in label_list:
            file_create = open(label_path + file_names + '.txt', 'w')
            file_create.close()

    txtfile.close()
    print(f'批量处理完成,图片标注率={100*(marked/totals):.2f}%')
    sleep(3)
