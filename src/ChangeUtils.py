# coding=utf-8
from tkinter import messagebox

import numpy

import MemoryUtils
import Window


class ChangeCar:
    def __init__(self, hwnd):
        self.original_id = 0
        self.original_ids = {}
        self.target_id = 0
        self.model = 1
        self.pid = Window.get_pid_window(hwnd)
        self.scanCache = {10020: []}
        self.codes10020 = []
        self.car10020 = []
        self.first = True
        self.reduction = False

    # 合并搜索结果
    def mergeAddr(self, scanAddrTemp):
        for key, value in scanAddrTemp.items():
            if not self.scanCache.__contains__(key):
                self.scanCache[key] = []
            self.scanCache[key] = numpy.unique(numpy.append(self.scanCache[key], value))

    # 原理搜索10020板车代码 和 original 自己装备的车的代码 直接改成 target目标车的代码
    def change_car(self, original, target, skinValue):
        # 窗口找不到 直接False
        if not Window.pid_extend(self.pid):
            print("window out date reChange...")
            return False
        h_process = None
        try:
            # 过tp
            MemoryUtils.install_kill_tp()

            # self.target_id = target
            # 获得操作句柄
            h_process = MemoryUtils.open_process(self.pid)
            # 搜索10020
            if len(self.car10020) < 1:
                print('search 10020 ...')
                scan_arr_temp = MemoryUtils.search_integer_batch(self.pid, [10020])
                # 10020真实地址记录
                if len(self.car10020) < 1:
                    self.car10020 = scan_arr_temp[1]
                if len(self.car10020) < 1:
                    # 关闭进程句柄
                    MemoryUtils.close_handle(h_process)
                    # 还原tp
                    MemoryUtils.unLoad_kill_tp()
                    return False
                # 读板车基址
                # self.scanCache[10020] = BaseModuleAddrUtils.get_moudle_base_addr(self.pid, "Top-Kart.dll", 0x025F1F28,
                #                                                        [0x100, 0x100, 0x554])
                # 整理10020
                # 排序10020的搜索结果
                # self.scanCache[10020] = numpy.sort(self.scanCache[10020])

            # self.codes10020 = self.scanCache[10020]
            # if self.model == 1:
            #     self.codes10020 = select_addr(self.scanCache[10020])
            # elif self.model == 2:
            #     self.codes10020 = select_addr_model2(self.scanCache[10020])
            # else:
            #     self.codes10020 = self.scanCache[10020]
            # 如果目标车id不一样 更新目标车
            if self.original_id != original:
                # 如果原车id换了 算首次
                self.first = True
                scanValues = [original]
                if 0 != skinValue:
                    scanValues.append(skinValue)
                scan_arr_temp = MemoryUtils.search_integer_batch(self.pid, scanValues)
                self.mergeAddr(scan_arr_temp)
                self.original_id = original
            else:
                self.first = False
            # self.scanCache[original] = scan_arr[self.original_id]

            # if self.original_id != original:
            #     self.original_id = original
            #     self.scanCache[original] = MemoryUtils.search_integer(self.pid, self.original_id)
            if not self.scanCache.__contains__(original) or len(self.scanCache[original]) < 1:
                messagebox.showinfo('错误', '原车代码似乎不正确')
                # 关闭进程句柄
                MemoryUtils.close_handle(h_process)
                # 还原tp
                MemoryUtils.unLoad_kill_tp()
                return False
            print("1 num ==> " + str(len(self.car10020)))
            # print("10020 num ==> " + str(len(self.codes10020)))
            print("3 num ==> " + str(len(self.scanCache[original])))

            # 修改三个结果集为目标代码
            # 写板车基址
            # 这里按照 10020 的目标id改

            # 如果能找到精确10020地址
            if len(self.car10020) > 0:
                res_1 = MemoryUtils.write_memory_batch(h_process, self.car10020, self.target_id)
            else:
                print("没找到 10020地址")
                # 关闭进程句柄
                MemoryUtils.close_handle(h_process)
                # 还原tp
                MemoryUtils.unLoad_kill_tp()
                return False
            if not res_1:
                print("reChanging scan1 fail ! ")
                # res_1 = MemoryUtils.write_memory_batch(h_process, self.scanCache[10020], self.target_id)
            if original != 10020:
                # 这里按照实际填的地址改
                # 首次全改  接下来把首次的恢复并且只改精确值
                if self.first:
                    MemoryUtils.write_memory_batch(h_process, self.scanCache[original], target)
                    if skinValue != 0:
                        MemoryUtils.write_memory_batch(h_process, self.scanCache[skinValue], 9988)
                    self.reduction = False
                else:
                    # 把首次改的全部恢复
                    if not self.reduction:
                        MemoryUtils.write_memory_batch(h_process, self.scanCache[original], original)
                        # if skinValue != 0:
                        #     MemoryUtils.write_memory_batch(h_process, self.scanCache[skinValue], skinValue)
                        self.reduction = True
                    # 改特殊值为目标车ID
                res_3 = MemoryUtils.write_memory_batch(h_process, self.scanCache[2], target)

                if not res_3:
                    print("reChanging scan3 fail !")
                    return False
            if res_1 == 0:
                return False

            # 关闭进程句柄
            MemoryUtils.close_handle(h_process)

            # 还原tp
            MemoryUtils.unLoad_kill_tp()

            return True
        except Exception as e:
            print(e)
            return False
        finally:
            # 还原tp
            MemoryUtils.unLoad_kill_tp()
            if h_process is not None:
                # 关闭进程句柄
                MemoryUtils.close_handle(h_process)

    # 还原车辆代码
    def fix(self):
        try:
            # 过tp
            MemoryUtils.install_kill_tp()

            # 获得操作句柄
            h_process = MemoryUtils.open_process(self.pid)
            # 修改缓存里的个结果集为key todo
            result = True
            for key, value in self.scanCache.items():
                res_1 = MemoryUtils.write_memory_batch(h_process, value, key)
                if not res_1:
                    result = res_1
            # 关闭进程句柄
            MemoryUtils.close_handle(h_process)
            return result
        finally:
            # 还原tp
            MemoryUtils.unLoad_kill_tp()


