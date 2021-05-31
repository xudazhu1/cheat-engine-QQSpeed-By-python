# coding=utf-8
import win32api
import win32con
import win32gui
import psutil
import time

import win32process
import os


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
