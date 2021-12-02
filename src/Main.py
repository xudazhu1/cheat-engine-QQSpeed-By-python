# coding=utf-8
import importlib
import random
import sys
import tkinter
import tkinter.messagebox

import pyperclip
# noinspection PyPackageRequirements
import win32gui
import win32process

import DriverUtil
import JsonUtils
import MemoryUtils
import MyTread
import QSpeedW
import TkUtils
import UIUtils
import webbrowser

import VersionControl
from ChangeUtils import ChangeCar
import QunVer


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
def on_closing(root):
    # if messagebox.askokcancel("Quit", "Do you want to quit?"):
    MemoryUtils.close_dll()
    root.destroy()


# 改车辆代码
def gai(values):
    # 获取选取的窗口 获得对应的dll对象和句柄
    # dll_temp = dll
    # handle = QSpeedW.get_window4speed()[0]
    # print(changeModelV.get())

    # global changeModel
    # global handle
    if values.handle == 0:
        windowTemp = QSpeedW.get_window4speed()
        if len(windowTemp) == 0:
            tkinter.messagebox.showinfo('提示! ', '没有检测到飞车窗口! ')
            return False
    handleTemp = QSpeedW.get_window4speed()[0]
    if handleTemp != values.handle:
        values.handle = handleTemp
        values.changeModel = ChangeCar(values.handle)
    ret = changeAddr(values)
    print("result: " + str(ret))
    if ret == 0:
        tkinter.messagebox.showinfo('失败! ', '失败!...')
        values.changeModel = ChangeCar(values.handle)
        return
    tkinter.messagebox.showinfo('其实我也不知道会不会失败', '成功,进出商城试试吧')


def changeAddr(values):
    # global changeModel
    # global defaultValues
    # global handle

    values.changeModel.model = values.changeModelV.get()
    # 获取填入的原车代码 和目标车代码
    ret = True
    changeBox2Values = values.changeBox2.getValues()
    changeBox3Values = values.changeBox3.getValues()
    # 把 2的目标id填入1的目标id
    values.changeBox1.targetIdBox.valBox.set(changeBox2Values.get("targetId"))
    # 把改车对象的目标id 改为 10020 的 original_id
    skinValue = 0
    if values.changeModelSkin.get() == 2 and len(changeBox3Values.get("originId")) > 0:
        skinValue = int(changeBox3Values.get("originId").split("--")[0])
    values.changeModel.target_id = int(changeBox2Values.get("targetId").split("--")[0])
    if changeBox2Values.get("originId") and changeBox2Values.get("targetId"):

        if int(changeBox2Values.get("originId").split("--")[0]) == 10020 \
                or int(changeBox2Values.get("originId").split("--")[0]) == 10020:
            tkinter.messagebox.showinfo('不支持的操作', '不支持使用新手赛车改车')
            return False
        # 保存改车数据
        values.defaultValues["changeModelSkin"] = values.changeModelSkin.get()
        mergeObj(changeBox2Values, values.defaultValues)
        values.defaultValues["changeBox3"] = changeBox3Values
        JsonUtils.write_ids(values.defaultValues)
        retTemp = values.changeModel.change_car(int(changeBox2Values.get("originId").split("--")[0]),
                                                int(changeBox2Values.get("targetId").split("--")[0]),
                                                skinValue)
        if not retTemp:
            ret = retTemp
    return ret


def fix(values):
    values.changeModel.fix()
    tkinter.messagebox.showinfo('代码还原', '车辆代码已还原, 进出商城试试吧')


def end_kills(values):
    # global threads
    index = 0
    for t in values.threads:
        if t.is_alive():
            MyTread.stop_thread(t)
        values.threads.pop(index)
        index = index + 1


def reload_lib(values):
    # 关闭kill hack.dll的线程
    end_kills(values)
    try:
        values.changeModel.fix()
    except ValueError:
        print(str(""))
    # win32api.FreeLibrary(dll._handle)
    values.handle = QSpeedW.get_window4speed()[0]
    values.changeModel = ChangeCar(values.handle)
    # 开启关闭hack.dll的线程
    # threads.append(MyTread.thread_it(Window.for_kill_by_name, "HACK.DLL"))


# 合并对象
def mergeObj(originObj, targetObj):
    for key, value in originObj.items():
        # if not targetObj.__contains__(key):
        #     targetObj[key] = None
        targetObj[key] = value


def reload_window(values):
    values.root.withdraw()
    reload_lib(values)
    values.root.update()
    values.root.deiconify()


def loadDriver(values):
    # global loaded
    if values.loaded:
        DriverUtil.unloadDriver()
        values.loaded = False
    else:
        DriverUtil.installDriver()
        values.loaded = True


def changeModelSkinValue(value, values):
    # global changeModelSkin
    # print(value)
    if value == 2:
        values.changeBox3.show()
    else:
        values.changeBox3.hide()
    values.changeModelSkin.set(value)


def openUrl():
    webbrowser.open(VersionControl.helpUrl)


