#
# This file is part of libdestruct (https://github.com/mrindeciso/libdestruct).
# Copyright (c) 2024 Roberto Alessandro Bertolini. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import MutableSequence

    from libdestruct.common.obj import obj


class StructField(ABC):
    """A generator for a field of a struct."""

    @abstractmethod
    def inflate(self: StructField, memory: MutableSequence, address: int) -> obj:
        """Inflate the field.

        Args:
            memory: The backing memory view.
            address: The address of the field in the memory view.
        """
