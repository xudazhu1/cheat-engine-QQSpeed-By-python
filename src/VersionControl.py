# coding=utf-8
import sys
import time
import tkinter.messagebox

# need to use  requests 2.20
import requests

myVersion = 220611
header = {"Cache-Control": "no-cache"}
proxies = {
  "http": None,
  "https": None,
}

# 帮助网址
vReq2 = requests.get("https://qjrgj.com/ChangeQSpeendHelp.txt", timeout=1, headers=header, verify=False
                     , proxies=proxies)
helpUrl = vReq2.text

# 检测版本
vReq = requests.get("https://qjrgj.com/ChangeQSpeendVersion.txt", timeout=1, headers=header, verify=False
                    , proxies=proxies)
vIntValue = int(vReq.text)
if vIntValue > myVersion:
    print("程序不是最新版本, 即将退出...")
    time.sleep(1)
    tkinter.messagebox.showinfo('版本过旧', '"程序不是最新版本, 即将退出..."')
    sys.exit()
