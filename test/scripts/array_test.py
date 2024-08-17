#
# This file is part of libdestruct (https://github.com/mrindeciso/libdestruct).
# Copyright (c) 2024 Roberto Alessandro Bertolini. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

import unittest

from libdebug import debugger
from libdestruct import array, array_of, inflater, c_int, c_long, struct

class ArrayTest(unittest.TestCase):
    def test_linear_arrays_1(self):
        d = debugger("binaries/array_test")

        d.run()

        bp = d.bp("do_nothing")

        d.cont()

        libdestruct = inflater(d.memory)

        assert bp.hit_on(d)

        test1 = libdestruct.inflate(array_of(c_int, 10), d.regs.rdi)

        for i in range(10):
            assert test1[i].value == i ** 2

        d.cont()

        class test2_t(struct):
            a: c_int

        test2 = libdestruct.inflate(array_of(test2_t, 10), d.regs.rdi)

        for i in range(10):
            assert test2[i].a.value == i ** 3

        d.cont()

        class test3_t(struct):
            a: c_int
            b: c_long

        test3 = libdestruct.inflate(array_of(test3_t, 10), d.regs.rdi)

        for i in range(10):
            assert test3[i].a.value == i * 100
            assert test3[i].b.value == i * 1000

        d.cont()

        class test4_t(struct):
            a: c_int
            b: array = array_of(c_int, 10)

        test4 = libdestruct.inflate(array_of(test4_t, 10), d.regs.rdi)

        for i in range(10):
            assert test4[i].a.value == i ** 4
            for j in range(10):
                assert test4[i].b[j].value == (i + 1) * j

        d.kill()
        d.terminate()