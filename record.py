import time
from PIL import Image, ImageDraw
import os
from pynput import mouse
from pynput.mouse import Button
import pyscreeze
from pynput import keyboard

# time_last_op = time.time()


def record_():
    time_last_op = time.time()
    file_name = 'records/record' + time.strftime("%Y%m%d%H%M%S") + '.txt'
    f = open(file_name, 'a')

    def count_wait_time():
        nonlocal time_last_op
        time_wait = float(time.time() - time_last_op)
        time_last_op = time.time()
        return time_wait

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

    i = 1

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
            f.write('{0} Pressed at ({1},{2},{3})'.format(button_name, x, y, time_wait) + '\n')
            print('{0} Pressed at ({1},{2},{3})'.format(button_name, x, y, time_wait))
        else:
            time_wait = count_wait_time()
            f.write('{0} Released at ({1},{2},{3})'.format(button_name, x, y, time_wait) + '\n')
            print('{0} Released at ({1},{2},{3})'.format(button_name, x, y, time_wait))
        if not pressed:
            # return False
            pass

    def on_scroll(x, y, dx, dy):
        time_wait = count_wait_time()
        f.write('scrolled {0} at {1}'.format('down' if dy < 0 else 'up', (x, y, dx, dy, time_wait)) + '\n')
        print('scrolled {0} at {1}'.format('down' if dy < 0 else 'up', (x, y, dx, dy, time_wait)))

    def on_press(key):
        try:
            key_char = key.char
            time_wait = count_wait_time()
            f.write('alphanumeric key [{0}] pressed --{1}'.format(key_char, time_wait) + '\n')
            print('alphanumeric key [{0}] pressed --{1}'.format(key_char, time_wait))
        except AttributeError:
            time_wait = count_wait_time()
            f.write('special key [{0}] pressed --{1}'.format(key, time_wait) + '\n')
            print('special key [{0}] pressed --{1}'.format(key, time_wait))

    def on_release(key):
        time_wait = count_wait_time()
        if '\'' in str(key):
            key = str(key).replace('\'', '')
        f.write('[{0}] released --{1}'.format(key, time_wait) + '\n')
        print('[{0}] released --{1}'.format(key, time_wait))
        if key == keyboard.Key.esc:
            # Stop listener
            return False

    listener1 = mouse.Listener(no_move=on_move, on_click=on_click, on_scroll=on_scroll, suppress=False)
    # Collect events until released
    listener2 = keyboard.Listener(on_press=on_press, on_release=on_release)
    try:
        listener1.start()
        listener2.start()
        # listener1.join()
        listener2.join()
    finally:
        f.close()
        listener1.stop()
        listener2.stop()

if __name__ == '__main__':
    record_()
