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

    address: int
    """The address of the object in the memory view."""

    endianness: str = "little"
    """The endianness of the backing refenrece view."""

    memory: MutableSequence
    """The backing memory view."""

    _frozen: bool = False
    """Whether the object is frozen."""

    _frozen_value: object = None
    """The frozen value of the object."""

    def __init__(self: obj, memory: MutableSequence, address: int | tuple[obj, int]) -> None:
        """Initialize a generic object.

        Args:
            memory: The backing memory view.
            address: The address of the object in the memory view
        """
        self.memory = memory

        if isinstance(address, tuple):
            self._address = None
            self._reference = address[0]
            self._offset = address[1]
        else:
            self._address = address

    @property
    def address(self: obj) -> int:
        """Return the address of the object in the memory view."""
        if self._address is not None:
            return self._address

        return self._reference.address + self._offset

    @abstractmethod
    def get(self: obj) -> object:
        """Return the value of the object."""

    @abstractmethod
    def _set(self: obj, value: object) -> None:
        """Set the value of the object to the given value."""

    def set(self: obj, value: object) -> None:
        """Set the value of the object to the given value."""
        if self._frozen:
            raise ValueError("Cannot set the value of a frozen object.")

        self._set(value)

    def freeze(self: obj) -> None:
        """Freeze the object."""
        self._frozen_value = self.get()
        self._frozen = True

    @property
    def value(self: obj) -> object:
        """Return the value of the object."""
        if self._frozen:
            return self._frozen_value
        return self.get()

    @value.setter
    def value(self: obj, value: object) -> None:
        """Set the value of the object to the given value."""
        if self._frozen:
            raise ValueError("Cannot set the value of a frozen object.")

        self._set(value)

    def to_str(self: obj, indent: int = 0) -> str:
        """Return a string representation of the object."""
        return f"{' ' * indent}{self.get()}"

    def __str__(self: obj) -> str:
        """Return a string representation of the object."""
        return self.to_str()

    def __repr__(self: obj) -> str:
        """Return a string representation of the object."""
        return f"{self.__class__.__name__}({self.get()})"

    def __eq__(self, value: object) -> bool:
        """Return whether the object is equal to the given value."""
        if not isinstance(value, obj):
            return False

        return self.get() == value.get()
