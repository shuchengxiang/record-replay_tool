from pynput import mouse
from pynput.mouse import Button, Controller as mouse_Controller
import pyscreeze
from pynput import keyboard
from pynput.keyboard import Key, Controller as keyboard_Controller
import time
import os
# import pyautogui
# pyautogui.scroll(-100)


def replay_(file_name=None):
    stop_replay = False
    replay_result = 'replay_complete'
    if not file_name:
        return
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

    def keyboard_type(keyboard_obj, readline, op):
        key = readline.split('[')[-1].split(']')[0]
        time_wait = float(readline.split('--')[-1])
        time.sleep(float(time_wait))
        if op == 'pressed':
            try:
                keyboard_obj.press(key)
            except ValueError:
                keyboard_obj.press(eval(key))
            print(key, 'pressed')

        elif op == 'released':
            try:
                keyboard_obj.release(key)
            except ValueError:
                keyboard_obj.release(eval(key))
            print(key, 'released')

    with open(file_name, 'r') as f:
        data = f.readlines()

    def on_press(key):
        if key == keyboard.Key.esc:
            print(key)
            nonlocal stop_replay
            stop_replay = True
            # Stop listener
            return False

    # 监听中断replay的键
    with keyboard.Listener(on_press=on_press, on_release=None) as listener1:
        for each in data:
            if 'Left Button Released at' in each:
                mouse_move_click(mouse1, each, 'released', Button.left)
            elif 'Right Button Released at' in each:
                mouse_move_click(mouse1, each, 'released', Button.right)
            elif 'Middle Button Released at' in each:
                mouse_move_click(mouse1, each, 'released', Button.middle)
            elif 'released' in each:
                keyboard_type(keyboard1, each, 'released')
            # 此处最好将中断放在release，防止出现结束还有按键按下的问题导致错乱，
            # 这也是把release代码放在上面判断的原因
            elif stop_replay:
                print('stop_replay')
                replay_result = 'stop_replay'
                break

            elif 'Left Button Pressed at' in each:
                mouse_move_click(mouse1, each, 'pressed', Button.left)
            elif 'Right Button Pressed at' in each:
                mouse_move_click(mouse1, each, 'pressed', Button.right)
            elif 'Middle Button Pressed at' in each:
                mouse_move_click(mouse1, each, 'pressed', Button.middle)

            elif 'scrolled' in each:
                mouse_scroll(mouse1, each)
            elif 'pressed' in each:
                keyboard_type(keyboard1, each, 'pressed')

    return replay_result
    # # Type 'Hello World' using the shortcut type method
    # keyboard.type('Hello World')

if __name__ == '__main__':
    newest_file = 'records/' + os.listdir('records')[-1]
    replay_(newest_file)
