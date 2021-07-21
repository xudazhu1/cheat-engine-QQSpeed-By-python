# coding=utf-8
import importlib
import tkinter as Tk
import sys
import pyperclip

import tkinter.messagebox
import TkUtils as MyTK
import win32gui

import win32process
import QSpeedW
import MyTread
import MemoryUtils
import JsonUtils
from ChangeUtils import ChangeCar
import UIUtils
import DriverUtil


# 通过窗口句柄获取pid
def get_pid_window(hwnd):
    if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
        thread_id, process_id = win32process.GetWindowThreadProcessId(hwnd)
        return process_id
    return False


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


# 结束进程
def on_closing():
    # if messagebox.askokcancel("Quit", "Do you want to quit?"):
    MemoryUtils.close_dll()
    root.destroy()


# 改车辆代码
def gai():
    # 获取选取的窗口 获得对应的dll对象和句柄
    # dll_temp = dll
    # handle = QSpeedW.get_window4speed()[0]
    global changeModel
    global handle
    if handle == 0:
        windowTemp = QSpeedW.get_window4speed()
        if len(windowTemp) == 0:
            tkinter.messagebox.showinfo('提示! ', '没有检测到飞车窗口! ')
            return False
        handle = QSpeedW.get_window4speed()[0]
        changeModel = ChangeCar(handle)

    ret = changeAddr()
    print("result: " + str(ret))
    index = 0
    while ret == 0:
        print("change Fail.. reload...")
        for e in DriverUtil.messages:
            print(e)
        reload_lib()
        ret = changeAddr()
        print("result: " + str(ret))
        index = index + 1
        if index == 2:
            tkinter.messagebox.showinfo('失败! ', '失败!...')
            return
    # 保存改车数据
    JsonUtils.write_ids(changeBox2.getValues())
    tkinter.messagebox.showinfo('其实我也不知道会不会失败', '成功,进出商城试试吧')


def changeAddr():
    global changeModel
    global handle
    # 获取填入的原车代码 和目标车代码
    ret = True
    changeBox2Values = changeBox2.getValues()
    # 把 2的目标id填入1的目标id
    changeBox1.targetIdBox.valBox.set(changeBox2Values.get("targetId"))
    # 把改车对象的目标id 改为 10020 的 original_id
    changeModel.target_id = int(changeBox2Values.get("targetId").split("--")[0])
    if changeBox2Values.get("originId") and changeBox2Values.get("targetId"):
        retTemp = changeModel.change_car(int(changeBox2Values.get("originId").split("--")[0]),
                                         int(changeBox2Values.get("targetId").split("--")[0]))
        if not retTemp:
            ret = retTemp
    return ret


def fix():
    changeModel.fix()
    tkinter.messagebox.showinfo('代码还原', '车辆代码已还原, 进出商城试试吧')


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
    try:
        changeModel.fix()
    except ValueError:
        print(str(""))
    # win32api.FreeLibrary(dll._handle)
    handle = QSpeedW.get_window4speed()[0]
    changeModel = ChangeCar(handle)
    # 开启关闭hack.dll的线程
    # threads.append(MyTread.thread_it(Window.for_kill_by_name, "HACK.DLL"))


def reload_window():
    root.withdraw()
    reload_lib()
    root.update()
    root.deiconify()


loaded = False


def loadDriver():
    global loaded
    if loaded:
        DriverUtil.unloadDriver()
        loaded = False
    else:
        DriverUtil.installDriver()
        loaded = True


importlib.reload(sys)
# sys.setdefaultencoding('utf8')
threads = []
window_temp = QSpeedW.get_window4speed()
handle = 0
if len(window_temp) > 0:
    handle = window_temp[0]
# 改车模块对象 传入QQ飞车窗口句柄
changeModel = ChangeCar(handle)
# threads.append(MyTread.thread_it(Window.for_kill_by_name, "HACK.DLL"))

# 打包exe脚本 pip install pyinstaller==3.1(划掉)
# pyinstaller -F -p ../../src --add-data=../../dll/kill-tp.dll;. --uac-admin -r ../../test_python.exe.manifest,1 ../../test_python.py
# pyinstaller -F -p ../../src --add-data=../../dll/kill-tp.dll;. --uac-admin  ../../test_python.py
# pyinstaller -F -p ../../src -p C:\Windows\SysWOW64\downlevel --paths C:\Windows\System32\downlevel --add-data=../../dll/FileDriver.sys;. --uac-admin -r ../../test_python.exe.manifest,1 ../../test_python.py

