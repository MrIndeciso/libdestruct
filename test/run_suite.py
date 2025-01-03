#
# This file is part of libdestruct (https://github.com/mrindeciso/libdestruct).
# Copyright (c) 2024 Roberto Alessandro Bertolini. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

import sys

from unittest import TestSuite, TextTestRunner, TestLoader

from scripts.array_test import ArrayTest
from scripts.basic_test import BasicTest
from scripts.basic_struct_test import BasicStructTest
from scripts.ctypes_test import CtypesTest
from scripts.enum_test import EnumTest
from scripts.string_test import StringTest

def test_suite():
    suite = TestSuite()

    suite.addTest(TestLoader().loadTestsFromTestCase(ArrayTest))
    suite.addTest(TestLoader().loadTestsFromTestCase(BasicTest))
    suite.addTest(TestLoader().loadTestsFromTestCase(BasicStructTest))
    suite.addTest(TestLoader().loadTestsFromTestCase(CtypesTest))
    suite.addTest(TestLoader().loadTestsFromTestCase(EnumTest))
    suite.addTest(TestLoader().loadTestsFromTestCase(StringTest))

    return suite

if __name__ == '__main__':
    if sys.version_info >= (3, 12):
        runner = TextTestRunner(verbosity=2, durations=3)
    else:
        runner = TextTestRunner(verbosity=2)

    runner.run(test_suite())
