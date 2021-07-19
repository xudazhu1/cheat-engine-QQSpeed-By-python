# coding=utf-8
import numpy

import MemoryUtils
import Window


class ChangeCar:
    def __init__(self, hwnd):
        self.original_id = 0
        self.target_id = 0
        self.pid = Window.get_pid_window(hwnd)
        self.scanCache = {10020: []}

    # 合并搜索结果
    def mergeAddr(self, scanAddrTemp):
        for key, value in scanAddrTemp.items():
            self.scanCache[key] = value

    # 原理搜索10020板车代码 和 original 自己装备的车的代码 直接改成 target目标车的代码
    def change_car(self, original, target):
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
            if len(self.scanCache[10020]) <= 1 or self.original_id != original:
                print('sCan 1 ...')
                scanAddrTemps = []
                # todo 处理 待搜索项 不包含就搜
                if not (self.scanCache.__contains__(original)):
                    scanAddrTemps.append(original)
                if not (self.scanCache.__contains__(10020)) or len(self.scanCache[10020]) <= 1:
                    scanAddrTemps.append(10020)

                scan_arr_temp = MemoryUtils.search_integer_batch(self.pid, scanAddrTemps)
                self.mergeAddr(scan_arr_temp)
                if len(self.scanCache[10020]) <= 1:
                    # 关闭进程句柄
                    MemoryUtils.close_handle(h_process)
                    # 还原tp
                    MemoryUtils.unLoad_kill_tp()
                    return False
                print(" scan 1 num ==> " + str(len(self.scanCache[10020])))
                # 读板车基址
                # self.scanCache[10020] = BaseModuleAddrUtils.get_moudle_base_addr(self.pid, "Top-Kart.dll", 0x025F1F28,
                #                                                        [0x100, 0x100, 0x554])
                # 整理10020
                # 排序10020的搜索结果
                self.scanCache[10020] = numpy.sort(self.scanCache[10020])
                self.scanCache[10020] = select_addr(self.scanCache[10020])
                self.original_id = original
                # self.scanCache[original] = scan_arr[self.original_id]

            # if self.original_id != original:
            #     self.original_id = original
            #     self.scanCache[original] = MemoryUtils.search_integer(self.pid, self.original_id)
            if len(self.scanCache[original]) <= 1:
                # 关闭进程句柄
                MemoryUtils.close_handle(h_process)
                # 还原tp
                MemoryUtils.unLoad_kill_tp()
                return False
            print("1 num ==> " + str(len(self.scanCache[10020])))
            print("3 num ==> " + str(len(self.scanCache[original])))

            # 修改三个结果集为目标代码
            # 写板车基址
            # 这里按照 10020 的目标id改
            res_1 = MemoryUtils.write_memory_batch(h_process, self.scanCache[10020], self.target_id)
            if not res_1:
                print("reChanging scan1 fail ! ")
                # res_1 = MemoryUtils.write_memory_batch(h_process, self.scanCache[10020], self.target_id)
            if original != 10020:
                # 这里按照实际填的地址改
                res_3 = MemoryUtils.write_memory_batch(h_process, self.scanCache[original], target)
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
def select_addr(arr_addr):
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

        while index <= num + 30:
            res.append(arr_addr[index])
            index += 1
    except TypeError:
        return res

    return res
