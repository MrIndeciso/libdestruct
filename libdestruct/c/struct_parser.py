#
# This file is part of libdestruct (https://github.com/mrindeciso/libdestruct).
# Copyright (c) 2024 Roberto Alessandro Bertolini. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

from __future__ import annotations

import ctypes
from typing import TYPE_CHECKING

from pycparser import c_ast, c_parser

from libdestruct.common.struct import struct

if TYPE_CHECKING:
    from libdestruct.common.obj import obj


def definition_to_type(definition: str) -> type[obj]:
    """Converts a C struct definition to a struct object."""
    parser = c_parser.CParser()

    ast = parser.parse(definition)

    if len(ast.ext) != 1:
        raise ValueError("Definition must contain exactly one top object.")

    root = ast.ext[0].type

    if not isinstance(root, c_ast.Struct):
        raise TypeError("Definition must be a struct.")

    return struct_to_type(root)


def struct_to_type(struct_node: c_ast.Struct) -> type[struct]:
    """Converts a C struct to a struct object."""
    if not isinstance(struct_node, c_ast.Struct):
        raise TypeError("Definition must be a struct.")

    fields = {}

    for decl in struct_node.decls:
        name = decl.name
        typ = type_decl_to_type(decl.type)
        fields[name] = typ

    type_name = struct_node.name if struct_node.name else "anon_struct"

    return type(type_name, (struct,), {"__annotations__": fields})


def type_decl_to_type(decl: c_ast.TypeDecl) -> type[obj]:
    """Converts a C type declaration to a type."""
    if not isinstance(decl, c_ast.TypeDecl):
        raise TypeError("Definition must be a type declaration.")

    if isinstance(decl.type, c_ast.Struct):
        return struct_to_type(decl.type)

    if isinstance(decl.type, c_ast.IdentifierType):
        return identifier_to_type(decl.type)

    raise TypeError("Unsupported type.")


def identifier_to_type(identifier: c_ast.IdentifierType) -> type[obj]:
    """Converts a C identifier to a type."""
    if not isinstance(identifier, c_ast.IdentifierType):
        raise TypeError("Definition must be an identifier.")

    identifier_name = "_".join(identifier.names)

    ctypes_name = f"c_{identifier_name}"

    if hasattr(ctypes, ctypes_name):
        return getattr(ctypes, ctypes_name)

    raise ValueError(f"Unsupported identifier: {identifier_name}.")
