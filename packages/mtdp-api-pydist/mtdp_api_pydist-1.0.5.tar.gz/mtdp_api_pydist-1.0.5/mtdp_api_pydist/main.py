#!/usr/bin/env python
import ctypes
import os

lib_path = os.path.join(os.path.dirname(__file__),"api.so")
lib = ctypes.CDLL(lib_path)

def call_long_running_function(src):
    lib.MtDpApi(src)