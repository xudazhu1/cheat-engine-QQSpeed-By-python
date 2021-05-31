# coding=utf-8
import os
import time
from ctypes import *
import numpy as np
import DriverUtil

import win32api

app_data_path = os.environ.get("APPDATA")
# dll_path = app_data_path[0: app_data_path.index("\\")] + "\\Windows\\System32\\kernel32.dll"
dll_kernel32 = windll.LoadLibrary("kernel32.dll")
results = []

# kill_tp_dll = windll.LoadLibrary("./dll/kill-tp.dll")


# kill_tp_dll.installdriver(1314520)


def install_kill_tp():
    # kill_tp_dll.installdriver(1314520)
    DriverUtil.installDriver()
    time.sleep(.01)


def unLoad_kill_tp():
    # kill_tp_dll.Uninstallthedriver()
    DriverUtil.unloadDriver()
    time.sleep(.01)


class MemoryBasicInformation(Structure):
    _fields_ = [
        # 区域基地址
        ("BaseAddress", c_int),
        # 分配基地址
        ("AllocationBase", c_int),
        # 原始保护
        ("AllocationProtect", c_int),
        # 区域大小
        ("RegionSize", c_int),
        # 状态
        ("State", c_int),
        # 保护
        ("Protect", c_int),
        # 类型
        ("Type", c_int),

    ]


def close_dll():
    # noinspection PyProtectedMember
    win32api.FreeLibrary(dll_kernel32._handle)
    # win32api.FreeLibrary(kill_tp_dll._handle)
    unLoad_kill_tp()

    # kill_tp_dll.Uninstallthedriver()

    # noinspection PyProtectedMember
    # win32api.FreeLibrary(kill_tp_dll._handle)


def close_handle(h):
    dll_kernel32.CloseHandle(h)
    return kill_p(h)


# 获得操作句柄
def open_process(pid):
    return dll_kernel32.OpenProcess(2035711, 0, pid)


# def search_integer_batch(pid, arr_lp_number):
#     res = {}
#     for lp_number in arr_lp_number:
#         rst = kill_tp_dll.search_memory_integer(pid, lp_number)
#         rst = string_at(rst, -1).decode('utf-8')
#         rst = rst[0:len(rst) - 1]
#         res[lp_number] = rst.split(",")
#     return res


def search_integer_batch1(h_process, arr_lp_number, fast_search):
    global results
    results = {}
    for i in arr_lp_number:
        results[i] = []

    # global results

    step = 1
    if fast_search:
        step = 4
    addr_index = 0
    while addr_index <= 2147483647:
        # 搜索
        read_temp = read_memory_integer(h_process, addr_index)

        for i in arr_lp_number:
            if read_temp == i:
                results[i].append(read_temp)
                print(addr_index)

        addr_index += step
    return results


# _查询内存地址信息
def virtual_query_ex(h_process, lp_address, info, dw_length):
    # info = MemoryBasicInformation()
    return dll_kernel32.VirtualQueryEx(h_process, lp_address, byref(info), dw_length)


# 批量内存搜索整数值 pid 进程id arr_lp_number 要搜索的地址值数组
def search_integer_batch(pid, arr_lp_number):
    # 长度 ＝ 取字节集长度 (搜索内容)
    res = {}
    for lp_number in arr_lp_number:
        res[lp_number] = []
    info = MemoryBasicInformation()
    memory_addr = 0
    h_process = open_process(pid)
    while virtual_query_ex(h_process, memory_addr, info, 28) != 0:
        # 16777216 262144
        if info.Type != 16777216 and info.Type != 262144 and info.Type != 16 and info.Type != 1 and info.Type != 128:

            # print "数组大小" + str(info.RegionSize)
            if info.RegionSize >= 2100000000:
                # print "大于"
                break

            my_buffer = np.zeros(info.RegionSize, np.int)  # chunk size; should be even bigger ..

            a = read_memory(h_process, memory_addr, my_buffer.ctypes.data, info.RegionSize, 0)
            if a != 0:
                for lp_number in arr_lp_number:
                    indices, = np.where(my_buffer == lp_number)  # fast bulk search
                    if len(indices):
                        for i in indices:
                            addr_temp = memory_addr + i * 4
                            # print hex(addr_temp)
                            res[lp_number].append(addr_temp)

        # 内存地址 ＝ 内存地址 ＋ 内存块信息.区域大小
        memory_addr = memory_addr + info.RegionSize

    close_handle(h_process)

    return res


# 结束进程
def kill_p(h_process):
    return dll_kernel32.TerminateProcess(h_process, 0)


# 搜索整数
def search_integer(pid, lp_number):
    return search_integer_batch(pid, [lp_number])[lp_number]

    # global results
    # results = []
    # step = 1
    # if fast_search:
    #     step = 4
    # addr_index = 0
    # while addr_index <= 2147483647:
    #     # 搜索
    #     read_temp = read_memory_integer(h_process, addr_index)
    #     if read_temp == lp_number:
    #         results.append(addr_index)
    #     addr_index += step
    # return results


# 读取内存
def read_memory(h_process, addr, pointer_lp_buffer, n_size, lp_number_of_bytes_written):
    return dll_kernel32.ReadProcessMemory(h_process, addr, pointer_lp_buffer, n_size, lp_number_of_bytes_written)


# 读取整数 返回读取的整数
def read_memory_integer(h_process, addr):
    read = pointer(c_int(0))
    read_memory(h_process, addr, read, 4, None)
    return read.__getitem__(0)


# 写入内存 返回写入是否成功
def write_memory(h_process, addr, pointer_lp_buffer, n_size, lp_number_of_bytes_written):
    return dll_kernel32.WriteProcessMemory(h_process, addr, pointer_lp_buffer, n_size, lp_number_of_bytes_written)


# 写入整数
def write_memory_integer(h_process, addr, lp_number):
    write = pointer(c_int(lp_number))
    return write_memory(h_process, addr, write, 4, None)


# 批量写入
def write_memory_batch(h_process, addr_arr, lp_number):
    try:
        res = True
        for addr in addr_arr:
            # print temp
            if write_memory_integer(h_process, addr, lp_number) == 0:
                res = False
        return res
    except ValueError:
        return False

# dll = windll.LoadLibrary('./dll/Change-v6.dll')

# window = QSpeedW.get_window4speed()[0]
# pid = Window.get_pid_window(window)
#
# # 获得操作句柄
# hProcess = dll.OpenProcess(2035711, 0, pid)
# readed = pointer(c_int(0))
# dll.ReadProcessMemory(hProcess, 1465748, readed, 4, None)
#
# print readed.__getitem__(0)
# ret = dll.WriteProcessMemory(hProcess, 1465748, pointer(c_int(10050)), 4, None)
# print ret
# print(app_data_path[0: app_data_path.index("\\")] + "\\Windows\\System32\\kernel32.dll")


# win32api.FreeLibrary(dll._handle)
