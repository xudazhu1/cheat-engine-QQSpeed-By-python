# coding=utf-8
import win32api
import win32con
import win32gui
import psutil
import time
import KeyCodeUtils

import win32process
import os
import win32com.client


def for_kill_by_name(name):
    while False:
        # for proc in psutil.process_iter():
        #     try:

        #         if proc.name() == name:
        #             proc.kill()
        #         # p_info = proc.as_dict(attrs=['pid', 'name'])
        #     except psutil.NoSuchProcess:
        #         pass
        command = 'taskkill /F /IM ' + name
        os.system(command)
        time.sleep(0.1)


def pid_extend(pid):
    for proc in psutil.process_iter():
        try:
            p_info = proc.as_dict(attrs=['pid', 'name'])
            if p_info["pid"] == pid:
                return True
        except psutil.NoSuchProcess:
            pass
    return False


def kill_by_pid(pid):
    for proc in psutil.process_iter():
        try:

            if proc.pid() == pid:
                proc.kill()
            # p_info = proc.as_dict(attrs=['pid', 'name'])
        except psutil.NoSuchProcess:
            pass


# class Window:

# 获取窗口大小 不包括边框
def get_window_size(hWnd):
    left, top, right, bottom = win32gui.GetClientRect(hWnd)
    return [right - left, bottom - top]


# 获取窗口边框偏移
def get_padding_size(window):
    left, top, right, bottom = win32gui.GetClientRect(window)
    left1, top1, right1, bottom1 = win32gui.GetWindowRect(window)
    # 左右边框
    left3 = (right1 - left1 - (right - left)) / 2
    # 上边框 高度差-左右边框
    top3 = bottom1 - (bottom - top) - top1 - left3
    return [left3, top3]


# 根据类名查找窗口
def find_window(class_name):
    h_wnd_list = []
    win32gui.EnumWindows(lambda h_wnd, param: param.append(h_wnd), h_wnd_list)

    find_windows = []
    for hWnd in h_wnd_list:
        # 中文系统默认title是gb2312的编码
        if win32gui.GetClassName(hWnd) == class_name:
            find_windows.append(hWnd)

    return find_windows


def get_pid_window(hwnd):
    if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
        thread_id, process_id = win32process.GetWindowThreadProcessId(hwnd)
        return process_id
    return False


# 唤起窗口 并切换至最前
def wake_w(window_h_wnd):
    win32gui.SendMessage(window_h_wnd, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
    win32gui.SetForegroundWindow(window_h_wnd)


# 获取窗口名字
def get_name4w(window):
    return win32gui.GetWindowText(window)


# 设置窗口大小
def set_window_pos(window, screenWidth, screenHeight):
    # 设置窗口为 1280 x 1024
    win32gui.SetWindowPos(window, win32con.HWND_TOP, 0, 0, screenWidth, screenHeight)


# 窗口相对定位 点击
def mouse_click(hwnd, x, y):
    client_pos = win32api.MAKELONG(x, y)
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, client_pos)
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, client_pos)


# 全局鼠标点击 并且点击后回到之前位置
def mouse_click_g(x, y):
    x1, y1 = win32api.GetCursorPos()
    # 鼠标定位到(x,y)
    win32api.SetCursorPos([x, y])
    # 执行左单键击，若需要双击则延时几毫秒再点击一次即可
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    # 鼠标定位到之前的位置
    win32api.SetCursorPos([x1, y1])


# 根据窗口名查找窗口
def find_window_by_name(window_name):
    h_wnd_list = []
    win32gui.EnumWindows(lambda h_wnd, param: param.append(h_wnd), h_wnd_list)

    find_windows = []
    for hWnd in h_wnd_list:
        # 中文系统默认title是gb2312的编码
        if win32gui.GetWindowText(hWnd) == window_name:
            find_windows.append(hWnd)

    return find_windows


# 隐藏窗口
def hide_window(window):
    win32gui.ShowWindow(window, win32con.SW_HIDE)


