import os
from time import sleep
try:
    import win32api
    import win32con
except ModuleNotFoundError:
    os.system("pip install pywin32")
    import win32api
    import win32con

# sets up constant variables for keys
SHIFT = 0x10
NINE = 0x39
ZERO = 0x30
LEFT_BRACKET = 0xDB
RIGHT_BRACKET = 0xDD
APOSTROPHE = 0xDE
LEFT_ARROW = 0x25

# main program
while True:

    # waits a bit to not overload cpu
    sleep(.01)

    # finishes ()
    if win32api.GetKeyState(SHIFT) < 0 and win32api.GetKeyState(NINE) < 0:
        win32api.keybd_event(NINE, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(SHIFT, 0, 0, 0)
        win32api.keybd_event(ZERO, 0, 0, 0)
        win32api.keybd_event(ZERO, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(SHIFT, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(LEFT_ARROW, 0, 0, 0)
        win32api.keybd_event(LEFT_ARROW, 0, win32con.KEYEVENTF_KEYUP, 0)

    # finishes []
    if win32api.GetKeyState(LEFT_BRACKET) < 0:
        win32api.keybd_event(LEFT_BRACKET, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(RIGHT_BRACKET, 0, 0, 0)
        win32api.keybd_event(RIGHT_BRACKET, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(LEFT_ARROW, 0, 0, 0)
        win32api.keybd_event(LEFT_ARROW, 0, win32con.KEYEVENTF_KEYUP, 0)

    # finishes {}
    if win32api.GetKeyState(SHIFT) < 0 and win32api.GetKeyState(LEFT_BRACKET) < 0:
        win32api.keybd_event(LEFT_BRACKET, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(SHIFT, 0, 0, 0)
        win32api.keybd_event(RIGHT_BRACKET, 0, 0, 0)
        win32api.keybd_event(RIGHT_BRACKET, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(SHIFT, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(LEFT_ARROW, 0, 0, 0)
        win32api.keybd_event(LEFT_ARROW, 0, win32con.KEYEVENTF_KEYUP, 0)

    # finishes ""
    if win32api.GetKeyState(SHIFT) < 0 and win32api.GetKeyState(APOSTROPHE) < 0:
        win32api.keybd_event(APOSTROPHE, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(SHIFT, 0, 0, 0)
        win32api.keybd_event(APOSTROPHE, 0, 0, 0)
        win32api.keybd_event(APOSTROPHE, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(SHIFT, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(LEFT_ARROW, 0, 0, 0)
        win32api.keybd_event(LEFT_ARROW, 0, win32con.KEYEVENTF_KEYUP, 0)
