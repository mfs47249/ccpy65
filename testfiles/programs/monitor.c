#include <isnumber.c>
#include <upchar.c>
#include <simplestrtok.c>

#include <findinstrings.c>

int convert_to_bin_err;
int convert_to_bin(ADDRESSPTR ptr) {
    ADDRESSPTR p;
    byte index, flag, ch;
    int result;

    convert_to_bin_err = 0;
    p = ptr;
    index = 0;
    result = 0;
    ch = peek(p);
    while (ch != 0) {
        ch = upchar(ch);
        if (ch > 64) {
            if (ch < 71) {
                ch = ch - 55;
            }
        }
        if (ch > 47) {
            if (ch < 58) {
                ch = ch - 48;
            }
        }
        if (ch > 15) {
            convert_to_bin_err = 1;
            return 0;
        }
        result = result + ch;
        p = p + 1;
        index = index + 1;
        ch = peek(p);
        if (ch != 0) {
            shiftleft(result,4);
        }
    }
    return result;
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

int analyse() {
    ADDRESSPTR p, chptr, tok;
    char ch, space;
    byte do_analyse, ishex;
    int result;
    char checkbuf[20];

    strcpy(search_buf, "run");
    result = findincmd();
    if (result >= 0) {
        p = adr(cmd_buf);
        run_program(p);
    }
    strcpy(search_buf, "dump");
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

    return 0;
    /*
    p = adr(cmd_buf);
    tok = strtok(p);
    while (tok != 0) {
        strcpy(checkbuf, tok);
        // println("tok:", tok, " checkbuf:", checkbuf);
        result = convert_to_bin(tok);
        if (convert_to_bin_err != 0) {
            println("Error converting HEX Value");
        }
        do_analyse = result;
        printlnhex("result:", result, " do_analyse:", do_analyse);
        tok = strtok(0);  // get next token

    }
    return 0;
    print("enter while loop");
    while (do_analyse) {
        ch = peek(chptr);
        println("debug, ch:", ch, " chptr:", chptr);
        if (ch == 0) {
            do_analyse = 0; // end, if null terminate
        }
        strcpy(search_buf, "run");
        result = findincmd();
        println("result:", result);
        tok = strtok(chptr);
        while (tok != 0) {
            println("tok:", tok);
            tok = strtok(chptr);
        }
        chptr = chptr + 1;
    }
    return 0;*/
}


int main(int argc, char ADDRESSPTR) {
    int retval, state;
    int chars_to_read;
    byte idx;
    char inchar, ch;
    ADDRESSPTR funcptr;

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