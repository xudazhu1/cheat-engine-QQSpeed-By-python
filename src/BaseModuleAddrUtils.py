# -*- coding:utf-8 -*-
"""
@author:
@file: GetBaseAddr.py
@time: 2020-05-13 21:07
@desc: KeyboArd
@Version: Python2.7
"""
import QSpeedW
import Window
import win32process
import win32api  # 调用系统模块
import ctypes  # C语言类型
from win32gui import FindWindow  # 界面
from ctypes import *

nt_dll = ctypes.WinDLL("ntdll.dll")
kernel32 = ctypes.windll.LoadLibrary("kernel32.dll")
GetLastError = kernel32.GetLastError

TH32CS_SNAPPROCESS = 0x00000002
dwOwnObj = 0xD2FB94
dwEntityList = 0x4D43AC4
dwGlowObjectManager = 0x528B8B0
m_iGlowIndex = 0xA428
m_iTeamNum = 0xF4
m_Hp = 0x100
TH32CS_SNAPMODULE = 0x00000008
STANDARD_RIGHTS_REQUIRED = 0x000F0000
SYNCHRONIZE = 0x00100000
PROCESS_ALL_ACCESS = (STANDARD_RIGHTS_REQUIRED | SYNCHRONIZE | 0xFFF)


class ProcessBasicInformation(ctypes.Structure):
    _fields_ = [('ExitStatus', ctypes.c_ulonglong),  # 接收进程终止状态
                ('PebBaseAddress', ctypes.c_ulonglong),  # 接收进程环境块地址
                ('AffinityMask', ctypes.c_ulonglong),  # 接收进程关联掩码
                ('BasePriority', ctypes.c_ulonglong),  # 接收进程的优先级类
                ('UniqueProcessId', ctypes.c_ulonglong),  # 接收进程ID
                ('InheritedFromUniqueProcessId', ctypes.c_ulonglong)]  # 接收父进程ID


class MODULEENTRY32(Structure):
    _fields_ = [('dwSize', c_long),
                ('th32ModuleID', c_long),
                ('th32ProcessID', c_long),
                ('GlblcntUsage', c_long),
                ('ProccntUsage', c_long),
                ('modBaseAddr', c_long),
                ('modBaseSize', c_long),
                ('hModule', c_void_p),
                ('szModule', c_char * 256),
                ('szExePath', c_char * 260)]


# CreateToolhelp32Snapshot
CreateToolHelp32Snapshot = windll.kernel32.CreateToolhelp32Snapshot
CreateToolHelp32Snapshot.reltype = c_long
CreateToolHelp32Snapshot.argtypes = [c_int, c_int]
# OpenProcess
OpenProcess = windll.kernel32.OpenProcess
OpenProcess.argtypes = [c_void_p, c_int, c_long]
OpenProcess.rettype = c_long
# GetPriorityClass
GetPriorityClass = windll.kernel32.GetPriorityClass
GetPriorityClass.argtypes = [c_void_p]
GetPriorityClass.rettype = c_long
# CloseHandle
CloseHandle = windll.kernel32.CloseHandle
CloseHandle.argtypes = [c_void_p]
CloseHandle.rettype = c_int
# Module32First
Module32First = windll.kernel32.Module32First
Module32First.argtypes = [c_void_p, POINTER(MODULEENTRY32)]
Module32First.rettype = c_int
# Module32Next
Module32Next = windll.kernel32.Module32Next
Module32Next.argtypes = [c_void_p, POINTER(MODULEENTRY32)]
Module32Next.rettype = c_int
# GetLastError
# GetLastError = windll.kernel32.GetLastError
GetLastError.rettype = c_long


# 读取内存
def read_memory(h_process, addr, pointer_lp_buffer, n_size, lp_number_of_bytes_written):
    return kernel32.ReadProcessMemory(h_process, addr, pointer_lp_buffer, n_size, lp_number_of_bytes_written)


# 读取整数 返回读取的整数
def read_memory_integer(h_process, addr):
    read = pointer(c_int(0))
    read_memory(h_process, addr, read, 4, None)
    return read.__getitem__(0)


def read_virtual_memory64(h_process, addr, n=4):
    # 这里定义一个函数来读取，传入三个参数，第一个是进程句柄，第二个是我们要读取的地址,我们可以默认为8，可以偷懒，第三个是要读取的长度

    addr = ctypes.c_ulonglong(addr)
    ret = ctypes.c_ulonglong()
    buffer_length = ctypes.c_ulonglong(n)

    nt_dll.NtWow64ReadVirtualMemory64(int(h_process), addr, ctypes.byref(ret), buffer_length, 0)
    """    
        这个函数并不是一个公开的API，找了很多文献才研究出来怎么用python去调用它，他一共有五个参数
        第一个参数是我们通过OpenProcess获取的进程句柄，在python中要记得把这个句柄转换成int类型，默认其实是个句柄类型，不
    转换会出错，
        第二个参数其实就是我们要读取的地址，我们辛苦找到的基址和便宜终于有了用武之地
        第三个参数是一个指针，我们通过ctypes中的byref方法可以将一个指针传进去，函数会把读取到的参数放进这个指针指向的地方，
    在这里也就是我们的ret中
        第四个参数是我们需要读取的长度
        第五个参数也是一个指针，存放实际读取的长度，需要的话可以传一个参数，这里我偷懒填的0        
    """

    return ret.value  # c_ulonglong的类型中，他的数值是放在他的属性value中的，所以返回的时候我们只需要获取value中存放的数值就好了