# 为10020搜索出的结果集筛选出合适的地址集 用于改车
def select_addr_model2(arr_addr):
    res = []
    index = 0
    while index < len(arr_addr) / 2 and index < len(arr_addr):
        res.append(arr_addr[index])
        index += 1

    return res


# 为10020搜索出的结果集筛选出合适的地址集 用于改车
def select_addr(arr_addr):
    if len(arr_addr) < 200:
        return arr_addr
    res = []
    try:
        num = 0
        # str_pref = "0"
        str_pref = 0
        index = 0
        for i in arr_addr:
            # str_p = hex(int(int(i.encode("utf-8")))[2:5]
            # print(hex(i)[2:].rjust(8, "0")[0:2])
            str_pref_temp = hex(i)[2:].rjust(8, "0")[0:2]
            # print(str_pref_temp)
            if str_pref_temp == str_pref:
                num += 1

            else:
                # if num > 25:
                # if 7 < num < 12:
                if num > 100:
                    index = index - num - 1
                    break
                num = 0

            str_pref = str_pref_temp
            index += 1

        num = index
        index = 0
        while index < num and index < len(arr_addr):
            res.append(arr_addr[index])
            index += 1
    except TypeError:
        return res

    return select_addr400p(arr_addr) if len(res) == 0 or len(res) == len(arr_addr) else res


# 为10020搜索出的结果集筛选出合适的地址集 用于改车
def select_addr400p(arr_addr):
    res = []
    try:
        num = 0
        # str_pref = "0"
        str_pref = 0
        index = 0
        for i in arr_addr:
            # str_pref_temp = hex(int(i.encode("utf-8")))[2:5]
            str_pref_temp = int(i / 0x100000)
            # print(str_pref_temp)
            if str_pref_temp == str_pref:
                num += 1

            else:
                # if num > 25:
                if 7 < num < 12:
                    index = index - num - 1
                    break
                num = 0

            str_pref = str_pref_temp
            index += 1

        num = index + num

        while index <= num + 30 and index < len(arr_addr):
            res.append(arr_addr[index])
            index += 1
    except TypeError:
        return res

    return res
