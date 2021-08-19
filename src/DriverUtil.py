# coding=utf-8

import win32api
import win32service
import os
import sys

from numpy import unicode

ERROR_SERVICE_EXISTS = 1073
ERROR_IO_PENDING = 997
ERROR_SERVICE_ALREADY_RUNNING = 1056
ERROR_SERVICE_NOT_EXISTS = 1060
ERROR_IO_FILE_NOT_EXIST = 123
messages = []
errors = []


def resource_path(relative_path):
    # 返回资源绝对路径
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller会创建临时文件夹temp
        # 并把路径存储在_MEIPASS中
        # noinspection PyProtectedMember
        base_path = sys._MEIPASS
        # messages.append("base_path", base_path)
    else:
        return "D:/project/my-python32/dll/" + relative_path
    return os.path.join(base_path, relative_path)


path = resource_path("Change.sys")
# path = "FileDriver.sys"
# messages.append(path)
# path = "./dll/FileDriver.sys"
driverName = "DriverQSpeedByEasy"


# 需要导入模块: import win32service [as 别名]
# 或者: from win32service import CreateService [as 别名]
def installDriver():
    # 先卸载服务
    unloadDriver()
    # 打开服务控制管理器
    hServiceMgr = OpenSCManager()
    if hServiceMgr is None:
        messages.append("no permission")
        return False

    hs = None
    bRet = False
    # 创建驱动所对应的服务
    try:
        hs = CreateService(hServiceMgr, driverName, path)
        # 判断服务是否失败
        if hs is None:
            dwRtn = win32api.GetLastError()
            if dwRtn != ERROR_IO_PENDING and dwRtn != ERROR_SERVICE_EXISTS:
                # 由于其他原因创建服务失败
                messages.append("CreateService(58) Fail %d ! " + str(dwRtn))

            # 驱动程序已经加载，只需要打开
            hs = OpenService(hServiceMgr, driverName)
            if hs is None:
                # 如果打开服务也失败，则意味错误
                e = win32api.GetLastError()
                messages.append("OpenService(65) Fail %d ! " + str(e.args[0]) + " " + str(e.args[1]))
                return False
        else:
            messages.append("CrateService(68) ok ! ")

        # 开启此项服务
        bRet = StartService(hs)
        messages.append(path)
        if not bRet:
            dwRtn = win32api.GetLastError()
            if dwRtn != ERROR_IO_PENDING and dwRtn != ERROR_SERVICE_ALREADY_RUNNING:
                bRet = False
            else:
                if dwRtn == ERROR_IO_PENDING:
                    # 设备被挂住
                    bRet = False
                else:
                    # 服务已经开启
                    bRet = True

    except Exception as e:
        messages.append(str(e.args[0]) + " " + str(e.args[1]))
        messages.append(unicode(eval(repr(e.args[2])), "gbk"))
    finally:
        if hs:
            win32service.CloseServiceHandle(hs)
        if hServiceMgr:
            win32service.CloseServiceHandle(hServiceMgr)
        return bRet


# 卸载驱动程序
def unloadDriver():
    bRet = False
    # SCM管理器的句柄
    hServiceMgr = None
    # NT驱动程序的服务句柄
    hServiceDDK = None
    try:
        # 打开服务控制管理器
        hServiceMgr = OpenSCManager()
        if hServiceMgr is None:
            messages.append("no permission")
            return False

        # 打开驱动所对应的服务
        hServiceDDK = OpenService(hServiceMgr, driverName)
        if hServiceDDK is None:
            errCode = win32api.GetLastError()
            # 服务不存在 直接返回True
            if errCode == ERROR_SERVICE_NOT_EXISTS:
                return True

        # 停止驱动程序，如果停止失败，只有重新启动才能，再动态加载。
        ControlService(hServiceDDK, win32service.SERVICE_CONTROL_STOP)
        # 动态卸载驱动程序。
        delete = DeleteService(hServiceDDK) is not None
        if not delete:
            # 卸载失败
            bRet = False
        bRet = True
    except Exception as e:
        messages.append(str(e.args[0]) + " " + str(e.args[1]))
        messages.append(unicode(eval(repr(e.args[2])), "gbk"))
    # 离开前关闭打开的句柄
    finally:
        if hServiceDDK:
            win32service.CloseServiceHandle(hServiceDDK)
        if hServiceMgr:
            win32service.CloseServiceHandle(hServiceMgr)
        return bRet


def CreateService(hServiceMgr, driverNameInner, pathInner):
    try:
        hs = win32service.CreateService(hServiceMgr,
                                        driverNameInner,
                                        driverNameInner,
                                        win32service.SERVICE_ALL_ACCESS,  # desired access
                                        win32service.SERVICE_KERNEL_DRIVER,  # service type
                                        win32service.SERVICE_DEMAND_START,
                                        win32service.SERVICE_ERROR_IGNORE,  # error control type
                                        pathInner,
                                        None,
                                        0,
                                        None,
                                        None,
                                        None)
        messages.append("CreateService ok " + str(hs))
        return hs
    except Exception as e:
        if e.args[0] != 1073:
            messages.append(str(e.args[0]) + " " + str(e.args[1]))
            messages.append(unicode(eval(repr(e.args[2])), "gbk"))
    return None


def OpenSCManager():
    try:
        res = win32service.OpenSCManager(None, None, win32service.SC_MANAGER_ALL_ACCESS)
        messages.append("OpenSCManager ok " + str(res))
        return res
    except Exception as e:
        messages.append(str(e.args[0]) + " " + str(e.args[1]))
        messages.append(unicode(eval(repr(e.args[2])), "gbk"))
    return None


def OpenService(hServiceMgr, driverNameInner):
    try:
        res = win32service.OpenService(hServiceMgr, driverNameInner, win32service.SERVICE_ALL_ACCESS)
        messages.append("OpenService ok " + str(res))
        return res
    except Exception as e:
        messages.append(str(e.args[0]) + " " + str(e.args[1]))
        messages.append(unicode(eval(repr(e.args[2])), "gbk"))
    return None


def StartService(hs):
    try:
        res = win32service.StartService(hs, None)
        messages.append("StartService ok " + str(res))
        return True
    except Exception as e:
        messages.append(str(e.args[0]) + " " + str(e.args[1]))
        messages.append(unicode(eval(repr(e.args[2])), "gbk"))
    return None


def ControlService(hs, status):
    try:
        res = win32service.ControlService(hs, status)
        messages.append("ControlService ok " + str(res))
        return res
    except Exception as e:
        if e.args[0] != 1062:
            messages.append(str(e.args[0]) + " " + str(e.args[1]))
            messages.append(unicode(eval(repr(e.args[2])), "gbk"))
    return None


def DeleteService(hs):
    try:
        res = win32service.DeleteService(hs)
        messages.append("DeleteService ok " + str(res))
        return True
    except Exception as e:
        if e.args[0] == 1072:
            return True
        messages.append(str(e.args[0]) + " " + str(e.args[1]))
        messages.append(unicode(eval(repr(e.args[2])), "gbk"))
        messages.append("DeleteService Field 213 " + str(e.args[0]) + " " + str(e.args[1]))
    return None
