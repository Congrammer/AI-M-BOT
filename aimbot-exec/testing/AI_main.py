from win32con import VK_END, PROCESS_ALL_ACCESS, SPI_GETMOUSE, SPI_SETMOUSE, SPI_GETMOUSESPEED, SPI_SETMOUSESPEED
from util import set_dpi, is_full_screen, is_admin, clear, restart, millisleep, get_window_info
from win32api import GetAsyncKeyState, GetCurrentProcessId, OpenProcess, GetSystemMetrics
from win32process import SetPriorityClass, ABOVE_NORMAL_PRIORITY_CLASS
from multiprocessing import Process, shared_memory, Array, Pipe, Lock
from mouse import mouse_xy, mouse_down, mouse_up, mouse_close
from darknet_yolo34 import FrameDetection34
from math import sqrt, pow, atan, cos, pi
from pynput.mouse import Listener, Button
from torch_yolox import FrameDetectionX
from scrnshot import WindowCapture
from sys import exit, platform
from collections import deque
from statistics import median
from random import uniform
from ctypes import windll
from time import time
import numpy as np
import pywintypes
import win32gui
import cv2
import os


# 检测是否存在配置与权重文件
def check_file(file):
    cfg_file = file + '.cfg'
    weights_file = file + '.weights'
    if not (os.path.isfile(cfg_file) and os.path.isfile(weights_file)):
        print(f'请下载{file}相关文件!!!')
        millisleep(3000)
        exit(0)


# 加锁换值
def change_withlock(arrays, var, target_var, locker):
    with locker:
        arrays[var] = target_var


# 移动鼠标
def move_mouse(a, b, fps_var, ranges, win_class, move_rx, move_ry):
    # move_rx, a = track_opt(move_rx, a)
    # move_ry, b = track_opt(move_ry, b)
    move_range = sqrt(pow(a, 2) + pow(b, 2))
    enhanced_holdback = win32gui.SystemParametersInfo(SPI_GETMOUSE)
    if enhanced_holdback[1]:
        win32gui.SystemParametersInfo(SPI_SETMOUSE, [0, 0, 0], 0)
    mouse_speed = win32gui.SystemParametersInfo(SPI_GETMOUSESPEED)
    if mouse_speed != 10:
        win32gui.SystemParametersInfo(SPI_SETMOUSESPEED, 10, 0)

    if fps_var and arr[6]:
        a = cos((pi - atan(a/arr[5])) / 2) * (2*arr[5]) / DPI_Var[0]
        b = cos((pi - atan(b/arr[5])) / 2) * (2*arr[5]) / DPI_Var[0]
        # if move_range > 6 * ranges:
        #     a *= uniform(0.9, 1.1)
        #     b *= uniform(0.9, 1.1)
        fps_factorx = pow(fps_var/4, 1/3)
        fps_factory = pow(fps_var/3, 1/3)
        x0 = {
            'CrossFire': a / 2.719 / fps_factorx,  # 32
            'Valve001': a * 1.667 / fps_factorx,  # 2.5
            'LaunchCombatUWindowsClient': a * 1.319 / fps_factorx,  # 10.0
            'LaunchUnrealUWindowsClient': a / 2.557 / fps_factorx,  # 20
        }.get(win_class, a / fps_factorx)
        y0 = {
            'CrossFire': b / 2.719 / fps_factory,  # 32
            'Valve001': b * 1.667 / fps_factory,  # 2.5
            'LaunchCombatUWindowsClient': b * 1.319 / fps_factory,  # 10.0
            'LaunchUnrealUWindowsClient': b / 2.557 / fps_factory,  # 20
        }.get(win_class, b / fps_factory)

        mouse_xy(int(round(x0)), int(round(y0)))

    if enhanced_holdback[1]:
        win32gui.SystemParametersInfo(SPI_SETMOUSE, enhanced_holdback, 0)
    if mouse_speed != 10:
        win32gui.SystemParametersInfo(SPI_SETMOUSESPEED, mouse_speed, 0)

    return move_rx, move_ry, move_range


