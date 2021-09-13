"""
New Detection method(onnxruntime) modified from Project YOLOX
YOLOX Project Authors: Zheng Ge, Songtao Liu, Feng Wang, Zeming Li, Jian Sun
YOLOX Project website: https://github.com/Megvii-BaseDetection/YOLOX
New Detection method(onnxruntime) cooperator: Barry
Detection code modified from project AIMBOT-YOLO
Detection code Author: monokim
Detection project website: https://github.com/monokim/AIMBOT-YOLO
Detection project video: https://www.youtube.com/watch?v=vQlb0tK1DH0
Screenshot method from: https://www.youtube.com/watch?v=WymCpVUPWQ4
Screenshot method code modified from project: opencv_tutorials
Screenshot method code Author: Ben Johnson (learncodebygaming)
Screenshot method website: https://github.com/learncodebygaming/opencv_tutorials
Mouse event method code modified from project logitech-cve
Mouse event method website: https://github.com/ekknod/logitech-cve
Mouse event method project Author: ekknod
"""

from multiprocessing import freeze_support


# 主程序
if __name__ == '__main__':
    # 为了Pyinstaller顺利生成exe
    freeze_support()

    # 选择标准/烧卡模式
    main_model = 0
    while not (2 >= main_model >= 1):
        user_choice = input('请问您的电脑是高配机吗?(1:是, 2:不是): ')
        try:
            main_model = int(user_choice)
        except ValueError:
            print('呵呵...请重新输入')
        finally:
            if not (2 >= main_model >= 1):
                print('请在给定范围选择')

    if main_model == 1:
        from AI_main_pow import main
    else:
        from AI_main import main

    main()
