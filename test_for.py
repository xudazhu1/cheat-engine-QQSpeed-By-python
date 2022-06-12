# 写
# import Register
#
# deviceId = Register.register().getCombinNumber()
# print(deviceId)
# print(222)

import win32api
import win32con

#获取当前设定
dm = win32api.EnumDisplaySettings(None, win32con.ENUM_CURRENT_SETTINGS)
# 储存当前宽高
oldWidth = dm.PelsWidth
oldHeight = dm.PelsHeight
# 修改成新的宽高
dm.PelsWidth = 1280
dm.PelsHeight = 1024
# 色深
# dm.BitsPerPel = 32
# dm.DisplayFixedOutput = 0
# 刷新率
# dm.DisplayFrequency = 120
# 设置
win32api.ChangeDisplaySettings(dm, 0)
