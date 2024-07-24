#
# This file is part of libdestruct (https://github.com/mrindeciso/libdestruct).
# Copyright (c) 2024 Roberto Alessandro Bertolini. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

from __future__ import annotations

from libdestruct.common.struct.struct import struct
from libdestruct.common.struct.struct_impl import struct_impl
from libdestruct.common.type_registry import TypeRegistry

registry = TypeRegistry()


def inflate_struct_type(reference_type: type[struct]) -> type[struct_impl]:
    """Inflate a struct type."""
    if issubclass(reference_type, struct_impl):
        return reference_type

    type_impl = type(reference_type.__name__, (struct_impl,), {"_members": {}})
    type_impl._reference_struct = reference_type

    reference_type._type_impl = type_impl

    type_impl.compute_own_size(reference_type)

    return type_impl


registry.register_type_handler(struct, inflate_struct_type)
registry.register_type_handler(struct_impl, inflate_struct_type)
