#
# This file is part of libdestruct (https://github.com/mrindeciso/libdestruct).
# Copyright (c) 2024 Roberto Alessandro Bertolini. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

from __future__ import annotations

from types import MethodType
from typing import TYPE_CHECKING

from libdestruct.common.field import Field

if TYPE_CHECKING:  # pragma: no cover
    from libdestruct.backing.resolver import Resolver
    from libdestruct.common.obj import obj


def is_field_bound_method(item: obj) -> bool:
    """Check if the provided item is the bound method of a Field object."""
    return isinstance(item, MethodType) and isinstance(item.__self__, Field)


def size_of(item_or_inflater: obj | callable[[Resolver], obj]) -> int:
    """Return the size of an object, from an obj or it's inflater."""
    if hasattr(item_or_inflater, "size"):
        return item_or_inflater.size

    # Check if item is the bound method of a Field
    if is_field_bound_method(item_or_inflater):
        field_object = item_or_inflater.__self__
        return field_object.get_size()

    raise ValueError(f"Cannot determine the size of {item_or_inflater}")
