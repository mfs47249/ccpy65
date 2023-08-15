
#include <simplestrtok.c>


char strtocdemo[512];

int main(int argc, ADDRESSPTR argv)  { 
    int bcount;
    char ch;
    ADDRESSPTR p;
    char buf[65];

    strcpy(strtocdemo, "");
    ch = 0x20;
    while (ch != 3) {
        bcount = avail();
        if (bcount > 0) {
            ch = getch();
            print(ch);
            if (ch == 3) {
                _JMP $8000;
            }
            strcat(strtocdemo, ch);
            if (ch == 13) {
                println("buf:", strtocdemo);
                p = adr(strtocdemo);
                p = strtok(p);
                while (p != 0) {
                    strcpy(buf, p);
                    println("tok:", p, "val:", buf);
                    p = strtok(0);
                }
                strcpy(strtocdemo,"");
            }
       }
    }
}