#include <dumpmemory.c>

char manychars[512];
char tempchars[512];

int main(int argc, ADDRESSPTR argv)  { 
    char chars;
    byte done;
    int c1;
    ADDRESSPTR start, end;

    c1 = 4;
    strcpy(manychars, "");
    while (c1 > 0) {
        chars = 'A';
        while (chars =< 'Z') {
            strcat(manychars, chars);
            chars = chars + 1;
        }
        chars = 'a';
        while (chars =< 'z') {
            strcat(manychars, chars);
            chars = chars + 1;
        }
        chars = '0';
        while (chars =< '9') {
            strcat(manychars, chars);
            chars = chars + 1;
        }
        c1 = c1 - 1;
    }

    c1 = strlen(manychars);
    println("Stringlength:", c1);

    done = 1;
    while (done) {
        start = 0x8000;
        end = 0xB000;
        dumpfromto(start, end);
        chars = avail();
        if (chars > 0) {
            chars = getch();
            if (chars == 3) {
                done = 0;
            }
        }
        done = 0;
    }


    done = 1;
    while (done) {
        println(manychars);
        chars = avail();
        if (chars > 0) {
            chars = getch();
            if (chars == 3) {
                done = 0;
            }
        }
    }


    _JSR $8000;
}