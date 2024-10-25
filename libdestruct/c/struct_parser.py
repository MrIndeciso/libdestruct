#
# This file is part of libdestruct (https://github.com/mrindeciso/libdestruct).
# Copyright (c) 2024 Roberto Alessandro Bertolini. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

from __future__ import annotations

import ctypes
import re
import subprocess
import tempfile
from typing import TYPE_CHECKING

from pycparser import c_ast, c_parser

from libdestruct.common.struct import struct

if TYPE_CHECKING:
    from libdestruct.common.obj import obj


def definition_to_type(definition: str) -> type[obj]:
    """Converts a C struct definition to a struct object."""
    parser = c_parser.CParser()

    # If the definition contains includes, we must expand them.
    if "#include" in definition:
        definition = cleanup_attributes(expand_includes(definition))
        force_more_tops = True
    elif "typedef" in definition:
        force_more_tops = True
    else:
        force_more_tops = False

    try:
        ast = parser.parse(definition)
    except c_parser.ParseError as e:
        raise ValueError("Invalid definition. Please add the necessary includes if using non-standard type definitions.") from e

    if not force_more_tops and len(ast.ext) != 1:
        raise ValueError("Definition must contain exactly one top object.")

    # If force_more_tops is True, we take the last top object.
    # This is useful when a struct definition is preceded by typedefs.
    root = ast.ext[-1].type if force_more_tops else ast.ext[0].type

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


def to_uniform_name(name: str) -> str:
    """Converts a name to a uniform name."""
    name = name.replace("unsigned", "u")
    name = name.replace("_Bool", "bool")
    name = name.replace("uchar", "ubyte") # uchar is not a valid ctypes type

    # We have to convert each intX, uintX, intX_t, uintX_t to the original char, short etc.
    name = name.replace("uint8_t", "ubyte")
    name = name.replace("int8_t", "char")
    name = name.replace("int16_t", "short")
    name = name.replace("int32_t", "int")
    name = name.replace("int64_t", "longlong")

    # Only size_t, ssize_t and time_t can end with _t
    if not any(x in name for x in ["size", "ssize", "time"]):
        name = name.replace("_t", "")

    return name


def expand_includes(definition: str) -> str:
    """Expands includes in a C definition using the C preprocessor."""
    # TODO: cache this result between subsequent runs of the same script
    with tempfile.NamedTemporaryFile(mode="w", suffix=".c") as f:
        f.write(definition)
        f.flush()

        result = subprocess.run(["cc", "-std=c99", "-E", f.name], capture_output=True, text=True, check=True) # noqa: S607

    return result.stdout


def cleanup_attributes(definition: str) -> str:
    """Cleans up attributes in a C definition."""
    # Remove __attribute__ ((...)) from the definition.
    pattern = r"__attribute__\s*\(\((?:[^()]+|\((?:[^()]+|\([^()]*\))*\))*\)\)" # ChatGPT provided this, don't ask me
    return re.sub(pattern, "", definition)


def identifier_to_type(identifier: c_ast.IdentifierType) -> type[obj]:
    """Converts a C identifier to a type."""
    if not isinstance(identifier, c_ast.IdentifierType):
        raise TypeError("Definition must be an identifier.")

    identifier_name = "".join(identifier.names)

    ctypes_name = "c_" + identifier_name

    if hasattr(ctypes, ctypes_name):
        return getattr(ctypes, ctypes_name)

    # Convert the identifier name to a uniform name, e.g., "unsigned int" -> "uint".
    ctypes_name = "c_" + to_uniform_name(identifier_name)

    if hasattr(ctypes, ctypes_name):
        return getattr(ctypes, ctypes_name)

    raise ValueError(f"Unsupported identifier: {identifier_name}.")
