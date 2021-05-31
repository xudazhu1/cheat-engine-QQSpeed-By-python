# coding=utf-8
import os
from ctypes import *

import win32api

import Window
import QSpeedW

search_dll = windll.LoadLibrary("./dll/my-search.dll")
# c_char_p("传入").value
pid = Window.get_pid_window(QSpeedW.get_window4speed()[0])

rst = search_dll.search_memory_integer(c_int(pid), c_int(10043))
rst = string_at(rst, -1).decode('utf-8')
rst = rst[0:len(rst) - 1]
print rst.split(",")
win32api.FreeLibrary(search_dll._handle)