def _get_process_id(className, windowName):
    h_game_window = FindWindow(className, windowName)
    pid = win32process.GetWindowThreadProcessId(h_game_window)[1]
    return pid


def _get_process_handle(pid):
    h_game_handle = win32api.OpenProcess(PROCESS_ALL_ACCESS, 0, pid)
    return h_game_handle


def get_process_image_base(ProcessId, moduleName):
    # p_process_image_base = 0
    # h_module_snap = c_void_p(0)
    me32 = MODULEENTRY32()
    me32.dwSize = sizeof(MODULEENTRY32)
    h_module_snap = CreateToolHelp32Snapshot(TH32CS_SNAPMODULE, ProcessId)

    # ret = Module32First(h_module_snap, pointer(me32))
    Module32First(h_module_snap, pointer(me32))
    # print(ret)
    if GetLastError() != 0:
        CloseHandle(h_module_snap)
        print('Handle Error %s' % GetLastError())
        return 'Error'
    else:
        if Module32First(h_module_snap, pointer(me32)):
            if me32.szModule == moduleName:
                CloseHandle(h_module_snap)
                return me32.modBaseAddr
            else:
                Module32Next(h_module_snap, pointer(me32))
                while int(GetLastError()) != 18:
                    if me32.szModule == moduleName:
                        CloseHandle(h_module_snap)
                        return me32.modBaseAddr
                    else:
                        Module32Next(h_module_snap, pointer(me32))
                CloseHandle(h_module_snap)
                print('Couldn\'t find Process with name %s' % moduleName)
        else:
            print('Module32First is False %s' % GetLastError())
            CloseHandle(h_module_snap)


# 读取模块基址 + 偏移
def get_moudle_base_addr(pid, module_name, module_offset, offset_arr):
    # m = Memory64(pid)  # 我们创建一个内存的操作类
    module_base_addr = get_process_image_base(pid, module_name)
    # print("ModuleBaseAddr", ModuleBaseAddr)
    """
    然后通过调用我们定义的GetBaseAddr的方法来获取模块的基址，这里需要注意，我们要区分大小写
    也可以在修改GetBaseAddr方法，在进行比名称的对比之前，对他们进行强行转码，全部转成大写或者小写，从而忽略大小写的问题  
    获取到模块基址过后，我们就可以通过我们刚刚找到的基址与偏离开始对游戏的数据进行读取了
    """
    _hGameHandle = _get_process_handle(pid)
    # ModuleBaseAddr = 197132288
    addr = read_virtual_memory64(_hGameHandle, module_base_addr + module_offset)  # addr = [jx3representx64 + 0x509E00]
    # print("0x%X" % addr)
    index = 0
    for offset in offset_arr:
        if index == len(offset_arr) - 1:
            return addr + offset
        else:
            addr = read_virtual_memory64(_hGameHandle, addr + offset)
        index += 1
    return 0


def test():
    addr = get_moudle_base_addr(74244, "Top-Kart.dll", 0x025F1F28, [0x100, 0x100, 0x554])
    print("0x%X" % addr)


def code():
    # ProcessId = _GetProcessId("Valve001", u"Counter-********")
    process_id = Window.get_pid_window(QSpeedW.get_window4speed()[0])
    # print(ProcessId)
    _hGameHandle = _get_process_handle(process_id)

    module_name = get_process_image_base(process_id, "Top-Kart.dll")
    print("0x%X" % module_name)

    # ModuleBaseAddr = 197132288
    addr = read_virtual_memory64(_hGameHandle, module_name + 0x025F1F28)  # addr = [jx3representx64 + 0x509E00]
    print("0x%X" % addr)
    addr = read_virtual_memory64(_hGameHandle, addr + 0x100)  # addr = [addr + 0x1AA28 + 0x10]
    print("一级偏移 ==> 0x%X" % addr)
    addr = read_virtual_memory64(_hGameHandle, addr + 0x100)  # addr = [addr + 0x1AA28 + 0x10]
    print("二级偏移 ==> 0x%X" % (addr + 0x554))
    # addr = ReadVirtualMemory64(addr)  # addr = [addr]
    # addr = ReadVirtualMemory64(addr)  # addr = [addr]
    # addr = ReadVirtualMemory64(addr + 0x65D0)  # addr = [addr+0x65D0]
    # addr = addr + 0x32D0 + 0x00000434 + 0x8  # 这个时候我们的addr其实已经是存放x坐标的地址了，我们可以在下面进行测试
    print(addr)
    ret = read_virtual_memory64(_hGameHandle, addr, 4)  # 这里记得只读取四个字节，多了的话读取到的数据肯定就是错误的了
    print("x坐标", ret)
