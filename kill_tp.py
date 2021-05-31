# coding=utf-8
import MemoryUtils
import QSpeedW
import Window
import DriverUtil
import os
from ctypes import *


kill_tp_dll = windll.LoadLibrary("./dll/kill-tp.dll")
kill_tp_dll.Uninstallthedriver()
# MemoryUtils.install_kill_tp()


# MemoryUtils.uninstall_kill_tp()
# DriverUtil.installDriver()
#


path = "D:\project\my-python32\dll\FileDriver.sys"
driverName = "DriverQSpeedByEasy"


print("当前路径", os.getcwd())
DriverUtil.installDriver()

DriverUtil.unloadDriver()
# print(DriverUtil.messages)
for e in DriverUtil.messages:
    print(e)

# print unicode(eval(DriverUtil.messages), "gbk")







