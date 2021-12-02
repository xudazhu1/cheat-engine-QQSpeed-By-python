#!/usr/bin/python
# -*- coding: UTF-8 -*-
import ctypes
import inspect
import threading

from concurrent import futures


pool = futures.ThreadPoolExecutor(max_workers=128)


def thread_it(func, *args):
    # '''将函数放入线程中执行'''
    # 创建线程
    t = threading.Thread(target=func, args=args)
    # 守护线程
    t.setDaemon(True)
    # 启动线程
    t.start()
    return t


def thread_it_disDaemon(func, *args):
    # '''将函数放入线程中执行'''
    # 创建线程
    t = threading.Thread(target=func, args=args)
    # 守护线程
    # t.setDaemon(True)
    # 启动线程
    t.start()
    return t


def threadByFuture(func, *args):
    # '''将函数放入线程中执行'''
    # 创建线程
    t = pool.submit(func, *args)
    # 守护线程
    # t.setDaemon(True)
    # 启动线程
    # t.start()
    return t


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    try:
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")
    except ValueError as e:
        print(str(e))


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)

# exitFlag = 0
#
#
# class MyThread(threading.Thread):  # 继承父类threading.Thread
#
#     def __init__(self, threadID, func, *args):
#         threading.Thread.__init__(self)
#         self.threadID = threadID
#         self.func = func
#         self.args = args
#
#     # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
#     def run(self):
#         end = self.func(self.args)
#         if not end:
#             print("操作结束,返回False")

# 创建新线程
# thread1 = myThread(1, "Thread-1", 1)
# thread2 = myThread(2, "Thread-2", 2)

# 开启线程
# thread1.start()
# thread2.start()
