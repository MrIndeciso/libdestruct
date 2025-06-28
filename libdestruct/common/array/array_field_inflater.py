#
# This file is part of libdestruct (https://github.com/mrindeciso/libdestruct).
# Copyright (c) 2024 Roberto Alessandro Bertolini. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#


from __future__ import annotations

from typing import TYPE_CHECKING

from libdestruct.common.array.linear_array_field import LinearArrayField
from libdestruct.common.type_registry import TypeRegistry

if TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Callable

    from libdestruct.backing.resolver import Resolver
    from libdestruct.common.obj import obj

registry = TypeRegistry()


def linear_array_field_inflater(
    field: LinearArrayField,
    _: type[obj],
    __: tuple[obj, type[obj]] | None,
) -> Callable[[Resolver], obj]:
    """Returns the inflater for an array field of a struct."""
    field.item = registry.inflater_for(field.item)

    return field.inflate


registry.register_instance_handler(LinearArrayField, linear_array_field_inflater)
