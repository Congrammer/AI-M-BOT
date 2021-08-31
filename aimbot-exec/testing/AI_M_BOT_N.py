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

from win32con import VK_END, PROCESS_ALL_ACCESS, SPI_GETMOUSE, SPI_SETMOUSE, SPI_GETMOUSESPEED, SPI_SETMOUSESPEED
from win32api import GetAsyncKeyState, GetCurrentProcessId, OpenProcess
from win32process import SetPriorityClass, ABOVE_NORMAL_PRIORITY_CLASS
from util import set_dpi, is_full_screen, is_admin, clear, restart
from multiprocessing import Process, Array, Pipe, freeze_support
from mouse import mouse_xy, mouse_down, mouse_up, mouse_close
from darknet_yolo34 import FrameDetection34
from math import sqrt, pow, atan, cos, pi
from torch_yolox import FrameDetectionX
from scrnshot import WindowCapture
from pynput.mouse import Listener
from sys import exit, platform
from collections import deque
from statistics import median
from time import sleep, time
from random import uniform
from ctypes import windll
import numpy as np
import pywintypes
import win32gui
import cv2
import os


# 确认窗口句柄与类名
def get_window_info():
    supported_games = 'Valve001 CrossFire LaunchUnrealUWindowsClient LaunchCombatUWindowsClient UnrealWindow UnityWndClass'
    test_window = 'Notepad3 PX_WINDOW_CLASS Notepad Notepad++'
    emulator_window = 'BS2CHINAUI Qt5154QWindowOwnDCIcon LSPlayerMainFrame'
    class_name = None
    hwnd_var = None
    testing_purpose = False
    while not hwnd_var:  # 等待游戏窗口出现
        hwnd_active = win32gui.GetForegroundWindow()
        try:
            class_name = win32gui.GetClassName(hwnd_active)
        except pywintypes.error:
            continue

        if class_name not in (supported_games + test_window + emulator_window):
            print('请使支持的游戏/程序窗口成为活动窗口...')
        else:
            try:
                hwnd_var = win32gui.FindWindow(class_name, None)
                if class_name in emulator_window:
                    hwnd_var = win32gui.FindWindowEx(hwnd_var, None, None, None)
            except pywintypes.error:
                print('您正使用沙盒')
                hwnd_var = hwnd_active
            print('已找到窗口')
            if class_name in test_window:
                testing_purpose = True
        sleep(3)
    return class_name, hwnd_var, testing_purpose


# 退出脚本
def close():
    if not arr[2]:
        show_proc.terminate()
    detect_proc.terminate()
    mouse_close()


# 检测是否存在配置与权重文件
def check_file(file):
    cfg_file = file + '.cfg'
    weights_file = file + '.weights'
    if not (os.path.isfile(cfg_file) and os.path.isfile(weights_file)):
        print(f'请下载{file}相关文件!!!')
        sleep(3)
        exit(0)