# 鼠标射击
def click_mouse(win_class, move_range, ranges, rate, go_fire):
    # 不分敌友射击
    if arr[15]:  # GetAsyncKeyState(VK_LBUTTON) < 0
        if time() * 1000 - arr[16] > 30.6:  # press_moment
            mouse_up()
    elif (win_class != 'CrossFire' or arr[13]):
        if (go_fire or move_range < ranges):
            if time() * 1000 - arr[17] > rate:  # release_moment
                mouse_down()
                change_withlock(arr, 18, arr[18] + 1, lock)

    if time() * 1000 - arr[17] > 219.4:
        change_withlock(arr, 18, 0, lock)

    if arr[18] > 12:
        change_withlock(arr, 18, 12, lock)


# 傻追踪优化
def track_opt(record_list, range_m):
    if len(record_list):
        if abs(median(record_list) - range_m) <= 15 and abs(range_m) <= 90:
            record_list.append(range_m)
        else:
            record_list.clear()
        if len(record_list) > sqrt(show_fps[0]) and arr[6]:
            range_m *= pow(show_fps[0]/3, 1/3)
            record_list.clear()
    else:
        record_list.append(range_m)

    return record_list, range_m


# 转变状态
def check_status(exit0, restart0):
    if GetAsyncKeyState(VK_END) < 0:  # End
        exit0 = True
        change_withlock(arr, 14, 1, lock)
    elif GetAsyncKeyState(0x31) < 0:  # 1
        change_withlock(arr, 6, 1, lock)
    elif GetAsyncKeyState(0x32) < 0:  # 2
        change_withlock(arr, 6, 2, lock)
    elif GetAsyncKeyState(0x33) < 0 or GetAsyncKeyState(0x34) < 0:  # 3,4
        change_withlock(arr, 6, 0, lock)
    elif GetAsyncKeyState(0x46) < 0:  # F
        change_withlock(arr, 8, 1, lock)
    elif GetAsyncKeyState(0x4A) < 0:  # J
        change_withlock(arr, 8, 0, lock)
    elif GetAsyncKeyState(0x50) < 0:  # P
        restart0 = 1
        change_withlock(arr, 14, 1, lock)

    return exit0, restart0


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
        }.get(array[6])
        try:
            img_ex = np.zeros((1, 1, 3), np.uint8)
            show_str0 = str('{:03.1f}'.format(array[4]))
            show_str1 = 'Detected ' + str('{:02.0f}'.format(array[7])) + ' targets'
            show_str2 = 'Aiming at ' + fire_target_show[int(array[11])] + ' position'
            show_str3 = 'Fire rate is at ' + str('{:02.0f}'.format((1000 / (array[10] + 30.6)))) + ' RPS'
            show_str4 = 'Please enjoy coding ^_^' if array[8] else 'Please enjoy coding @_@'
            if show_img.any():
                show_img_h, show_img_w = show_img.shape[:2]
                show_img = cv2.resize(show_img, (int(array[3]), int(array[3] / show_img_w * show_img_h)))
                img_ex = cv2.resize(img_ex, (int(array[3]), int(array[3] / 2)))
                cv2.putText(show_img, show_str0, (int(array[3] / 25), int(array[3] / 12)), font, array[3] / 600, (127, 255, 0), 2, cv2.LINE_AA)
                cv2.putText(img_ex, show_str1, (10, int(array[3] / 9)), font, array[3] / 450, show_color, 1, cv2.LINE_AA)
                cv2.putText(img_ex, show_str2, (10, int(array[3] / 9) * 2), font, array[3] / 450, show_color, 1, cv2.LINE_AA)
                cv2.putText(img_ex, show_str3, (10, int(array[3] / 9) * 3), font, array[3] / 450, show_color, 1, cv2.LINE_AA)
                cv2.putText(img_ex, show_str4, (10, int(array[3] / 9) * 4), font, array[3] / 450, show_color, 1, cv2.LINE_AA)
                show_image = cv2.vconcat([show_img, img_ex])
                cv2.imshow('Show frame', show_image)
                cv2.waitKey(1)
        except (AttributeError, cv2.error):
            cv2.destroyAllWindows()

        if array[14]:
            break

    cv2.destroyAllWindows()


