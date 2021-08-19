# coding=utf-8

import DriverUtil
import MemoryUtils
import TkUtils as MyTK

root = MyTK.create_window("CE卡图标 by easy", "290x30")

# 结束进程
def on_closing():
    MemoryUtils.close_dll()
    root.destroy()


# pyinstaller --windowed -F -p ../../.. -p C:\Windows\SysWOW64\downlevel --paths C:\Windows\System32\downlevel --add-data=../../dll/FileDriver.sys;. --uac-admin -r ../../test_python.exe.manifest,1 ../../test_python.py

DriverUtil.installDriver()
for e in DriverUtil.messages:
    print(e)
# 为关闭窗口按钮绑定结束程序事件
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()





