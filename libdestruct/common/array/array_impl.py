#
# This file is part of libdestruct (https://github.com/mrindeciso/libdestruct).
# Copyright (c) 2024 Roberto Alessandro Bertolini. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

from __future__ import annotations

from typing import TYPE_CHECKING

from libdestruct.c.c_integer_types import _c_integer
from libdestruct.c.ctypes_generic import _ctypes_generic
from libdestruct.common.array.array import array
from libdestruct.common.obj import obj
from libdestruct.common.struct.struct import struct

if TYPE_CHECKING: # pragma: no cover
    from collections.abc import Generator

    from libdestruct.backing.resolver import Resolver
    from libdestruct.common.obj import obj


class array_impl(array):
    """A linear sequential array."""

    size: int
    """The size of the array."""

    def __init__(
        self: array_impl,
        resolver: Resolver,
        backing_type: obj,
        count: int,
    ) -> None:
        """Initialize the array."""
        super().__init__(resolver)

        self.backing_type = backing_type
        self._count = count
        self.size = self.backing_type.size * self._count

    def count(self: array_impl) -> int:
        """Get the size of the array."""
        return self._count

    def get(self: array, index: int) -> object:
        """Return the element at the given index."""
        return self.backing_type(self.resolver.relative_from_own(index * self.backing_type.size, 0))

    def _set(self: array_impl, _: list[obj]) -> None:
        """Set the array from a list."""
        raise NotImplementedError("Cannot set items in an array.")

    def set(self: array_impl, _: list[obj]) -> None:
        """Set the array from a list."""
        raise NotImplementedError("Cannot set items in an array.")

    def to_bytes(self: array_impl) -> bytes:
        """Return the serialized representation of the array."""
        return b"".join(bytes(x) for x in self)

    def to_str(self: array_impl, indent: int = 0) -> str:
        """Return the string representation of the array."""
        if self._count == 0:
            return "[]"

        # If the backing type is a struct, we need to indent the output differently
        if issubclass(self.backing_type, struct):
            padding = ",\n" + " " * (indent + 4)
            spacing = " " * (indent + 4)
            return "[\n" + spacing + padding.join(x.to_str(indent + 4) for x in self) + "\n" + " " * (indent) + "]"

        return "[" + ", ".join(x.to_str(indent + 4) for x in self) + "]"

    def __setitem__(self: array_impl, index: int, value: obj) -> None:
        """Set an item in the array."""
        raise NotImplementedError("Cannot set items in an array.")

    def __iter__(self: array_impl) -> Generator[obj, None, None]:
        """Iterate over the array."""
        for i in range(self._count):
            yield self[i]
