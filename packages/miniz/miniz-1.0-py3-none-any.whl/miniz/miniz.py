import ctypes
import os

from .utils import get_dependency_filename

# Load the compiled miniz
root_dir = os.path.abspath(os.path.dirname(__file__))
library = ctypes.cdll.LoadLibrary(f'{root_dir}/dependencies/{get_dependency_filename()}')

# Define function signatures for decompression and compression
library.mz_compress2.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_ulong), ctypes.c_void_p, ctypes.c_ulong, ctypes.c_int]
library.mz_compress2.restype = ctypes.c_int

library.mz_uncompress.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_ulong), ctypes.c_void_p, ctypes.c_ulong]
library.mz_uncompress.restype = ctypes.c_int


class Miniz:
    # Decompress using miniz
    def decompress(data):
        source = ctypes.create_string_buffer(data)
        source_len = len(data)
        dest_len = ctypes.c_ulong(source_len * 4)  # Allocate more space for decompressed data
        dest = ctypes.create_string_buffer(dest_len.value)

        result = library.mz_uncompress(dest, ctypes.byref(dest_len), source, source_len)
        if result != 0:
            raise RuntimeError("Decompression failed")
        return dest.raw[:dest_len.value]


    # Compress using miniz with the default compression level
    def compress(data, level=1):
        source = ctypes.create_string_buffer(data)
        source_len = len(data)
        dest_len = ctypes.c_ulong(source_len * 2)  # Allocate more space for compressed data
        dest = ctypes.create_string_buffer(dest_len.value)

        result = library.mz_compress2(dest, ctypes.byref(dest_len), source, source_len, level)
        if result != 0:
            raise RuntimeError("Compression failed")
        return dest.raw[:dest_len.value]