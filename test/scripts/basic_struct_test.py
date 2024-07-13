#
# This file is part of libdestruct (https://github.com/mrindeciso/libdestruct).
# Copyright (c) 2024 Roberto Alessandro Bertolini. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

import unittest

from libdebug import debugger
from libdestruct import inflater, c_int, c_long, c_uint, c_ulong, struct, ptr, ptr_to, ptr_to_self

class BasicStructTest(unittest.TestCase):
    def test_simple_struct(self):
        d = debugger("binaries/basic_struct_test")

        def empty_callback(_, __):
            pass

        d.run()
        bp1 = d.bp("signpost1")
        bp2 = d.bp("signpost2")
        check = d.bp("check", callback=empty_callback)
        d.cont()

        assert bp1.hit_on(d)

        libdestruct = inflater(d.memory)

        ptr = d.regs.rdi

        class test1(struct):
            a: c_int
            b: c_uint
            c: c_long
            d: c_ulong

        test = libdestruct.inflate(test1, ptr)

        self.assertEqual(test.a.get(), 0x1)
        self.assertEqual(test.b.get(), 0x2)
        self.assertEqual(test.c.get(), 0x3)
        self.assertEqual(test.d.get(), 0x4)

        test.a.value = 0x7eadbeef
        test.b.value = 0xbeefdead
        test.c.value = 0x7eadbeefdeadbeef
        test.d.value = 0xbeefdeadbeefdead

        d.cont()

        assert bp2.hit_on(d)

        self.assertEqual(test.a.value, 0xeadbeef)
        self.assertEqual(test.b.value, 0xdeadbeef)
        self.assertEqual(test.c.value, 0xeadbeefdeadbeef)
        self.assertEqual(test.d.value, 0xdeadbeefdeadbeef)

        d.kill()

        self.assertEqual(check.hit_count, 0)

        d.terminate()

    def test_linked_list_struct(self):
        d = debugger("binaries/basic_struct_test")

        d.run()

        bp = d.bp("signpost3")

        d.cont()

        assert bp.hit_on(d)

        class test2(struct):
            b: c_long
            next: ptr = ptr_to_self()

        libdestruct = inflater(d.memory)

        test_ptr = d.regs.rdi

        test = libdestruct.inflate(test2, test_ptr)

        for i in range(0, 11):
            self.assertEqual(test.b.value, i)
            test = test.next.unwrap()

        d.kill()
        d.terminate()

    def test_nested_struct(self):
        d = debugger("binaries/basic_struct_test")

        def empty_callback(_, __):
            pass

        d.run()

        bp1 = d.bp("signpost4")
        check = d.bp("check", hardware=True, callback=empty_callback)
        bp2 = d.bp("signpost5")

        check.disable()

        d.cont()

        assert bp1.hit_on(d)

        check.enable()

        libdestruct = inflater(d.memory)

        struct_ptr = d.regs.rdi

        class test4(struct):
            x: c_int
            y: c_int

        class test3(struct):
            a: c_int
            b: test4

        test = libdestruct.inflate(test3, struct_ptr)

        self.assertEqual(test.a.value, 0x1)
        self.assertEqual(test.b.x.value, 0x2)
        self.assertEqual(test.b.y.value, 0x3)

        test.a.value = 0x7eadbeef
        test.b.x.value = 0x12345678
        test.b.y.value = 0x23456789

        d.cont()

        assert bp2.hit_on(d)

        self.assertEqual(check.hit_count, 0)

        d.kill()
        d.terminate()

    def test_nested_structs_2(self):
        d = debugger("binaries/basic_struct_test")

        d.run()

        bp = d.bp("signpost6")

        d.cont()

        assert bp.hit_on(d)

        libdestruct = inflater(d.memory)

        struct_ptr = d.regs.rdi

        class test7(struct):
            y: c_int
            _: c_int # Padding
            z: c_ulong

        class test6(struct):
            x: c_ulong
            z: test7

        class test5(struct):
            a: c_int
            _: c_int # Padding
            b: test6

        test = libdestruct.inflate(test5, struct_ptr)

        self.assertEqual(test.a.value, 0x7eadbeef)
        self.assertEqual(test.b.x.value, 0x1234567801234567)
        self.assertEqual(test.b.z.y.value, 0x23456789)
        self.assertEqual(test.b.z.z.value, 0x3456789034567890)

        d.kill()
        d.terminate()

    def test_struct_ptr(self):
        d = debugger("binaries/basic_struct_test")

        def empty_callback(_, __):
            pass

        d.run()

        bp1 = d.bp("signpost7")
        check = d.bp("check", hardware=True, callback=empty_callback)
        bp2 = d.bp("signpost8")
        bp3 = d.bp("signpost9")

        check.disable()

        d.cont()

        assert bp1.hit_on(d)

        check.enable()

        class test7(struct):
            y: c_int
            _: c_int # Padding
            z: c_ulong

        class test6(struct):
            x: c_ulong
            z: test7

        class test5(struct):
            a: c_int
            _: c_int # Padding
            b: test6

        class test4(struct):
            x: c_int
            y: c_int

        class test3(struct):
            a: c_int
            b: test4

        class test8(struct):
            a: ptr = ptr_to(test5)
            b: test3

        libdestruct = inflater(d.memory)

        struct_ptr = d.regs.rdi

        test = libdestruct.inflate(test8, struct_ptr)

        self.assertEqual(test.a.unwrap().a.value, 0x5eadbeef)
        self.assertEqual(test.a.unwrap().b.x.value, 0x2345678012345671)
        self.assertEqual(test.a.unwrap().b.z.y.value, 0x12345678)
        self.assertEqual(test.a.unwrap().b.z.z.value, 0x2345678903456789)
        self.assertEqual(test.b.a.value, 0x7eadbeef)
        self.assertEqual(test.b.b.x.value, 0x12345678)
        self.assertEqual(test.b.b.y.value, 0x23456789)

        test.a.unwrap().a.value = 0x7eadbeef
        test.a.unwrap().b.x.value = 0x1234567801234567
        test.a.unwrap().b.z.y.value = 0x23456789
        test.a.unwrap().b.z.z.value = 0x3456789034567890
        test.b.a.value = 0x5eadbeef
        test.b.b.x.value = 0x23456789
        test.b.b.y.value = 0x12345678

        d.cont()

        assert bp2.hit_on(d)

        self.assertEqual(check.hit_count, 0)

        test.a.set(0x1234)

        d.cont()

        assert bp3.hit_on(d)

        self.assertEqual(test.a.value, 0x1234)
        self.assertEqual(check.hit_count, 0)

        d.kill()
        d.terminate()
