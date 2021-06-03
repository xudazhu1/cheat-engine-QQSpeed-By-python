# coding=utf-8
import time

import win32api
import win32con
import win32gui

import Window


def get_game_ame(h_wnd):
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


# 调整飞车窗口到 800*600
def change2_800_600(h_wnd):
    # 唤起窗口 并切换至最前
    win32gui.SendMessage(h_wnd, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
    win32gui.SetForegroundWindow(h_wnd)

    target_size = [800, 600]
    while Window.get_window_size(h_wnd) != target_size:
        win32api.PostMessage(h_wnd, win32con.WM_KEYDOWN, win32con.VK_F8, 0)
        time.sleep(0.3)


# 获取飞车窗口集合
def get_window4speed():
    return Window.find_window("GAMEAPP")

