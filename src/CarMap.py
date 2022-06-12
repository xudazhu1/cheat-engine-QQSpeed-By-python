# coding=utf-8
import json
import os
import sys

import requests
import QunVer


def resource_path(relative_path):
    # 返回资源绝对路径
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller会创建临时文件夹temp
        # 并把路径存储在_MEIPASS中
        # noinspection PyProtectedMember
        base_path = sys._MEIPASS
        # messages.append("base_path", base_path)
    else:
        return "D:\\project\\my-python32\\dll\\" + relative_path
    return os.path.join(base_path, relative_path)


def append2Map(textTemp):
    global car_map
    for item in textTemp.split('\r\n'):
        if len(item) > 5:
            s = item.split("-")
            car_map[int(s[0])] = item[item.index("-") + 1: len(item)]


car_map = {
    115166: "[S]爆天雪",
    110711: "[S][皮肤]众神之神-麒麟",
    63702: "[S]金焰战神",
    10020: "[D]新手赛车",
    12720: "[A]雷诺"
}

# # 读取本地
# ids = {}
# # 读取本地QQ&密码 没有则为空
# with open(resource_path('cars1.json'), 'r', encoding='UTF-8') as f:
#     carsTemp = json.load(f, encoding="UTF-8")
#     f.close()
#     # 合并
#     for key in carsTemp:
#         if not car_map.__contains__(key):
#             car_map[int(key)] = carsTemp[key]


# try:
#     # 借用友站的地址 ( ﹁ ﹁ ) ~→
#     # S
#     sReq = requests.get("http://39.99.242.216/S%E8%BD%A6.txt", timeout=1)
#     # A
#     aReq = requests.get("http://39.99.242.216/A%E8%BD%A6.txt", timeout=1)
#     # B
#     bReq = requests.get("http://39.99.242.216/B%E8%BD%A6.txt", timeout=1)
#     # T
#     tReq = requests.get("http://39.99.242.216/T%E8%BD%A6.txt", timeout=1)
#
#     sReq.encoding = "GBK"
#     aReq.encoding = "GBK"
#     bReq.encoding = "GBK"
#     tReq.encoding = "GBK"
#     append2Map(sReq.text)
#     append2Map(aReq.text)
#     append2Map(bReq.text)
#     append2Map(tReq.text)
#
# except:
#     print("请求友站地址错误, 加载车辆代码异常")

max_10_car_map = [
]


def get_car():
    try:
        # S
        url = QunVer.REGISTER_BASE_URL + '/car'
        r = requests.get(url, proxies=QunVer.PROXIES)
        # r.encoding = "UTF8"
        if r.ok:
            r_data = r.json()
            index = 0
            for car in r_data['result']:
                # print(car)
                car_map[car['id']] = '[' + car['type'] + ']' + car['name']
                # 是否火热
                if index < 10:
                    max_10_car_map.append(car)
                    index = index + 1

        # print(r)
        # sReq = requests.get("http://39.99.242.216/S%E8%BD%A6.txt", timeout=1)
        # # sReq.encoding = "GBK"
        # append2Map(sReq.text)

    except:
        print("请求车辆错误, 加载车辆代码异常")


# 改过某辆车 上传服务器记录下
def click_car(car_id):
    # 上传
    url = QunVer.REGISTER_BASE_URL + '/car/click'
    data = {
        'carId': car_id,
    }
    r = requests.put(url, data=data, proxies=QunVer.PROXIES)
    if r.status_code == 200:
        print("上传成功")
