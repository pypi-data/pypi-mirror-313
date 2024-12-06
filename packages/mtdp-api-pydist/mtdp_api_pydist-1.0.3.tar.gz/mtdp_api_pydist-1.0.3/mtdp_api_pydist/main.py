#!/usr/bin/env python
import ctypes

# 加载共享库
lib = ctypes.CDLL('./api.so')

# 定义一个线程函数来调用Go函数
def call_long_running_function(src):
    lib.MtDpApi(src)