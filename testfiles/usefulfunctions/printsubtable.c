
ADDRESSPTR nextafterterminator(ADDRESSPTR s) {
    ADDRESSPTR p;
    byte endofloop, found;

    endofloop = 1;
    p = s;
    while (endofloop) {
        endofloop = peek(p);
        p = p + 1;
    }
    return p;
}

/*  we can now use peekword() for this feature

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
*/

void printsubtable() {
    ADDRESSPTR p, q;
    int ad, le;
    int x1,x2;
    byte endofloop;
    char subname[128];

    endofloop = 1;
    p = adr("subroutinetable"); // get address of subroutinetable in this program!
    println("Table is at:", p);
    le = 0;
    while (endofloop) {
        strcpy(subname, p);
        q = nextafterterminator(p);
        ad = peekword(q);
        le = ad - le;
        printlnhex(ad, " is:", subname, " len:", le);
        le = ad;
        p = q + 2;
        ad = peekword(p);
        if (ad == 0xACF1) {
            endofloop = 0;
        }
    }
}
