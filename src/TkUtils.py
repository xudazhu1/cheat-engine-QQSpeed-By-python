# coding=utf-8
# python3  使用 tkinter
import tkinter


# 创建一个窗口  指定窗口大小
def create_window(title, size):
    root = tkinter.Tk()
    root.title(title)
    root.geometry(size)
    return root


# 插入文本
def text(root, info, x, y):
    w = tkinter.Label(root, text=info)
    w.place(x=x, y=y)
    w.text = "we"
    return w


# 插入单选框
def check_box(root, info, value, func, x, y):
    c_box = tkinter.Checkbutton(root, text=info, command=lambda: func(value))
    c_box.place(x=x, y=y)
    return c_box
