void dumpfromto(ADDRESSPTR start, ADDRESSPTR end) {
    ADDRESSPTR p, q, endaddress;
    int index, ci;
    char ch;
    byte b;

    p = start;
    endaddress = end;
    while (p < endaddress) {
        q = p;
        print(q, ": ");
        index = 0;
        b = peek(q);
        while (index < 8) {
            q = q + 1;
            b = peek(q);
            print(b," ");
            index = index + 1;
        }
        print(" ");
        index = 0;
        b = peek(p);
        while (index < 8) {
            p = p + 1;
            ch = peek(p);
            if (ch < ' ') {
                ch = '.';
            }
            if (ch > 127) {
                ch = '.';
            }
            print(ch);
            index = index + 1;
        }
        println();
        ci = avail();
        if (ci > 0) {
            ch = getch();
            if (ch == ' ') {
                // space typed, wait until next char
                ci = 0;
                while (ci == 0) {
                    ci = avail();
                }
                while (ci) {
                    ch = getch();
                    if (ch == 'q') {
                        return;
                    }
                    ci = avail();
                }
            }
        }
    }
}
