#
# This file is part of libdestruct (https://github.com/mrindeciso/libdestruct).
# Copyright (c) 2024 Roberto Alessandro Bertolini. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

from __future__ import annotations

from typing import TYPE_CHECKING

from libdestruct.common.obj import obj
from libdestruct.common.struct import struct, struct_impl
from libdestruct.common.struct.ptr_struct_field import PtrStructField

if TYPE_CHECKING:
    from collections.abc import MutableSequence

    from libdestruct.common.struct.struct_field import StructField


class TypeInflater:
    """The memory manager, which inflates any memory-referencing type."""

    def __init__(self: TypeInflater, memory: MutableSequence) -> None:
        """Initialize the memory manager."""
        self.memory = memory

    def inflate(self: TypeInflater, item: type, address: int | tuple[obj, int]) -> obj:
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

    def inflate_field(
        self: TypeInflater,
        _: type,
        own: type,
        field: StructField,
        address: int | tuple[obj, int],
    ) -> obj:
        """Inflate a field of a struct that has an associated generator."""
        if isinstance(field, PtrStructField) and not field.backing_type:
            field.backing_type = own

        return field.inflate(self.memory, address)

    def inflate_struct(self: TypeInflater, item: struct, address: int | tuple[obj, int]) -> struct:
        """Inflate a struct.

        Args:
            item: The struct to inflate.
            address: The address of the struct in the memory view.

        Returns:
            The inflated struct.
        """
        new_type = type(item.__name__, (struct_impl,), {"_members": {}})

        new_type._reference = None

        impl = new_type(self.memory, address)

        new_type._reference = item
        new_type._inflater = self

        self._inflate_struct_instance(impl, new_type)

        return impl

    def _inflate_struct_instance(self: TypeInflater, impl: struct_impl, new_type: type) -> None:
        item = impl._reference

        current_offset = 0

        for name, annotation in item.__annotations__.items():
            if name in item.__dict__:
                # Field associated with the annotation
                field = getattr(item, name)
                result = self.inflate_field(annotation, new_type, field, (impl, current_offset))
            else:
                result = self.inflate(annotation, (impl, current_offset))

            setattr(new_type, name, result)
            impl._members[name] = result
            current_offset += annotation.size

        impl.length = current_offset
