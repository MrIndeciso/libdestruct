from enum import IntEnum

from ctypes import c_int
from libdestruct import inflater, struct

class provola2(struct):
    a: c_int

memory = b"\x01\x00\x00\x00"

libdestruct = inflater(memory)

a = libdestruct.inflate(provola2, 0x0)

print(a.a)