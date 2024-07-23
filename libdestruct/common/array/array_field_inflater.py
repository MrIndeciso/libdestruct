#
# This file is part of libdestruct (https://github.com/mrindeciso/libdestruct).
# Copyright (c) 2024 Roberto Alessandro Bertolini. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#


from __future__ import annotations

from typing import TYPE_CHECKING

from libdestruct.common.array.linear_array_field import LinearArrayField
from libdestruct.common.struct.struct import struct
from libdestruct.common.struct.struct_impl import struct_impl
from libdestruct.common.type_registry import TypeRegistry

if TYPE_CHECKING:
    from collections.abc import Callable, MutableSequence

    from libdestruct.common.obj import obj

registry = TypeRegistry()


def linear_array_field_inflater(
    field: LinearArrayField,
    _: type[obj],
    __: tuple[obj, type[obj]] | None,
) -> Callable[[MutableSequence, int | tuple[obj, int]], obj]:
    """Returns the inflater for an array field of a struct."""
    if issubclass(field.item, struct) and not issubclass(field.item, struct_impl):
        field.item = registry.inflater_for(field.item)

    return field.inflate


registry.register_instance_handler(LinearArrayField, linear_array_field_inflater)
