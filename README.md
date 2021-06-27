# AI-M-BOT
![image](PDF_Images/神经自瞄.png)

[![Badgs](https://img.shields.io/badge/链接-996.icu-green)](https://996.icu/#/zh_CN)  [![Badge](https://img.shields.io/badge/link-996.icu-pink)](https://996.icu/#/en_US)  [![LICENSE](https://img.shields.io/badge/许可证-反对996-red)](https://github.com/996icu/996.ICU/blob/master/LICENSE_CN)  [![LICENSE](https://img.shields.io/badge/license-Anti996-blue)](https://github.com/996icu/996.ICU/blob/master/LICENSE)

[![img](https://img.shields.io/github/stars/JiaPai12138/AI-M-BOT?label=点赞)](https://github.com/JiaPai12138/AI-M-BOT)  [![img](https://img.shields.io/github/forks/JiaPai12138/AI-M-BOT?label=克隆)](https://github.com/JiaPai12138/AI-M-BOT)  [![img](https://img.shields.io/github/last-commit/JiaPai12138/AI-M-BOT?label=最近提交)](https://github.com/JiaPai12138/AI-M-BOT)  [![img](https://img.shields.io/github/release/JiaPai12138/AI-M-BOT?label=最新版本)](https://github.com/JiaPai12138/AI-M-BOT/releases)  [![img](https://img.shields.io/github/license/JiaPai12138/AI-M-BOT?label=许可证)](https://github.com/JiaPai12138/AI-M-BOT/blob/main/LICENSE)  [![img](https://img.shields.io/badge/URL-帮助文档-blue)](https://github.com/JiaPai12138/AI-M-BOT/blob/main/使用说明.rtf)

* 使用自瞄时请将游戏分辨率调整至<font style="background: #FFFF00">**1600*900**</font>及以下，将画面效果调整至<font style="background: #FFFF00">**中等**</font>及以下
* 需要计算能力6.1及以上版本的<font style="background: #FFFF00">**N卡**</font>以及安装相应驱动，详情请见[CUDA wiki](https://zh.wikipedia.org/wiki/CUDA)
* 按1或2或3选择极速模式或标准模式或高精模式(图像预测尺寸递增，预测速度递减)![image](PDF_Images/自瞄模式选择.png)
* 等待游戏窗口成为当前活动窗口(点击一下游戏窗口即可)![image](PDF_Images/自瞄等待窗口.png)
* 按"i"键关效果展示，桌面左上角别区域小视频消失
* 按"o"键开效果展示，开启时桌面左上角会显示截屏识别区域小视频![image](PDF_Images/自瞄显示图像.png)
* 按"1"/"2"键保持自瞄状态并控制鼠标![image](PDF_Images/自瞄控制运行.png)
* 按"3"/"4"键保持自瞄状态但不控制鼠标![image](PDF_Images/自瞄待命运行.png)
* 按"p"键重启程序
* 按"END"结束程序
* 自瞄只截屏识别准星附近区域，对于16:9的CF游戏窗口识别区域大小为(高=游戏窗口高*3/5，宽=高*4/3)
* 本程序使用python语言以及自源码编译的opencv-cuda加速库
* 本程序使用yolov4-tiny模型，只因其快(目前使用b站大佬[VeniVediVeci](https://space.bilibili.com/196421117)训练的权值)
* 本程序<font style="background: #FFFF00">**很吃性能**</font>，使用前请先确认您的电脑配置: [GPU天梯1](http://cdn.malu.me/gpu/)，[GPU天梯2](https://topic.expreview.com/GPU/)或[参考知乎](https://zhuanlan.zhihu.com/p/133845310)