#
# This file is part of libdestruct (https://github.com/mrindeciso/libdestruct).
# Copyright (c) 2024 Roberto Alessandro Bertolini. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from libdestruct.common.enum import enum
from libdestruct.common.field import Field

if TYPE_CHECKING:  # pragma: no cover
    from libdestruct.backing.resolver import Resolver
    from libdestruct.common.obj import obj


class EnumField(Field):
    """A generator for an enum."""

    base_type: type[obj] = enum

    @abstractmethod
    def inflate(self: EnumField, resolver: Resolver) -> enum:
        """Inflate the field.

        Args:
            resolver: The backing resolver for the object.
        """
