#include <isnumber.c>
#include <upchar.c>
#include <simplestrtok.c>
#include <findinstrings.c>
#include <convert_to_bin.c>


void dumpfromto(ADDRESSPTR start, ADDRESSPTR end) {
    ADDRESSPTR p, endaddress;
    int index;
    char ch;
    byte b;

    p = start;
    endaddress = end;
    println("\ndump from:", p, " to:", endaddress);
    while (p < endaddress) {
        print(p, ": ");
        index = 0;
        b = peek(p);
        while (index < 16) {
            p = p + 1;
            b = peek(p);
            print(b," ");
            index = index + 1;
        }
        println();
    }
}

int dump_memory(ADDRESSPTR cmd_line) {
    ADDRESSPTR p;
    int result, startaddress, endaddress;
    byte conversionerror;
    // char temp[40];

    conversionerror = 0;
    p = cmd_line;
    p = strtok(p); // skip over "dump" command
    p = strtok(0); // get first argument
    // strcpy(temp, p); 
    startaddress = convert_to_bin(p);
    // println("dump p:", temp, "startaddress:", startaddress);
    if (convert_to_bin_err != 0) {
        conversionerror = conversionerror + 1;
    }
    p = strtok(0);  // get second argument
    // strcpy(temp, p);
    // println("dump p:", temp, "endaddress:", endaddress);
    endaddress = convert_to_bin(p);
    if (convert_to_bin_err != 0) {
        conversionerror = conversionerror + 1;
    }
    if (conversionerror == 0) {
        // println("dump memory from:", startaddress, " to:", endaddress);
        dumpfromto(startaddress, endaddress);
        return 0;
    }
    println("error converting dump addresses, try again")
    return 1;
}



int analyse() {
    ADDRESSPTR p, chptr, tok;
    char ch, space;
    byte do_analyse, ishex;
    int result;
    char checkbuf[20];

    strcpy(search_buf, "dump");
    println()
    result = findincmd();
    if (result >= 0) {
        p = adr(cmd_buf);
        dump_memory(p);
    }
    strcpy(search_buf, "exit");
    result = findincmd();
    if (result >= 0) {
        println("\nexit monitor...\n");
        return 1;
    }
    strcpy(search_buf, "wozmon");
    result = findincmd();
    if (result >= 0) {
        println("\nexit monitor to wozmon...\n");
        _JMP wozmonentrypoint;
    }
    println();
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
    println("\nSTART mon...:");
    strcpy(cmd_buf, "");
    while (retval == 0) {
        chars_to_read = avail();
        if (chars_to_read > 0) {
            inchar = getch();
            if (inchar == 0x3) { // press control c returns to wozmon
                retval = 1;
            }
            if (inchar == 0x0D) {
                // print("do:", cmd_buf);
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