def checked(idTemp, values):
    # copies all the data the user has copied
    pyperclip.copy(idTemp)
    values.changeBox2.targetIdBox.valBox.set(idTemp)


class Start:
    def __init__(self):
        title = ["Cha", "nge", "QS_", "2.11", ".28 ", "by ", "easy"]
        random.shuffle(title)
        self.root = TkUtils.create_window(''.join(title), "590x450")
        # 群验证
        QunVer.run(self.root)
        self.loaded = False
        importlib.reload(sys)
        # sys.setdefaultencoding('utf8')
        self.threads = []
        self.window_temp = QSpeedW.get_window4speed()
        self.handle = 0
        if len(self.window_temp) > 0:
            self.handle = self.window_temp[0]
        # 改车模块对象 传入QQ飞车窗口句柄
        self.changeModel = ChangeCar(self.handle)

        # 初始化飞车窗口按钮
        # 仨修改组件
        TkUtils.text(self.root, "板车: ", 5, 70)
        self.changeBox1 = UIUtils.Instance4ChangeBox(self.root, {"x": 50, "y": 70, "readonly": True})
        self.changeBox1.setValues({"targetId": "", "originId": 10020})
        TkUtils.text(self.root, "原车: ", 5, 110)
        self.changeBox2 = UIUtils.Instance4ChangeBox(self.root, {"x": 50, "y": 110})
        TkUtils.text(self.root, "皮肤: ", 5, 140)
        self.changeBox3 = UIUtils.Instance4ChangeBox(self.root, {"x": 50, "y": 140, "skin": True})

        # 默认值
        self.defaultValues = {"changeBox3": {}, "changeModelSkin": 1}
        mergeObj(JsonUtils.read_ids(), self.defaultValues)
        self.changeBox2.setValues(self.defaultValues)
        self.changeBox3.setValues(self.defaultValues.get("changeBox3"))
        if self.defaultValues.get("changeModelSkin") != 2:
            self.changeBox3.hide()
        # MyTK.text(root, "皮肤: ", 5, 120)
        # changeBox3 = UIUtils.Instance4ChangeBox(root, {"x": 50, "y": 120, "show": False})

        tkinter.Button(self.root, command=lambda: gai(self), text='     改TA!   ').place(x=1, y=1 + 20)
        # Tk.Button(root, command=lambda: fix(), text='  还原车辆代码  ').place(x=80, y=1 + 20)
        self.changeModelV = tkinter.IntVar()
        self.changeModelV.set(1)

        self.changeModelSkin = tkinter.IntVar()
        self.changeModelSkin.set(self.defaultValues.get("changeModelSkin"))
        TkUtils.text(self.root, " 你装备的车俩类型是", 80, y=1 + 20)
        tkinter.Radiobutton(
            self.root, command=lambda: changeModelSkinValue(1, self),
            variable=self.changeModelSkin, text='常规', value=1).place(x=200, y=1 + 20)
        tkinter.Radiobutton(
            self.root, command=lambda: changeModelSkinValue(2, self),
            variable=self.changeModelSkin, text='皮肤', value=2).place(x=260, y=1 + 20)
        # Tk.Radiobutton(root, variable=changeModelV, text='模式3', value=3).place(x=320, y=1 + 20)

        tkinter.Button(self.root, command=lambda: openUrl(), text=' 查看B站视频教程 ').place(x=475, y=1 + 20)
        # Tk.Button(root, command=lambda: reload_window(self), text=' 重新读取飞车窗口 ').place(x=185, y=1 + 20)
        # Tk.Button(root, command=lambda: loadDriver(), text=' 安装/删除驱动 ').place(x=150, y=320)

        TkUtils.text(self.root, "tips: 宝石有没有看运气, 别问了", 10, 360)
        TkUtils.text(self.root, "tips: 改完进退商城见效", 300, 360)
        TkUtils.text(self.root, "tips: 输入框打字可搜索 ", 10, 380)
        TkUtils.text(self.root, "tips: 崩溃是常规操作, 莫慌, 重开游戏再改", 300, 380)
        TkUtils.text(self.root, "tips: 不懂可点右上角查看教程 ", 10, 400)
        TkUtils.text(self.root, "tips: 新版本应该不怎么崩溃了 敬请体验", 300, 400)

        # 常用代码
        tkinter.Label(self.root, text="常用代码").place(x=1, y=180)

        tkinter.Button(self.root, command=lambda: checked(74362, self), text='爆天甲').place(x=181 - 110, y=60 + 121)
        tkinter.Button(self.root, command=lambda: checked(88865, self), text='终极爆天甲').place(x=281 - 110, y=60 + 121)
        tkinter.Button(self.root, command=lambda: checked(98830, self), text='爆天雷诺').place(x=381 - 110, y=60 + 121)
        tkinter.Button(self.root, command=lambda: checked(106674, self), text='至尊·爆天甲').place(x=481 - 110, y=60 + 121)
        tkinter.Button(self.root, command=lambda: checked(115166, self), text='爆天雪').place(x=581 - 110, y=60 + 121)

        tkinter.Button(self.root, command=lambda: checked(106676, self), text='至尊·盘龙').place(x=181 - 110, y=90 + 121)
        tkinter.Button(self.root, command=lambda: checked(106674, self), text='至尊·爆天甲').place(x=281 - 110, y=90 + 121)
        tkinter.Button(self.root, command=lambda: checked(107370, self), text='至尊·麦凯伦').place(x=381 - 110, y=90 + 121)
        tkinter.Button(self.root, command=lambda: checked(109563, self), text='至尊·涅槃').place(x=481 - 110, y=90 + 121)
        tkinter.Button(self.root, command=lambda: checked(110710, self), text='至尊·冰凤').place(x=581 - 110, y=90 + 121)

        tkinter.Button(self.root, command=lambda: checked(78292, self), text='创世之神').place(x=181 - 110, y=120 + 121)
        tkinter.Button(self.root, command=lambda: checked(71452, self), text='神谕天尊').place(x=281 - 110, y=120 + 121)
        tkinter.Button(self.root, command=lambda: checked(102219, self), text='圣殿剑魂').place(x=381 - 110, y=120 + 121)
        tkinter.Button(self.root, command=lambda: checked(85942, self), text='圣域大天使').place(x=481 - 110, y=120 + 121)
        tkinter.Button(self.root, command=lambda: checked(109560, self), text='圣域炽天使').place(x=581 - 110, y=120 + 121)

        tkinter.Button(self.root, command=lambda: checked(63429, self), text='终极幻影').place(x=181 - 110, y=150 + 121)
        tkinter.Button(self.root, command=lambda: checked(94838, self), text='上古魔尊').place(x=281 - 110, y=150 + 121)
        tkinter.Button(self.root, command=lambda: checked(115159, self), text='黑域电魔-张飞').place(x=381 - 110, y=150 + 121)
        tkinter.Button(self.root, command=lambda: checked(113415, self), text='智慧之神-Kitty限定').place(x=481 - 110,
                                                                                                    y=150 + 121)
        tkinter.Button(self.root, command=lambda: checked(113413, self), text='S青龙偃月刀-关羽').place(x=581 - 110,
                                                                                                 y=150 + 121)

        tkinter.Button(self.root, command=lambda: checked(115168, self), text='[帅]奔雷圣卫').place(x=181 - 110, y=180 + 121)
        tkinter.Button(self.root, command=lambda: checked(89936, self), text='终极烈焰新星').place(x=281 - 110, y=180 + 121)
        tkinter.Button(self.root, command=lambda: checked(115160, self), text='[S]至曜-玄武').place(x=381 - 110,
                                                                                                y=180 + 121)
        tkinter.Button(self.root, command=lambda: checked(110709, self), text='爆天甲-朋克').place(x=481 - 110, y=180 + 121)
        tkinter.Button(self.root, command=lambda: checked(110711, self), text='众神之神-麒麟').place(x=581 - 110, y=180 + 121)

        tkinter.Button(self.root, command=lambda: checked(101885, self), text='终极黑域电魔').place(x=181 - 110, y=210 + 121)
        tkinter.Button(self.root, command=lambda: checked(91957, self), text='终极银天使').place(x=281 - 110, y=210 + 121)
        tkinter.Button(self.root, command=lambda: checked(70047, self), text='终极麦凯伦').place(x=381 - 110, y=210 + 121)
        tkinter.Button(self.root, command=lambda: checked(85949, self), text='终极紫电神驹').place(x=481 - 110, y=210 + 121)
        tkinter.Button(self.root, command=lambda: checked(106675, self), text='终极众神之神').place(x=581 - 110, y=210 + 121)

        # 为关闭窗口按钮绑定结束程序事件
        self.root.protocol("WM_DELETE_WINDOW", lambda: on_closing(self.root))
        tkinter.mainloop()


# 打包exe脚本 pip install pyinstaller==3.1(划掉)
'''
pyinstaller -F -p ../../src --add-data=../../dll/kill-tp.dll;. --uac-admin -r ^
../../test_python.exe.manifest,1 ../../test_python.py'''
# pyinstaller -F -p ../../src --add-data=../../dll/kill-tp.dll;. --uac-admin  ../../test_python.py
''' 老命令
pyinstaller -F -w -p ../../src --add-data=../../dll/ChangeQS.sys;. --add-data=../../dll/cars1.json;. ^
--uac-admin -r ../../test_python.exe.manifest,1 ../../test_python.py
'''
# 加密
# python setup.py build_ext --inplace
''' 加密打包
pyinstaller -F -w -p ./build --add-data=./dll/ChangeQS.dll;. --add-data=./dll/cars1.json;. ^
--uac-admin -r ./test_python.exe.manifest,1 ./start.py
'''
''' 加壳打包
pyinstaller -F -w -p ./build --add-data=D:/project/my-python32/dist/start.exe;. ^
--uac-admin -r ./test_python.exe.manifest,1 ./startO.py
'''
