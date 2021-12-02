import os
import random
import shutil
import signal
import sys


def resource_path():
    # 返回资源绝对路径
    res = "D:\\project\\my-python32\\dist\\start.exe"
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller会创建临时文件夹temp
        # 并把路径存储在_MEIPASS中
        # noinspection PyProtectedMember
        base_path = sys._MEIPASS
        # messages.append("base_path", base_path)
        res = os.path.join(base_path, "start.exe")
    # print("当前目录: " + base_path)
    tempPath = os.environ.get('APPDATA') + '\\..\\Local\\Temp\\QsTemp'
    if not os.path.exists(tempPath):
        os.mkdir(tempPath)
    else:
        # 清空缓存
        shutil.rmtree(tempPath)
        os.mkdir(tempPath)

    tempName = str(random.random() * 100000000000000.00 * random.random())
    runFilePath = tempPath + "\\" + tempName + ".exe"
    shutil.copy(res, runFilePath)
    # 写
    file = open(runFilePath, 'ab')
    file.write(bytes(tempName, encoding='utf8'))
    file.close()
    return runFilePath


def run():
    path = resource_path()
    # MyTread.thread_it_disDaemon(run)
    os.system('start "" /d ' + os.path.dirname(path) + " " + path)
    # win32api.ShellExecute(0, 'open', path, '', '', 1)
    # sys.exit(1)
    pid = os.getpid()
    os.kill(pid, signal.SIGINT)
    sys.exit(1)
