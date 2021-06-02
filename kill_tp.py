# coding=utf-8
import MemoryUtils
import QSpeedW
import Window
import DriverUtil
import ChangeUtils
import os
from ctypes import *
import time


# kill_tp_dll = windll.LoadLibrary("./dll/kill-tp.dll")
# kill_tp_dll.Uninstallthedriver()
# MemoryUtils.install_kill_tp()


# MemoryUtils.uninstall_kill_tp()
# DriverUtil.installDriver()
#


path = "D:\project\my-python32\dll\FileDriver.sys"
driverName = "DriverQSpeedByEasy"


print("当前路径", os.getcwd())
DriverUtil.installDriver()

startTime = time.time()

window_temp = QSpeedW.get_window4speed()
handle = 0
if len(window_temp) > 0:
    handle = window_temp[0]
pid = Window.get_pid_window(handle)
scan_arr = MemoryUtils.search_integer_batch(pid, [10020, 10043, 63702])
print(len(scan_arr[10020]))
print(len(scan_arr[10043]))
print(len(scan_arr[63702]))

print(time.time() - startTime)

DriverUtil.unloadDriver()
# print(DriverUtil.messages)
for e in DriverUtil.messages:
    print(e)

# print unicode(eval(DriverUtil.messages), "gbk")







