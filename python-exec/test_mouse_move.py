from win32con import SPI_GETMOUSE, SPI_SETMOUSE
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
    windll.user32.mouse_event(0x0002, 0, 0, 0, 0)
    windll.user32.mouse_event(0x0004, 0, 0, 0, 0)
    sleep(0.3)
    for i in range(10):
        windll.user32.mouse_event(0x0001, int(num/DPI_Var), 0, 0, 0)
        print(str('{:02.0f}'.format(i+1)), end='\r')
        sleep(0.3)
    windll.user32.mouse_event(0x0002, 0, 0, 0, 0)
    windll.user32.mouse_event(0x0004, 0, 0, 0, 0)
    sleep(0.3)
    windll.user32.mouse_event(0x0001, int(num*-5/DPI_Var), 0, 0, 0)
    sleep(0.3)

    # MOUSEEVENTF_MOVE = 0x0001 # mouse move
    # MOUSEEVENTF_LEFTDOWN = 0x0002 # left button down
    # MOUSEEVENTF_LEFTUP = 0x0004 # left button up
    # MOUSEEVENTF_RIGHTDOWN = 0x0008 # right button down
    # MOUSEEVENTF_RIGHTUP = 0x0010 # right button up
    # MOUSEEVENTF_MIDDLEDOWN = 0x0020 # middle button down
    # MOUSEEVENTF_MIDDLEUP = 0x0040 # middle button up
    # MOUSEEVENTF_WHEEL = 0x0800 # wheel button rolled
    # MOUSEEVENTF_ABSOLUTE = 0x8000 # absolute move

    if enhanced_holdback[1]:
        win32gui.SystemParametersInfo(SPI_SETMOUSE, enhanced_holdback, 0)


os.chdir(os.path.dirname(os.path.abspath(__file__)))
find_window = 0

if not is_admin():
    restart()

while not find_window:
    hwnd_active = win32gui.GetForegroundWindow()
    try:
        title_name = win32gui.GetWindowText(hwnd_active)
        class_name = win32gui.GetClassName(hwnd_active)
        result = windll.user32.MessageBoxW(0, title_name, 'Is this the window you want?', 4)
        find_window = (1 if result == 6 else 0)
    except pywintypes.error:
        continue
    sleep(3)

with mss() as sct:
    hwnd = win32gui.FindWindow(class_name, None)
    client_rect = win32gui.GetClientRect(hwnd)
    corner_xy = win32gui.ClientToScreen(hwnd, (0, 0))
    monitor = {'top': corner_xy[1], 'left': corner_xy[0], 'width': client_rect[2] - client_rect[0], 'height': client_rect[3] - client_rect[1]}
    print('Get start!!! ' + class_name)
    moved = 0
    while True:
        if is_pressed('left'):
            mouse_move_lr(-10)
            moved = 1
        elif is_pressed('right'):
            mouse_move_lr(10)
            moved = 1
        if moved:
            sct_img = sct.grab(monitor)
            output = 'sct-{top}x{left}_{width}x{height}'.format(**monitor) + f'_{time()}.png'
            tools.to_png(sct_img.rgb, sct_img.size, output=output)
            moved = 0
        if is_pressed('end'):
            break

exit(0)