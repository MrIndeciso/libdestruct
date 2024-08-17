#
# This file is part of libdestruct (https://github.com/mrindeciso/libdestruct).
# Copyright (c) 2024 Roberto Alessandro Bertolini. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from libdestruct.common.field import Field

if TYPE_CHECKING:
    from libdestruct.backing.resolver import Resolver
    from libdestruct.common.obj import obj


class StructField(Field):
    """A generator for a field of a struct."""

    @abstractmethod
    def inflate(self: StructField, resolver: Resolver) -> obj:
        """Inflate the field.

        Args:
            resolver: The backing resolver for the object.
        """
