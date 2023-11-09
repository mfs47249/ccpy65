#include <factorial.c>
#include <printsubtable.c>

void checkabort() {
    char ch;
    int count;

    count = avail();
    if (count > 0) {
        ch = getch();
        if (ch == 'q') {
            _JMP 0x8000;
        }
    }
}


long main(int argc, ADDRESSPTR argv) {
    ADDRESSPTR s, t, p, f1, f2;
    long i, max, sum;

    println("Calculating 100 x");
    f1 = adr("programstart");
    f2 = adr("kima_konst");
    max = 10000;
    i = 0;
    while (i < max) {
        p = f1;
        sum = 0;
        while (p < f2) {
            sum = sum + peek(p);
            p = p + 1;
        }
        // println("i:", i, " f1:", f1, " f2:", f2, " sum:", sum);
        p = adr("lcd_update_seconds");
        // s = getintataddress(p);
        t = peekword(p);
        println("getintaddress:", s, " peekword:", t);
        i = i + 1;
        printsubtable();
        checkabort();
    }
}