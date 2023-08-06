
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

void wozlogconst() {
    long l2e, a2, b2, c2, d;
    wozfloat l2e_f, a2_f, b2_f, c2_f, d_f;

    l2e = 0x1E555C80;
    a2 = 0xE16A5786;
    b2 = 0x1D3F4D89;
    c2 = 0x70FA467B;
    d = 0x03A34F83;
    l2e_f = l2e;
    a2_f = a2;
    b2_f = b2;
    c2_f = c2;
    d_f = d;
    l2e_f = l2e_f * real(1000);
    a2_f = a2_f * real(100);
    b2_f = b2_f * real(10);
    c2_f = c2_f * real(10000);
    d_f = d_f * real(1000);
    l2e = integer(l2e_f);
    itoa(l2e);
    println("L2E:", l2e_f, " dec/1000:", _memarea);
    a2 = integer(a2_f);
    itoa(a2);
    println("a2:", a2_f, " dec:/100 :", _memarea);
    b2 = integer(b2_f);
    itoa(b2);
    println("b2:", b2_f, " dec:/10  :", _memarea);
    c2 = integer(c2_f);
    itoa(c2);
    println("c2:", c2_f, " dec:/1000:", _memarea);
    d = integer(d_f);
    itoa(d);
    println("d:", d_f, " dec:/1000:", _memarea);
}

/*
        #self.emit.createcode("DCM","1.4426950409","LOG BASE 2 OF E",name="wozL2E")
        #self.emit.createcode("DCM","87.417497202",name="wozA2")
        #self.emit.createcode("DCM","617.9722695",name="wozB2")
        #self.emit.createcode("DCM",".03465735903",name="wozC2")
        #self.emit.createcode("DCM","9.9545957821",name="wozD")
*/


int main(int argc, ADDRESSPTR argv) {
    wozfloat a, b, c, d, ex;
    longlong ia, ib, ic;
    longlong x, y, z;
    byte e;
    long m;

    ic = 1000000;
    ia = 1;
    wozlogconst();
    while (/* ia < ic */ 0) {
        a = real(ia);
        c = log(a) * real(1);
        e = wozexponent(a);
        m = wozmantissa(a);
        itoa(ia);
        print("e:", e " ",m , "  a:", a, " a(d):", _memarea);
        // ex = 0x1E555C80 * real(1000); 
        ex = exp(c);
        ib = integer(ex);
        itoa(ib);
        println(" ib:", ib, " log(a):", _memarea);
        ia = ia * 2;
    }
    ic = 1000000;
    ia = 1;
    a = real(1);
    while (ia < ic) {
        a = real(ia);
        e = wozexponent(a);
        m = wozmantissa(a);
        itoa(ia);
        print("e:", e " ",m , "  a:", ia, " a(d):", _memarea);
        // ex = 0x1E555C80 * real(1000); 
        a = a * real(2);
        ia = ia * 2;
    }
    ia = integer(a);
    println(ia);
    return integer(a);
}

