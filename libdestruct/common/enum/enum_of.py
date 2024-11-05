#
# This file is part of libdestruct (https://github.com/mrindeciso/libdestruct).
# Copyright (c) 2024 Roberto Alessandro Bertolini. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

from __future__ import annotations

from enum import IntEnum
from typing import TYPE_CHECKING

from libdestruct.common.enum.int_enum_field import IntEnumField

if TYPE_CHECKING:  # pragma: no cover
    from libdestruct.common.enum.enum_field import EnumField


def enum_of(enum_type: type[IntEnum], lenient: bool = True, size: int = 4) -> EnumField:
    """Return a new enum field."""
    if not issubclass(enum_type, IntEnum):
        raise TypeError("The enum type must be a subclass of IntEnum.")

    return IntEnumField(enum_type, lenient, size)
