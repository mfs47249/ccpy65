
int getintataddress(ADDRESSPTR q) {
    ADDRESSPTR p;
    int ad, x;

    p = q;
    ad = peek(p);
    p = p + 1;
    x = peek(p);
    shiftleft(x,8);
    return ad + x;
}


int main(int argc, ADDRESSPTR argv) {
    ADDRESSPTR search;
    byte dosearch;
    ADDRESSPTR pattern, prgstart, q;


    if (q == 0x100) {
        q = 0;
    }
    search = adr("programstart");
    search = search - 2;
    q = getintataddress(search);
    printlnhex("Searching for startaddress of table:", q);
    dosearch = 1;
    printlnhex("Starting with search at adr:", search);
    while (dosearch) {
        pattern = getintataddress(search);
        if (pattern == 0x05B1) {
            search = search + 2;
            pattern = getintataddress(search);
            if (pattern == 0x0DF0) {
                search = search + 2;
                dosearch = 0;
                printlnhex("Found Pattern at:", search);
            } 
        }
        if (search > 0x3000) {
            printlnhex("Search stoppted at:", search);
            dosearch = 0;
            search = 0;
        }
        search = search + 1;
    }
    return 0;
}