# 隐藏窗口
def show_window(window):
    win32gui.ShowWindow(window, win32con.SW_SHOW)  # 设置显示


def get_child_windows(parent, class_name):
    # '''
    # 获得parent的所有子窗口句柄
    #  返回子窗口句柄列表
    #  '''
    if not parent:
        return
    hwnd_child_list = []
    new_list = []
    win32gui.EnumChildWindows(parent, lambda hwnd, param: param.append(hwnd), hwnd_child_list)
    for hwnd in hwnd_child_list:
        # 获取某个句柄的类名和标题
        # title = win32gui.GetWindowText(hwnd)
        class_name_temp = win32gui.GetClassName(hwnd)
        if class_name_temp == class_name:
            new_list.append(hwnd)
    return new_list


def get_child_windows_by_class_and_name(parent, class_name, window_name):
    # '''
    # 获得parent的所有子窗口句柄
    #  返回子窗口句柄列表
    #  '''
    if not parent:
        return
    hwnd_child_list = []
    new_list = []
    win32gui.EnumChildWindows(parent, lambda hwnd, param: param.append(hwnd), hwnd_child_list)
    for hwnd in hwnd_child_list:
        # 获取某个句柄的类名和标题
        title = win32gui.GetWindowText(hwnd)
        class_name_temp = win32gui.GetClassName(hwnd)
        if class_name_temp == class_name and title == window_name:
            new_list.append(hwnd)
    return new_list


def write_str_hwnd(hwnd, string: str):
    for i in string:
        # 唤起窗口 并切换至最前
        win32gui.SendMessage(hwnd, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
        win32gui.SetForegroundWindow(hwnd)

        # win32api.PostMessage(hwnd, win32con.WM_CHAR, ord(i), 0)
        if i in KeyCodeUtils.Up.keys():
            win32api.keybd_event(KeyCodeUtils.low['left_shift'], 0, 0, 0)
            win32api.keybd_event(KeyCodeUtils.Up[i], 0, 0, 0)
            time.sleep(.03)
            win32api.keybd_event(KeyCodeUtils.low['left_shift'], 0, win32con.KEYEVENTF_KEYUP, 0)
            win32api.keybd_event(KeyCodeUtils.Up[i], 0, win32con.KEYEVENTF_KEYUP, 0)
        else:
            win32api.keybd_event(KeyCodeUtils.low[i], 0, 0, 0)
            time.sleep(.03)
            win32api.keybd_event(KeyCodeUtils.low[i], 0, win32con.KEYEVENTF_KEYUP, 0)

        # print('输入: ' + i)
        time.sleep(0.03)


def write_controller_key(hwnd, key_name):
    # 唤起窗口 并切换至最前
    win32gui.SendMessage(hwnd, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
    win32gui.SetForegroundWindow(hwnd)
    win32api.keybd_event(KeyCodeUtils.low[key_name], 0, 0, 0)
    time.sleep(.03)
    win32api.keybd_event(KeyCodeUtils.low[key_name], 0, win32con.KEYEVENTF_KEYUP, 0)


# write_str_hwnd_test('xudaA.z')xudaA.z
# write_str_hwnd(66400, 'waxhh521')


def get_edit(ed_textHwnd):
    # 获取识别结果中输入框文本
    length = win32gui.SendMessage(ed_textHwnd, win32con.WM_GETTEXTLENGTH) + 1
    buf = win32gui.PyMakeBuffer(length)
    # 发送获取文本请求
    win32api.SendMessage(ed_textHwnd, win32con.WM_GETTEXT, length, buf)
    # 下面应该是将内存读取文本
    address, length = win32gui.PyGetBufferAddressAndLen(buf[:-1])
    text = win32gui.PyGetString(address, length)
    print("获取到的值=>" + text)


def getTargetPath4Lnk(lnkPath):
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(lnkPath)
    return shortcut.Targetpath

