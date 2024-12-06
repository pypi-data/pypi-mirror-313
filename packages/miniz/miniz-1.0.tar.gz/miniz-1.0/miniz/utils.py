from sys        import platform
from platform   import machine

import ctypes


def get_dependency_filename():
    if platform == 'darwin':
        file_ext = '-macOS-arm64.dylib' if machine() == "arm64" else '-macOS-x86_64.dylib'
    elif platform in ('win32', 'cygwin'):
        file_ext = '-Windows-arm64.dll' if 8 == ctypes.sizeof(ctypes.c_voidp) else '-Windows-x86_64.dll'
    else:
        if machine() == "aarch64":
            file_ext = '-Linux-arm64.so'
        elif "x86" in machine():
            file_ext = '-Linux-x86_64.so'
        else:
            file_ext = '-Linux-arm64.so'

    return f'miniz{file_ext}'