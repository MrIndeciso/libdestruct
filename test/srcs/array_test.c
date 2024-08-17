//
// This file is part of libdestruct (https://github.com/mrindeciso/libdestruct).
// Copyright (c) 2024 Roberto Alessandro Bertolini. All rights reserved.
// Licensed under the MIT license. See LICENSE file in the project root for details.
//

// gcc -o binaries/array_test srcs/array_test.c

#include <stdlib.h>

#pragma pack(push, 1)
int test1[10];

struct test2 {
    int a;
};

struct test2 test2[10];

struct test3 {
    int a;
    long b;
};

struct test3 test3[10];

struct test4 {
    int a;
    int b[10];
};

struct test4 test4[10];
#pragma pack(pop)

void do_nothing(void* addr)
{

}

int main()
{
    for (int i = 0; i < 10; i++)
        test1[i] = i * i;

    for (int i = 0; i < 10; i++)
        test2[i].a = i * i * i;

    for (int i = 0; i < 10; i++) {
        test3[i].a = 100 * i;
        test3[i].b = 1000 * i;
    }

    for (int i = 0; i < 10; i++) {
        test4[i].a = i * i * i * i;
        for (int j = 0; j < 10; j++)
            test4[i].b[j] = (i + 1) * j;
    }

    do_nothing(test1);
    do_nothing(test2);
    do_nothing(test3);
    do_nothing(test4); 

    return 0;
}