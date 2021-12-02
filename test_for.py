import os

# 写
import random
import shutil
import time

r = random.random() * 100000000000000.00 * random.random()
shutil.copy(r'D:\project\my-python32\dist\start.exe', r'D:\project\my-python32\dist\start' + str(r) + r'.exe')
file = open(r'D:\project\my-python32\dist\start' + str(r) + r'.exe', 'ab')
# 2e59b6e508a0ccb05cdb891bba27b129
# d8f3e8f038ccb1e3be3ce14f337e6189

# index = 1
# while index < random.randint(500, 2000):
file.write(bytes(str(r), encoding='utf8'))
file.close()