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
    from collections.abc import MutableSequence

    from libdestruct.common.array import array
    from libdestruct.common.obj import obj


class ArrayField(Field):
    """A generator for an array of items."""

    @abstractmethod
    def inflate(self: ArrayField, memory: MutableSequence, address: int | tuple[obj, int]) -> array:
        """Inflate the field.

        Args:
            memory: The backing memory view.
            address: The address of the field in the memory view.
        """