# 移动鼠标(并射击)
def control_mouse(a, b, fps_var, ranges, rate, go_fire, win_class, move_rx, move_ry, down_time, up_time):
    DPI_Var = windll.user32.GetDpiForWindow(window_hwnd_name) / 96
    move_rx, a = track_opt(move_rx, a)
    move_ry, b = track_opt(move_ry, b)
    arr[20] = recoil_control[0] * shoot_times[0]  # if arr[12] == 1 or arr[14] else 0
    move_range = sqrt(pow(a, 2) + pow(b, 2))
    enhanced_holdback = win32gui.SystemParametersInfo(SPI_GETMOUSE)
    if enhanced_holdback[1]:
        win32gui.SystemParametersInfo(SPI_SETMOUSE, [0, 0, 0], 0)
    mouse_speed = win32gui.SystemParametersInfo(SPI_GETMOUSESPEED)
    if mouse_speed != 10:
        win32gui.SystemParametersInfo(SPI_SETMOUSESPEED, 10, 0)

    if fps_var and arr[17] and arr[11] and arr[4]:
        a = cos((pi - atan(a/arr[18])) / 2) * (2*arr[18]) / DPI_Var
        b = cos((pi - atan(b/arr[18])) / 2) * (2*arr[18]) / DPI_Var
        if move_range > 6 * ranges:
            a *= uniform(0.9, 1.1)
            b *= uniform(0.9, 1.1)
        fps_factorx = pow(fps_var/4, 1/3)
        fps_factory = pow(fps_var/3, 1/3)
        x0 = {
            'CrossFire': a / 2.719 * (client_ratio / (4/3)) / fps_factorx,  # 32
            'Valve001': a * 1.667 / fps_factorx,  # 2.5
            'LaunchCombatUWindowsClient': a * 1.319 / fps_factorx,  # 10.0
            'LaunchUnrealUWindowsClient': a / 2.557 / fps_factorx,  # 20
        }.get(win_class, a / fps_factorx)
        y0 = {
            'CrossFire': b / 2.719 * (client_ratio / (4/3)) / fps_factory,  # 32
            'Valve001': b * 1.667 / fps_factory,  # 2.5
            'LaunchCombatUWindowsClient': b * 1.319 / fps_factory,  # 10.0
            'LaunchUnrealUWindowsClient': b / 2.557 / fps_factory,  # 20
        }.get(win_class, b / fps_factory)

        mouse_xy(int(round(x0)), int(round(y0)))

    # 不分敌友射击
    if arr[21]:  # GetAsyncKeyState(VK_LBUTTON) < 0 or GetKeyState(VK_LBUTTON) < 0
        if time() * 1000 - down_time > 30.6:  # or not arr[11]
            mouse_up()
            up_time = time() * 1000
    elif (win_class != 'CrossFire' or arr[19]) and arr[4]:
        if (go_fire or move_range < ranges):  # and arr[11]
            if time() * 1000 - up_time > rate:
                mouse_down()
                down_time = time() * 1000
                shoot_times[0] += 1

    if time() * 1000 - up_time > 219.4:
        shoot_times[0] = 0

    if shoot_times[0] > 12:
        shoot_times[0] = 12

    if enhanced_holdback[1]:
        win32gui.SystemParametersInfo(SPI_SETMOUSE, enhanced_holdback, 0)
    if mouse_speed != 10:
        win32gui.SystemParametersInfo(SPI_SETMOUSESPEED, mouse_speed, 0)

    return move_rx, move_ry, down_time, up_time


# 傻追踪优化
def track_opt(record_list, range_m):
    if len(record_list):
        if abs(median(record_list) - range_m) <= 15 and abs(range_m) <= 90:
            record_list.append(range_m)
        else:
            record_list.clear()
        if len(record_list) > sqrt(show_fps[0]) and arr[4]:
            range_m *= pow(show_fps[0]/3, 1/3)
            record_list.clear()
    else:
        record_list.append(range_m)

    return record_list, range_m


# 转变状态
def check_status(exit0, mouse):
    if GetAsyncKeyState(VK_END) < 0:  # End
        exit0 = True
    if GetAsyncKeyState(0x31) < 0:  # 1
        mouse = 1
        arr[15] = 1
    if GetAsyncKeyState(0x32) < 0:  # 2
        mouse = 2
        arr[15] = 2
    if GetAsyncKeyState(0x33) < 0 or GetAsyncKeyState(0x34) < 0:  # 3,4
        mouse = 0
        arr[15] = 0
    if GetAsyncKeyState(0x46) < 0:  # F
        arr[17] = 1
    if GetAsyncKeyState(0x4A) < 0:  # J
        arr[17] = 0
    if GetAsyncKeyState(0x50) < 0:  # P
        close()
        restart(__file__)

    return exit0, mouse


