#
# This file is part of libdestruct (https://github.com/mrindeciso/libdestruct).
# Copyright (c) 2024 Roberto Alessandro Bertolini. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

from __future__ import annotations

from ctypes import _SimpleCData, sizeof

from libdestruct.c.ctypes_generic import _ctypes_generic
from libdestruct.common.type_registry import TypeRegistry


def ctypes_type_handler(obj_type: type) -> type[_ctypes_generic]:
    """Return the ctypes type handler for the given object type.

    Args:
        obj_type: The object type to handle.
    """
    if not issubclass(obj_type, _SimpleCData):
        raise TypeError(f"Unsupported object type: {obj_type}.")

    return type(
        f"ctypes_{obj_type.__name__}",
        (_ctypes_generic,),
        {"backing_type": obj_type, "size": sizeof(obj_type)},
    )


TypeRegistry().register_type_handler(_SimpleCData, ctypes_type_handler)
