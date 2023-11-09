// #include <isnumber.c>
// #include <upchar.c>
#include <simplestrtok.c>

#include <findinstrings.c>
#include <convert_to_bin.c>
#include <dumpmemory.c>
#include <printsubtable.c>
// #include <factorial.c>

int dump_memory(ADDRESSPTR cmd_line) {
    ADDRESSPTR p, q, converr_ptr;
    int result, startaddress, endaddress;
    byte converr;

    p = cmd_line;
    p = strtok(p); // skip over "dump" command
    p = strtok(0); // get first argument, startaddress
    converr_ptr = adr(converr);
    startaddress = hex_to_long(p, converr_ptr);
    if (converr) {
        println("error converting start address");
        return 1;
    }
    q = strtok(0);  // get second argument, endaddress
    endaddress = hex_to_long(q, converr_ptr);
    if (converr) {
        println("error converting end address");
        return 1;
    }
    if (q == 0) {
        endaddress = startaddress + 0x80;
    }
    dumpfromto(startaddress, endaddress);
}
/*
ADDRESSPTR jumpaddress;
int run_program(ADDRESSPTR cmd_line) {
    ADDRESSPTR p, converr_ptr;
    long runaddress;
    byte converr;

    p = cmd_line;
    p = strtok(p); // skip over "run" command
    p = strtok(0); // get first argument
    converr_ptr = adr(converr);
    runaddress = hex_to_long(p, converr_ptr);
    and(runaddress, 0xFFFF);
    if (converr) {
        println();
        println(" error converting program start address");
        return 1;
    }
    if (runaddress < 0x200) {
        println();
        println(" runaddress must be greater then 1FF:", runaddress);
        return 0;
    }
    println(" run address is:", runaddress);
    jumpaddress = runaddress;
    _JMP (global_jumpaddress);
    return 0;
}
*/


ADDRESSPTR jsraddress;
int jsr_program(ADDRESSPTR cmd_line) {
    ADDRESSPTR p, converr_ptr;
    long runaddress;
    byte converr;

    p = cmd_line;
    p = strtok(p); // skip over "run" command
    p = strtok(0); // get first argument
    converr_ptr = adr(converr);
    runaddress = hex_to_long(p, converr_ptr);
    and(runaddress, 0xFFFF);
    if (converr) {
        println();
        println(" error converting subroutine start address");
        return 1;
    }
    if (runaddress < 0x200) {
        println();
        println(" subaddress must be greater then 1FF:", runaddress);
        return 0;
    }
    println(" sub address is:", runaddress);
    jsraddress = runaddress;
    _JSR callsubroutine;
    return 0;

_LABEL callsubroutine;
    _JMP (global_jsraddress);
}


void readbytes(ADDRESSPTR q, byte count) {
    ADDRESSPTR p;
    byte databyte, readcount;

    p = q;
    readcount = count;
    while (readcount) {
        databyte = getch();
        if (databyte == ' ') { // jump over one space
            databyte = getch();
        }
        if (errno) {
            // print out receive errors on lcd display, (P)arity, (F)raming, (O)verrun, (I)spur irq
            lcddata(errno);
        }
        poke(p, databyte);
        p = p + 1;
        readcount = readcount - 1;
    }
    poke(p,0);
}

char databuf[16];
void communication() {
    ADDRESSPTR datalength, dataaddress, dataitem, checkptr, address, headerchecksum, converr_ptr;
    int length, checksum, index, calcchecksum, header, errors, converr;
    byte databyte, readcount;
    char ch;

    errors = 0;
    converr = 0;
    converr_ptr = adr(converr);
    strcpy(databuf, "    ");
    calcchecksum = 0;
    // read length
    readbytes(databuf, 2);
    length = hex_to_long(databuf, converr_ptr);
    errors = errors + converr;
    // read address
    readbytes(databuf, 4);
    address = hex_to_long(databuf, converr_ptr);
    errors = errors + converr;
    // read header-checksum
    readbytes(databuf, 4);
    header = hex_to_long(databuf, converr_ptr);
    errors = errors + converr;
    calcchecksum = length + address;
    // print("checksum:", header, " len:", length, " adr:", address);
    if (errors == 0) {
        if (calcchecksum == header) {
            index = 0;
            calcchecksum = 0;
            while (index < length) {
                readbytes(databuf, 2);
                databyte = hex_to_long(databuf, converr_ptr);
                poke(address, databyte);
                // print("d:",databyte);
                calcchecksum = calcchecksum + databyte;
                errors = errors + converr;
                index = index + 1;
                address = address + 1;
            }
            // read checksum
            readbytes(databuf, 4);
            checksum = hex_to_long(databuf, converr_ptr);
            calcchecksum = calcchecksum + errors;
            if (checksum == calcchecksum) {
                printlnhex("OK,next: ", address);
                return;
            }
            printlnhex("ERR: data:", header, " calc:", calcchecksum, " read:", checksum, " errors:", errors);
            return;
        }
    }
    printlnhex("ERR: header:", header, " calc:", calcchecksum, " address:", address, " errors:", errors);
}