# 鼠标检测进程
def mouse_detection(array, lock):
    def on_click(x, y, button, pressed):
        change_withlock(array, 15, 1 if pressed and button == Button.left else 0, lock)
        if pressed and button == Button.left:
            change_withlock(array, 16, time() * 1000, lock)
        elif not pressed and button == Button.left:
            change_withlock(array, 17, time() * 1000, lock)

    with Listener(on_click=on_click) as listener:
        listener.join()


# 截图进程
def capturing(array, the_class_name, the_hwnd_name, lock):
    shm_img = shared_memory.SharedMemory(create=True, size=GetSystemMetrics(0) * GetSystemMetrics(1) * 3, name='shareimg')  # 创建进程间共享内存
    cf_enemy_color = np.array([3487638, 3487639, 3487640, 3487641, 3422105, 3422106, 3422362, 3422363, 3422364, 3356828, 3356829, 3356830, 3356831, 3291295, 3291551, 3291552, 3291553, 3291554, 3226018, 3226019, 3226020, 3226276, 3226277, 3160741, 3160742, 3160743, 3160744, 3095208, 3095209, 3095465, 3095466, 3095467, 3029931, 3029932, 3029933, 3029934, 3030190, 2964654, 2964655, 2964656, 2964657, 2899121, 2899122, 2899123, 2899379, 2899380, 2833844, 2833845, 2833846, 2833847, 2768311, 2768567, 2768568, 2768569, 2768570, 2703034, 2703035, 2703036, 2703292, 2703292, 2703293, 2637757, 2637758, 2637759, 2637760, 2572224, 2572225, 2572481, 2572482, 2572483, 2506948, 2506949, 2506950, 2507206, 2507207, 2441671, 2441672, 2441673, 2441674, 2376138, 2376139, 2376395, 2376396, 2376397, 2310861, 2310862, 2310863, 2310864, 2311120, 2245584, 2245585, 2245586, 2245587, 2180051, 2180052, 2180308, 2180309, 2180310, 2114774, 2114775, 2114776, 2114777, 2049241, 2049497, 2049498, 2049499, 2049500, 1983964, 1983965, 1983966, 1984222, 1984223, 1918687, 1918688, 1918689, 1918690, 1853154, 1853155, 1853411, 1853412, 1853413, 1787877, 1787878, 1787879, 1787880, 1788136, 1722600, 1722601, 1722602, 1722603, 1657067, 1657068, 1657069, 1657325, 1657326, 1591790, 1591791, 1591792, 1591793, 1526514])  # CF敌方红名库

    win_cap = WindowCapture(the_class_name, the_hwnd_name, 4/9, 192/224)  # 初始化截图类
    winw, winh = win_cap.get_window_info()  # 获取窗口宽高
    cutw, cuth = win_cap.get_cut_info()  # 获取截屏宽高
    change_withlock(array, 1, cutw, lock)
    change_withlock(array, 0, cuth, lock)

    # 计算基础边长
    change_withlock(array, 5, win_cap.get_side_len(), lock)
    change_withlock(array, 2, 1, lock)
    print(f'基础边长 = {array[5]}')

    while True:
        millisleep(1)  # 降低平均cpu占用
        # screenshot = win_cap.grab_screenshot()
        screenshots = win_cap.get_screenshot()
        change_withlock(array, 0, screenshots.shape[0], lock)
        change_withlock(array, 1, screenshots.shape[1], lock)
        with lock:
            shared_img = np.ndarray(screenshots.shape, dtype=screenshots.dtype, buffer=shm_img.buf)
            shared_img[:] = screenshots[:]  # 将截取数据拷贝进分享的内存
        if the_class_name == 'CrossFire':
            cut_scrn = screenshots[cuth // 2 + winh // 16 : cuth // 2 + winh // 15, cutw // 2 - winw // 40 : cutw // 2 + winw // 40]  # 从截屏中截取红名区域

            # 将红名区域rgb转为十进制数值
            hexcolor = []
            for i in range(cut_scrn.shape[0]):
                for j in range(cut_scrn.shape[1]):
                    rgbint = cut_scrn[i][j][0]<<16 | cut_scrn[i][j][1]<<8 | cut_scrn[i][j][2]
                    hexcolor.append(rgbint)

            # 与内容中的敌方红名色库比较
            hexcolor = np.array(hexcolor)
            indices = np.intersect1d(cf_enemy_color, hexcolor)
            change_withlock(array, 13, len(indices), lock)

        win_left = (150 if win_cap.get_window_left() - 10 < 150 else win_cap.get_window_left() - 10)
        change_withlock(array, 3, win_left, lock)

        if array[14]:
            break

    win_cap.release_resource()
    shm_img.close()


# 主程序
def main():
    set_dpi()  # 设置高DPI不受影响
    os.chdir(os.path.dirname(os.path.abspath(__file__)))  # 设置工作路径
    check_file('yolov4-tiny')  # 如果文件不存在则退出

    if not is_admin():  # 检查管理员权限
        restart(__file__)

    # 提升进程优先级
    if platform == 'win32':
        pid = GetCurrentProcessId()
        handle = OpenProcess(PROCESS_ALL_ACCESS, True, pid)
        SetPriorityClass(handle, ABOVE_NORMAL_PRIORITY_CLASS)
    else:
        os.nice(1)

    # 滑稽/选择模型
    Conan = -1
    while not (2 >= Conan >= 0):
        user_choice = input('柯南能在本程序作者有生之年完结吗?(1:能, 2:能, 0:不能): ')
        try:
            Conan = int(user_choice)
        except ValueError:
            print('呵呵...请重新输入')
        finally:
            if not (2 >= Conan >= 0):
                print('请在给定范围选择')

    global show_fps, DPI_Var
    show_fps, DPI_Var = [1], [1]

    # 寻找读取游戏窗口类型并确认截取位置
    window_class_name, window_hwnd_name, window_outer_hwnd, test_win = get_window_info()

    mouse_detect_proc = Process(target=mouse_detection, args=(arr, lock,))  # 鼠标检测进程
    frame_output, frame_input = Pipe(False)  # 初始化管道(receiving,sending)
    show_proc = Process(target=show_frames, args=(frame_output, arr,))  # 效果展示进程
    capture_proc = Process(target=capturing, args=(arr, window_class_name, window_hwnd_name, lock,))  # 截图进程

    # 检查窗口DPI
    DPI_Var[0] = max(windll.user32.GetDpiForWindow(window_outer_hwnd) / 96, windll.user32.GetDpiForWindow(window_hwnd_name) / 96)
    if DPI_Var[0] == 0.0:
        DPI_Var[0] = 1.0

    process_times = deque()
    exit_program, restart_program = False, False
    move_record_x, move_record_y = [], []

    arr[0] = 0  # 截图宽
    arr[1] = 0  # 截图高
    arr[2] = 0  # 截图进程状态
    arr[3] = 0  # 左侧距离
    arr[4] = 0  # FPS值
    arr[5] = 600  # 基础边长
    arr[6] = 0  # 控制鼠标/所持武器
    arr[7] = 0  # 目标数量
    arr[8] = 1  # 移动鼠标与否
    arr[9] = 1  # 按击鼠标与否
    arr[10] = 94.4  # 射击速度
    arr[11] = 0  # 瞄准位置(0中1头2胸)
    arr[12] = 0  # 简易后坐力控制
    arr[13] = 0  # CF下红名
    arr[14] = 0  # 是否退出
    arr[15] = 0  # 鼠标状态
    arr[16] = time()  # 左键按下时刻
    arr[17] = time()  # 左键抬起时刻
    arr[18] = 0  # 连续射击次数

    # 确认大致平均后坐影响
    recoil_control = {
        'CrossFire': 2,  # 32
        'Valve001': 2,  # 2.5
        'LaunchCombatUWindowsClient': 2,  # 10.0
        'LaunchUnrealUWindowsClient': 5,  # 20
    }.get(window_class_name, 2)

    capture_proc.start()  # 开始截图进程
    mouse_detect_proc.start()  # 开始鼠标监测进程

    # 如果非全屏则展示效果
    F11_Mode = 1 if is_full_screen(window_hwnd_name) else 0
    if not F11_Mode:
        show_proc.start()
    else:
        print('全屏模式下不会有小窗口...')

    # 等待游戏画面完整出现(拥有大于0的长宽)
    window_ready = 0
    while not window_ready:
        millisleep(1000)
        win_client_rect = win32gui.GetClientRect(window_hwnd_name)
        win_pos = win32gui.ClientToScreen(window_hwnd_name, (0, 0))
        if win_client_rect[2] - win_client_rect[0] > 0 and win_client_rect[3] - win_client_rect[1] > 0:
            window_ready = 1

    print(win_pos[0], win_pos[1], win_client_rect[2], win_client_rect[3])

    # 初始化分析类
    Analysis = FrameDetectionX(window_hwnd_name) if Conan == 1 else FrameDetection34(window_hwnd_name)

    # 等待截图类初始化
    while not arr[2]:
        millisleep(4000)

    # clear()  # 清空命令指示符面板

    ini_sct_time = 0  # 初始化计时
    small_float = np.finfo(np.float64).eps  # 初始化一个尽可能小却小得不过分的数
    existing_shm = shared_memory.SharedMemory(name='shareimg')

    while True:
        try:
            screenshots = np.ndarray((int(arr[0]), int(arr[1]), 3), dtype=np.uint8, buffer=existing_shm.buf)
            if screenshots.any():
                screenshot = np.ndarray(screenshots.shape, dtype=screenshots.dtype)
                screenshot[:] = screenshots[:]
                frame_height, frame_width = screenshot.shape[:2]

            # 画实心框避免错误检测武器与手
            if window_class_name == 'CrossFire':
                cv2.rectangle(screenshot, (int(frame_width*2/3), int(frame_height*3/5)), (frame_width, frame_height), (127, 127, 127), cv2.FILLED)
                cv2.rectangle(screenshot, (0, int(frame_height*3/5)), (int(frame_width*1/3), frame_height), (127, 127, 127), cv2.FILLED)
            elif window_class_name == 'Valve001':
                cv2.rectangle(screenshot, (int(frame_width*5/6), int(frame_height*2/3)), (frame_width, frame_height), (127, 127, 127), cv2.FILLED)
                cv2.rectangle(screenshot, (0, int(frame_height*2/3)), (int(frame_width*1/6), frame_height), (127, 127, 127), cv2.FILLED)

        except (AttributeError, pywintypes.error) as e:
            print('窗口已关闭\n' + str(e))
            break

        if Conan:
            target_count, moveX, moveY, fire0range, fire0pos, enemy_close, can_fire, screenshot = Analysis.detect(screenshot, arr[12])
            change_withlock(arr, 7, target_count, lock)
            change_withlock(arr, 11, fire0pos, lock)

        if str(win32gui.GetForegroundWindow()) in (str(window_hwnd_name) + str(window_outer_hwnd)) and not test_win:
            change_withlock(arr, 12, recoil_control * arr[18], lock)
            if arr[6]:  # 是否需要控制鼠标
                if arr[6] == 1:  # 主武器
                    change_withlock(arr, 10, 94.4 if enemy_close or arr[11] != 1 else 169.4, lock)
                elif arr[6] == 2:  # 副武器
                    change_withlock(arr, 10, 69.4 if enemy_close or arr[11] != 1 else 94.4, lock)
                move_record_x, move_record_y, move0range = move_mouse(moveX, moveY, show_fps[0], fire0range, window_class_name, move_record_x, move_record_y)
                click_mouse(window_class_name, move0range, fire0range, arr[10], can_fire)

        if not F11_Mode:
            frame_input.send(screenshot)

        exit_program, restart_program = check_status(exit_program, restart_program)
        if exit_program or restart_program:
            break

        time_used = time() - ini_sct_time
        ini_sct_time = time()
        process_times.append(time_used)
        med_time = median(process_times)
        show_fps[0] = 1 / med_time if med_time > 0 else 1 / (med_time + small_float)
        change_withlock(arr, 4, int(show_fps[0]*10) / 10, lock)
        if len(process_times) > 119:
            process_times.popleft()

    millisleep(1000)  # 为了稳定
    if not arr[2]:
        show_proc.terminate()
    mouse_detect_proc.terminate()
    capture_proc.terminate()
    mouse_close()
    if restart_program:
        restart(__file__)
    exit(0)


arr = Array('d', range(20))  # 进程间分享数据
lock = Lock()  # 锁
