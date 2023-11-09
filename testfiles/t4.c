
void iterate(int n) {
    int x;

    x = n;
    while (x > 1) {
        x = x - 1;
    }
}

void setpcm(byte x) {
    _LDY #setpcm_x; 
    _LDA (_userstack),Y;
    _JSR setpwm;
    _JSR lowCB2;
    _JSR highCB2;
    println("set:", x);
}

void sleept(int ticks) {
    int a,b,c;

    a = ticks;
    b = a;
    c = a;
    while (a > 0) {
        while (b > 0) {
            while (c > 0) {
                c = c - 1;
            }
            b = b - 1;
        }
        a = a - 1;
    }
}

int main(int argc, char *argv) {
    byte a, b, chars_to_read;
    byte exit;
    char ch, inchar;
    int value;
    ADDRESSPTR p;

    a = 0;
    exit = 0;

    while (exit) {
        chars_to_read = avail();
        if (chars_to_read > 0) {
            inchar = getch();
            if (inchar == 'q') {
                return 1;
            }
            inchar = inchar - 'a';
            setpcm(inchar);
        }
    }
    exit = 1;


    while (exit) {
        chars_to_read = avail();
        if (chars_to_read > 0) {
            inchar = getch();
            if (inchar == '1') {
                _JSR startmeasurement;
                _WAI;
            }
            if (inchar == '2') {
                p = adr(temp_time);
                value = peekword(p);
                println(value);
            }
            if (inchar == 'q') {
                exit = 0;
            } else {
                inchar = inchar - 'a';
                setpcm(inchar);
            }
        } else {
            _JSR startmeasurement;
            sleept(1000);
            p = adr(temp_time);
            value = peekword(p);
            println(value);

        }
    }
    println("Ende");
}
