# coding=utf-8
import os
import time
import tkinter

import win32api
import win32com
import win32con
# noinspection PyPackageRequirements
import win32gui

import Window


def get_game_name(h_wnd):
    window_name = Window.get_name4w(h_wnd)
    try:
        region = window_name[window_name.index('【') + 1: window_name.index('】')]
        window_name = window_name[window_name.index('】') + 1:]
        # 【】
        window_name = window_name[window_name.index('】') + 1:]
        print(window_name)
        return region + ':   ' + window_name[window_name.index('【'): window_name.index('】') + 1]
    except ValueError:
        return window_name


# 返回飞车顶层
def to_top(window):
    print('待续' + str(window))


# 刷许愿树 1次 已打开许愿树的清况


# 调整飞车窗口到屏幕分辨率 也就是全屏无边框 然后F7 全屏
def change2_full_display(h_wnd):
    DEFAULT_DM = win32api.EnumDisplaySettings(None, win32con.ENUM_CURRENT_SETTINGS)
    target_size = [DEFAULT_DM.PelsWidth, DEFAULT_DM.PelsHeight]
    while Window.get_window_size(h_wnd) != target_size:
        win32api.PostMessage(h_wnd, win32con.WM_KEYDOWN, win32con.VK_F8, 0)
        time.sleep(0.18)

    # change2_800_600(h_wnd)

    win32api.PostMessage(h_wnd, win32con.WM_KEYDOWN, win32con.VK_F7, 0)


# F8退出 全屏
def exit_full_display(h_wnd):
    # win32api.PostMessage(h_wnd, win32con.WM_KEYDOWN, win32con.VK_F7, 0)
    # time.sleep(0.13)
    win32api.PostMessage(h_wnd, win32con.WM_KEYDOWN, win32con.VK_F8, 0)
    time.sleep(0.1)
    win32api.PostMessage(h_wnd, win32con.WM_KEYDOWN, win32con.VK_F8, 0)

    # while Window.get_window_size(h_wnd)[0] < 1023 or \
    #         Window.DEFAULT_SIZE[0] == Window.get_window_size(h_wnd)[0]:
    #     win32api.PostMessage(h_wnd, win32con.WM_KEYDOWN, win32con.VK_F8, 0)
    #     time.sleep(0.18)


