#include <isnumber.c>
#include <upchar.c>
#include <simplestrtok.c>
#include <convert_to_bin.c>

char cmd_buf[256];

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
                // print("do:", cmd_buf);
                //puttomem();
                strcpy(cmd_buf, "");
                print(":");
            }
            if (inchar == 0x2A) { // start packet with * Symbol
                // print("do:", cmd_buf);
                puttomem();
                strcpy(cmd_buf, "");
            }
    
            if (inchar != 0x0D) {
                strcat(cmd_buf, inchar);
                print(inchar);
            }
        }
    }
    return retval;
}