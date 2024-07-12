#
# This file is part of libdestruct (https://github.com/mrindeciso/libdestruct).
# Copyright (c) 2024 Roberto Alessandro Bertolini. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

from __future__ import annotations

from typing import TYPE_CHECKING

from libdestruct.common.type_inflater import TypeInflater

if TYPE_CHECKING:
    from collections.abc import MutableSequence


def inflater(memory: MutableSequence) -> TypeInflater:
    """Return a TypeInflater instance."""
    return TypeInflater(memory)
