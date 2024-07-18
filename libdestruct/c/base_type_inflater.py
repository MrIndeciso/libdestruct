#
# This file is part of libdestruct (https://github.com/mrindeciso/libdestruct).
# Copyright (c) 2024 Roberto Alessandro Bertolini. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

from __future__ import annotations

from libdestruct.c.c_int import c_int
from libdestruct.c.c_long import c_long
from libdestruct.c.c_str import c_str
from libdestruct.c.c_uint import c_uint
from libdestruct.c.c_ulong import c_ulong
from libdestruct.common.type_registry import TypeRegistry

registry = TypeRegistry()


registry.register_mapping(c_int, c_int)
registry.register_mapping(c_uint, c_uint)
registry.register_mapping(c_long, c_long)
registry.register_mapping(c_ulong, c_ulong)
registry.register_mapping(c_str, c_str)
