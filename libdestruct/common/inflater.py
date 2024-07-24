#
# This file is part of libdestruct (https://github.com/mrindeciso/libdestruct).
# Copyright (c) 2024 Roberto Alessandro Bertolini. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

from __future__ import annotations

from typing import TYPE_CHECKING

from libdestruct.common.type_registry import TypeRegistry

if TYPE_CHECKING:
    from collections.abc import MutableSequence

    from libdestruct.common.obj import obj


class Inflater:
    """The memory manager, which inflates any memory-referencing type."""

    def __init__(self: Inflater, memory: MutableSequence) -> None:
        """Initialize the memory manager."""
        self.memory = memory
        self.type_registry = TypeRegistry()

    def inflate(self: Inflater, item: type, address: int | tuple[obj, int]) -> obj:
        """Inflate a memory-referencing type.

        Args:
            item: The type to inflate.
            address: The address of the object in the memory view.

        Returns:
            The inflated object.
        """
        return self.type_registry.inflater_for(item)(self.memory, address)