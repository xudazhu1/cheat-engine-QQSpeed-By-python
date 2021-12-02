# -*- coding = utf-8 -*-
# @Time : 2020/9/27
# @Author : 小柠檬
# @File : QQ扫码登录QQ群官网.py
# @changed : easy
# @Software:
# import tkinter
from mttkinter import mtTkinter as tkinter
import MyTread

import requests
from PIL import Image, ImageTk
import time
import re
import sys
import JsonUtils

QGid = 716688204


def bkn(Skey):
    t = 5381
    n = 0
    o = len(Skey)
    while n < o:
        t += (t << 5) + ord(Skey[n])
        n += 1
    return t & 2147483647


def ptQrToken(qrsig):
    n = len(qrsig)
    i = 0
    e = 0
    while n > i:
        e += (e << 5) + ord(qrsig[i])
        i += 1
    return 2147483647 & e


tempPath = JsonUtils.local_user_path + '\\QR.png'


# 获取登录QQ二维码 并返回二维码id和二维码图片路径
# noinspection PyUnresolvedReferences
def QR():
    url = 'https://ssl.ptlogin2.qq.com/ptqrshow?appid=715030901&e=2&l=M&s=3&d=72&v=4&t=0.' + str(
        time.time()) + '&daid=73&pt_3rd_aid=0'
    r = requests.get(url)
    qrsig = requests.utils.dict_from_cookiejar(r.cookies).get('qrsig')
    with open(tempPath, 'wb') as f:
        f.write(r.content)

    print('登录二维码获取成功', time.strftime('%Y-%m-%d %H:%M:%S'))
    # im.show()

    return {"qrsig": qrsig, "path": tempPath}


# noinspection PyUnresolvedReferences
def cookies(qrsig, ptqrToken):
    while 1:
        url = 'https://ssl.ptlogin2.qq.com/ptqrlogin?u1=https%3A%2F%2Fqun.qq.com%2Fmanage.html%23click&ptqrtoken=' \
              + str(ptqrToken) + '&ptredirect=1&h=1&t=1&g=1&from_ui=1&ptlang=2052&action=0-0-' \
              + str(time.time()) + '&js_ver=20032614&js_type=1&login_sig=&pt_uistyle=40&aid=715030901&daid=73&'
        cookiesT = {
            'qrsig': qrsig}
        r = requests.get(url, cookies=cookiesT)
        r1 = r.text
        if '二维码未失效' in r1:
            print('群验证: ' + str(time.strftime('%Y-%m-%d %H:%M:%S')))
        elif '二维码认证中' in r1:
            print('群验证: 登录中...')
        elif '二维码已失效' in r1:
            print('Q群验证: 二维码已失效')
        else:
            print('登录成功!')
            cookiesT = requests.utils.dict_from_cookiejar(r.cookies)
            uin = requests.utils.dict_from_cookiejar(r.cookies).get('uin')
            regex = re.compile(r'ptsigx=(.*?)&')
            sigx = re.findall(regex, r.text)[0]
            url = 'https://ptlogin2.qun.qq.com/check_sig?pttype=1&uin=' \
                  + uin + '&service=ptqrlogin&nodirect=0&ptsigx=' \
                  + sigx + '&s_url=https%3A%2F%2Fqun.qq.com%2Fmanage.html&f_url=&ptlang=2052&ptredirect=101' \
                           '&aid=715030901&daid=73&j_later=0&low_login_hour=0®master=0&pt_login_type=3' \
                           '&pt_aid=0&pt_aaid=16&pt_light=0&pt_3rd_aid=0'
            r2 = requests.get(url, cookies=cookiesT, allow_redirects=False)
            targetCookies = requests.utils.dict_from_cookiejar(r2.cookies)
            sKey = requests.utils.dict_from_cookiejar(r2.cookies).get('skey')
            break
        time.sleep(1)
    return targetCookies, sKey


def qun(cookiesV, bknV, num):
    url = 'https://qun.qq.com/cgi-bin/qun_mgr/get_group_list'
    data = {
        'bkn': bknV}
    # cookies = cookies
    r = requests.post(url, data=data, cookies=cookiesV)
    regex = re.compile(r'"gc":(\d+),"gn')
    r = re.findall(regex, r.text)
    if num in r:
        return True
    else:
        return False


def verify(qrsig, root):
    ptQrTokenV = ptQrToken(qrsig)
    cookie = cookies(qrsig, ptQrTokenV)
    sKey = cookie[1]
    bknV = bkn(sKey)
    ck = cookie[0]
    state = qun(ck, bknV, str(getQGid()))
    if state:
        print('恭喜你，验证成功~')
        print('这里执行验证成功后的代码')
        # 窗口置顶
        root.parent.focus_force()
        root.ok()
    else:
        print('很遗憾，验证失败~')
        print('程序即将退出...')
        time.sleep(1)
        sys.exit(0)


def getQGid():
    return str(QGid ^ 70127613)


class PopupDialog(tkinter.Toplevel):
    def __init__(self, parent):
        super().__init__()
        self.title('QQ扫码群验证')
        self.parent = parent  # 显式地保留父窗口
        self.protocol("WM_DELETE_WINDOW", self.cancel)

    def ok(self):
        # 显式地更改父窗口参数
        # self.parent.name = self.name.get()
        # self.parent.age = self.age.get()
        # # 显式地更新父窗口界面
        # self.parent.l1.config(text=self.parent.name)
        # self.parent.l2.config(text=self.parent.age)
        # self.destroy()  # 销毁窗口

        # THE CLUE
        self.parent.wm_attributes("-disabled", False)
        self.destroy()

    def cancel(self):
        self.destroy()
        self.parent.destroy()


def run(parent):
    qrsig = QR()
    child = PopupDialog(parent)
    # THE CLUE
    parent.wm_attributes("-disabled", True)

    im = Image.open(qrsig.get("path"))
    im = im.resize((300, 300))
    img_png = ImageTk.PhotoImage(im)
    tkinter.Label(child, image=img_png).pack()

    # 窗口置顶
    child.wm_attributes('-topmost', 1)
    MyTread.thread_it(verify, qrsig.get("qrsig"), child)

    # root = tkinter.Tk()
    # root.title('QQ扫码群验证')
    # im = Image.open(qrsig.get("path"))
    # im = im.resize((350, 350))
    # img_png = ImageTk.PhotoImage(im)
    # label_img = tkinter.Label(root, image=img_png)
    # label_img.pack()

    parent.wait_window(child)
    return
