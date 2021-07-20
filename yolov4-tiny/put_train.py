from time import sleep
from tqdm import tqdm
from sys import exit
import random
import os


final_path = './标注完成/'  # 标注好的图片路径
label_path = './素材标注/'
train_txt = 'train.txt'  # 标注好用于训练的图片
test_txt = 'test.txt'  # 标注好用于测试的图片


def Diff(li1, li2):
    return list(set(li1) - set(li2)) + list(set(li2) - set(li1))


if not os.path.isdir(final_path):
    os.makedirs(final_path)


if __name__ == '__main__':
    if not os.listdir(final_path):
        exit(0)

    train_file = open(train_txt, 'w')
    test_file = open(test_txt, 'w')
    label_list = []
    file_list = []
    marked = 0
    totals = 0

    for labels in (os.listdir(label_path)):
        label_list.append(labels.replace('.txt', ''))
        if labels != 'classes.txt' and os.path.getsize(label_path + labels):
            marked += 1

    for files in tqdm(os.listdir(final_path)):
        file_names, file_ext =  os.path.splitext(files)
        file_list.append(file_names)
        if random.randint(0, 999) >= 100:
            train_file.write(final_path + file_names + file_ext + '\n')  # 录入文件名
        else:
            test_file.write(final_path + file_names + file_ext + '\n')  # 录入文件名
        totals += 1
        if not file_names in label_list:
            file_create = open(label_path + file_names + '.txt', 'w')
            file_create.close()
            label_list.append(file_names)

    train_file.close()
    test_file.close()

    print(f'批量处理完成,图片标注率={100*(marked/totals):.2f}%')
    print(f'不同处={Diff(label_list, file_list)}')
    sleep(3)
