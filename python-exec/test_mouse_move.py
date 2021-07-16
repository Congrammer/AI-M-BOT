from win32con import MOUSEEVENTF_MOVE, MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP
from sys import exit, executable
from win32api import mouse_event
from keyboard import is_pressed
from time import sleep, time
from ctypes import windll
import win32gui
import mss
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


os.chdir(os.path.dirname(os.path.abspath(__file__)))
image = 0

if not is_admin():
    restart()

with mss.mss() as sct:
    while True:
        hwnd_active = win32gui.GetForegroundWindow()
        client_rect = win32gui.GetClientRect(hwnd_active)
        corner_xy = win32gui.ClientToScreen(hwnd_active, (0, 0))
        monitor = {'top': corner_xy[1], 'left': corner_xy[0], 'width': client_rect[2] - client_rect[0], 'height': client_rect[3] - client_rect[1]}
        output = 'sct-{top}x{left}_{width}x{height}'.format(**monitor) + f'_{time()}.png'

        if is_pressed('left'):
            mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0)
            mouse_event(MOUSEEVENTF_LEFTUP, 0, 0)
            for i in range(10):
                mouse_event(MOUSEEVENTF_MOVE, -2, 0, 0, 0)
                print(i)
                sleep(0.5)
            mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0)
            mouse_event(MOUSEEVENTF_LEFTUP, 0, 0)
            mouse_event(MOUSEEVENTF_MOVE, 10, 0, 0, 0)
            image += 1

            sct_img = sct.grab(monitor)
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
        elif is_pressed('right'):
            mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0)
            mouse_event(MOUSEEVENTF_LEFTUP, 0, 0)
            for i in range(10):
                mouse_event(MOUSEEVENTF_MOVE, 2, 0, 0, 0)
                print(i)
                sleep(0.5)
            mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0)
            mouse_event(MOUSEEVENTF_LEFTUP, 0, 0)
            mouse_event(MOUSEEVENTF_MOVE, -10, 0, 0, 0)
            image += 1

            sct_img = sct.grab(monitor)
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
        elif is_pressed('end'):
            break

exit(0)