# coding=utf-8
import time
from ctypes import windll

import win32api

# import MemoryUtils
# search_dll = windll.LoadLibrary("./my-search.dll")


def kill_tp():


    # 安装过保护驱动
    kill_tp_dll = windll.LoadLibrary("./dll/BugTrace.dll")
    print kill_tp_dll.init_bugtrace()
    print "kill"
    #time.sleep(10)

    # kill_tp_dll.Uninstallthedriver()

    win32api.FreeLibrary(kill_tp_dll._handle)



kill_tp()
