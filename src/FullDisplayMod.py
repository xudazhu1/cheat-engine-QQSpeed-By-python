import win32gui
import pynput
import Window
import QSpeedW


# 通过属性判断按键类型。

def on_release(key):
    # 松开按键时执行
    try:
        hw = win32gui.GetForegroundWindow()
        if 'GAMEAPP' == win32gui.GetClassName(hw) \
                and '{0}'.format(key) == 'Key.f9':
            if Window.get_resolving() == Window.DEFAULT_SIZE:
                # 调整分辨率至1280x1024
                Window.set_resolving([1280, 1024])
                # F8后F7
                QSpeedW.change2_full_display(hw)
            else:
                # Window.default_resolving()
                # 直接F7
                QSpeedW.exit_full_display(hw)
    except:
        print("except")
    # print('{0} released'.format(key))
    # if key == keyboard.Key.esc:
    #     # Stop listener
    #     return False


def listen_f9():
    with pynput.keyboard.Listener(
            # on_press=on_press,
            on_release=on_release) as listener:
        listener.join()
