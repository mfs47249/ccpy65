

char cmd_buf[256];
char search_buf[64];

byte isletter(char ch) {
    // check for Upper ASCII Letter A-Z
    if (ch > 63) { // check for ascii > '@'
        if (ch < 91) { // check for ascii < '[' 
            return 1;
        }
    }
    // check for lower ASCII Letter a-z
    if (ch > 60) { // check for ascii > '`'
        if (ch < 123) { // check for ascii < '{' 
            return 1;
        }
    }
    return 0;
}

byte isnumber(char ch) {
    // check for 0-9
    if (ch > 47) { // check for ascii > '/'
        if (ch < 58) { // check for ascii < ':' 
            return 1;
        }
    }
    return 0;
}

char upchar(char ch) {
    byte isletter;

    isletter = isletter(ch);
    if (isletter) {
        return (ch + 32);
    }
    return ch;
}

byte ishex(char ch) {
    // check for 0-9 and A-F
    char c;
    byte isnumber;

    isnumber = isnumber(ch);
    if (isnumber) {
        return 1;
    }
    c = upchar(ch);
    if (c > 63) { // check for ascii > '@'
        if (c < 71) { // check for ascii < 'G' 
            return 1;
        }
    }
    return 0;
}

int findincmd() {
    ADDRESSPTR cmdptr, searchptr, p1, p2;
    int cmdlen, searchlen, searchidx, cmdidx, pos, zero;
    byte found, search, endwhile;
    char ch1,ch2;

    cmdptr = adr(cmd_buf);
    cmdlen = strlen(cmd_buf);
    searchptr = adr(search_buf);
    searchlen = strlen(search_buf);
    found = 0;           // not found
    search = 1;          // do search
    cmdidx = 0;
    while (found == 0) { // do until not found
        searchptr = adr(search_buf);
        found = 1;       // assume we will found the item
        search = 1;
        searchidx = 0;
        endwhile = 1;
        pos = cmdidx;
        while (endwhile) {
            p1 = cmdptr + searchidx;
            p2 = searchptr + searchidx;
            ch1 = peek(p1);
            ch2 = peek(p2);
            if (ch1 != ch2) {
                search = 0;
                endwhile = 0;
                found = 0;
            }
            searchidx = searchidx + 1;
            if (searchidx >= searchlen) {
                return pos;
            }
        }
        cmdptr = cmdptr + 1;
        cmdidx = cmdidx + 1;
        if (cmdidx > cmdlen) {
            found = 1;
        }
        if (search) {
            found = 1;
        }
    }
    zero = 0;
    pos = zero - 1;
    return pos;
}

ADDRESSPTR strtok_nextstring;
int strtok_laststringcount;
ADDRESSPTR strtok(ADDRESSPTR string_adr) {
    ADDRESSPTR startptr, stringptr, delimfound;
    byte done;
    int sizeofstring, stringindex, zero;
    char searchfor, delim;

    done = 0;
    delim = 0x20;
    stringindex = 0;
    startptr = string_adr;
    stringptr = string_adr;
    if (stringptr == 0) {
        stringptr = strtok_nextstring;
        startptr = strtok_nextstring;
    }
    sizeofstring = strlen(stringptr);
    if (stringptr) {
        strtok_laststringcount = sizeofstring;
    }
    if (strtok_laststringcount =< 0) {
        // println("end of string");
        stringptr = 0;
        return stringptr;
    }
    delimfound = 0;
    // println("adr(string_adr):", string_adr);
    while (done == 0) {
        searchfor = peek(stringptr);
        // println("sf:", searchfor);
        if (searchfor == delim) {
            delimfound = stringptr;
            done = 1;
        }
        if (searchfor == 0) {
            delimfound = stringptr;
            done = 1;
        }
        if (delimfound == 0) {
            stringptr = stringptr + 1;
            stringindex = stringindex + 1;
        }
        strtok_laststringcount = strtok_laststringcount - 1;
        /* zero = strtok_laststringcount;
        println("ch:", searchfor, " size:", sizeofstring, " adr:", stringptr, " lastcnt:", zero); */
    }
    if (delimfound) {
        // println("delim found at:", stringptr);
        zero = 0;
        poke(stringptr, zero);
        strtok_nextstring = stringptr;
        if (strtok_laststringcount > 0) {
            // println("increment laststringcount");
            strtok_nextstring = stringptr + 1;
        }
        return startptr;
    }
    return 0;
}


int analyse() {
    ADDRESSPTR chptr, tok;
    char ch, space;
    byte do_analyse, ishex;
    int result;
    char checkbuf[20];

    space = 0x20;
    chptr = adr(cmd_buf);
    do_analyse = 1;
    ishex = 0;
    strcpy(search_buf, "run");
    result = findincmd();
    println("result:", result);

    tok = strtok(chptr);
    while (tok != 0) {
        strcpy(checkbuf, tok);
        println("tok:", tok, " checkbuf:", checkbuf);
        tok = strtok(0);
    }



    return 0;
/*  print("enter while loop");
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
    char inchar;
    ADDRESSPTR funcptr;

    state = 0;
    retval = 0;
    strcpy(cmd_buf, "");
    while (retval == 0) {
        chars_to_read = avail();
        if (chars_to_read > 0) {
            inchar = getch();
            if (inchar == 0x3) { // press control c returns to wozmon
                retval = 1;
            }
            if (inchar == 0x0D) {
                println("\ncmd:", cmd_buf);
                state = analyse();
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