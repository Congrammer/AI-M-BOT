from win32con import SPI_GETMOUSE, SPI_SETMOUSE, SPI_GETMOUSESPEED, SPI_SETMOUSESPEED
from ctypes import windll, c_long, c_ulong, Structure, Union, c_int, POINTER, sizeof
from sys import exit, executable
from keyboard import is_pressed
from time import sleep, time
from mss import mss, tools
import pywintypes
import win32gui
import os


# ↓↓↓↓↓↓↓↓↓ 简易鼠标行为模拟,使用SendInput函数 ↓↓↓↓↓↓↓↓↓
LONG = c_long
DWORD = c_ulong
ULONG_PTR = POINTER(DWORD)


class MOUSEINPUT(Structure):
    _fields_ = (('dx', LONG),
                ('dy', LONG),
                ('mouseData', DWORD),
                ('dwFlags', DWORD),
                ('time', DWORD),
                ('dwExtraInfo', ULONG_PTR))


class _INPUTunion(Union):
    _fields_ = (('mi', MOUSEINPUT), ('mi', MOUSEINPUT))


class INPUT(Structure):
    _fields_ = (('type', DWORD),
                ('union', _INPUTunion))


def SendInput(*inputs):
    nInputs = len(inputs)
    LPINPUT = INPUT * nInputs
    pInputs = LPINPUT(*inputs)
    cbSize = c_int(sizeof(INPUT))
    return windll.user32.SendInput(nInputs, pInputs, cbSize)


def Input(structure):
    return INPUT(0, _INPUTunion(mi=structure))


def MouseInput(flags, x, y, data):
    return MOUSEINPUT(x, y, data, flags, 0, None)


def Mouse(flags, x=0, y=0, data=0):
    return Input(MouseInput(flags, x, y, data))


def sp_mouse_xy(x, y):
    return SendInput(Mouse(0x0001, x, y))


def sp_mouse_down(key = 'LButton'):
    if key == 'LButton':
        return SendInput(Mouse(0x0002))
    elif key == 'RButton':
        return SendInput(Mouse(0x0008))


def sp_mouse_up(key = 'LButton'):
    if key == 'LButton':
        return SendInput(Mouse(0x0004))
    elif key == 'RButton':
        return SendInput(Mouse(0x0010))


def sp_mouse_click(key = 'LButton'):
    sp_mouse_down(key)
    sp_mouse_up(key)
# ↑↑↑↑↑↑↑↑↑ 简易鼠标行为模拟,使用SendInput函数 ↑↑↑↑↑↑↑↑↑


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

    sp_mouse_click()
    sleep(0.3)
    sp_mouse_xy(int(num/DPI_Var), 0)
    sleep(0.3)
    sp_mouse_click()
    sleep(0.3)
    sp_mouse_xy(-int(num/2/DPI_Var), 0)
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
        if is_pressed('left'):
            mouse_move_lr(-200)
            moved = 1
        elif is_pressed('right'):
            mouse_move_lr(200)
            moved = 1
        if moved:
            sct_img = sct.grab(monitor)
            output = 'sct-{top}x{left}_{width}x{height}'.format(**monitor) + f'_{time()}.png'
            tools.to_png(sct_img.rgb, sct_img.size, output=output)
            moved = 0
        if is_pressed('end'):
            break

exit(0)