#
# This file is part of libdestruct (https://github.com/mrindeciso/libdestruct).
# Copyright (c) 2024 Roberto Alessandro Bertolini. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

from __future__ import annotations

from typing import TYPE_CHECKING

from libdestruct.common.struct import struct

if TYPE_CHECKING:
    from collections.abc import MutableSequence


class struct_impl(struct):
    """The implementation for the C struct type."""

    def __init__(self: struct_impl, name: str, memory: MutableSequence, address: int) -> None:
        """Initialize the struct implementation."""
        self.name = name
        self.memory = memory
        self.address = address
        self.length = 0

    def value(self: struct_impl) -> str:
        """Return the value of the struct."""
        return f"{self.name}(address={self.address}, length={self.length})"
