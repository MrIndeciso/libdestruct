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


class obj(ABC):
    """A generic object, with reference to the backing memory view."""

    endianness: str = "little"
    """The endianness of the backing refenrece view."""

    def __init__(self: obj, memory: MutableSequence, address: int) -> None:
        """Initialize a generic object.

        Args:
            memory: The backing memory view.
            address: The address of the object in the memory view
        """
        self.memory = memory
        self.address = address

    @abstractmethod
    def value(self: obj) -> object:
        """Return the value of the object."""

    def __str__(self: obj) -> str:
        """Return a string representation of the object."""
        return str(self.value())

    def __repr__(self: obj) -> str:
        """Return a string representation of the object."""
        return f"{self.__class__.__name__}({self.value()})"
