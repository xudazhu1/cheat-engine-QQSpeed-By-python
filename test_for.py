# coding=utf-8
import time

import MemoryUtils
import QSpeedW
import Window

print time.time()
res = MemoryUtils.search_integer_batch(Window.get_pid_window(QSpeedW.get_window4speed()[0]), [10020])
print time.time()
print res[10020]

for addr in res[10020]:
    print addr / 0x100000

