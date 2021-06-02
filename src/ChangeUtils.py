# coding=utf-8
import MemoryUtils
import Window


class ChangeCar:
    def __init__(self, hwnd):
        self.scan_1 = []
        self.scan_2 = []
        self.scan_3 = []
        self.original_id = 0
        self.target_id = 0
        self.pid = Window.get_pid_window(hwnd)

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

            self.target_id = target
            # 获得操作句柄
            h_process = MemoryUtils.open_process(self.pid)
            # 搜索10043 和 10051
            # self.scan_1 = MemoryUtils.search_integer(h_process, 10043, True)
            # self.scan_2 = MemoryUtils.search_integer(h_process, 10051, True)
            # self.scan_3 = MemoryUtils.search_integer(h_process, self.original_id, True)
            if len(self.scan_1) <= 1:
                print('sCan 1 ...')
                scan_arr = MemoryUtils.search_integer_batch(self.pid, [10020, 10043, original])
                self.scan_1 = scan_arr[10020]
                if len(self.scan_1) <= 1:
                    # 关闭进程句柄
                    MemoryUtils.close_handle(h_process)
                    # 还原tp
                    MemoryUtils.unLoad_kill_tp()
                    return False
                print(" scan 1 num ==> " + str(len(self.scan_1)))
                # 读板车基址
                # self.scan_1 = BaseModuleAddrUtils.get_moudle_base_addr(self.pid, "Top-Kart.dll", 0x025F1F28,
                #                                                        [0x100, 0x100, 0x554])
                # 整理10020
                self.scan_1 = select_addr(self.scan_1)
                self.original_id = original
                self.scan_3 = scan_arr[self.original_id]
                # for i in self.scan_1:
                #     print hex(int(i.encode("utf-8")))

            if self.original_id != original:
                self.original_id = original
                self.scan_3 = MemoryUtils.search_integer(self.pid, self.original_id)
            if len(self.scan_3) <= 1:
                # 关闭进程句柄
                MemoryUtils.close_handle(h_process)
                # 还原tp
                MemoryUtils.unLoad_kill_tp()
                return False
            print("1 num ==> " + str(len(self.scan_1)))
            print("3 num ==> " + str(len(self.scan_3)))

            # 修改三个结果集为目标代码
            # 写板车基址
            # res_1 = MemoryUtils.write_memory_integer(h_process, self.scan_1, self.target_id)
            res_1 = MemoryUtils.write_memory_batch(h_process, self.scan_1, self.target_id)
            if not res_1:
                print("reChanging scan1 fail ! ")
                # res_1 = MemoryUtils.write_memory_batch(h_process, self.scan_1, self.target_id)
            res_3 = MemoryUtils.write_memory_batch(h_process, self.scan_3, self.target_id)
            if res_1 == 0:
                return False
            if not res_3:
                print("reChanging scan3 fail !")
                return False
                # res_3 = MemoryUtils.write_memory_batch(h_process, self.scan_3, self.target_id)
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
            # 修改三个结果集为目标代码
            res_1 = MemoryUtils.write_memory_batch(h_process, self.scan_1, 10020)
            res_2 = MemoryUtils.write_memory_batch(h_process, self.scan_2, 10043)
            res_3 = MemoryUtils.write_memory_batch(h_process, self.scan_3, self.original_id)

            # 关闭进程句柄
            MemoryUtils.close_handle(h_process)
            return res_1 and res_2 and res_3
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
