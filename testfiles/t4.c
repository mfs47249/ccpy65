
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

void sleept(long ticks) {
    byte t;

    t = ticks;
    while (t > 0) {
        _WAI;
        t = t - 1;
    }
}

int main(int argc, char *argv) {
    byte a, b, chars_to_read;
    byte exit;
    char ch, inchar;

    a = 0;
    exit = 1;

    while (exit) {
        chars_to_read = avail();
        if (chars_to_read > 0) {
            inchar = getch();
            if (inchar == '1') {
                _JSR stopmeasurement;
                _WAI;
            }
            if (inchar == '2') {
                _JSR startmeasurement;
                _WAI;
            }
            if (inchar == 'q') {
                exit = 0;
            } else {
                inchar = inchar - 'a';
                // setpcm(inchar);
            }
        } else {
            _JSR stopmeasurement;
            sleept(100);
            _JSR startmeasurement;
            sleept(100);
        }
    }
    println("Ende");
}
