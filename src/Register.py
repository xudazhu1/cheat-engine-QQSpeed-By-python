import base64

import des as des
import wmi as wmi


class register:
    def __init__(self):
        self.Des_Key = "DESCRYPT"  # Key
        self.Des_IV = "\x15\1\x2a\3\1\x23\2\0"  # 自定IV向量

    # 1. 获取硬件信息,输出 macode
    #   1.CPU序列号（ID） 2.本地连接 无线局域网 以太网的MAC 3.硬盘序列号（唯一） 4.主板序列号（唯一）

    global s
    s = wmi.WMI()

    # cpu 序列号
    def get_CPU_info(self):
        cpu = []
        try:
            cp = s.Win32_Processor()
            # print("cpu_info:", cp)
            for u in cp:
                cpu.append(
                    {
                        "Name": u.Name,
                        "Serial Number": u.ProcessorId,
                        "CoreNum": u.NumberOfCores
                    }
                )
        except Exception as e:
            return [{"Serial Number": ""}]
        return cpu

    # 硬盘序列号
    def get_disk_info(self):
        disk = []
        # print("disk_info:", s.Win32_PhysicalMedia())
        try:
            for pd in s.Win32_DiskDrive():
                disk.append(
                    {
                        "Serial": s.Win32_PhysicalMedia()[0].SerialNumber.lstrip().rstrip(),  # 获取硬盘序列号，调用另外一个win32 API
                        "ID": pd.deviceid,
                        "Caption": pd.Caption,
                        "size": str(int(float(pd.Size) / 1024 / 1024 / 1024)) + "G"
                    }
                )
            # print(":::Disk info:", json.dumps(disk))
        except Exception as e:
            return [{"Serial": ""}]
        return disk

    # mac 地址（包括虚拟机的）
    def get_network_info(self):
        network = []
        for nw in s.Win32_NetworkAdapterConfiguration():  # IPEnabled=0
            if nw.MACAddress != None:
                network.append(
                    {
                        "MAC": nw.MACAddress,  # 无线局域网适配器 WLAN 物理地址
                        "ip": nw.IPAddress
                    }
                )
        # print(":::Network info:", json.dumps(network))
        return network

    # 主板序列号
    def get_mainboard_info(self):
        mainboard = []
        # print("mainboard_info:", s.Win32_BaseBoard())
        try:
            for board_id in s.Win32_BaseBoard():
                mainboard.append(board_id.SerialNumber.strip().strip('.'))
        except Exception as e:
            return [""]
        return mainboard

        #  由于机器码太长，故选取机器码字符串部分字符

    #  E0:DB:55:B5:9C:16BFEBFBFF00040651W3P0VKEL6W8T1Z1.CN762063BN00A8
    #  1 61 k 8Z
    #     machinecode_str = ""
    #     machinecode_str = machinecode_str+a[0]['MAC']+b[0]['Serial Number']+c[0]['Serial']+d[0]
    def getCombinNumber(self):
        # network_info = self.get_network_info()
        cpu_info = self.get_CPU_info()
        disk_info = self.get_disk_info()
        mainboard_info = self.get_mainboard_info()
        # print("network_info:", network_info)
        # print("cpu_info:", cpu_info)
        # print("disk_info:", disk_info)
        # print("mainboard_info:", mainboard_info)
        machinecode_str = cpu_info[0]['Serial Number'] + disk_info[0]['Serial'] + mainboard_info[0]
        # selectindex = [15, 30, 32, 38, 43, 46]
        # macode = ""
        # for i in selectindex:
        #     macode = macode + machinecode_str[i]
        ###   print(macode)
        # return machinecode_str
        return cpu_info[0]['Serial Number']

    ############ 2. 注册登录

    # # DES+base64加密
    # def Encrypted(self, tr):
    #     k = des(self.Des_Key, CBC, self.Des_IV, pad=None, padmode=PAD_PKCS5)
    #     EncryptStr = k.encrypt(tr)
    #     # EncryptStr = binascii.unhexlify(k.encrypt(str))
    #     ###  print('注册码：',base64.b64encode(EncryptStr))
    #     return base64.b64encode(EncryptStr)  # 转base64编码返回
