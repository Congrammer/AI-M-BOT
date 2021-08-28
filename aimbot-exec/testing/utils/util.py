from platform import release
from ctypes import windll
from os import system
from sys import exit
import nvidia_smi
import pywintypes
import win32gui
import pynvml


# 简单检查gpu是否够格
def check_gpu():
    try:
        pynvml.nvmlInit()
        gpu_handle = pynvml.nvmlDeviceGetHandleByIndex(0)  # 默认卡1
        gpu_name = pynvml.nvmlDeviceGetName(gpu_handle)
        memory_info = pynvml.nvmlDeviceGetMemoryInfo(gpu_handle)
        pynvml.nvmlShutdown()
    except (FileNotFoundError, pynvml.nvml.NVML_ERROR_LIBRARY_NOT_FOUND) as e:
        print(str(e))
        nvidia_smi.nvmlInit()
        gpu_handle = nvidia_smi.nvmlDeviceGetHandleByIndex(0)  # 默认卡1
        gpu_name = nvidia_smi.nvmlDeviceGetName(gpu_handle)
        memory_info = nvidia_smi.nvmlDeviceGetMemoryInfo(gpu_handle)
        nvidia_smi.nvmlShutdown()
    if b'RTX' in gpu_name:
        return 2
    memory_total = memory_info.total / 1024 / 1024
    if memory_total > 3000:
        return 1
    return 0


# 高DPI感知
def set_dpi():
    if int(release()) >= 7:
        try:
            windll.shcore.SetProcessDpiAwareness(1)
        except AttributeError:
            windll.user32.SetProcessDPIAware()
    else:
        exit(0)


# 检测是否全屏
def is_full_screen(hWnd):
    try:
        full_screen_rect = (0, 0, windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1))
        window_rect = win32gui.GetWindowRect(hWnd)
        return window_rect == full_screen_rect
    except pywintypes.error as e:
        print('全屏检测错误\n' + str(e))
        return False


# 检查是否为管理员权限
def is_admin():
    try:
        return windll.shell32.IsUserAnAdmin()
    except OSError as err:
        print('OS error: {0}'.format(err))
        return False


# 清空命令指示符输出
def clear():
    _ = system('cls')
