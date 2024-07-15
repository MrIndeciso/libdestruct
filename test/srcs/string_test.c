//
// This file is part of libdestruct (https://github.com/mrindeciso/libdestruct).
// Copyright (c) 2024 Roberto Alessandro Bertolini. All rights reserved.
// Licensed under the MIT license. See LICENSE file in the project root for details.
//

// gcc -o binaries/string_test srcs/string_test.c

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>

void signpost1(char *address)
{

}

void signpost2()
{

}

void check()
{

}

int main()
{
    char test_string[] = "Hello, world!\0";

    signpost1(test_string);

    if (strcmp(test_string, "Hello, WORLD!") != 0) {
        check();
    }

    test_string[6] = '\0';

    signpost2();

    if (strcmp(test_string, ", world!") != 0) {
        check();
    }

    return 0;
}