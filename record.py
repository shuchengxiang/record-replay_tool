import time
from PIL import Image, ImageDraw, ImageGrab
import os
from pynput import mouse
from pynput.mouse import Button
import pyscreeze
from pynput import keyboard

# time_last_op = time.time()


def record_():
    time_last_op = time.time()
    f_list = []
    # screen_shot_area = [0, 0, 0, 0]
    i = 1

    def count_wait_time():
        nonlocal time_last_op
        time_wait = float(time.time() - time_last_op)
        time_last_op = time.time()
        return time_wait

    def capture(x1, y1, x2, y2, path):
        # 参数说明
        # 第一个参数 开始截图的x坐标
        # 第二个参数 开始截图的y坐标
        # 第三个参数 结束截图的x坐标
        # 第四个参数 结束截图的y坐标
        bbox = (x1, y1, x2, y2)
        im = ImageGrab.grab(bbox)

        # 参数 保存截图文件的路径
        im.save(path)
        print('screen_shot succeed', im.size)

    def picture_draw(path, locate):
        oriImg = pyscreeze.screenshot()
        # Img.save(path)
        # oriImg = Image.open(path)
        maskImg = Image.new('RGBA', oriImg.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(maskImg)
        draw.ellipse(locate, fill=(255, 255, 0, 100))

        final = Image.composite(maskImg, oriImg, maskImg)
        final.save(path)

    def on_move(x, y):
        # pass
        print('Pointer moved to {0}'.format((x,y)))

    def on_click(x, y, button, pressed):
        nonlocal i
        button_name = ''
        if button == Button.left:
            button_name = 'Left Button'
        elif button == Button.middle:
            button_name = 'Middle Button'
        elif button == Button.right:
            button_name = 'Right Button'
        else:
            button_name = 'Unknown'
        if pressed:
            # if button == Button.left:
                # button_name = 'Left Button'
                # picture_path = os.path.abspath('.') + '\\picture%s.png' % str(i)
                # picture_draw(picture_path, (int(x) - 25, int(y) - 25, int(x) + 25, int(y) + 25))
                # i += 1
            time_wait = count_wait_time()
            # f.write('{0} Pressed at ({1},{2},{3})'.format(button_name, x, y, time_wait) + '\n')
            f_list.append('{0} Pressed at ({1},{2},{3})'.format(button_name, x, y, time_wait) + '\n')
            print('{0} Pressed at ({1},{2},{3})'.format(button_name, x, y, time_wait))
        else:
            time_wait = count_wait_time()
            f_list.append('{0} Released at ({1},{2},{3})'.format(button_name, x, y, time_wait) + '\n')
            print('{0} Released at ({1},{2},{3})'.format(button_name, x, y, time_wait))

    def on_scroll(x, y, dx, dy):
        time_wait = count_wait_time()
        f_list.append('scrolled {0} at {1}'.format('down' if dy < 0 else 'up', (x, y, dx, dy, time_wait)) + '\n')
        print('scrolled {0} at {1}'.format('down' if dy < 0 else 'up', (x, y, dx, dy, time_wait)))

    def on_press(key):
        if key == keyboard.Key.esc:
            # Stop listener
            return False

        key_char = keycode_convert(str(key))
        time_wait = count_wait_time()
        f_list.append('key [{0}] pressed --{1}'.format(key_char, time_wait) + '\n')
        print('key [{0}] pressed --{1}'.format(key_char, time_wait))

    def on_release(key):
        if key == keyboard.Key.esc:
            # Stop listener
            return False

        key_char = keycode_convert(str(key))
        if key_char == 'pause' or key_char == 'resume':
            pass
        else:
            time_wait = count_wait_time()
            f_list.append('key [{0}] released --{1}'.format(key_char, time_wait) + '\n')
            print('key [{0}] released --{1}'.format(key_char, time_wait))

    def keycode_convert(key_char):
        if '\'' in key_char:
            key_char = str(key_char).replace('\'', '')
        if '\\x01' in key_char:
            key_char = key_char.replace('\\x01', 'a')
        if '\\x13' in key_char:
            key_char = key_char.replace('\\x13', 's')
        if '\\x18' in key_char:
            key_char = key_char.replace('\\x18', 'x')
        if '\\x03' in key_char:
            key_char = key_char.replace('\\x03', 'c')
        if '\\x16' in key_char:
            key_char = key_char.replace('\\x16', 'v')
        return key_char

    with mouse.Listener(no_move=on_move, on_click=on_click, on_scroll=on_scroll, suppress=False) as listener1:
        # Collect events until released
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener2:
            listener2.join()

    return f_list

if __name__ == '__main__':
    record_()
