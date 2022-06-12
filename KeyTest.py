import win32gui
from pynput import keyboard
import Window
import QSpeedW

def on_press(key):
    '按下按键时执行。'
    try:
        if key == keyboard.Key.left:
            print("1")
        # if key == keyboard.KeyCode.from_char('enter'):
        #     pass
        # elif key == keyboard.Key.left:
        #     print("1")
        # elif key == keyboard.Key.right:
        #     print("2")
        # elif key == keyboard.Key.up:
        #     print("3")
        # elif key == keyboard.Key.down:
        #     print("3")
        # elif key == keyboard.KeyCode.from_char('q'):
        #     exit(-1)

    except AttributeError:
        print('special key {0} pressed'.format(key))


# 通过属性判断按键类型。

def on_release(key):
    # '松开按键时执行。'
    if '{0}'.format(key) == 'Key.f9':
        if Window.get_resolving() == Window.DEFAULT_SIZE:
            # 调整分辨率至1280x1024
            Window.set_resolving([1280, 1024])
            # F8后F7
            QSpeedW.change2_full_display(QSpeedW.get_window4speed()[0])

        else:
            # Window.default_resolving()
            # 直接F7
            QSpeedW.exit_full_display(QSpeedW.get_window4speed()[0])
    print('{0} released'.format(key))
    # if key == keyboard.Key.esc:
    #     # Stop listener
    #     return False


if __name__ == '__main__':
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()
