#
# This file is part of libdestruct (https://github.com/mrindeciso/libdestruct).
# Copyright (c) 2024 Roberto Alessandro Bertolini. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

from __future__ import annotations

from typing import TYPE_CHECKING

from libdestruct.common.enum.int_enum_field import IntEnumField
from libdestruct.common.type_registry import TypeRegistry

if TYPE_CHECKING:
    from collections.abc import Callable, MutableSequence

    from libdestruct.common.enum.enum_field import EnumField
    from libdestruct.common.obj import obj

registry = TypeRegistry()


def generic_enum_field_inflater(
    field: EnumField,
    _: type[obj],
    __: tuple[obj, type[obj]] | None,
) -> Callable[[MutableSequence, int | tuple[obj, int]], obj]:
    """Returns the inflater for an enum field of a struct."""
    return field.inflate


registry.register_instance_handler(IntEnumField, generic_enum_field_inflater)