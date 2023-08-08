
char upchar(char ch) {
    char c;

    c = ch;
    // check for lower ASCII Letter a-z
    if (c > 96) { // check for ascii > '`'
        if (c < 123) { // check for ascii < '{' 
            c = c - 32;
            return c;
        }
    }
    return c;
}