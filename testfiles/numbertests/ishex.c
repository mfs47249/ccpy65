byte ishex(char ch) {
    // check for 0-9 and A-F
    char c;
    byte isn;

    c = ch;
    isn = isnumber(c);
    if (isn) {
        return 1;
    }
    c = upchar(c);
    if (c > 64) { // check for ascii > '@'
        if (c < 71) { // check for ascii < 'G' 
            return 1;
        }
    }
    return 0;
}