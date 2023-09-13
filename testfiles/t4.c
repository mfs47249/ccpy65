
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
    ADDRESSPTR pattern;


    while (dosearch) {
        dosearch = 0;
    }
    search = 0x200;
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
        } else {
            print("x");
        }
        if (search > 0x3000) {
            dosearch = 0;
            search = 0;
        }
        search = search + 1;
    }
    return 0;
}