#include <isnumber.c>
#include <upchar.c>
#include <simplestrtok.c>
#include <findinstrings.c>
#include <dumpmemory.c>
#include <convert_to_bin.c>


int dump_memory(ADDRESSPTR cmd_line) {
    ADDRESSPTR p, converr_ptr;
    int result, startaddress, endaddress;
    byte converr;

    p = cmd_line;
    p = strtok(p); // get first argument, startaddress
    converr_ptr = adr(converr);
    startaddress = hex_to_long(p, converr_ptr);
    if (converr) {
        println("error converting start address");
        return 1;
    }
    p = strtok(0);  // get second argument, endaddress
    endaddress = hex_to_long(p, converr_ptr);
    if (converr) {
        println("error converting end address");
        return 1;
    }
    println("dump memory from:", startaddress, " to:", endaddress);
    dumpfromto(startaddress, endaddress);
}

int analyse() {
    ADDRESSPTR p, chptr, tok;
    char ch, space;
    byte do_analyse, ishex;
    int result;
    char checkbuf[20];

    println("cmdbuffer:", cmd_buf);
    dump_memory(cmd_buf);
    println("end dump");
    return 0;
}


int main(int argc, char ADDRESSPTR) {
    int retval, state;
    int chars_to_read;
    byte idx;
    char inchar, ch;
    ADDRESSPTR funcptr;
    longlong timerinterval;

    timerinterval = 10000;
    settimer(timerinterval);
    state = 0;
    retval = 0;
    println("START commandtest...:");
    println("input start address and end address: 100 200 for example")
    strcpy(cmd_buf, "                ");
    while (retval == 0) {
        chars_to_read = avail();
        if (chars_to_read > 0) {
            inchar = getch();
            if (inchar == 0x3) { // press control c returns to wozmon
                retval = 1;
            }
            if (inchar == 0x0D) {
                // print("do:", cmd_buf);
                println(); // do crlf
                retval = analyse();
                strcpy(cmd_buf, "");

            }
            if (inchar != 0xD) {
                strcat(cmd_buf, inchar);
                print(inchar);
            }
        }
    }
    return retval;
}