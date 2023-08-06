void itoa(longlong num) {
    longlong in, tenpow;
    char n;
    byte prezero;
    longlong u;

    if (num == 0) {
        strcpy(_memarea,"0");
        return;
    }
    if (num < 0) {
        strcpy(_memarea,"negative");
        return;
    }
    tenpow = 1000000000000000000;
    u = num;
    in = 19;
    n = 48; /* ASCII Letter '0' */
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

void itoatest () {
    longlong x,y;

    x = 20;
    while (x > 0) {
        y = 10 - x;
        itoa(y);
        println("y:", y, "  itoa(y):", _memarea);
        x = x - 1;
    }
}
