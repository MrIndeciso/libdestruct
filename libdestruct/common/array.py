#
# This file is part of libdestruct (https://github.com/mrindeciso/libdestruct).
# Copyright (c) 2024 Roberto Alessandro Bertolini. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

from __future__ import annotations

from abc import ABC, abstractmethod


class array(ABC):
    @abstractmethod
    def size(self: array) -> int:
        """Return the size of the array."""

    def __len__(self: array) -> int:
        """Return the size of the array."""
        return self.size()

    @abstractmethod
    def get(self: array, index: int) -> object:
        """Return the element at the given index."""

    def __getitem__(self: array, index: int) -> object:
        """Return the element at the given index."""
        return self.get(index)

    @abstractmethod
    def set(self: array, index: int, value: object) -> None:
        """Set the element at the given index to the given value."""

    def __setitem__(self: array, index: int, value: object) -> None:
        """Set the element at the given index to the given value."""
        self.set(index, value)

    @abstractmethod
    def __iter__(self: array) -> iter:
        """Return an iterator over the array."""

    def __contains__(self: array, value: object) -> bool:
        """Return whether the array contains the given value."""
        return any(value == element for element in self)
