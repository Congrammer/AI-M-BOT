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
from AI_main import main


# 主程序
if __name__ == '__main__':
    # 为了Pyinstaller顺利生成exe
    freeze_support()

    main()
