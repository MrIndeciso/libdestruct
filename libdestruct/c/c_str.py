#
# This file is part of libdestruct (https://github.com/mrindeciso/libdestruct).
# Copyright (c) 2024 Roberto Alessandro Bertolini. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

from __future__ import annotations

from libdestruct.common.array import array
from libdestruct.common.obj import obj


class c_str(obj, array):
    """A C string."""

    def size(self: c_str) -> int:
        """Return the size of the string."""
        size = 0

        try:
            while self.memory[self.address + size] != 0:
                size += 1
        except IndexError as e:
            raise RuntimeError("String is not null-terminated.") from e

        return size

    def get(self: c_str, index: int) -> bytes:
        """Return the character at the given index."""
        if index < 0 or index >= self.size():
            raise IndexError("String index out of range.")

        return bytes([self.memory[self.address + index]])

    def _set(self: c_str, index: int, value: bytes) -> None:
        """Set the character at the given index to the given value."""
        if index < 0 or index >= self.size():
            raise IndexError("String index out of range.")

        self.memory[self.address + index] = value

    def __iter__(self: c_str) -> iter:
        """Return an iterator over the string."""
        for i in range(self.size()):
            yield self.get(i)
