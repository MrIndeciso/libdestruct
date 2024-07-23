#
# This file is part of libdestruct (https://github.com/mrindeciso/libdestruct).
# Copyright (c) 2024 Roberto Alessandro Bertolini. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

from __future__ import annotations

from typing import TYPE_CHECKING

from libdestruct.common.struct.ptr_struct_field import PtrStructField
from libdestruct.common.struct.struct import struct
from libdestruct.common.struct.struct_impl import struct_impl
from libdestruct.common.type_registry import TypeRegistry

if TYPE_CHECKING:
    from collections.abc import Callable, MutableSequence

    from libdestruct.common.obj import obj

registry = TypeRegistry()


def ptr_field_inflater(
    field: PtrStructField,
    _: type[obj],
    owner: tuple[obj, type[obj]] | None,
) -> Callable[[MutableSequence, int | tuple[obj, int]], obj]:
    """Returns the inflated for a field of a struct that has an associated generator."""
    if not field.backing_type:
        if owner:
            _, owner_type = owner
            field.backing_type = owner_type
    elif issubclass(field.backing_type, struct) and not issubclass(field.backing_type, struct_impl):
        field.backing_type = registry.inflater_for(field.backing_type)

    return field.inflate


registry.register_instance_handler(PtrStructField, ptr_field_inflater)
