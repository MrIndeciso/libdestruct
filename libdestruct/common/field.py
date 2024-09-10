#
# This file is part of libdestruct (https://github.com/mrindeciso/libdestruct).
# Copyright (c) 2024 Roberto Alessandro Bertolini. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING: # pragma: no cover
    from libdestruct.backing.resolver import Resolver
    from libdestruct.common.obj import obj


class Field(ABC):
    """A generator for a generic field."""

    @abstractmethod
    def inflate(self: Field, resolver: Resolver) -> obj:
        """Inflate the field.

        Args:
            resolver: The backing resolver for the object.
        """
