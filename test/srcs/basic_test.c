//
// This file is part of libdestruct (https://github.com/mrindeciso/libdestruct).
// Copyright (c) 2024 Roberto Alessandro Bertolini. All rights reserved.
// Licensed under the MIT license. See LICENSE file in the project root for details.
//

// gcc -o binaries/basic_test srcs/basic_test.c

#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>

void signpost1()
{

}

void signpost2()
{

}

void signpost3()
{

}

int main()
{
    char *address = mmap((void*) 0xdeadbeef, 0x1000, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);

    if (address == MAP_FAILED) {
        perror("mmap");
        return 1;
    }

    int *provola1 = (int *) (address + 0x000);
    unsigned int *provola2 = (unsigned int *) (address + 0x100);
    long *provola3 = (long *) (address + 0x200);
    unsigned long *provola4 = (unsigned long *) (address + 0x300);

    *provola1 = 1;
    *provola2 = 2;
    *provola3 = 3;
    *provola4 = 4;

    signpost1();

    *provola1 = 0xdeadbeef;
    *provola2 = 0xdeadbeef * 2;
    *provola3 = 0xdeadbeefdeadbeefULL;
    *provola4 = 0xdeadbeefdeadbeefULL * 2;

    signpost2();

    if (*provola1 != 1) {
        printf("provola1 failed\n");
        return 1;
    }

    if (*provola2 != 2) {
        printf("provola2 failed\n");
        return 1;
    }

    if (*provola3 != 3) {
        printf("provola3 failed\n");
        return 1;
    }

    if (*provola4 != 4) {
        printf("provola4 failed\n");
        return 1;
    }

    signpost3();

    return 0;
}
