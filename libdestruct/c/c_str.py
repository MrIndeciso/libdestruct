#
# This file is part of libdestruct (https://github.com/mrindeciso/libdestruct).
# Copyright (c) 2024 Roberto Alessandro Bertolini. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

from __future__ import annotations

from libdestruct.common.array.array import array


class c_str(array):
    """A C string."""

    def size(self: c_str) -> int:
        """Return the size of the string."""
        size = 0

        try:
            while self.memory[self.address + size] != b"\x00":
                size += 1
        except IndexError as e:
            raise RuntimeError("String is not null-terminated.") from e

        return size

    def get(self: c_str, index: int = -1) -> bytes:
        """Return the character at the given index."""
        if index != -1 and index < 0 or index >= self.size():
            raise IndexError("String index out of range.")

        if index == -1:
            return self.memory[self.address : self.address + self.size()]

        return bytes([self.memory[self.address + index]])

    def to_bytes(self: c_str) -> bytes:
        """Return the serialized representation of the object."""
        return self.memory[self.address : self.address + self.size()]

    def _set(self: c_str, value: bytes, index: int = -1) -> None:
        """Set the character at the given index to the given value."""
        if index != -1 and index < 0 or index >= self.size():
            raise IndexError("String index out of range.")

        if index == -1:
            self.memory[self.address] = value
        else:
            self.memory[self.address + index] = value

    def __iter__(self: c_str) -> iter:
        """Return an iterator over the string."""
        for i in range(self.size()):
            yield self.get(i)
