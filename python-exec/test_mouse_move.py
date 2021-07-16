from sys import exit, executable
from win32api import mouse_event
from keyboard import is_pressed
from time import sleep, time
from mss import mss, tools
from ctypes import windll
import pydirectinput
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
    pydirectinput.click()
    for i in range(10):
        pydirectinput.move(num, 0)
        print(str('{:02.0f}'.format(i+1)), end='\r')
        sleep(0.5)
    pydirectinput.click()
    pydirectinput.move(num*-5, 0)


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
    print('Get start!!!')
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