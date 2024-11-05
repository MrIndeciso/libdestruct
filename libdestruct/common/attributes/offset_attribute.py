#
# This file is part of libdestruct (https://github.com/mrindeciso/libdestruct).
# Copyright (c) 2024 Roberto Alessandro Bertolini. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

from __future__ import annotations

from libdestruct.common.attribute import Attribute


class OffsetAttribute(Attribute):
    """A field that represents an offset in a struct."""

    offset: int

    def __init__(self: OffsetAttribute, offset: int) -> None:
        """Initialize the offset field."""
        self.offset = offset
