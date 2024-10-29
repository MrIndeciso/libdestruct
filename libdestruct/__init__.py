#
# This file is part of libdestruct (https://github.com/mrindeciso/libdestruct).
# Copyright (c) 2024 Roberto Alessandro Bertolini. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

try: # pragma: no cover
    from rich.traceback import install

    install()
except ImportError: # pragma: no cover
    pass

from libdestruct.c import c_int, c_long, c_str, c_uint, c_ulong
from libdestruct.common.array import array, array_of
from libdestruct.common.attributes import offset
from libdestruct.common.enum import enum, enum_of
from libdestruct.common.ptr import ptr
from libdestruct.common.struct import ptr_to, ptr_to_self, struct
from libdestruct.libdestruct import inflater

__all__ = [
    "array",
    "array_of",
    "offset",
    "c_int",
    "c_long",
    "c_str",
    "c_uint",
    "c_ulong",
    "enum",
    "enum_of",
    "inflater",
    "struct",
    "ptr",
    "ptr_to",
    "ptr_to_self",
]
