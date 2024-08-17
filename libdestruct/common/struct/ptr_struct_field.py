#
# This file is part of libdestruct (https://github.com/mrindeciso/libdestruct).
# Copyright (c) 2024 Roberto Alessandro Bertolini. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

from __future__ import annotations

from typing import TYPE_CHECKING

from libdestruct.common.field import Field
from libdestruct.common.ptr import ptr
from libdestruct.common.struct.struct_field import StructField

if TYPE_CHECKING:
    from libdestruct.backing.resolver import Resolver
    from libdestruct.common.obj import obj


class PtrStructField(StructField):
    """A generator for a field of a struct."""

    def __init__(self: PtrStructField, backing_type: type | Field) -> None:
        """Initialize a pointer field.

        Args:
            backing_type: The type of the object the pointer points to.
        """
        self.backing_type = backing_type

    def inflate(self: PtrStructField, resolver: Resolver) -> obj:
        """Inflate the field.

        Args:
            resolver: The backing resolver for the object.
        """
        if isinstance(self.backing_type, Field):
            return ptr(resolver, self.backing_type.inflate)

        return ptr(resolver, self.backing_type)
