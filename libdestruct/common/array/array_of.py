#
# This file is part of libdestruct (https://github.com/mrindeciso/libdestruct).
# Copyright (c) 2024 Roberto Alessandro Bertolini. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

from __future__ import annotations

from typing import TYPE_CHECKING

from libdestruct.common.array.linear_array_field import LinearArrayField

if TYPE_CHECKING: # pragma: no cover
    from libdestruct.common.array.array_field import ArrayField
    from libdestruct.common.obj import obj


def array_of(item: type[obj], size: int) -> ArrayField:
    """Create an array of items."""
    return LinearArrayField(item, size)
