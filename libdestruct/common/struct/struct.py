#
# This file is part of libdestruct (https://github.com/mrindeciso/libdestruct).
# Copyright (c) 2024 Roberto Alessandro Bertolini. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

from __future__ import annotations

from dataclasses import dataclass

from libdestruct.common.obj import obj


@dataclass(init=False, repr=False, eq=False, order=False, unsafe_hash=False, frozen=False, slots=True)
class struct(obj):
    """A C struct."""

    def __init__(self: obj) -> None:
        """Initialize the struct."""
        raise RuntimeError("This type should not be directly instantiated.")
