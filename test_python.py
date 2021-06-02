# coding=utf-8
import importlib
import tkinter as Tk
import sys

import tkinter.messagebox
import TkUtils as MyTK
import CarMap as carMap
import win32gui

import win32process
import QSpeedW
import MyTread
import MemoryUtils
from ChangeUtils import ChangeCar
import DriverUtil


# 通过窗口句柄获取pid
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
        handle = QSpeedW.get_window4speed()[0]
        changeModel = ChangeCar(handle)

    # 获取填入的原车代码 和目标车代码
    addr = int(sv.get())
    mv = int(sv2.get())
    # 调用
    print(addr)
    print(mv)

    ret = changeModel.change_car(addr, mv)
    print("result: " + str(ret))
    index = 0

    while ret == 0:
        # print("change Fail.. reload...")
        for e in DriverUtil.messages:
            print(e)
        reload_lib()
        ret = changeModel.change_car(addr, mv)
        print("result: " + str(ret))
        index = index + 1
        if index == 2:
            tkinter.messagebox.showinfo('失败! ', '失败!...')
            return
    tkinter.messagebox.showinfo('其实我也不知道会不会失败', '成功,进出商城试试吧')


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

# window = QSpeedW.get_window4speed()[0]
# pid = get_pid_window(window)
# 打包exe脚本 pip install pyinstaller==3.1
# pyinstaller -F -p ../../src --add-data=../../dll/kill-tp.dll;. --uac-admin -r ../../test_python.exe.manifest,1 ../../test_python.py
# pyinstaller -F -p ../../src --add-data=../../dll/kill-tp.dll;. --uac-admin  ../../test_python.py
# pyinstaller -F -p ../../src --add-data=../../dll/FileDriver.sys;. --uac-admin -r ../../test_python.exe.manifest,1 ../../test_python.py

# 过保护
# MyTread.thread_it(MemoryUtils.kill_tp)
root = MyTK.create_window("改车 by easy", "570x350")
# 初始化飞车窗口按钮
# addr = 84544
# mv = 98263

L1 = Tk.Label(root, text="原车ID")
L1.place(x=1, y=5)

sv = Tk.StringVar()
# sv.trace("w", lambda name, index, : no_thing())
E1 = Tk.Entry(root, bd=6, width=8, textvariable=sv)
# 默认金焰战神
sv.set(63702)
E1.place(x=50, y=1)

L = Tk.Label(root, text="  ==> ")
L.place(x=110, y=5)

L12 = Tk.Label(root, text="目标车ID")
L12.place(x=160, y=5)

sv2 = Tk.StringVar()
# sv2.trace("w", lambda name, index, : no_thing())
E12 = Tk.Entry(root, bd=6, width=8, textvariable=sv2)
# 默认黄金爆天甲
sv2.set(106674)
E12.place(x=230, y=1)

Tk.Button(root, command=lambda: gai(), text='     改TA!   ').place(x=320, y=1)
Tk.Button(root, command=lambda: fix(), text='  还原车辆代码  ').place(x=430, y=1)

Tk.Button(root, command=lambda: reload_window(), text=' 重新读取飞车窗口 ').place(x=1, y=320)
# Tk.Button(root, command=lambda: loadDriver(), text=' 安装/删除驱动 ').place(x=150, y=320)

# tk.Button(root, command=lambda: init_window(), text='  重新初始化  ').place(x=320, y=1)
MyTK.text(root, "tips: 点击搜索结果或按钮会把 代码自动填入目标ID ", 270, 260)
MyTK.text(root, "tips: 先进出一次商城再改比较不容易崩溃 ", 270, 280)
MyTK.text(root, "tips: 改完进退商城见效", 270, 300)
MyTK.text(root, "tips: 崩溃是常规操作, 莫慌, 重开游戏再改", 270, 320)


def checked(value):
    sv2.set(value)


def on_keyrelease(event):
    # get text from entry
    value = event.widget.get()
    value = value.strip().lower()

    # get data from test_list
    if value == '':
        data = test_list
    else:
        data = []
        for item in test_list:
            temp = item + '--' + carMap.car_map.get(item)
            if value in temp.lower():
                data.append(item)
    # update data in listbox
    listbox_update(data)


def listbox_update(data):
    # delete previous data
    listbox.delete(0, 'end')

    # sorting data
    data = sorted(data, key=str.lower)

    # put new data
    for item in data:
        listbox.insert('end', item + '--' + carMap.car_map.get(item))


