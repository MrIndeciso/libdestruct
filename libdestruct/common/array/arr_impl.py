#
# This file is part of libdestruct (https://github.com/mrindeciso/libdestruct).
# Copyright (c) 2024 Roberto Alessandro Bertolini. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

from __future__ import annotations

from typing import TYPE_CHECKING

from libdestruct.common.array.array import array

if TYPE_CHECKING:
    from collections.abc import MutableSequence

    from libdestruct.common.obj import obj


class arr_impl(array):
    """A linear sequential array."""

    size: int
    """The size of the array."""

    def __init__(
        self: arr_impl,
        memory: MutableSequence,
        address: int | tuple[obj, int],
        backing_type: obj,
        count: int,
    ) -> None:
        """Initialize the array."""
        self.memory = memory
        self.address = address
        self.backing_type = backing_type
        self.count = count

        self.size = self.backing_type.size * self.count

    def __getitem__(self: arr_impl, index: int) -> obj:
        """Get an item from the array."""
        return self.backing_type(self.memory, (self.address, index * self.backing_type.size))

    def __setitem__(self: arr_impl, index: int, value: obj) -> None:
        """Set an item in the array."""
        raise NotImplementedError("Cannot set items in an array.")
