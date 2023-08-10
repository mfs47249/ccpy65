#include <isnumber.c>
#include <upchar.c>
#include <simplestrtok.c>

#include <findinstrings.c>
#include <convert_to_bin.c>


void printuptime(longlong interval) {
    longlong ticks;
    longlong usec;
    longlong timeval;
    longlong timeinusec;
    longlong time_in_sec;

    timeval = gettimer();
    usec = timeval;
    ticks = timeval;
    and(usec, 0xFFFF);
    shiftright(ticks, 16);
    timeinusec = (ticks * interval) + usec;
    time_in_sec = timeinusec / 1000000;
    println("Uptime time is, in usec:", timeinusec, " in sec:", time_in_sec);
}

void dumpfromto(int start, int end) {
    int startaddress, endaddress;

    startaddress = start;
    endaddress = end;
    println("\ndump from:", startaddress, " to:", endaddress);
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

ADDRESSPTR jumpaddress;
int run_program(ADDRESSPTR cmd_line) {
    ADDRESSPTR p;
    int runaddress;
    byte conversionerror;

    conversionerror = 0;
    p = cmd_line;
    p = strtok(p); // skip over "run" command
    p = strtok(0); // get first argument
    runaddress = convert_to_bin(p);
    if (convert_to_bin_err == 0) {
        println("\nrun address is:", runaddress);
        jumpaddress = runaddress;
        _JMP (global_jumpaddress);
        return 0;
    }
    println("error converting start address of program, try again");
    return 1;
}

void process_buffer() {
    ADDRESSPTR p, datalength, dataaddress, dataitem, checkptr, address;
    int length, checksum, index, calcchecksum, errors;
    byte databyte;

    errors = 0;
    calcchecksum = 0;
    p = adr(cmd_buf);
    datalength = strtok(p); // get length of data from packet
    length = convert_to_bin(datalength);
    if (convert_to_bin_err != 0) {
        errors = errors + 64;
        println("lenerr");
    }
    dataaddress = strtok(0); // get address of data to put
    address = convert_to_bin(dataaddress);
    if (convert_to_bin_err != 0) {
        errors = errors + 128;
        println("adrerr");
    }
    if (errors == 0) {
        index = 0;
        while (index < length) {
            dataitem = strtok(0);
            databyte = convert_to_bin(dataitem);
            if (convert_to_bin_err != 0) {
                errors = errors + 1;
                index = length; // end while loop
            }
            if (convert_to_bin_err == 0) {
                poke(address, databyte);
                calcchecksum = calcchecksum + databyte;
                // print(databyte);
            }
            address = address + 1;
            index = index + 1;
        }
        checkptr = strtok(0);
        checksum = convert_to_bin(checkptr);
        if (convert_to_bin_err != 0) {
            errors = errors + 256;
        }
        if (checksum != calcchecksum) {
            errors = errors + 512;
        }
    }
    if (errors > 0) {
        println("errorcode:", errors);
        return;
    }
    println("OK,next:", address);
    //println("len:", length, " adr:", address, " sum:", checksum, " calcsum:", calcchecksum, " errors:", errors);
}

void puttomem() {
    int startaddress, endaddress;
    byte endofdata, chars_to_read;
    char inchar;
    // sendpacket = "%02X %04X %s %02X"  length,address,data,checksum

    endofdata = 0;
    strcpy(cmd_buf, "");
    while (endofdata == 0) {
        chars_to_read = avail();
        if (chars_to_read > 0) {
            inchar = getch();
            if (inchar == 0x2E) { // "." is end of data packet
                process_buffer();
                strcpy(cmd_buf, "");
                return;
            }
            if (inchar != 0x2E) {
                strcat(cmd_buf, inchar);
            }
        }  
    } 
}

int analyse() {
    ADDRESSPTR p, chptr, tok;
    char ch, space;
    byte do_analyse, ishex;
    int result;
    char checkbuf[20];

    strcpy(search_buf, "run");
    println();
    result = findincmd();
    if (result >= 0) {
        p = adr(cmd_buf);
        run_program(p);
    }
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
    strcpy(search_buf, "uptime");
    println();
    result = findincmd();
    if (result >= 0) {
        printuptime(10000);
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
            if (inchar == 0x2A) { // start packet with * Symbol
                // print("do:", cmd_buf);
                puttomem();
                strcpy(cmd_buf, "");
                inchar == 0xD;
            }
            if (inchar != 0xD) {
                strcat(cmd_buf, inchar);
                print(inchar);
            }
        }
    }
    return retval;
}