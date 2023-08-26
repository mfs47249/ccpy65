
char cmd_buf[256];
char search_buf[64];

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
