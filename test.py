# coding=utf-8
from ctypes import *
import Tkinter as tk

import win32api

import TkUtils as MyTK
import win32gui

import win32process
import QSpeedW
import MyTread
import Window


def get_pid_window(hwnd):
    if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
        thread_id, process_id = win32process.GetWindowThreadProcessId(hwnd)
        return process_id
    return False


def no_thing():
    print(sv.get())


# def op(handle, res, ref):
# dll = windll.LoadLibrary('./dll/Change-v2.dll')
# dll.gai(c_int(handle), c_int(res), c_int(ref))
# win32api.FreeLibrary(dll._handle)

# int_arr4 = c_int*400
#
# str = create_string_buffer("asd1122Aa")
# res = dll1.test_array(byref(str))
#
# rst = string_at(res, -1)

def on_closing():
    # if messagebox.askokcancel("Quit", "Do you want to quit?"):
    win32api.FreeLibrary(changeModel._handle)
    root.destroy()


def gai_by_python():
    global handle
    if handle == 0:
        handle = QSpeedW.get_window4speed()[0]
        # 获取填入的原车代码 和目标车代码
        addr = int(sv.get())
        mv = int(sv2.get())
        # 调用
        print("原车ID" + str(addr))
        print("目标ID" + str(mv))



def gai():
    # 获取选取的窗口 获得对应的dll对象和句柄
    # dll_temp = dll
    # handle = QSpeedW.get_window4speed()[0]
    global handle
    if handle == 0:
        handle = QSpeedW.get_window4speed()[0]

    # 获取填入的原车代码 和目标车代码
    addr = int(sv.get())
    mv = int(sv2.get())
    # 调用
    print(addr)
    print(mv)

    ret = changeModel.gai(c_int(handle), c_int(addr), c_int(mv))
    print("result: " + str(ret))
    while ret == 0:
        print("change Fail.. reload...")
        reload_lib()
        ret = changeModel.gai(c_int(handle), c_int(addr), c_int(mv))
        print("result: " + str(ret))


def fix():
    changeModel.fix()


def end_kills():
    global threads
    index = 0
    for t in threads:
        if t.is_alive():
            MyTread.stop_thread(t)
        threads.pop(index)
        index = index + 1


def reload_lib():
    global changeModel
    global handle
    # 关闭kill hack.dll的线程
    end_kills()

    dll.fix()
    win32api.FreeLibrary(dll._handle)
    dll = windll.LoadLibrary('./dll/Change-v6.dll')
    # 开启关闭hack.dll的线程
    threads.append(MyTread.thread_it(Window.for_kill_by_name, "HACK.DLL"))

    widnows = QSpeedW.get_window4speed()
    print("window size = > " + str(len(widnows)))
    handle = widnows[0]


def reload_window():
    root.withdraw()
    reload_lib()
    root.update()
    root.deiconify()


threads = []

changeModel = windll.LoadLibrary('./dll/Change-v6.dll')
threads.append(MyTread.thread_it(Window.for_kill_by_name, "HACK.DLL"))

handle = 0
# window = QSpeedW.get_window4speed()[0]
# pid = get_pid_window(window)
# pyinstaller -F   -p ../../src  --uac-admin -r ../../__init__.py,1 ../../test.py


root = MyTK.create_window("卡商城", "560x350")
# 初始化飞车窗口按钮
# addr = 84544
# mv = 98263

L1 = tk.Label(root, text="原车ID")
L1.place(x=1, y=5)

sv = tk.StringVar()
# sv.trace("w", lambda name, index, : no_thing())
E1 = tk.Entry(root, bd=6, width=8, textvariable=sv)
# 默认金焰战神
sv.set(63702)
E1.place(x=50, y=1)

L = tk.Label(root, text="  ==> ")
L.place(x=110, y=5)

L12 = tk.Label(root, text="目标车ID")
L12.place(x=160, y=5)

sv2 = tk.StringVar()
# sv2.trace("w", lambda name, index, : no_thing())
E12 = tk.Entry(root, bd=6, width=8, textvariable=sv2)
# 默认黄金爆天甲
sv2.set(106674)
E12.place(x=230, y=1)

tk.Button(root, command=lambda: gai(), text='     改TA!   ').place(x=320, y=1)
tk.Button(root, command=lambda: fix(), text='  还原车辆代码  ').place(x=430, y=1)

tk.Button(root, command=lambda: reload_window(), text=' 重新读取飞车窗口 ').place(x=1, y=320)

# tk.Button(root, command=lambda: init_window(), text='  重新初始化  ').place(x=320, y=1)
MyTK.text(root, "tips: 点击按钮自动填入目标ID ", 270, 270)
MyTK.text(root, "tips: 改完进退商城见效 最好不要用雷诺卡 ", 270, 300)
MyTK.text(root, "还原代码/重新读取窗口 都可能使改过车的飞车窗口崩溃", 270, 320)


def checked(value):
    sv2.set(value)


# 常用代碼

tk.Label(root, text="常用代碼S").place(x=1, y=35)

tk.Button(root, command=lambda: checked(106674), text='至尊丶爆天甲').place(x=1, y=60)
tk.Button(root, command=lambda: checked(98830), text='爆天雷诺').place(x=101, y=60)
tk.Button(root, command=lambda: checked(88865), text='终极爆天甲').place(x=181, y=60)
tk.Button(root, command=lambda: checked(74362), text='爆天甲').place(x=261, y=60)
tk.Button(root, command=lambda: checked(101885), text='终极黑域电魔').place(x=331, y=60)
tk.Button(root, command=lambda: checked(91957), text='终极银天使').place(x=431, y=60)

tk.Button(root, command=lambda: checked(89936), text='终极烈焰新星').place(x=1, y=90)
tk.Button(root, command=lambda: checked(77236), text='终极猛兽').place(x=101, y=90)
tk.Button(root, command=lambda: checked(75808), text='终极针尖王者').place(x=181, y=90)
tk.Button(root, command=lambda: checked(74363), text='终极鬼战刀').place(x=271, y=90)
tk.Button(root, command=lambda: checked(68643), text='终极暴风雪').place(x=351, y=90)
tk.Button(root, command=lambda: checked(83042), text='终极变形销魂').place(x=431, y=90)

tk.Label(root, text="常用代碼T3").place(x=1, y=125)

tk.Button(root, command=lambda: checked(78292), text='创世之神').place(x=1, y=155)
tk.Button(root, command=lambda: checked(71452), text='神谕天尊').place(x=101, y=155)
tk.Button(root, command=lambda: checked(102219), text='圣殿剑魂').place(x=181, y=155)
tk.Button(root, command=lambda: checked(63429), text='终极幻影').place(x=261, y=155)
tk.Button(root, command=lambda: checked(94838), text='上古魔尊').place(x=351, y=155)
tk.Button(root, command=lambda: checked(85942), text='圣域大天使').place(x=431, y=155)

tk.Label(root, text="常用代碼").place(x=1, y=190)

tk.Button(root, command=lambda: checked(106673), text='爱神维纳斯').place(x=1, y=220)
# tk.Button(root, command=lambda: checked(106675), text='终极众神之神').place(x=101, y=220)
tk.Button(root, command=lambda: checked(106676), text='炫金盘龙').place(x=191, y=220)
tk.Button(root, command=lambda: checked(90945), text='众神之神').place(x=261, y=220)
tk.Button(root, command=lambda: checked(96785), text='光明之神').place(x=351, y=220)
tk.Button(root, command=lambda: checked(86998), text='疾影M18').place(x=431, y=220)

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