# 调整飞车窗口到 800*600
def change2_800_600(h_wnd):
    # 唤起窗口 并切换至最前
    win32gui.SendMessage(h_wnd, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
    win32gui.SetForegroundWindow(h_wnd)

    target_size = [800, 600]
    while Window.get_window_size(h_wnd) != target_size:
        win32api.PostMessage(h_wnd, win32con.WM_KEYDOWN, win32con.VK_F8, 0)
        time.sleep(0.18)


# 调整飞车窗口到 800*600
def change2_1280_800(h_wnd):
    # 唤起窗口 并切换至最前
    win32gui.SendMessage(h_wnd, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
    win32gui.SetForegroundWindow(h_wnd)

    target_size = [1280, 800]
    while Window.get_window_size(h_wnd) != target_size:
        win32api.PostMessage(h_wnd, win32con.WM_KEYDOWN, win32con.VK_F8, 0)
        time.sleep(0.18)


# 获取飞车窗口集合
def get_window4speed():
    return Window.find_window("GAMEAPP")


# noinspection PyShadowingNames
def show_speed_window(my_tk):
    h_wnd_list = get_window4speed()
    index = -1

    buttons = []
    for hWnd in h_wnd_list:
        index = index + 1
        # 中文系统默认title是gb2312的编码

        # title = win32gui.GetWindowText(hWnd)
        # title = gbk2utf8(title)
        # clsname = win32gui.GetClassName(hWnd)

        # print ( "窗口句柄:%s " % (hWnd) )
        # print ('编号: ' + str(index) +  '   :%s' % (title) )
        # print ('窗口类名:%s' % (clsname) )
        # print ('')
        temp = index
        button = tkinter.Button(my_tk, command=lambda temp=temp: change_speed(h_wnd_list[temp], my_tk),
                                text=('  窗口 :  %s' % (get_game_name(hWnd))),
                                height=1, relief=tkinter.RAISED)
        button.place(x=index * 200 + 5, y=270)
        buttons.append(button)

    return buttons


def login_window(filename, user_name: str, password: str):
    # print("start '' /d " + os.path.dirname(filename) + " " + filename)
    r_v = os.system('start \"\" /d \"' + os.path.dirname(filename) + "\" \"" + filename + "\"")
    print("启动情况=>" + str(r_v))
    # 循环检查是否产生 类名为 #32770 的登录窗口 确认两遍
    index = 0
    windows = []
    while index <= 1:
        time.sleep(0.05)
        windows = Window.find_window_by_name("QQ飞车")
        if len(windows) == 4 and Window.get_window_size(windows[3])[0] > 799:
            index += 1
    parent = windows[3]
    time.sleep(1.0)
    # 唤起窗口 并切换至最前
    win32gui.SendMessage(parent, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
    # noinspection PyUnresolvedReferences
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys('%')
    win32gui.SetForegroundWindow(parent)

    # 记录现在所有game app窗口
    # windows = get_window4speed()

    edits = Window.get_child_windows(parent, "Edit")
    print(edits)
    time.sleep(0.5)
    # win32gui.SetWindowText(edits[0], '112233')
    # 输入QQ账号
    # win32gui.SendMessage(edits[0], win32con.WM_SETTEXT, None, user_name)

    # keyboard.write(user_name)
    # win32gui.SendMessage(edits[1], win32con.WM_SETTEXT, None, password)
    # 输入密码
    Window.write_str_hwnd(edits[1], password)
    Window.write_str_hwnd(edits[0], user_name)
    time.sleep(0.1)
    Window.write_controller_key(edits[1], "enter")
    # print(user_name + '=>' + password)
    # login_button = Window.get_child_windows_by_class_and_name(parent, 'Button', "登录")
    # Window.mouse_click(login_button[0], 70, 30)


def change_speed(window, root):
    # 判断是否是全屏模式 是的话发送一次F8
    left, top, right, bottom = win32gui.GetWindowRect(window)
    if left == 0 and top == 0 and bottom == root.winfo_screenheight():
        win32api.PostMessage(window, win32con.WM_KEYDOWN, win32con.VK_F8, 0)

    # 唤起窗口 并切换至最前
    win32gui.SendMessage(window, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
    win32gui.SetForegroundWindow(window)

    # 设置窗口为 1280 x 1024
    win32gui.SetWindowPos(window, win32con.HWND_TOP, 5, 5, int((root.winfo_screenheight() - 40 - 5) * 1.25),
                          root.winfo_screenheight() - 40 - 5, win32con.SWP_FRAMECHANGED)

    # 鼠标定位到(30,50)
    # ##win32api.SetCursorPos([6,6])
    # 执行左单键击，若需要双击则延时几毫秒再点击一次即可
    # ##win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)

    mouse_click(window, 1, 1)

    time.sleep(0.5)

    # 拉伸窗口
    win32gui.SetWindowPos(window, win32con.HWND_TOP, 5, 5, root.winfo_screenwidth() - 10,
                          root.winfo_screenheight() - 40 - 5, win32con.SWP_SHOWWINDOW)


def mouse_click(hwnd, x, y):
    x1, y1 = win32api.GetCursorPos()
    # 鼠标定位到(6,6)
    win32api.SetCursorPos([6, 6])
    # 执行左单键击，若需要双击则延时几毫秒再点击一次即可
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    # 鼠标定位到之前的位置
    win32api.SetCursorPos([x1, y1])

    # client_pos = win32api.MAKELONG(x, y)
    # win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, client_pos )
    # win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, client_pos )

    # long_position = win32api.MAKELONG(x, y)
    # win32api.PostMessage(hwnd,win32con.WM_LBUTTONDOWN,win32con.MK_LBUTTON,long_position)
    # win32api.PostMessage(hwnd , win32con.WM_LBUTTONDOWN|win32con.MK_RBUTTON, x , y )


def flush(my_tk, g_buttons):
    for button in g_buttons:
        button.destroy()
    return show_speed_window(my_tk)
