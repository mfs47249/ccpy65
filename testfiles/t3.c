longlong global_ll_var;

void itoa(longlong num) {
    longlong in, accum, tenpow;
    char n;
    byte prezero;
    longlong u;

    if (num == 0) {
        strcpy(_memarea,"0");
        return;
    }
    tenpow = 1000000000000000000;
    u = num;
    in = 19;
    n = 48; /* Buchstabe '0' */
    prezero = 1;
    strcpy(_memarea, "");
    while (in > 0) {
            n = 48;
            while (u >= tenpow) {
                u = u - tenpow;
                n = n + 1;
            }
            if (n != 48) {
                prezero = 0;
            }
            if (prezero == 0) {
                strcat(_memarea, n);
            }
            tenpow = tenpow / 10;
            in = in - 1;
    }
}

longlong factorial(longlong factor) {
    longlong f;
    longlong a;
    byte *p;

    if (factor == 0) {
        return 1;
    }
    // a = factorial(factor - 1);
    a = factor;
    a = a * factorial(a - 1);
    return a;
}

long getint(wozfloat x) {
    long z;

    z = integer(x);
    return z;
}

wozfloat toreal(long x) {
    wozfloat y;

    y = real(x);
    return y;
}

long toint(wozfloat a) {
    long x;

    x = wozfloat(a);
    return x;
}

long retval(long x) {
    return x;
}


int main (int argc, int *argv) {
    longlong a, zehn;

    wozfloat afloat, bfloat, cfloat, einsfloat, zweifloat, dreifloat, xfloat;
    long aint;
    long bint;
    long testvalue;
    long cint;
    char xfloatstring[20];
    longlong a;
    longlong b;
    longlong c;

    testvalue = 0 + retval(0x111) + retval(0x222);
    a = 1;
    /* while (a < 2) {
        zehn = a;
        while (zehn < 100000000000000000) {
            zehn = zehn * 3;
            itoa(zehn);
            println(_memarea);
        }
        while (zehn > 0) {
            zehn = zehn / 5;
            itoa(zehn);
            println(_memarea);
        }
        a = a + 1;
    } */
    einsfloat = real(1);
    zweifloat = real(2);
    dreifloat = real(3);
    xfloat = real(30);
    afloat = real(200);
    aint = 1;
    println("Int:", aint);
    aint = 0;‚
    xfloat = afloat;
    while (aint < 100) {
        bint = xfloat;
        cint = integer(xfloat);
        itoa(cint);
        strcpy(xfloatstring, _memarea);
        cint = integer(afloat)
        itoa(cint);
        if (1) {
            println("Float in Hex:", bint, " int(afloat):", afloat, " int(afloat):", _memarea, " int_(xfloat):", xfloatstring);
        }
        afloat = afloat - toreal(2);
        dreifloat = toreal(1) + toreal(2);
        println("dreifloat:", dreifloat);
        // afloat = afloat - zweifloat;
        xfloat = afloat / zweifloat;
        bint = 0;
        testvalue = 1 * retval(111) * 1 + retval(222);
        println("testvalue:", testvalue);
        aint = aint + retval(1);
    }
    return 0xfeedc0de;
    aint = integer(afloat);
    itoa(aint);
    println("integer(aint):", _memarea);
    b = 1;
    c = 0;
    while (b < 21) {
        a = c + factorial(b);
        itoa(a);
        println(_memarea);
        b = b + 1;
    }
    return 1;
}
