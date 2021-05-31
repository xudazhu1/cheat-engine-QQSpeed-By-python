# coding=utf-8
from win32gui import FindWindow  # 获取窗口句柄
from win32api import OpenProcess, CloseHandle  # 创建进程句柄与关闭进程句柄
from win32con import PROCESS_VM_READ, PROCESS_VM_WRITE, \
    PROCESS_QUERY_INFORMATION  # win32con里面放的是一些pywin32中的常量,我们导入我们需要的进程权限
from win32process import GetWindowThreadProcessId  # 通过窗口句柄获取进程ID
from ctypes import WinDLL, c_ulonglong, byref, c_wchar_p, c_ulong, Structure

import QSpeedW

"""
WinDLL这个函数是导入系统的动态链接库，因为pywin32中并没有直接可以对内存进行读取和写入操作的函数，对于32位的程序，我们可以用kernel32.dll中的readmemor这些，
但是到了64位程序我们发现没有用了，这也是主要难点，所以需要通过ntdll.dll中的某些未公开的api来达到小青龙们不可告人的秘密
64位地址的长度是8字节，python中调用api时默认的int只有4个字节，所以用ctypes中的c_ulonglong类型来存放我们的数据，避免精度的丢失
byref python本身是没有指针的概念的，所以我们需要通过这个参数来传递指针
c_wchar_p 创建一个wchar类型的指针变量
c_ulong 参考c_ulonglong
Structure 在python中进行结构体的定义的话，需要继承这个类
"""


class PROCESS_BASIC_INFORMATION(Structure):
    """
    这里我们通过python定义一个C中的结构体，这个结构体是用来存放我们在下面的函数中获取的进程相关信息的
    结构体中每个参数中存放的内容见如下备注

    """
    _fields_ = [('ExitStatus', c_ulonglong),  # 接收进程终止状态
                ('PebBaseAddress', c_ulonglong),  # 接收进程环境块地址
                ('AffinityMask', c_ulonglong),  # 接收进程关联掩码
                ('BasePriority', c_ulonglong),  # 接收进程的优先级类
                ('UniqueProcessId', c_ulonglong),  # 接收进程ID
                ('InheritedFromUniqueProcessId', c_ulonglong)]  # 接收父进程ID


class Memory64():
    """定义一个类，方便我们的调用"""

    def __init__(self, pid):  # 这里我们在类创建的时候，接受一个窗口句柄，然后通过窗口句柄让类自己去创建相应的进程
        self.ntdll = WinDLL("ntdll.dll")
        # pid = GetWindowThreadProcessId(hwnd)
        self.hProcess = OpenProcess(PROCESS_VM_READ | PROCESS_QUERY_INFORMATION | PROCESS_VM_WRITE, False, pid[1])
        """ 这个函数有三个参数，第一个参数是你需要的权限，我不是很喜欢这种直接获取全部权限，因为有的时候权限太高并不是好事情
        容易被检测GG，当然这里是单机无所谓可以随便来
            第二个参数是是否继承，一般都是选False,第三个参数是线程的ID，python里一定要记得取第1位的值，也就是第二个值，因为python里
         GetWindowThreadProcessId这个函数返回的值有两个"""

    def CloseHandle(self):  # 一定要记得释放资源
        CloseHandle(self.hProcess)  # 因为这里还要调用原始的hProcess类型去关闭进程句柄，所以我们没有一开始对self.hProcess直接转换成int

    def __del__(self):  # 这里在类被清除时，尝试释放资源，防止忘记释放资源而引起不必要的占用
        try:
            self.CloseHandle(self.hProcess)
        except:
            pass

    def ReadVirtualMemory64(self, addr, n=4):
        # 这里定义一个函数来读取，传入三个参数，第一个是进程句柄，第二个是我们要读取的地址,我们可以默认为8，可以偷懒，第三个是要读取的长度

        addr = c_ulonglong(addr)
        ret = c_ulonglong()
        BufferLength = c_ulonglong(n)

        self.ntdll.NtWow64ReadVirtualMemory64(int(self.hProcess), addr, byref(ret), BufferLength, 0)
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

    def ReadProcessMemory64_Wchar(self, addr, n,
                                  length):  # 这个函数用以读取模块名称，与ReadVirtualMemory64不同的点还有一个是我们会传入一个缓冲区的长度length，用于定义一个c_wchar_p的缓冲区
        addr = c_ulonglong(addr)
        ret = c_wchar_p("0" * length)  # 这里选用wchar其实与编码有关，感兴趣的同学自行百度wchar，宽字符等关键字学习
        BufferLength = c_ulonglong(n)
        self.ntdll.NtWow64ReadVirtualMemory64(int(self.hProcess), addr, ret, BufferLength, 0)
        return ret.value

    def WriteVirtualMemory64(self, addr, s, n=8):  # 这个函数与读取的其实是一样的，区别只是一个是读一个写，不作介绍了，参考读取的函数,s参数是我们要写入的数据

        addr = c_ulonglong(addr)
        ret = c_ulonglong(s)
        BufferLength = c_ulonglong(n)
        self.ntdll.NtWow64WriteVirtualMemory64(int(self.hProcess), addr, byref(ret), BufferLength, 0)

    def GetBaseAddr(self, ModuleName):  # 传入需要查找的模块的名称，就可以返回相应的模块基址了
        NumberOfBytesRead = c_ulong()
        Buffer = PROCESS_BASIC_INFORMATION()
        Size = c_ulong(48)
        name_len = len(ModuleName)

        self.ntdll.NtWow64QueryInformationProcess64(int(self.hProcess), 0, byref(Buffer), Size,
                                                    byref(NumberOfBytesRead))
        """
        这同样是一个未公开的api，可以通过他获取进程的信息，然后存入我们一开始定义的结构体中，他的五个参数分别是：
        进程句柄，信息类型，缓冲指针，以字节为单位的缓冲大小， 写入缓冲的字节数
        而至于下面为什么要这么写，其实涉及到了程序的PE结构，这里不做赘述，因为这个东西不是一会会说的清楚的，可以自行百度
        """
        ret = self.ReadVirtualMemory64(Buffer.PebBaseAddress + 24, 8)
        ret = self.ReadVirtualMemory64(ret + 24, 8)

        for i in range(100000):  # 这里用for循环其实是怕程序卡死，下面如果出了问题不能退出的话，循环结束一样可以退出
            modulehandle = self.ReadVirtualMemory64(ret + 48, 8)
            if modulehandle == 0:
                break
            nameaddr = self.ReadVirtualMemory64(ret + 96, 8)
            name = self.ReadProcessMemory64_Wchar(nameaddr, name_len * 2 + 1, name_len)
            if name == ModuleName:
                return modulehandle
            ret = self.ReadVirtualMemory64(ret + 8, 8)


