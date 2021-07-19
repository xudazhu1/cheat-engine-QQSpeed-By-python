# coding=utf-8
import requests


def append2Map(textTemp):
    global car_map
    for item in textTemp.split('\r\n'):
        if len(item) > 5:
            s = item.split("-")
            car_map[int(s[0])] = item[item.index("-") + 1: len(item)]


car_map = {}
# 借用友站的地址 ( ﹁ ﹁ ) ~→
# S
sReq = requests.get("http://39.99.242.216/S%E8%BD%A6.txt")
# A
aReq = requests.get("http://39.99.242.216/A%E8%BD%A6.txt")
# B
bReq = requests.get("http://39.99.242.216/B%E8%BD%A6.txt")
# T
tReq = requests.get("http://39.99.242.216/T%E8%BD%A6.txt")

sReq.encoding = "GBK"
aReq.encoding = "GBK"
bReq.encoding = "GBK"
tReq.encoding = "GBK"
append2Map(sReq.text)
append2Map(aReq.text)
append2Map(bReq.text)
append2Map(tReq.text)
