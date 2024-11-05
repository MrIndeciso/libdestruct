#
# This file is part of libdestruct (https://github.com/mrindeciso/libdestruct).
# Copyright (c) 2024 Roberto Alessandro Bertolini. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

from __future__ import annotations

from typing import TYPE_CHECKING

from libdestruct.common.ptr.ptr_field import PtrField
from libdestruct.common.type_registry import TypeRegistry

if TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Callable

    from libdestruct.backing.resolver import Resolver
    from libdestruct.common.obj import obj

registry = TypeRegistry()


def ptr_field_inflater(
    field: PtrField,
    _: type[obj],
    owner: tuple[obj, type[obj]] | None,
) -> Callable[[Resolver], obj]:
    """Returns the inflated for a field of a struct that has an associated generator."""
    if not field.backing_type and owner:
        _, owner_type = owner
        field.backing_type = owner_type

    # if field.backing_type and not isinstance(field.backing_type, Field):
    if field.backing_type:
        field.backing_type = registry.inflater_for(field.backing_type)

    return field.inflate


registry.register_instance_handler(PtrField, ptr_field_inflater)
