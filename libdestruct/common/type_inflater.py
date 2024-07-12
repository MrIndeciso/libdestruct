#
# This file is part of libdestruct (https://github.com/mrindeciso/libdestruct).
# Copyright (c) 2024 Roberto Alessandro Bertolini. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

from __future__ import annotations

from typing import TYPE_CHECKING

from libdestruct.common.obj import obj
from libdestruct.common.struct import struct, struct_impl

if TYPE_CHECKING:
    from collections.abc import MutableSequence

    from libdestruct.common.struct.struct_field import StructField


class TypeInflater:
    """The memory manager, which inflates any memory-referencing type."""

    def __init__(self, memory: MutableSequence) -> None:
        """Initialize the memory manager."""
        self.memory = memory

    def inflate(self: TypeInflater, item: type, address: int) -> obj:
        """Inflate a memory-referencing type.

        Args:
            item: The type to inflate.
            address: The address of the object in the memory view.

        Returns:
            The inflated object.
        """
        if not issubclass(item, obj):
            raise TypeError(f"Cannot inflate unknown type {item.__class__.__name__}.")

        if issubclass(item, struct):
            return self.inflate_struct(item, address)

        return item(self.memory, address)

    def inflate_field(self: TypeInflater, _: type, field: StructField, address: int) -> obj:
        """Inflate a field of a struct that has an associated generator."""
        return field.inflate(self.memory, address)

    def inflate_struct(self: TypeInflater, item: struct, address: int) -> struct:
        """Inflate a struct.

        Args:
            item: The struct to inflate.
            address: The address of the struct in the memory view.

        Returns:
            The inflated struct.
        """
        result = struct_impl(item.__qualname__, self.memory, address)
        current_address = address

        for name, annotation in item.__annotations__.items():
            if name in item.__dict__:
                # Field associated with the annotation
                field = getattr(item, name)
                setattr(result, name, self.inflate_field(annotation, field, current_address))
            else:
                setattr(result, name, self.inflate(annotation, current_address))

            current_address += annotation.size

        result.length = current_address - address

        return result
