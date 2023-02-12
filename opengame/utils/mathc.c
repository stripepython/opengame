/*
Library written in C language.
Used to accelerate and replace functions that Python cannot implement.

Compile: gcc -shared -o mathc.dll mathc.c
In Linux: gcc mathc.c -shared -fPIC -o mathc.so
*/

#include <stdint.h>

float InvSqrt(float n) {
    uint32_t i;
    float x2, y;
    x2 = n * 0.5F;
    y = n;
    i = *(uint32_t *) &y;
    //i = 0x5f3759df - (i >> 1);
    i = 0x5f375a86 - (i >> 1);
    y = *(float *) &i;
    y = y * (1.5F - (x2 * y * y));
    return y;
}

int IntegerLog2(int val) {
    int res = 0;
    while ((val >>= 1) != 0) {
        res++;
    }
    return res;
}
