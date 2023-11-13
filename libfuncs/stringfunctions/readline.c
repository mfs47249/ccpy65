
int readline(ADDRESSPTR buf, int max) {
    ADDRESSPTR p;
    int charsread, count;
    char in;

    charsread = 0;
    p = buf;
    while (1) {
        count = avail();
        if (count > 0) {
            in = getch();
            if (in == 3) {   // control c to abort
                return -1;
            }
            if (charsread >= max) {
                return charsread;
            }
            if (in == 13) {  // ch is carriage return
                poke(p, 0);
                return charsread;
            } else {
                poke(p, in);
                print(in);
                charsread = charsread + 1;
                p = p + 1;
            }
        }
    }
}
