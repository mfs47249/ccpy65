#include <isnumber.c>
#include <upchar.c>
#include <simplestrtok.c>

#include <findinstrings.c>
#include <convert_to_bin.c>
#include <dumpmemory.c>

void help() {
    println("du(mp) from to - dump memory from x to y");
    println("ru(n) start    - run program at start");
    println("up(time)       - show system uptime");
    println("woz(mon)       - start wozmon");
    println("he(lp)         - show this help");
}


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

ADDRESSPTR jumpaddress;
int run_program(ADDRESSPTR cmd_line) {
    ADDRESSPTR p;
    int runaddress;
    byte converr;

    p = cmd_line;
    p = strtok(p); // skip over "run" command
    p = strtok(0); // get first argument

    converr = hex_to_bin_check(p);
    if (converr) {
        println("error converting program start address");
        return 1;
    }
    runaddress = hex_to_bin(p);
    println("\nrun address is:", runaddress);
    jumpaddress = runaddress;
    _JMP (global_jumpaddress);
    return 0;
}

void readbytes(ADDRESSPTR q, byte count) {
    ADDRESSPTR p;
    byte databyte, readcount, zero;

    zero = 0;
    p = q;
    readcount = count;
    while (readcount) {
        databyte = getch();
        if (databyte == 0x20) { // jump over one space
            databyte = getch();
        }
        poke(p, databyte);
        p = p + 1;
        readcount = readcount - 1;
    }
    poke(p,zero);
    return;
}

void communication() {
    ADDRESSPTR p, q, datalength, dataaddress, dataitem, checkptr, address, headerchecksum;
    int length, checksum, index, calcchecksum, errors, header;
    byte databyte, readcount, zero;
    char databuf[16];

    errors = 0;
    zero = 0;
    calcchecksum = 0;
    p = adr(databuf);
    // read length
    readbytes(p, 2);
    length = hex_to_bin(p);
    // read address
    readbytes(p, 4);
    address = hex_to_bin(p);
    // read header-checksum
    readbytes(p, 4);
    header = hex_to_bin(p);
    calcchecksum = length + address;
    // print("checksum:", header, " len:", length, " adr:", address);
    if (calcchecksum == header) {
        index = 0;
        calcchecksum = 0;
        while (index < length) {
            readbytes(p, 2);
            databyte = hex_to_bin(p);
            poke(address, databyte);
            // print("d:",databyte);
            calcchecksum = calcchecksum + databyte;
            index = index + 1;
            address = address + 1;
        }
        // read checksum
        readbytes(p, 4);
        checksum = hex_to_bin(p);
        if (checksum == calcchecksum) {
            println("OK,next: ", address);
            return;
        }
        println("ERR calc:", calcchecksum, " read:", checksum);
    }
    println("ERR head:", header);
}

void process_buffer() {
    ADDRESSPTR p, datalength, dataaddress, dataitem, checkptr, address;
    int length, checksum, index, calcchecksum, headerchecksum, errors;
    byte databyte, converr;

    errors = 0;
    p = adr(cmd_buf);
    datalength = strtok(p); // get length of data from packet
    length = hex_to_bin(datalength);
    calcchecksum = length;
    dataaddress = strtok(0); // get address of data to put
    address = hex_to_bin(dataaddress);
    calcchecksum = calcchecksum + address;
    dataaddress = strtok(0); // get checksum of length + address
    headerchecksum = hex_to_bin(dataaddress);
    if (calcchecksum != headerchecksum) {
        errors = 1;
    }
    if (errors == 0) {
        calcchecksum = 0;
        index = 0;
        while (index < length) {
            dataitem = strtok(0);
            databyte = hex_to_bin(dataitem);
            poke(address, databyte);
            calcchecksum = calcchecksum + databyte;
            address = address + 1;
            index = index + 1;
        }
        checkptr = strtok(0);
        checksum = hex_to_bin(checkptr);
        if (checksum != calcchecksum) {
            errors = errors + 2;
        }
    }
    if (errors > 0) {
        println("calccheck:", calcchecksum, ",err:", errors);
        return;
    }
    println("OK,next:", address);
    //println("len:", length, " adr:", address, " sum:", checksum, " calcsum:", calcchecksum, " errors:", errors);
}

void puttmem() {
    int startaddress, endaddress, timeout;
    byte chars_to_read;
    char inchar;
    // sendpacket = "%02X %04X %s %02X"  length,address,data,checksum

    timeout = 0;
    strcpy(cmd_buf, "");
    while (timeout < 5000) {
        chars_to_read = avail();
        timeout = timeout + 1;  
        if (chars_to_read > 0) {
            inchar = getch();
            if (inchar == 0x2E) { // "." is end of data packet
                process_buffer();
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
    byte do_analyse, ishex, notfound;
    int result;
    char checkbuf[20];

    println();
    notfound = 1;
    if (notfound) {
        strcpy(search_buf, "ru");
        result = findincmd();
        if (result >= 0) {
            p = adr(cmd_buf);
            run_program(p);
            notfound = 0;
        }
    }
    if (notfound) {
        strcpy(search_buf, "du");
        result = findincmd();
        if (result >= 0) {
            p = adr(cmd_buf);
            dump_memory(p);
            notfound = 0;
        }
    }
    if (notfound) {
        strcpy(search_buf, "woz");
        result = findincmd();
        if (result >= 0) {
            println("exit monitor to wozmon...");
            _JMP wozmonentrypoint;
        }
    }
    if (notfound) {
        strcpy(search_buf, "up");
        result = findincmd();
        if (result >= 0) {
            println();
            printuptime(50000);
            notfound = 0;
        }
    }
    if (notfound) {
        strcpy(search_buf, "help");
        result = findincmd();
        if (result >= 0) {
            help();
            println();
            notfound = 0;
        }
    }
    if (notfound) {
        strcpy(search_buf, "exit");
        result = findincmd();
        if (result >= 0) {
            println("exit monitor...");
            return 1;
        }
    }
    strcpy(search_buf, "");
    strcpy(cmd_buf, "");
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

    timerinterval = 50000;
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
                retval = analyse();
                strcpy(cmd_buf, "");

            }
            if (inchar == 0x2A) { // start packet with * Symbol
                puttmem();
                strcpy(cmd_buf, "");
                inchar = 0x0D;
            }
            if (inchar == 0x2B) { // start packet with + Symbol
                communication();
                strcpy(cmd_buf, "");
                inchar = 0x0D;
            }

            if (inchar != 0xD) {
                strcat(cmd_buf, inchar);
                print(inchar);
            }
        }
    }
    return retval;
}