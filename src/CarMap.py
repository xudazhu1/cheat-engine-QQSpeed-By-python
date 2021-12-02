# coding=utf-8
import json
import os
import sys


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
    12720: "[A]雷诺",
    11869: "海盗",
    26670: "冰块",
    10076: "幻影",
    14706: "锦鲤",
    21268: "幻火",
    15225: "飞碟丶",
    15434: "联想",
    14099: "海鸥",
    13309: "甲壳虫",
    19296: "财付通",
    13317: "筋斗云",
    10070: "挑战者",
    10181: "[C]渡鸦",
    10182: "[C]虹",
    10205: "[C]反物质",
    10228: "[C]樱",
    10229: "[C]刺客",
    10230: "[C]金刚",
    10250: "[C]岩石",
    10251: "[C]蔷薇",
    10319: "[C]黑风暴",
    10320: "[C]矩阵",
    10321: "[C]猎豹",
    10424: "[C]女武神",
    10476: "[C]福",
    10534: "[C]爱神之心",
    10535: "[C]爱神之吻",
    10589: "[C]烈焰",
    10630: "[C]狂徒",
    10631: "[C]白鲨",
    10649: "[C]解放",
    10698: "[C]旋涡",
    10986: "[C]火石",
    10987: "[C]天龙",
    10988: "[C]紫罗兰",
    10989: "[C]雄鹰",
    10990: "[C]火花",
    10991: "[C]熊猫",
    11143: "[C]白星",
    11144: "[C]蓝焰",
    11145: "[C]龙舟",
    11146: "[C]拦路虎",
    11178: "[C]积木",
    11235: "[C]噪音",
    11236: "[C]抓地虎",
    11239: "[C]格兰",
    11372: "[C]冰峰",
    11373: "[C]奶牛",
    11374: "[C]雷神",
    11375: "[C]小哈",
    11870: "[C]坦克",
    11871: "[C]羚羊",
    11959: "[C]大熊",
    12035: "[C]哈雷",
    12042: "[C]迷你电动车",
    12260: "[C]超兔",
    12296: "[C]悟空",
    12460: "[C]救护车",
    12461: "[C]火狐",
    12828: "[C]南瓜车",
    12829: "[C]消防车",
    13311: "[C]珍珠",
    13322: "[C]雪橇车",
    14490: "[C]旋风",
    14958: "[C]婴儿车",
    15431: "[C]冰箭",
    15433: "[C]烈火",
    15454: "[C]飞龙战天",
    15983: "[C]绿色美年达",
    15984: "[C]橙色美年达",
    15991: "[C]怒焰",
    15992: "[C]雪暴鬣鹰",
    16570: "[C]云雀",
    17108: "[C]双头鲨",
    17664: "[C]雷达",
    17665: "[C]梅里号",
    17667: "[C]瑞瑟",
    18170: "[C]虎虎生威",
    18176: "[C]驯鹿雪橇",
    18762: "[C]鲸鲨",
    18769: "[C]石中剑",
    19302: "[C]甜心号",
    19622: "[C]小飞侠",
    19957: "[C]尖啸",
    20243: "[C]凯旋",
    20679: "[C]灵鲨",
    21085: "[C]女妖",
    21583: "[C]奔雷",
    21908: "[C]白龙",
    22119: "[C]祥兔",
    22795: "[C]草莓",
    23014: "[C]战蝠",
    23234: "[C]蓝鲸",
    23377: "[C]神农架",
    23462: "[C]黑豹",
    23679: "[C]红豆",
    23990: "[C]布丁",
    24214: "[C]魅族者",
    24215: "[C]瓦尔基里",
    24409: "[C]南瓜精灵",
    24607: "[C]粉红豹",
    24936: "[C]劳伦斯",
    25623: "[C]红色精灵",
    25887: "[C]蓝芽",
    26156: "[C]古玩",
    26584: "[C]冰魔",
    26958: "[C]斯科特",
    27241: "[C]火灵",
    27588: "[C]金锐",
}


# 读取本地
ids = {}
# 读取本地QQ&密码 没有则为空
with open(resource_path('cars1.json'), 'r', encoding='UTF-8') as f:
    carsTemp = json.load(f, encoding="UTF-8")
    f.close()
    # 合并
    for key in carsTemp:
        if not car_map.__contains__(key):
            car_map[int(key)] = carsTemp[key]



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
