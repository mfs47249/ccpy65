
#include <simplestrtok.c>

#include <convert_to_bin.c>


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

int dump_memory(ADDRESSPTR cmd_line) {
    ADDRESSPTR p;
    int result, startaddress, endaddress;
    byte converr;
    // char temp[40];

    p = cmd_line;
    p = strtok(p); // skip over "dump" command
    p = strtok(0); // get first argument, startaddress
    // strcpy(temp, p); 
    converr = hex_to_bin_check(p);
    if (converr) {
        println("error converting start address");
        return 1;
    }
    startaddress = hex_to_bin(p);
    // println("dump p:", temp, "startaddress:", startaddress);
    p = strtok(0);  // get second argument, endaddress
    converr = hex_to_bin_check(p);
    if (converr) {
        println("error converting end address");
        return 1;
    }
    endaddress = hex_to_bin(p);
    // println("dump memory from:", startaddress, " to:", endaddress);
    dumpfromto(startaddress, endaddress);
}

char buffer[128];

int main(int argc, char ADDRESSPTR) {
    ADDRESSPTR b;

    strcpy(buffer, "dump 200 2000");
    b = adr(buffer);
    dump_memory(b);
}