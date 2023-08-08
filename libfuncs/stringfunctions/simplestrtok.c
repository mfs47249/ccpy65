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
