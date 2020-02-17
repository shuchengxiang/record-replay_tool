from pynput import mouse
from pynput.mouse import Button, Controller as mouse_Controller
import pyscreeze
from pynput.keyboard import Key, Controller as keyboard_Controller
import time
import os
# import pyautogui
# pyautogui.scroll(-100)


def replay_(file_name):
    mouse1 = mouse_Controller()
    keyboard1 = keyboard_Controller()

    def mouse_move_click(mouse_obj, readline, op, button):
        x, y, time_wait = readline.split('(')[-1][:-2].split(',')
        time.sleep(float(time_wait))
        if op == 'pressed':
            mouse_obj.position = (int(x), int(y))
            print('Now we have moved it to {0}'.format(mouse_obj.position))
            mouse_obj.press(button)
        else:
            mouse_obj.position = (int(x), int(y))
            print('Now we have moved it to {0}'.format(mouse_obj.position))
            mouse_obj.release(button)

    def mouse_scroll(mouse_obj, readline):
        x, y, dx, dy, time_wait = readline.split('(')[-1][:-2].split(',')
        time.sleep(float(time_wait))
        mouse_obj.position = (int(x), int(y))
        mouse_obj.scroll(int(dx)*100, int(dy)*100)

    def keyboard_type(keyboard_obj, readline, key_type, op):
        key = readline.split('[')[-1].split(']')[0]
        time_wait = float(readline.split('--')[-1])
        time.sleep(float(time_wait))
        if op == 'pressed':
            if key_type == 'alphanumeric key':
                keyboard_obj.press(key)
                print(key, 'pressed')
            elif key_type == 'special key':
                keyboard_obj.press(eval(key))

        elif op == 'released':
            if key_type == 'alphanumeric key':
                print(key, 'released')
                keyboard_obj.release(key)
            elif key_type == 'special key':
                print(key, 'released')
                keyboard_obj.release(eval(key))

    with open(file_name, 'r') as f:
        data = f.readlines()
    for each in data:
        if 'Left Button Pressed at' in each:
            mouse_move_click(mouse1, each, 'pressed', Button.left)
        elif 'Left Button Released at' in each:
            mouse_move_click(mouse1, each, 'released', Button.left)
        elif 'Right Button Pressed at' in each:
            mouse_move_click(mouse1, each, 'pressed', Button.right)
        elif 'Right Button Released at' in each:
            mouse_move_click(mouse1, each, 'released', Button.right)
        elif 'Middle Button Pressed at' in each:
            mouse_move_click(mouse1, each, 'pressed', Button.middle)
        elif 'Middle Button Released at' in each:
            mouse_move_click(mouse1, each, 'released', Button.middle)
        elif 'scrolled' in each:
            mouse_scroll(mouse1, each)

        elif 'pressed' in each:
            if 'alphanumeric key' in each:
                keyboard_type(keyboard1, each, 'alphanumeric key', 'pressed')
            elif 'special key' in each:
                keyboard_type(keyboard1, each, 'special key', 'pressed')
        elif 'released' in each:
            if 'Key.' in each:
                keyboard_type(keyboard1, each, 'special key', 'released')
            else:
                keyboard_type(keyboard1, each, 'alphanumeric key', 'released')

    # # Type 'Hello World' using the shortcut type method
    # keyboard.type('Hello World')

if __name__ == '__main__':
    newest_file = 'records/' + os.listdir('records')[-1]
    replay_(newest_file)
