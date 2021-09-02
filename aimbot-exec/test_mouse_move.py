from win32con import SPI_GETMOUSE, SPI_SETMOUSE, SPI_GETMOUSESPEED, SPI_SETMOUSESPEED, MOUSEEVENTF_MOVE, MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP
from win32api import mouse_event
from sys import exit, executable
from keyboard import is_pressed
from time import sleep, time
from mss import mss, tools
from ctypes import windll
import pywintypes
import win32gui
import os


def restart():
    windll.shell32.ShellExecuteW(None, 'runas', executable, __file__, None, 1)
    exit(0)


def is_admin():
    try:
        return windll.shell32.IsUserAnAdmin()
    except OSError as err:
        print('OS error: {0}'.format(err))
        return False


def mouse_move_lr(num):
    DPI_Var = windll.user32.GetDpiForWindow(hwnd) / 96
    enhanced_holdback = win32gui.SystemParametersInfo(SPI_GETMOUSE)
    if enhanced_holdback[1]:
        win32gui.SystemParametersInfo(SPI_SETMOUSE, [0, 0, 0], 0)
    mouse_speed = win32gui.SystemParametersInfo(SPI_GETMOUSESPEED)
    if mouse_speed != 10:
        win32gui.SystemParametersInfo(SPI_SETMOUSESPEED, 10, 0)

    mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    sleep(0.3)
    for i in range(20):
        mouse_event(MOUSEEVENTF_MOVE, int(num/DPI_Var), 0, 0, 0)
        sleep(0.2)
    mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    sleep(0.3)
    mouse_event(MOUSEEVENTF_MOVE, -int(num*10/DPI_Var), 0, 0, 0)
    sleep(0.3)

    if enhanced_holdback[1]:
        win32gui.SystemParametersInfo(SPI_SETMOUSE, enhanced_holdback, 0)
    if mouse_speed != 10:
        win32gui.SystemParametersInfo(SPI_SETMOUSESPEED, mouse_speed, 0)


os.chdir(os.path.dirname(os.path.abspath(__file__)))
find_window = 0

if not is_admin():
    restart()

while not find_window:
    sleep(3)
    hwnd_active = win32gui.GetForegroundWindow()
    try:
        title_name = win32gui.GetWindowText(hwnd_active)
        class_name = win32gui.GetClassName(hwnd_active)
        result = windll.user32.MessageBoxW(0, title_name, 'Is this the window you want?', 4)
        find_window = (1 if result == 6 else 0)
    except pywintypes.error:
        continue

with mss() as sct:
    hwnd = win32gui.FindWindow(class_name, None)
    client_rect = win32gui.GetClientRect(hwnd)
    corner_xy = win32gui.ClientToScreen(hwnd, (0, 0))
    monitor = {'top': corner_xy[1], 'left': corner_xy[0], 'width': client_rect[2] - client_rect[0], 'height': client_rect[3] - client_rect[1]}
    print('Get start!!! ' + class_name)
    moved = 0
    while True:
        sleep(0.1)
        if is_pressed('left'):
            mouse_move_lr(-5)
            moved = 1
        elif is_pressed('right'):
            mouse_move_lr(5)
            moved = 1
        if moved:
            sct_img = sct.grab(monitor)
            output = 'sct-{top}x{left}_{width}x{height}'.format(**monitor) + f'_{time()}.png'
            tools.to_png(sct_img.rgb, sct_img.size, output=output)
            moved = 0
        if is_pressed('end'):
            break

exit(0)