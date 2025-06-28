#
# This file is part of libdestruct (https://github.com/mrindeciso/libdestruct).
# Copyright (c) 2024 Roberto Alessandro Bertolini. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

from __future__ import annotations

from libdestruct.common.attributes.offset_attribute import OffsetAttribute


def offset(offset: int) -> OffsetAttribute:
    """Create an offset field."""
    return OffsetAttribute(offset)