def on_select(event):
    # display element selected on list
    # print('(event) previous:', event.widget.get('active'))
    # print('(event)  current:', event.widget.get(event.widget.curselection()))
    # print('---')
    # 找到value一样的 key 设置进输入框
    selected = event.widget.get(event.widget.curselection())
    checked(selected.split('--')[1])
    # for item in carMap.car_map.keys():
    #     if carMap.car_map.get(item) == selected:
    #         checked(item)
    #         break


# 待选择车辆列表
Tk.Label(root, text="代码搜索").place(x=1, y=35)
test_list = carMap.car_map.keys()

entry = Tk.Entry(root)
entry.place(x=1, y=60)
entry.bind('<KeyRelease>', on_keyrelease)

listbox = Tk.Listbox(root)
listbox.place(x=1, y=80)
# listbox.bind('<Double-Button-1>', on_select)
listbox.bind('<<ListboxSelect>>', on_select)
listbox_update(test_list)

# 创建Scrollbar
y_scrollbar = Tk.Scrollbar(listbox, command=listbox.yview)
y_scrollbar.place(x=125, y=1, height=180)
# y_scrollbar.pack(side=Tk.RIGHT, fill=Tk.Y)
listbox.config(yscrollcommand=y_scrollbar.set)


def get_focus(*args):
    # txt = listbox.focus_get()
    # listbox.event_generate('<Down>')
    listbox.focus_set()


# 鼠标进入事件 使它获取焦点 然后混动条生效
listbox.bind("<Enter>", lambda x: listbox.focus_set())
listbox.bind("<Leave>", lambda x: root.focus_set())

# 常用代碼

Tk.Label(root, text="常用代碼S").place(x=181, y=35)

Tk.Button(root, command=lambda: checked(88865), text='终极爆天甲').place(x=181, y=60)
Tk.Button(root, command=lambda: checked(74362), text='爆天甲').place(x=281, y=60)
Tk.Button(root, command=lambda: checked(101885), text='终极黑域电魔').place(x=381, y=60)
Tk.Button(root, command=lambda: checked(91957), text='终极银天使').place(x=481, y=60)
Tk.Button(root, command=lambda: checked(106675), text='终极众神之神').place(x=181, y=90)
Tk.Button(root, command=lambda: checked(106676), text='至尊丶盘龙').place(x=281, y=90)
Tk.Button(root, command=lambda: checked(106674), text='至尊丶爆天甲').place(x=381, y=90)
Tk.Button(root, command=lambda: checked(98830), text='爆天雷诺').place(x=481, y=90)

Tk.Button(root, command=lambda: checked(78292), text='创世之神').place(x=181, y=120)
Tk.Button(root, command=lambda: checked(71452), text='神谕天尊').place(x=281, y=120)
Tk.Button(root, command=lambda: checked(102219), text='圣殿剑魂').place(x=381, y=120)
Tk.Button(root, command=lambda: checked(110710), text='至尊·冰凤').place(x=481, y=120)
Tk.Button(root, command=lambda: checked(63429), text='终极幻影').place(x=181, y=150)
Tk.Button(root, command=lambda: checked(94838), text='上古魔尊').place(x=281, y=150)
Tk.Button(root, command=lambda: checked(85942), text='圣域大天使').place(x=381, y=150)
Tk.Button(root, command=lambda: checked(110711), text='众神之神-麒麟').place(x=481, y=150)

Tk.Button(root, command=lambda: checked(106673), text='爱神维纳斯').place(x=181, y=180)
Tk.Button(root, command=lambda: checked(106676), text='炫金盘龙').place(x=281, y=180)
Tk.Button(root, command=lambda: checked(90945), text='众神之神').place(x=381, y=180)
Tk.Button(root, command=lambda: checked(110709), text='爆天甲-朋克').place(x=481, y=180)
Tk.Button(root, command=lambda: checked(107370), text='至尊·麦凯伦').place(x=181, y=210)
Tk.Button(root, command=lambda: checked(86998), text='疾影M18').place(x=281, y=210)
Tk.Button(root, command=lambda: checked(112176), text='冥王·哈迪斯').place(x=381, y=210)
Tk.Button(root, command=lambda: checked(112181), text='神圣雅典娜').place(x=481, y=210)

# 为关闭窗口按钮绑定结束程序事件
root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
