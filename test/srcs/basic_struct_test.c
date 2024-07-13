//
// This file is part of libdestruct (https://github.com/mrindeciso/libdestruct).
// Copyright (c) 2024 Roberto Alessandro Bertolini. All rights reserved.
// Licensed under the MIT license. See LICENSE file in the project root for details.
//

// gcc -o binaries/struct_test srcs/struct_test.c

#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>

struct test1 {
    int a;
    unsigned int b;
    long c;
    unsigned long d;
};

struct test2 {
    unsigned long b;
    struct test2 *next;
};

struct test3 {
    int a;
    struct test4 {
        int x;
        int y;
    } b;
};

__attribute__((packed))
struct test5 {
    int a;
    struct test6 {
        unsigned long x;
        struct test7 {
            int y;
            unsigned long z;
        } z;
    } b;
};

struct test8 {
    struct test5 *a;
    struct test3 b;
};

void signpost1(void *address)
{

}

void signpost2()
{

}

void signpost3(void *address)
{

}

void signpost4()
{

}

void signpost5()
{

}

void signpost6(void *address)
{

}

void signpost7(void *address)
{

}

void signpost8()
{

}

void signpost9()
{

}

void check()
{

}

int main()
{
    struct test1 *ptr = malloc(sizeof(struct test1));

    ptr->a = 1;
    ptr->b = 2;
    ptr->c = 3;
    ptr->d = 4;

    signpost1(ptr);

    if (ptr->a != 0x7eadbeef) {
        check();
    }

    if (ptr->b != 0xbeefdead) {
        check();
    }

    if (ptr->c != 0x7eadbeefdeadbeefULL) {
        check();
    }

    if (ptr->d != 0xbeefdeadbeefdeadULL) {
        check();
    }

    ptr->a = 0xeadbeef;
    ptr->b = 0xdeadbeef;
    ptr->c = 0xeadbeefdeadbeefULL;
    ptr->d = 0xdeadbeefdeadbeefULL;

    signpost2();

    free(ptr);

    struct test2 *ptr2 = malloc(sizeof(struct test2));
    struct test2 *head = ptr2;

    for (int i = 0; i < 10; i++) {
        ptr2->b = i;
        ptr2->next = malloc(sizeof(struct test2));
        ptr2 = ptr2->next;
    }

    ptr2->b = 10;

    signpost3(head);

    for (int i = 0; i < 11; i++) {
        struct test2 *tmp = head;
        head = head->next;
        free(tmp);
    }

    struct test3 prova = {};
    prova.a = 1;
    prova.b.x = 2;
    prova.b.y = 3;

    signpost4(&prova);

    if (prova.a != 0x7eadbeef) {
        check();
    }

    if (prova.b.x != 0x12345678) {
        check();
    }

    if (prova.b.y != 0x23456789) {
        check();
    }

    signpost5();

    struct test5 *ptr3 = malloc(sizeof(struct test8));

    ptr3->a = 0x7eadbeef;
    ptr3->b.x = 0x1234567801234567;
    ptr3->b.z.y = 0x23456789;
    ptr3->b.z.z = 0x3456789034567890;

    signpost6(ptr3);

    free(ptr3);

    struct test8 *ptr4 = malloc(sizeof(struct test8));

    ptr4->a = malloc(sizeof(struct test5));
    ptr4->a->a = 0x5eadbeef;
    ptr4->a->b.x = 0x2345678012345671;
    ptr4->a->b.z.y = 0x12345678;
    ptr4->a->b.z.z = 0x2345678903456789;
    ptr4->b.a = 0x7eadbeef;
    ptr4->b.b.x = 0x12345678;
    ptr4->b.b.y = 0x23456789;

    signpost7(ptr4);

    if (ptr4->a->a != 0x7eadbeef) {
        check();
    }

    if (ptr4->a->b.x != 0x1234567801234567) {
        check();
    }

    if (ptr4->a->b.z.y != 0x23456789) {
        check();
    }

    if (ptr4->a->b.z.z != 0x3456789034567890) {
        check();
    }

    if (ptr4->b.a != 0x5eadbeef) {
        check();
    }

    if (ptr4->b.b.x != 0x23456789) {
        check();
    }

    if (ptr4->b.b.y != 0x12345678) {
        check();
    }

    free(ptr4->a);

    signpost8();

    if (ptr4->a != (void*) 0x1234) {
        check();
    }

    signpost9();

    free(ptr4);

    return 0;
}
