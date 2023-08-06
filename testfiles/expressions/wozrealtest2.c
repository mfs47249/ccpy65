#include <itoa.c>

int wozexponent(wozfloat x) {
    byte exponent;

    _LDY #wozexponent_x;
    _LDA (_userstack),Y;
    _LDY #wozexponent_exponent;
    _STA (_userstack),Y;
    return exponent;
}

long wozmantissa(wozfloat x) {
    long m;

    m = x;
    shiftright(m,8);
    return m;
}


int main(int argc, ADDRESSPTR argv) {
    wozfloat a, b, c, d, ex;
    long ia, ib, ic;
    long x, y, z, e1, m1;
    byte e;
    char buffer[20];
    long m;

    x = 1;
    a = real(1);
    while (x < 1000 * 4000) {
        e1 = wozexponent(a);
        m1 = wozmantissa(a);
        itoa(m1);
        strcpy(buffer,_memarea);
        itoa(x);
        println("a: exponent:", e1, " mantissa(hex):", m1, " mantissa(dec):", buffer, " d(a):", _memarea);
        a = a * real(2);
        x = x * 2;
    }
}