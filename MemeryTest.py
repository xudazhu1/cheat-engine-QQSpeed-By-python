import MemoryUtils
from ctypes import *
import tkinter as Tk
import TkUtils
import DriverUtil


def gai():
    h_process = MemoryUtils.open_process(14972)
    addr = 1304504
    global data
    write = pointer(c_int(data % 2))
    data += 1
    MemoryUtils.write_memory(h_process, addr, write, 4, 0)


data = 2
DriverUtil.installDriver()

root = TkUtils.create_window("改车2.9.2 测试版 by easy", "590x450")
Tk.Button(root, command=lambda: gai(), text='     改TA!   ').place(x=1, y=1 + 20)
print(DriverUtil.messages)
root.mainloop()

