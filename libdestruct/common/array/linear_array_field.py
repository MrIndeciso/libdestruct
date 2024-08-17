#
# This file is part of libdestruct (https://github.com/mrindeciso/libdestruct).
# Copyright (c) 2024 Roberto Alessandro Bertolini. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

from __future__ import annotations

from typing import TYPE_CHECKING

from libdestruct.common.array.array_field import ArrayField
from libdestruct.common.array.array_impl import array_impl

if TYPE_CHECKING:
    from libdestruct.backing.resolver import Resolver
    from libdestruct.common.array.array import array
    from libdestruct.common.obj import obj


class LinearArrayField(ArrayField):
    """A generator for an array of items."""

    def __init__(self: LinearArrayField, item: type[obj], size: int) -> None:
        """Initialize the field."""
        self.item = item
        self.size = size

    def inflate(self: LinearArrayField, resolver: Resolver) -> array:
        """Inflate the field.

        Args:
            resolver: The backing resolver for the object.
        """
        return array_impl(resolver, self.item, self.size)
