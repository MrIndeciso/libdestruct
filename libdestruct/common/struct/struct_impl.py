#
# This file is part of libdestruct (https://github.com/mrindeciso/libdestruct).
# Copyright (c) 2024 Roberto Alessandro Bertolini. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

from __future__ import annotations

from typing import TYPE_CHECKING

from libdestruct.common.obj import obj
from libdestruct.common.struct import struct
from libdestruct.common.type_registry import TypeRegistry

if TYPE_CHECKING:
    from collections.abc import MutableSequence

    from libdestruct.common.obj import obj


class struct_impl(struct):
    """The implementation for the C struct type."""

    size: int
    """The size of the struct in bytes."""

    _members: dict[str, obj]
    """The members of the struct."""

    _reference_struct: struct
    """The reference struct."""

    _inflater: TypeRegistry = TypeRegistry()
    """The type registry, used for inflating the attributes."""

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

        reference_type = self._reference_struct
        self._inflate_struct_attributes(self._inflater, memory, reference_type)

    def _inflate_struct_attributes(
        self: struct_impl,
        inflater: TypeRegistry,
        memory: MutableSequence,
        reference_type: type,
    ) -> None:
        current_offset = 0

        for name, annotation in reference_type.__annotations__.items():
            if name in reference_type.__dict__:
                # Field associated with the annotation
                field = getattr(reference_type, name)
                resolved_type = inflater.inflater_for((field, annotation), owner=(self, reference_type._type_impl))
            else:
                resolved_type = inflater.inflater_for(annotation)

            result = resolved_type(memory, (self, current_offset))
            setattr(self, name, result)
            self._members[name] = result
            current_offset += result.size

    @classmethod
    def compute_own_size(cls: type[struct_impl], reference_type: type) -> None:
        """Compute the size of the struct."""
        size = 0

        for name, annotation in reference_type.__annotations__.items():
            if name in reference_type.__dict__:
                # Field associated with the annotation
                field = getattr(reference_type, name)
                attribute = cls._inflater.inflater_for((field, annotation))(None, 0)
                size += attribute.size
            else:
                attribute = cls._inflater.inflater_for(annotation)
                size += attribute.size

        cls.size = size

    def get(self: struct_impl) -> str:
        """Return the value of the struct."""
        return f"{self.name}(address={self.address}, size={self.size})"

    def to_bytes(self: struct_impl) -> bytes:
        """Return the serialized representation of the struct."""
        return b"".join(member.to_bytes() for member in self._members.values())

    def _set(self: struct_impl, _: str) -> None:
        """Set the value of the struct to the given value."""
        raise RuntimeError("Cannot set the value of a struct.")

    def freeze(self: obj) -> None:
        """Freeze the struct."""
        # The struct has no implicit value, but it must freeze its members
        for member in self._members.values():
            member.freeze()

        self._frozen = True

    def to_str(self: struct_impl, indent: int = 0) -> str:
        """Return a string representation of the struct."""
        members = ",\n".join(
            [
                f"{' ' * (indent + 4)}{name}: {member.to_str(indent + 4) if isinstance(member, struct) else member.to_str(0)}"
                for name, member in self._members.items()
            ],
        )
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

    def __eq__(self: struct_impl, value: object) -> bool:
        """Return whether the struct is equal to the given value."""
        if not isinstance(value, struct_impl):
            return False

        if self.size != value.size:
            return False

        if not self._members.keys() == value._members.keys():
            return False

        return all(getattr(self, name) == getattr(value, name) for name in self._members)
