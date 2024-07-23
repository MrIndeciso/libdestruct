#
# This file is part of libdestruct (https://github.com/mrindeciso/libdestruct).
# Copyright (c) 2024 Roberto Alessandro Bertolini. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

from __future__ import annotations

from typing import TYPE_CHECKING

from libdestruct.common.array.array import array
from libdestruct.common.obj import obj

if TYPE_CHECKING:
    from collections.abc import Generator, MutableSequence

    from libdestruct.common.obj import obj


class array_impl(array):
    """A linear sequential array."""

    size: int
    """The size of the array."""

    def __init__(
        self: array_impl,
        memory: MutableSequence,
        address: int | tuple[obj, int],
        backing_type: obj,
        count: int,
    ) -> None:
        """Initialize the array."""
        self.memory = memory
        self.backing_type = backing_type
        self.count = count

        if isinstance(address, tuple):
            self._address = None
            self._reference = address[0]
            self._offset = address[1]
        else:
            self._address = address

        self.size = self.backing_type.size * self.count

    def size(self: array_impl) -> int:
        """Get the size of the array."""
        return self.size

    def get(self: array_impl) -> str:
        """Get the array as a string."""
        return f"[{', '.join(str(i) for i in self)}]"

    def _set(self: array_impl, _: list[obj]) -> None:
        """Set the array from a list."""
        raise NotImplementedError("Cannot set items in an array.")

    def set(self: array_impl, _: list[obj]) -> None:
        """Set the array from a list."""
        raise NotImplementedError("Cannot set items in an array.")

    def to_bytes(self: array_impl) -> bytes:
        """Return the serialized representation of the array."""
        return b"".join(x for x in self)

    def __getitem__(self: array_impl, index: int) -> obj:
        """Get an item from the array."""
        if self._address:
            return self.backing_type(self.memory, (self._address, index * self.backing_type.size))

        return self.backing_type(self.memory, (self._reference, self._offset + index * self.backing_type.size))

    def __setitem__(self: array_impl, index: int, value: obj) -> None:
        """Set an item in the array."""
        raise NotImplementedError("Cannot set items in an array.")

    def __iter__(self: array_impl) -> Generator[obj, None, None]:
        """Iterate over the array."""
        for i in range(self.count):
            yield self[i]
