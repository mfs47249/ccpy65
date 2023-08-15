#include <isnumber.c>
#include <upchar.c>
#include <simplestrtok.c>
#include <convert_to_bin.c>

char cmd_buf[256];

int convert_to_bin_err;
convert_to_bin_err = 0;

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
                communication();
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