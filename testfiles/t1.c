


int test(int x, int y) {
    int t;

    t = test(x);
    return x+y;
}


int testroutine(int number) {
    int a, b, c;

    a = 100 * b / c + 10 - number - test(b,c);
    a = 100 * b / c + 10 - number;
}



int itoa(longlong num) {
    longlong in, accum, tenpow;
    char n;
    byte prezero;
    longlong u;

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

    println("Factor:", factor);
    if (factor == 0) {
        return 1;
    }
    a = factorial(factor - 1);
    a = factor * a;
    return a;
}

int main(int argc, ADDRESSPTR argv)  { 
    longlong facresult;
    longlong counter;
    longlong decimal;

    counter = 0;
    while (counter < 21) {
        facresult = factorial(counter);
        print("fac():", counter, " is:");
        itoa(facresult);
        println(_memarea);
        counter = counter + 1;
    }
    decimal = 10;
    decimal = 100 + factorial(decimal);
    println("counter:", counter);

    return 0xFEEDC0DE;
}
