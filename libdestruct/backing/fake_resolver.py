#
# This file is part of libdestruct (https://github.com/mrindeciso/libdestruct).
# Copyright (c) 2024 Roberto Alessandro Bertolini. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

from __future__ import annotations

from typing import TYPE_CHECKING

from libdestruct.backing.resolver import Resolver


class FakeResolver(Resolver):
    """A class that can resolve elements in a simulated memory storage."""

    def __init__(self: FakeResolver, memory: dict | None = None, address: int | None = 0) -> FakeResolver:
        """Initializes a basic fake resolver."""
        self.memory = memory if memory is not None else {}
        self.address = address
        self.parent = None
        self.offset = None

    def resolve_address(self: FakeResolver) -> int:
        """Resolves self's address, mainly used by children to determine their own address."""
        if self.address is not None:
            return self.address

        return self.parent.resolve_address() + self.offset

    def relative_from_own(self: FakeResolver, address_offset: int, _: int) -> FakeResolver:
        """Creates a resolver that references a parent, such that a change in the parent is propagated on the child."""
        new_resolver = FakeResolver(self.memory, None)
        new_resolver.parent = self
        new_resolver.offset = address_offset
        return new_resolver

    def absolute_from_own(self: FakeResolver, address: int) -> FakeResolver:
        """Creates a resolver that has an absolute reference to an object, from the parent's view."""
        return FakeResolver(self.memory, address)

    def resolve(self: FakeResolver, size: int, _: int) -> bytes:
        """Resolves itself, providing the bytes it references for the specified size and index."""
        address = self.resolve_address()
        # We store data in the dictionary as 4K pages
        page_address = address & ~0xFFF
        page_offset = address & 0xFFF

        result = b""

        while size:
            page = self.memory.get(page_address, b"\x00" * (0x1000 - page_offset))
            page_size = min(size, 0x1000 - page_offset)
            result += page[page_offset : page_offset + page_size]
            size -= page_size
            page_address += 0x1000
            page_offset = 0

        return result

    def modify(self: FakeResolver, size: int, _: int, value: bytes) -> None:
        """Modifies itself in memory."""
        address = self.resolve_address()
        # We store data in the dictionary as 4K pages
        page_address = address & ~0xFFF
        page_offset = address & 0xFFF

        while size:
            page = self.memory.get(page_address, b"\x00" * 0x1000)
            page_size = min(size, 0x1000 - page_offset)
            page = page[:page_offset] + value[:page_size] + page[page_offset + page_size :]
            self.memory[page_address] = page
            size -= page_size
            value = value[page_size:]
            page_address += 0x1000
            page_offset = 0
