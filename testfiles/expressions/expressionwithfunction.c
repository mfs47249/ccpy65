long getx(long x) {
    long a;

    a = x;
    return a;
}

long retval(long parameter) {
    long x;

    x = parameter;
    x = getx(x);
    return x;
}

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
    longlong eins;

    eins = 1;
    if (factor == 0) {
        return eins;
    }
    a = factor;
    a = a * factorial(a - 1);
    return a;
}


int main(int argc, ADDRESSPTR argv) {
    long b, c;
    longlong fac;
    longlong a;

    b = retval(111); println("b:", b);
    c = retval(222); println("c:", c);
    a = 0 + retval(b) + retval(c);
    println("a, from plus operation is:", a);
    a = retval(b) + retval(c);
    println("a, from plus operation is:", a);
    a = 1 + 2 + (b * 3) + retval(1) + retval(1) + retval(1) + retval(1) + retval(1) + retval(1) + retval(1) + retval(1);
    itoa(a);
    println("a from special calc:", a, "  ", _memarea);
    a = 0;
    while (a < 21) {
        fac = factorial(a);
        itoa(fac);
        println("a:", _memarea);
        a = a + 1;‚
    }
    return a;
}