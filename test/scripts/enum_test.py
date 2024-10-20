#
# This file is part of libdestruct (https://github.com/mrindeciso/libdestruct).
# Copyright (c) 2024 Roberto Alessandro Bertolini. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

import unittest

from enum import Enum, IntEnum
from libdestruct import inflater, enum, enum_of, struct

class EnumTest(unittest.TestCase):
    def test_enum(self):
        class Test(IntEnum):
            A = 0
            B = 1
            C = 2
            D = 3

        libdestruct = inflater((0).to_bytes(4, "little"))

        a = libdestruct.inflate(enum_of(Test), 0)

        self.assertEqual(a.value, Test.A)

        self.assertEqual(bytes(a), b"\x00\x00\x00\x00")

        class TestHolder(struct):
            a: enum = enum_of(Test)
            b: enum = enum_of(Test)
            c: enum = enum_of(Test)
            d: enum = enum_of(Test)

        libdestruct = inflater(b"".join(i.to_bytes(4, "little") for i in range(4)))

        test = libdestruct.inflate(TestHolder, 0)

        self.assertEqual(test.a.value, Test.A)
        self.assertEqual(test.b.value, Test.B)
        self.assertEqual(test.c.value, Test.C)
        self.assertEqual(test.d.value, Test.D)

        self.assertEqual(bytes(test), b"".join(i.to_bytes(4, "little") for i in range(4)))

        with self.assertRaises(TypeError):
            enum_of(Enum)

        # Let's try with enums of different sizes
        class TestHolder2(struct):
            a: enum = enum_of(Test, size=1)
            b: enum = enum_of(Test, size=2)
            c: enum = enum_of(Test, size=4)
            d: enum = enum_of(Test, size=8)

        memory = (1).to_bytes(1, "little") + (2).to_bytes(2, "little") + (3).to_bytes(4, "little") + (3).to_bytes(8, "little")

        libdestruct = inflater(memory)

        test = libdestruct.inflate(TestHolder2, 0)

        self.assertEqual(test.a.value, Test.B)
        self.assertEqual(test.b.value, Test.C)
        self.assertEqual(test.c.value, Test.D)
        self.assertEqual(test.d.value, Test.D)

        self.assertEqual(bytes(test), memory)

        with self.assertRaises(ValueError):
            enum_of(Test, size=3)

        with self.assertRaises(ValueError):
            enum_of(Test, size=9)
