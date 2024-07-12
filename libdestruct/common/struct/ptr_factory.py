#
# This file is part of libdestruct (https://github.com/mrindeciso/libdestruct).
# Copyright (c) 2024 Roberto Alessandro Bertolini. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

from __future__ import annotations

from typing import TYPE_CHECKING

from libdestruct.common.struct.ptr_struct_field import PtrStructField

if TYPE_CHECKING:
    from libdestruct.common.obj import obj


def ptr_to(item: obj) -> PtrStructField:
    """Crafts a struct member which is a pointer to an object."""
    return PtrStructField(item)
