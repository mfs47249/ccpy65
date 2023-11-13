#include <factorial.c>
#include <printsubtable.c>
#include <strcmp.c>
#include <readline.c>
#include <simplestrtok.c>

void checkabort() {
    char ch;
    int count;

    count = avail();
    if (count > 0) {
        ch = getch();
        if (ch == 3) {  // control-c aborts
            _JMP 0x8000;
        }
    }
}


int checkcommand(ADDRESSPTR cmd) {
    ADDRESSPTR p, q, cmdptr;
    int n, match;
    byte f;
    char cmd_list[80];


    strcpy(cmd_list, "dump set prtab run sub uptime wozmon ntemp gtemp clear help");
    p = adr(cmd_list);
    cmdptr = strtok(p); // get first command from list
    q = cmd;
    n = 0;
    f = 1;
    checkcommandloop:
        match = strcmp(p,q);
        if (match == 0) {
            return n;
        }
        n = n + 1;
        p = strtok(0);
        if (p == 0) {
            return -1;
        }
    goto checkcommandloop:
}

char buffer[100];
char teststr[10];

long main(int argc, ADDRESSPTR argv) {
    ADDRESSPTR s, t, p, f1, f2, bufptr, testptr;
    long i, max, sum;
    int numcharsread, index;

    bufptr = adr(buffer);
    i = 0;
    max = 100;
    testptr = adr(teststr);
    strcpy(teststr, "test");
    while (i < max) {
        numcharsread = readline(bufptr, 100);
        if (numcharsread == -1) {
            return numcharsread;
        }
        index = checkcommand(bufptr);
        switch (index) {
                case 1: {
                    i = i + 1;
                    println("case is 1");
                }
                break;
                case 2: {
                    i = i - 1;
                    println("case is 2");
                }
                break;
                case 5: {
                    i = i - 1;
                    println("case is 5");
                }
                break;
        }
        println();
        println("index:", index, " buffer:", buffer);
        i = i + 1;
    }
}