void process_buffer() {
    ADDRESSPTR p, datalength, dataaddress, dataitem, checkptr, address, converr_ptr;
    int length, checksum, index, calcchecksum, headerchecksum;
    byte databyte, converr, errors;

    errors = 0;
    converr_ptr = adr(converr);
    p = adr(cmd_buf);
    datalength = strtok(p); // get length of data from packet
    length = hex_to_long(datalength, converr_ptr);
    errors = errors + converr;
    calcchecksum = length;
    dataaddress = strtok(0); // get address of data to put
    address = hex_to_long(dataaddress, converr_ptr);
    errors = errors + converr;
    calcchecksum = calcchecksum + address;
    dataaddress = strtok(0); // get checksum of length + address
    headerchecksum = hex_to_long(dataaddress, converr_ptr);
    if (calcchecksum != headerchecksum) {
        errors = errors + 1;
    }
    if (errors == 0) {
        calcchecksum = 0;
        index = 0;
        while (index < length) {
            dataitem = strtok(0);
            databyte = hex_to_long(dataitem, converr_ptr);
            errors = errors + converr;
            poke(address, databyte);
            calcchecksum = calcchecksum + databyte;
            address = address + 1;
            index = index + 1;
        }
        checkptr = strtok(0);
        checksum = hex_to_long(checkptr, converr_ptr);
        errors = errors + converr;
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

int terminal(ADDRESSPTR cmdline) {
    byte doloop;
    char inchar;

    println("");
    println("mini Term startet, every Input");
    println("sets the PIA Port B and strobes CB2");
    println("characters will be echoed here");
    println("control-Z exits.");
    doloop = 1;
    while (doloop) {
        inchar = getch();
        if (inchar == 0x1A) {
            // if control-z is pressed, leave loop
            doloop = 0;
        } else {
            // get content of var inchar in accu
            _LDY #terminal_inchar; 
            _LDA (_userstack),Y;
            // call setport to write accu to io-port and strobe CB2
            _JSR setPORTA;
        }
        print(inchar);
        if (inchar == 13) {
            println();
        }
    }
    println("done");
    return 0;
}

int setmemory(ADDRESSPTR cmdline) {
    ADDRESSPTR p, q, st, converr_ptr;
    byte hexbyte, converr;

    converr_ptr = adr(converr);
    p = cmdline;
    p = strtok(p); // skip over "set" command
    p = strtok(0); // get first argument, startaddress
    q = hex_to_long(p, converr_ptr);
    st = q;
    if (converr) {
        println("error converting start address");
        return 1;
    }
    p = strtok(0); // get byte to write
    while (p) {
        hexbyte = hex_to_long(p, converr_ptr);
        if (converr) {
            println("error during byte input");
            return 1;
        }
        poke(q, hexbyte);
        q = q + 1;
        p = strtok(0); // get byte to write
    }
    println();
    dumpfromto(st, q);
    println();
    return 0;
}

int gettemp() {
    ADDRESSPTR p;
    int value;

    p = adr(temp_time);
    value = peekword(p);
    println();
    println("Temp-Value is:", value);
}

int settemp(ADDRESSPTR cmdline) {
    ADDRESSPTR p, st, converr_ptr;
    long q;
    byte hexbyte, converr;

    converr_ptr = adr(converr);
    p = cmdline;
    p = strtok(p); // skip over "nt" command
    p = strtok(0); // get first argument, newtemp value
    q = hex_to_long(p, converr_ptr);
    if (converr) {
        println("error converting temp value");
        return 1;
    }
    _LDY #settemp_q; 
    _LDA (_userstack),Y;
    _JSR setpwm;
    println();
}

int analyse() {
    ADDRESSPTR p, chptr, tok;
    char ch, space;
    byte do_analyse, ishex, notfound;
    int result;
    char checkbuf[20];

    notfound = 1;
    if (notfound) {
        strcpy(search_buf, "set");
        result = findincmd();
        if (result == 0) {
            setmemory(cmd_buf);
            notfound = 0;
        }
    }
    if (notfound) {
        strcpy(search_buf, "ntemp");
        result = findincmd();
        if (result == 0) {
            settemp(cmd_buf);
            notfound = 0;
        }
    }
    if (notfound) {
        strcpy(search_buf, "gtemp");
        result = findincmd();
        if (result == 0) {
            gettemp();
            notfound = 0;
        }
    }
    if (notfound) {
        strcpy(search_buf, "term");
        result = findincmd();
        if (result == 0) {
            terminal(cmd_buf);
            notfound = 0;
        }
    }

/*
    if (notfound) {
        strcpy(search_buf, "ru");
        result = findincmd();
        if (result == 0) {
            p = adr(cmd_buf);
            run_program(p);
            // usally, this will never come back
            notfound = 0;
        }
    }
    */
    if (notfound) {
        strcpy(search_buf, "su");
        result = findincmd();
        if (result == 0) {
            p = adr(cmd_buf);
            jsr_program(p);
            notfound = 0;
        }
    }
    if (notfound) {
        strcpy(search_buf, "prtab");
        result = findincmd();
        if (result == 0) {
            println();
            printsubtable();
            notfound = 0;
        }
    }
    if (notfound) {
        strcpy(search_buf, "du");
        result = findincmd();
        if (result == 0) {
            println();
            p = adr(cmd_buf);
            dump_memory(p);
            notfound = 0;
        }
    }
    if (notfound) {
        strcpy(search_buf, "woz");
        result = findincmd();
        if (result == 0) {
            println("exit monitor to wozmon...");
            _JMP wozmonentrypoint;
        }
    }
    if (notfound) {
        println();
    }
    return 0;
}

int main(int argc, char ADDRESSPTR) {
    int retval, state;
    int chars_to_read;
    long inputs;
    byte idx;
    char inchar, ch;
    ADDRESSPTR funcptr;
    long ti;

    state = 0;
    retval = 0;
    inputs = 0;
    println("START mon...:");
    strcpy(cmd_buf, "");
    while (retval == 0) {
        chars_to_read = avail();
        if (chars_to_read > 0) {
            inchar = getch();
            if (inchar == 0x0D) {
                inputs = inputs + 1;
                retval = analyse();
                strcpy(cmd_buf, "");
                print("#", inputs,">");
            }
            if (inchar == 8) {   // Backspace pressed
                println("buffer cleared!");
                strcpy(cmd_buf, "");
                print("#", inputs,">");
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