#
# This file is part of libdestruct (https://github.com/mrindeciso/libdestruct).
# Copyright (c) 2024 Roberto Alessandro Bertolini. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

import unittest

from libdebug import debugger
from libdestruct import inflater, c_int, c_long, c_uint, c_ulong

class BasicTest(unittest.TestCase):
    def test_basic_types(self):
        d = debugger("binaries/basic_test")

        d.run()

        # Validate readings
        bp1 = d.bp(0x4011fd)

        # Validate assignments
        bp2 = d.bp(0x401272)

        libdestruct = inflater(d.memory)

        d.cont()

        assert bp1.hit_on(d)

        def twos_complement(value, bits):
            if value & (1 << bits - 1):
                return value - (1 << bits)
            return value

        provola1 = libdestruct.inflate(c_int, 0xdeadb000)
        provola2 = libdestruct.inflate(c_uint, 0xdeadb000 + 0x100)
        provola3 = libdestruct.inflate(c_long, 0xdeadb000 + 0x200)
        provola4 = libdestruct.inflate(c_ulong, 0xdeadb000 + 0x300)

        self.assertEqual(provola1.get(), twos_complement(0xdeadbeef, 32))
        self.assertEqual(provola2.value, (0xdeadbeef * 2) & ((1 << 32) - 1))
        self.assertEqual(provola3.get(), twos_complement(0xdeadbeefdeadbeef, 64))
        self.assertEqual(provola4.get(), (0xdeadbeefdeadbeef * 2) & ((1 << 64) - 1))

        provola1.set(0x1)
        provola2.set(0x2)
        provola3.value = 0x3
        provola4.set(0x4)

        d.cont()

        assert bp2.hit_on(d)

        d.kill()