# 多线程展示效果
def show_frames(output_pipe, array):
    set_dpi()
    cv2.namedWindow('Show frame', cv2.WINDOW_KEEPRATIO)
    cv2.moveWindow('Show frame', 0, 0)
    cv2.destroyAllWindows()
    font = cv2.FONT_HERSHEY_SIMPLEX  # 效果展示字体
    fire_target_show = ['middle', 'head', 'chest']
    while True:
        show_img = output_pipe.recv()
        show_color = {
            0: (127, 127, 127),
            1: (255, 255, 0),
            2: (0, 255, 0)
        }.get(array[4])
        try:
            img_ex = np.zeros((1, 1, 3), np.uint8)
            show_str0 = str('{:03.0f}'.format(array[3]))
            show_str1 = 'Detected ' + str('{:02.0f}'.format(array[11])) + ' targets'
            show_str2 = 'Aiming at ' + fire_target_show[array[12]] + ' position'
            show_str3 = 'Fire rate is at ' + str('{:02.0f}'.format((10000 / (array[13] + 306)))) + ' RPS'
            show_str4 = 'Please enjoy coding ^_^' if array[17] else 'Please enjoy coding @_@'
            if show_img.any():
                show_img_h, show_img_w = show_img.shape[:2]
                show_img = cv2.resize(show_img, (array[5], int(array[5] / show_img_w * show_img_h)))
                img_ex = cv2.resize(img_ex, (array[5], int(array[5] / 2)))
                cv2.putText(show_img, show_str0, (int(array[5] / 25), int(array[5] / 12)), font, array[5] / 600, (127, 255, 0), 2, cv2.LINE_AA)
                cv2.putText(img_ex, show_str1, (10, int(array[5] / 9)), font, array[5] / 450, show_color, 1, cv2.LINE_AA)
                cv2.putText(img_ex, show_str2, (10, int(array[5] / 9) * 2), font, array[5] / 450, show_color, 1, cv2.LINE_AA)
                cv2.putText(img_ex, show_str3, (10, int(array[5] / 9) * 3), font, array[5] / 450, show_color, 1, cv2.LINE_AA)
                cv2.putText(img_ex, show_str4, (10, int(array[5] / 9) * 4), font, array[5] / 450, show_color, 1, cv2.LINE_AA)
                show_image = cv2.vconcat([show_img, img_ex])
                cv2.imshow('Show frame', show_image)
                cv2.waitKey(1)
        except (AttributeError, cv2.error):
            cv2.destroyAllWindows()


# 分析进程
def detection(array):
    array[1] = 1
    def on_click(x, y, button, pressed):
        array[21] = 1 if pressed else 0

    with Listener(on_click=on_click) as listener:
        listener.join()


