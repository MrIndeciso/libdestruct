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
    def get(self: obj) -> object:
        """Return the value of the object."""

    @abstractmethod
    def set(self: obj, value: object) -> None:
        """Set the value of the object to the given value."""

    @property
    def value(self: obj) -> object:
        """Return the value of the object."""
        return self.get()

    @value.setter
    def value(self: obj, value: object) -> None:
        """Set the value of the object to the given value."""
        self.set(value)

    def __str__(self: obj) -> str:
        """Return a string representation of the object."""
        return str(self.get())

    def __repr__(self: obj) -> str:
        """Return a string representation of the object."""
        return f"{self.__class__.__name__}({self.get()})"