def get_moudle_base_addr(pid, moudle_name, moudle_offset , offset_arr):
    m = Memory64(pid)  # 我们创建一个内存的操作类
    ModuleBaseAddr = m.GetBaseAddr(moudle_name)
    print("ModuleBaseAddr", ModuleBaseAddr)
    """
    然后通过调用我们定义的GetBaseAddr的方法来获取模块的基址，这里需要注意，我们要区分大小写
    也可以在修改GetBaseAddr方法，在进行比名称的对比之前，对他们进行强行转码，全部转成大写或者小写，从而忽略大小写的问题  
    获取到模块基址过后，我们就可以通过我们刚刚找到的基址与偏离开始对游戏的数据进行读取了
    """
    ModuleBaseAddr = 197132288
    addr = m.ReadVirtualMemory64(ModuleBaseAddr + 0x025F1F28)  # addr = [jx3representx64 + 0x509E00]
    print("0x%X" % addr)
    addr = m.ReadVirtualMemory64(addr + 0x100)  # addr = [addr + 0x1AA28 + 0x10]
    print("一级偏移 ==> 0x%X" % addr)
    addr = m.ReadVirtualMemory64(addr + 0x100)  # addr = [addr + 0x1AA28 + 0x10]
    print("二级偏移 ==> 0x%X" % (addr + 0x554))

if __name__ == '__main__':
    hwnd = QSpeedW.get_window4speed()[0]
    m = Memory64(hwnd)  # 我们创建一个内存的操作类

    ModuleBaseAddr = m.GetBaseAddr("Top-Kart.dll")
    print("ModuleBaseAddr", ModuleBaseAddr)
    """
    然后通过调用我们定义的GetBaseAddr的方法来获取模块的基址，这里需要注意，我们要区分大小写
    也可以在修改GetBaseAddr方法，在进行比名称的对比之前，对他们进行强行转码，全部转成大写或者小写，从而忽略大小写的问题  
    获取到模块基址过后，我们就可以通过我们刚刚找到的基址与偏离开始对游戏的数据进行读取了
    """
    ModuleBaseAddr = 197132288
    addr = m.ReadVirtualMemory64(ModuleBaseAddr + 0x025F1F28)  # addr = [jx3representx64 + 0x509E00]
    print("0x%X" % addr)
    addr = m.ReadVirtualMemory64(addr + 0x100)  # addr = [addr + 0x1AA28 + 0x10]
    print("一级偏移 ==> 0x%X" % addr)
    addr = m.ReadVirtualMemory64(addr + 0x100)  # addr = [addr + 0x1AA28 + 0x10]
    print("二级偏移 ==> 0x%X" % (addr+0x554))
    addr = m.ReadVirtualMemory64(addr + 0x554)  # addr = [addr + 0x1AA28 + 0x10]
    addr = addr + 0x32D0 + 0x00000434 + 0x8
    print("三1级偏移 ==> 0x%X" % addr)
    addr = m.ReadVirtualMemory64(addr)  # addr = [addr + 0x1AA28 + 0x10]
    addr = m.ReadVirtualMemory64(addr)  # addr = [addr + 0x1AA28 + 0x10]
    print("三2级偏移 ==> 0x%X" % addr)
    print("三级偏移 ==> 0x%X" % addr)
    # addr = m.ReadVirtualMemory64(addr + 0x1BD4, 4)  # addr = [addr + 0x1AA28 + 0x10]
    # print("四级偏移 ==> 0x%X" % addr)

    ret = m.ReadVirtualMemory64(addr, 4)  # 这里记得只读取四个字节，多了的话读取到的数据肯定就是错误的了
    print "x坐标" +  str(ret)