# 主程序
if __name__ == '__main__':
    # 为了Pyinstaller顺利生成exe
    freeze_support()

    # 检查管理员权限
    if not is_admin():
        restart(__file__)

    # 设置高DPI不受影响
    set_dpi()

    # 设置工作路径
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # 滑稽
    Conan = -1
    while not (2 >= Conan >= 0):
        user_choice = input('柯南能在本程序作者有生之年完结吗?(1:能, 2:能, 0:不能): ')
        try:
            Conan = int(user_choice)
        except ValueError:
            print('呵呵...请重新输入')
        else:
            if not (2 >= Conan >= 0):
                print('请在给定范围选择')

    # 初始化变量以及提升进程优先级
    if platform == 'win32':
        pid = GetCurrentProcessId()
        handle = OpenProcess(PROCESS_ALL_ACCESS, True, pid)
        SetPriorityClass(handle, ABOVE_NORMAL_PRIORITY_CLASS)
    else:
        os.nice(1)

    frame_output, frame_input = Pipe(False)  # 初始化管道(receiving,sending)
    press_time, up_time, show_fps = [0], [0], [1]
    process_time = deque()
    exit_program = False
    test_win = [False]
    move_record_x = []
    move_record_y = []
    shoot_times = [0]
    recoil_control = [0]
    d_time, u_time = 0, 0
    cf_enemy_color = np.array([3487638, 3487639, 3487640, 3487641, 3422105, 3422106, 3422362, 3422363, 3422364, 3356828, 3356829, 3356830, 3356831, 3291295, 3291551, 3291552, 3291553, 3291554, 3226018, 3226019, 3226020, 3226276, 3226277, 3160741, 3160742, 3160743, 3160744, 3095208, 3095209, 3095465, 3095466, 3095467, 3029931, 3029932, 3029933, 3029934, 3030190, 2964654, 2964655, 2964656, 2964657, 2899121, 2899122, 2899123, 2899379, 2899380, 2833844, 2833845, 2833846, 2833847, 2768311, 2768567, 2768568, 2768569, 2768570, 2703034, 2703035, 2703036, 2703292, 2703292, 2703293, 2637757, 2637758, 2637759, 2637760, 2572224, 2572225, 2572481, 2572482, 2572483, 2506948, 2506949, 2506950, 2507206, 2507207, 2441671, 2441672, 2441673, 2441674, 2376138, 2376139, 2376395, 2376396, 2376397, 2310861, 2310862, 2310863, 2310864, 2311120, 2245584, 2245585, 2245586, 2245587, 2180051, 2180052, 2180308, 2180309, 2180310, 2114774, 2114775, 2114776, 2114777, 2049241, 2049497, 2049498, 2049499, 2049500, 1983964, 1983965, 1983966, 1984222, 1984223, 1918687, 1918688, 1918689, 1918690, 1853154, 1853155, 1853411, 1853412, 1853413, 1787877, 1787878, 1787879, 1787880, 1788136, 1722600, 1722601, 1722602, 1722603, 1657067, 1657068, 1657069, 1657325, 1657326, 1591790, 1591791, 1591792, 1591793, 1526514])  # CF敌方红名库

    # 如果文件不存在则退出
    check_file('yolov4-tiny')

    # 分享数据以及展示新进程
    arr = Array('i', range(22))
    """
    0  窗口句柄
    1  分析进程状态
    2  是否全屏
    3  截图FPS整数值
    4  控制鼠标
    5  左侧距离除数
    6  使用GPU/CPU(1/0)
    7  鼠标移动x
    8  鼠标移动y
    9  鼠标开火r
    10 柯南
    11 敌人数量
    12 瞄准位置
    13 射击速度
    14 敌人近否
    15 所持武器
    16 指向身体
    17 自瞄自火
    18 基础边长
    19 火线红名
    20 后坐力控制
    21 鼠标按键
    """
    arr[1] = 0  # 分析进程状态
    arr[2] = 0  # 是否全屏
    arr[3] = 0  # FPS值
    arr[4] = 0  # 控制鼠标
    arr[7] = 0  # 鼠标移动x
    arr[8] = 0  # 鼠标移动r
    arr[9] = 0  # 鼠标开火r
    arr[10] = Conan  # 柯南
    arr[11] = 0  # 敌人数量
    arr[12] = 0  # 瞄准位置(0中1头2胸)
    arr[13] = 944  # 射击速度
    arr[14] = 0  # 敌人近否
    arr[15] = 0  # 所持武器(0无1主2副)
    arr[16] = 0  # 指向身体
    arr[17] = 1  # 自瞄/自火
    arr[18] = 0  # 基础边长
    arr[19] = 0  # CF下红名
    arr[20] = 0  # 简易后坐力控制
    detect_proc = Process(target=detection, args=(arr,))

    # 寻找读取游戏窗口类型并确认截取位置
    window_class_name, window_hwnd_name, test_win[0] = get_window_info()
    arr[0] = window_hwnd_name

    # 确认大致平均后坐力
    recoil_control[0] = {
        'CrossFire': 2,  # 32
        'Valve001': 2,  # 2.5
        'LaunchCombatUWindowsClient': 2,  # 10.0
        'LaunchUnrealUWindowsClient': 5,  # 20
    }.get(window_class_name, 2)

    # 如果非全屏则展示效果
    arr[2] = 1 if is_full_screen(window_hwnd_name) else 0
    if not arr[2]:
        show_proc = Process(target=show_frames, args=(frame_output, arr,))
        show_proc.start()
    else:
        print('全屏模式下不会有小窗口...')

    # 等待游戏画面完整出现(拥有大于0的长宽)
    window_ready = 0
    while not window_ready:
        sleep(1)
        win_client_rect = win32gui.GetClientRect(window_hwnd_name)
        win_pos = win32gui.ClientToScreen(window_hwnd_name, (0, 0))
        if win_client_rect[2] - win_client_rect[0] > 0 and win_client_rect[3] - win_client_rect[1] > 0:
            window_ready = 1
    client_ratio = (win_client_rect[2] - win_client_rect[0]) / (win_client_rect[3] - win_client_rect[1])
    print(win_pos[0], win_pos[1], win_client_rect[2], win_client_rect[3])

    # 初始化截图类
    win_cap = WindowCapture(window_class_name, window_hwnd_name, 4/9, 192/224)

    # 初始化分析类
    # Analysis = FrameDetectionX(arr[0])
    Analysis = FrameDetection34(arr[0])

    # 计算基础边长
    arr[18] = win_cap.get_side_len()

    # 开始分析进程
    detect_proc.start()

    # 等待分析类初始化
    while not arr[1]:
        sleep(4)

    # clear()  # 清空命令指示符面板

    ini_sct_time = 0  # 初始化计时
    small_float = np.finfo(np.float64).eps  # 初始化一个尽可能小却小得不过分的数

    winw, winh = win_cap.get_window_info()
    cutw, cuth = win_cap.get_cut_info()

    while True:
        screenshot = win_cap.grab_screenshot()
        # screenshot = win_cap.get_screenshot()
        if window_class_name == 'CrossFire':
            cut_scrn = screenshot[cuth // 2 + winh // 16 : cuth // 2 + winh // 15, cutw // 2 - winw // 40 : cutw // 2 + winw // 40]  # 从截屏中截取红名区域
            # 将红名区域rgb转为十进制数值
            hexcolor = []
            for i in range(cut_scrn.shape[0]):
                for j in range(cut_scrn.shape[1]):
                    rgbint = cut_scrn[i][j][0]<<16 | cut_scrn[i][j][1]<<8 | cut_scrn[i][j][2]
                    hexcolor.append(rgbint)
            # 与内容中的敌方红名色库比较
            hexcolor = np.array(hexcolor)
            indices = np.intersect1d(cf_enemy_color, hexcolor)
            arr[19] = len(indices)

        try:
            screenshot.any()
            frame_height, frame_width = screenshot.shape[:2]

            # 画实心框避免错误检测武器与手
            if window_class_name == 'CrossFire':
                cv2.rectangle(screenshot, (int(frame_width*5/6), int(frame_height*3/4)), (frame_width, frame_height), (127, 127, 127), cv2.FILLED)
                cv2.rectangle(screenshot, (0, int(frame_height*3/4)), (int(frame_width*1/6), frame_height), (127, 127, 127), cv2.FILLED)
                if frame_width / frame_height > 1.3:
                    frame_width = int(frame_width / 4 * 3)
                    dim = (frame_width, frame_height)
                    screenshot = cv2.resize(screenshot, dim, interpolation=cv2.INTER_AREA)
            elif window_class_name == 'Valve001':
                cv2.rectangle(screenshot, (int(frame_width*5/6), int(frame_height*2/3)), (frame_width, frame_height), (127, 127, 127), cv2.FILLED)
                cv2.rectangle(screenshot, (0, int(frame_height*2/3)), (int(frame_width*1/6), frame_height), (127, 127, 127), cv2.FILLED)

            arr[5] = (150 if win_cap.get_window_left() - 10 < 150 else win_cap.get_window_left() - 10)
        except (AttributeError, pywintypes.error) as e:
            print('窗口已关闭\n' + str(e))
            break

        if arr[10]:
            arr[11], arr[7], arr[8], arr[9], arr[12], arr[14], arr[16], screenshot = Analysis.detect(screenshot, arr[20])
        if not arr[2]:
            frame_input.send(screenshot)

        exit_program, arr[4] = check_status(exit_program, arr[4])
        if exit_program:
            break

        if win32gui.GetForegroundWindow() == window_hwnd_name and not test_win[0]:
            if arr[4]:  # 是否需要控制鼠标
                if arr[15] == 1:  # 主武器
                    arr[13] = (944 if arr[14] or arr[12] != 1 else 1694)
                elif arr[15] == 2:  # 副武器
                    arr[13] = (694 if arr[14] or arr[12] != 1 else 944)
            move_record_x, move_record_y, d_time, u_time = control_mouse(arr[7], arr[8], show_fps[0], arr[9], arr[13] / 10, arr[16], window_class_name, move_record_x, move_record_y, d_time, u_time)

        time_used = time() - ini_sct_time
        ini_sct_time = time()
        current_fps = 1 / (time_used + small_float)
        process_time.append(current_fps)
        if len(process_time) > 119:
            process_time.popleft()

        show_fps[0] = median(process_time)  # 计算fps
        arr[3] = int(show_fps[0])

    win_cap.release_resource()
    close()
    exit(0)
