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
            ci = peek(p);
            if (ci < 0x20) {
                ci = 46;
            }
            if (ci > 127) {
                ci = 46;
            }
            ch = ci;
            print(ch,"");
            index = index + 1;
        }
        println();
        ci = avail();
        if (ci > 0) {
            ch = getch();
            if (ch == 3) {
                // ctrl-c typed, abort
                p = endaddress;
            }
            if (ch == 0x20) {
                // space typed, wait until next char
                ci = 0;
                while (ci == 0) {
                    ci = avail();
                }
                while (ci) {
                    ch = getch();
                    ci = avail();
                }
            }
        }
    }
}
