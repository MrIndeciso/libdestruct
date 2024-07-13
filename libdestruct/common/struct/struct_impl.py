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

    from libdestruct.common.obj import obj
    from libdestruct.common.type_inflater import TypeInflater


class struct_impl(struct):
    """The implementation for the C struct type."""

    size: int
    """The size of the struct in bytes."""

    _members: dict[str, obj]
    """The members of the struct."""

    _reference: struct
    """The reference struct."""

    _inflater: TypeInflater
    """The type inflater."""

    def __init__(self: struct_impl, memory: MutableSequence, address: int | tuple[obj, int]) -> None:
        """Initialize the struct implementation."""
        self.name = self.__class__.__name__
        self.memory = memory

        if isinstance(address, tuple):
            self._address = None
            self._reference = address[0]
            self._offset = address[1]
        else:
            self._address = address

        self.size = 0
        self._members = {}

        if hasattr(self, "_reference_struct") and hasattr(self, "_inflater"):
            reference_type = self._reference_struct
            self._inflater._inflate_struct_instance(self, reference_type, reference_type._type_impl)

    def get(self: struct_impl) -> str:
        """Return the value of the struct."""
        return f"{self.name}(address={self.address}, size={self.size})"

    def set(self: struct_impl, _: str) -> None:
        """Set the value of the struct to the given value."""
        raise RuntimeError("Cannot set the value of a struct.")

    def to_str(self: struct_impl, indent: int = 0) -> str:
        """Return a string representation of the struct."""
        members = ",\n".join([f"{' ' * (indent + 4)}{name}: {member.to_str(indent + 4) if isinstance(member, struct) else member.to_str(0)}" for name, member in self._members.items()])
        return f"""{self.name} {{
{members}
{' ' * indent}}}"""

    def __str__(self: struct_impl) -> str:
        """Return a string representation of the struct."""
        return self.to_str()

    def __repr__(self: struct_impl) -> str:
        """Return a string representation of the struct."""
        members = ",\n".join([f"{name}: {member}" for name, member in self._members.items()])
        return f"""{self.name} {{
    address: 0x{self.address:x},
    size: 0x{self.size:x},
    members: {{
        {members}
    }}
}}"""
