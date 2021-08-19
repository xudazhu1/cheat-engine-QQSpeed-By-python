# coding=utf-8
import sys
import time
import tkinter.messagebox

import requests

myVersion = 383
header = {"Cache-Control": "no-cache"}

# 帮助网址
vReq2 = requests.get("https://qjrgj.com/ChangeQSpeendHelp.txt", timeout=1, headers=header)
helpUrl = vReq2.text

# 检测版本
vReq = requests.get("https://qjrgj.com/ChangeQSpeendVersion.txt", timeout=1, headers=header)
vIntValue = int(vReq.text)
if vIntValue > myVersion:
    print("程序不是最新版本, 即将退出...")
    time.sleep(1)
    tkinter.messagebox.showinfo('版本过旧', '"程序不是最新版本, 即将退出..."')
    sys.exit()
