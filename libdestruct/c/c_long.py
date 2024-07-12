#
# This file is part of libdestruct (https://github.com/mrindeciso/libdestruct).
# Copyright (c) 2024 Roberto Alessandro Bertolini. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

from __future__ import annotations

from libdestruct.common.obj import obj


class c_long(obj):
    """A C long."""

    size: int = 8
    """The size of an integer in bytes."""

    def value(self: c_long) -> int:
        """Return the value of the integer."""
        return int.from_bytes(self.memory[self.address : self.address + self.size], self.endianness, signed=True)

    def set(self: c_long, value: int) -> None:
        """Set the value of the integer to the given value."""
        self.memory[self.address : self.address + self.size] = value.to_bytes(self.size, self.endianness, signed=True)
