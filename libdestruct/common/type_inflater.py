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

    def inflate_field(self: TypeInflater, own: type, field: StructField, address: int | tuple[obj, int]) -> obj:
        """Inflate a field of a struct that has an associated generator."""
        if isinstance(field, PtrStructField):
            if not field.backing_type:
                field.backing_type = own
            elif issubclass(field.backing_type, struct) and not issubclass(field.backing_type, struct_impl):
                field.backing_type = field.backing_type._type_impl

        return field.inflate(self.memory, address)

    def inflate_struct(self: TypeInflater, reference_type: type, address: int | tuple[obj, int]) -> struct:
        """Inflate a struct.

        Args:
            reference_type: The struct to inflate.
            address: The address of the struct in the memory view.

        Returns:
            The inflated struct.
        """
        if hasattr(reference_type, "_type_impl"):
            type_impl = reference_type._type_impl
            instance = type_impl(self.memory, address)
        else:
            type_impl = type(reference_type.__name__, (struct_impl,), {"_members": {}})

            type_impl._reference_struct = None

            instance = type_impl(self.memory, address)

            type_impl._reference_struct = reference_type
            type_impl._inflater = self

            reference_type._type_impl = type_impl

        self._inflate_struct_instance(instance, reference_type)

        reference_type.size = instance.size

        return instance

    def _inflate_struct_instance(self: TypeInflater, instance: struct_impl, reference_type: type) -> None:
        current_offset = 0

        for name, annotation in reference_type.__annotations__.items():
            if name in reference_type.__dict__:
                # Field associated with the annotation
                field = getattr(reference_type, name)
                result = self.inflate_field(annotation, field, (instance, current_offset))
            else:
                result = self.inflate(annotation, (instance, current_offset))

            setattr(instance, name, result)
            instance._members[name] = result
            current_offset += annotation.size

        instance.size = current_offset
