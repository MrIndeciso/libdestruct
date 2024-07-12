#
# This file is part of libdestruct (https://github.com/mrindeciso/libdestruct).
# Copyright (c) 2024 Roberto Alessandro Bertolini. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

from __future__ import annotations

from libdestruct.common.obj import obj


class ptr(obj):
    """A pointer to an object in memory."""

    size: int = 8
    """The size of a pointer in bytes."""

    def __init__(self, memory: bytearray, address: int, wrapper: type | None = None) -> None:
        """Initialize a pointer.

        Args:
            memory: The backing memory view.
            address: The address of the pointer in the memory view.
            wrapper: The object this pointer points to.
        """
        super().__init__(memory, address)
        self.wrapper = wrapper

    def get(self: ptr) -> int:
        """Return the value of the pointer."""
        return int.from_bytes(self.memory[self.address : self.address + self.size], self.endianness)

    def set(self: ptr, value: int) -> None:
        """Set the value of the pointer to the given value."""
        self.memory[self.address : self.address + self.size] = value.to_bytes(self.size, self.endianness)

    def unwrap(self, length: int | None = None) -> obj:
        """Return the object pointed to by the pointer.

        Args:
            length: The length of the object in memory this points to.
        """
        address = self.get()

        if self.wrapper:
            if length:
                raise ValueError("Length is not supported when unwrapping a pointer to a wrapper object.")

            return self.wrapper(self.memory, address)

        if not length:
            length = 1

        return self.memory[address : address + length]

    def try_unwrap(self, length: int | None = None) -> obj | None:
        """Return the object pointed to by the pointer, if it is valid.

        Args:
            length: The length of the object in memory this points to.
        """
        address = self.get()

        try:
            # If the address is invalid, this will raise an IndexError or ValueError.
            self.memory[address]
        except (IndexError, ValueError):
            return None

        return self.unwrap(length)
