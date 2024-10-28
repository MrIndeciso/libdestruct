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


def size_of(item_or_inflater: obj | callable[[Resolver], obj]) -> int:
    """Return the size of an object, from an obj or it's inflater."""
    if hasattr(item_or_inflater, "size"):
        return item_or_inflater.size

    # Check if item is the bound method of a Field
    if not isinstance(item_or_inflater, MethodType):
        raise TypeError("Provided inflater is not the bound method of a Field object")

    field_object = item_or_inflater.__self__

    if not isinstance(field_object, Field):
        raise TypeError("Provided inflater is not the bound method of a Field object")

    return field_object.get_size()