root = MyTK.create_window("改车2.7 by easy", "590x450")
# 初始化飞车窗口按钮
# 仨修改组件
MyTK.text(root, "板车: ", 5, 70)
changeBox1 = UIUtils.Instance4ChangeBox(root, {"x": 50, "y": 70, "readonly": True})
changeBox1.setValues({"targetId": "", "originId": 10020})
MyTK.text(root, "原车: ", 5, 110)
changeBox2 = UIUtils.Instance4ChangeBox(root, {"x": 50, "y": 110})
# 默认值
defaultValues = JsonUtils.read_ids()
changeBox2.setValues(defaultValues)
# MyTK.text(root, "皮肤: ", 5, 120)
# changeBox3 = UIUtils.Instance4ChangeBox(root, {"x": 50, "y": 120, "show": False})

Tk.Button(root, command=lambda: gai(), text='     改TA!   ').place(x=1, y=1 + 20)
Tk.Button(root, command=lambda: fix(), text='  还原车辆代码  ').place(x=80, y=1 + 20)

Tk.Button(root, command=lambda: reload_window(), text=' 重新读取飞车窗口 ').place(x=185, y=1 + 20)
# Tk.Button(root, command=lambda: loadDriver(), text=' 安装/删除驱动 ').place(x=150, y=320)

MyTK.text(root, "tips: 点击常用代码会复制代码, 请手动粘贴", 10, 360)
MyTK.text(root, "tips: 先进出一次商城再改比较不容易崩溃 ", 10, 380)
MyTK.text(root, "tips: 改完进退商城见效", 300, 360)
MyTK.text(root, "tips: 崩溃是常规操作, 莫慌, 重开游戏再改", 300, 380)


def checked(idTemp):
    # copies all the data the user has copied
    pyperclip.copy(idTemp)
    changeBox2.targetIdBox.valBox.set(idTemp)


# 常用代码
Tk.Label(root, text="常用代码").place(x=1, y=160)

Tk.Button(root, command=lambda: checked(88865), text='终极爆天甲').place(x=181 - 110, y=60 + 121)
Tk.Button(root, command=lambda: checked(74362), text='爆天甲').place(x=281 - 110, y=60 + 121)
Tk.Button(root, command=lambda: checked(101885), text='终极黑域电魔').place(x=381 - 110, y=60 + 121)
Tk.Button(root, command=lambda: checked(91957), text='终极银天使').place(x=481 - 110, y=60 + 121)
Tk.Button(root, command=lambda: checked(106675), text='终极众神之神').place(x=181 - 110, y=90 + 121)
Tk.Button(root, command=lambda: checked(106676), text='至尊丶盘龙').place(x=281 - 110, y=90 + 121)
Tk.Button(root, command=lambda: checked(106674), text='至尊丶爆天甲').place(x=381 - 110, y=90 + 121)
Tk.Button(root, command=lambda: checked(98830), text='爆天雷诺').place(x=481 - 110, y=90 + 121)

Tk.Button(root, command=lambda: checked(78292), text='创世之神').place(x=181 - 110, y=120 + 121)
Tk.Button(root, command=lambda: checked(71452), text='神谕天尊').place(x=281 - 110, y=120 + 121)
Tk.Button(root, command=lambda: checked(102219), text='圣殿剑魂').place(x=381 - 110, y=120 + 121)
Tk.Button(root, command=lambda: checked(110710), text='至尊·冰凤').place(x=481 - 110, y=120 + 121)
Tk.Button(root, command=lambda: checked(63429), text='终极幻影').place(x=181 - 110, y=150 + 121)
Tk.Button(root, command=lambda: checked(94838), text='上古魔尊').place(x=281 - 110, y=150 + 121)
Tk.Button(root, command=lambda: checked(85942), text='圣域大天使').place(x=381 - 110, y=150 + 121)
Tk.Button(root, command=lambda: checked(110711), text='众神之神-麒麟').place(x=481 - 110, y=150 + 121)

Tk.Button(root, command=lambda: checked(106673), text='爱神维纳斯').place(x=181 - 110, y=180 + 121)
Tk.Button(root, command=lambda: checked(106676), text='炫金盘龙').place(x=281 - 110, y=180 + 121)
Tk.Button(root, command=lambda: checked(90945), text='众神之神').place(x=381 - 110, y=180 + 121)
Tk.Button(root, command=lambda: checked(110709), text='爆天甲-朋克').place(x=481 - 110, y=180 + 121)
Tk.Button(root, command=lambda: checked(107370), text='至尊·麦凯伦').place(x=181 - 110, y=210 + 121)
Tk.Button(root, command=lambda: checked(86998), text='疾影M18').place(x=281 - 110, y=210 + 121)
Tk.Button(root, command=lambda: checked(112176), text='冥王·哈迪斯').place(x=381 - 110, y=210 + 121)
Tk.Button(root, command=lambda: checked(112181), text='神圣雅典娜').place(x=481 - 110, y=210 + 121)

# 为关闭窗口按钮绑定结束程序事件
root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
