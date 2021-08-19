import win32api
dm = win32api.EnumDisplaySettings(None, 0)
dm.PelsHeight = 1536
dm.PelsWidth = 2048
dm.BitsPerPel = 32
dm.DisplayFixedOutput = 1
win32api.ChangeDisplaySettings(dm, 1)
# 适应 分辨率 整个屏幕