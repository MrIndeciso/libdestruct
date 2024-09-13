//
// This file is part of libdestruct (https://github.com/mrindeciso/libdestruct).
// Copyright (c) 2024 Roberto Alessandro Bertolini. All rights reserved.
// Licensed under the MIT license. See LICENSE file in the project root for details.
//

// gcc -o binaries/ctypes_test srcs/ctypes_test.c

#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
#include <math.h>

#pragma pack(push, 1)
struct provola {
    _Bool a;
    unsigned short b;
    char c;
    char *d;
    double e;
    float f;
    int g;
    int16_t h;
    int32_t i;
    int64_t j;
    int8_t k;
    long l;
    long double m;
    long long n;
    short o;
    size_t p;
    time_t r;
    void *s;
    unsigned int t;
    uint16_t u;
    uint32_t v;
    uint64_t w;
    uint8_t x;
    unsigned long y;
    unsigned long long z;
};
#pragma pack(pop)

char NAME[] = "LIBDESTRUCT\0";

void leak(struct provola *ptr)
{

}

void correct()
{

}

int main()
{
    struct provola object;
    object.a = 1;
    object.b = 1337;
    object.c = 23;
    object.d = NAME;
    object.e = 1337.1337;
    object.f = 123.456;
    object.g = 12345;
    object.h = 23456;
    object.i = 0x0eadbeef;
    object.j = 0x0eadbeefdeadbeef;
    object.k = 123;
    object.l = 0xeefd00dbeefd00d;
    object.m = 123456.789;
    object.n = 0xeefdeadbeefdead;
    object.o = 9876;
    object.p = 0xdeadbeefdeadbeef;
    object.r = 0x123456;
    object.s = (void *) 0x1234;
    object.t = 0xdeadbeef;
    object.u = 0x1234;
    object.v = 0xd00dbeef;
    object.w = 0xd00ddeadbeefbeef;
    object.x = 0x46;
    object.y = 0xbeefbeefbeef;
    object.z = 0xd00dd00dd00dd00d;

    leak(&object);

    if (object.a != 0)
        return 0;

    if (object.b != 1234)
        return 0;

    if (object.c != 0x23)
        return 0;

    if (object.e != 1234.5678)
        return 0;

    if (object.f < 234.5 || object.f > 234.6)
        return 0;

    if (object.g != 23456)
        return 0;

    if (object.h != 32767)
        return 0;

    if (object.i != 0xadbeef)
        return 0;

    if (object.j != 0xadbeefdeadbeef)
        return 0;

    if (object.k != 98)
        return 0;

    if (object.l != 0xadbeefd00dbeef)
        return 0;

    if (object.m != 345.678)
        return 0;

    if (object.n != 0xedbeefdeadbeef)
        return 0;

    if (object.o != 8765)
        return 0;

    if (object.p != 0xeadbeefdeadbeef)
        return 0;

    if (object.r != 0x234567)
        return 0;

    if (object.s != (void *) 0x2345)
        return 0;

    if (object.t != 0xeadbeef)
        return 0;

    if (object.u != 0x2345)
        return 0;

    if (object.v != 0xbadbeef)
        return 0;

    if (object.w != 0xbadbeefbadbeef)
        return 0;

    if (object.x != 0x28)
        return 0;

    if (object.y != 0xbadbadbadbad)
        return 0;

    if (object.z != 0xbadd00dbadd00d)
        return 0;

    correct();

    return 0;
}