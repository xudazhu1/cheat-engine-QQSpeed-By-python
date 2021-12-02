import os

import requests

import MyTread


def downCar(code):
    try:
        url = 'http://iips.speed.qq.com/images/' + str(code) + '.png'
        r = requests.get(url)

        dirs = "D:\\hack\\cars\\" + str(int(code/2000))
        if not os.path.exists(dirs):
            print('初始化创建文件夹')
            os.mkdir(dirs)

        with open(dirs + "\\" + str(code) + ".png", "wb") as code:
            code.write(r.content)
        print("下载物品 ==> " + str(code))
    except:
        print("下载物品错误" + str(code))


def threadDown(start, end):
    global endG
    if end > endG:
        end = endG
    while start <= end:
        downCar(start)
        start += 1


threads = []
startG = 118550
endG = 121650
step = 300
index = startG
while index < endG:
    threads.append(MyTread.threadByFuture(threadDown,
                                          index, index + step))
    index += step

for t in threads:
    t.result()
