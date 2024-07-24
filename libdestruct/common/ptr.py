#
# This file is part of libdestruct (https://github.com/mrindeciso/libdestruct).
# Copyright (c) 2024 Roberto Alessandro Bertolini. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

from __future__ import annotations

from libdestruct.common.field import Field
from libdestruct.common.obj import obj


class ptr(obj):
    """A pointer to an object in memory."""

    size: int = 8
    """The size of a pointer in bytes."""

    def __init__(self: ptr, memory: bytearray, address: int, wrapper: type | None = None) -> None:
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

    def to_bytes(self: obj) -> bytes:
        """Return the serialized representation of the object."""
        if self._frozen:
            return self._frozen_value.to_bytes(self.size, self.endianness)

        return self.memory[self.address : self.address + self.size]

    def _set(self: ptr, value: int) -> None:
        """Set the value of the pointer to the given value."""
        self.memory[self.address : self.address + self.size] = value.to_bytes(self.size, self.endianness)

    def unwrap(self: ptr, length: int | None = None) -> obj:
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

    def try_unwrap(self: ptr, length: int | None = None) -> obj | None:
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

    def to_str(self: ptr, indent: int = 0) -> str:
        """Return a string representation of the pointer."""
        if not self.wrapper:
            return f"{' ' * indent}ptr@0x{self.get():x}"

        # Pretty print inflaters:
        if callable(self.wrapper) and hasattr(self.wrapper, "__self__") and isinstance(self.wrapper.__self__, Field):
            name = self.wrapper.__self__.__class__.__qualname__
        else:
            name = self.wrapper.__name__

        return f"{' ' * indent}{name}@0x{self.get():x}"


    def __str__(self: ptr) -> str:
        """Return a string representation of the pointer."""
        return self.to_str()
