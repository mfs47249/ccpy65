byte isletter(char ch) {
    // check for Upper ASCII Letter A-Z
    if (ch > 63) { // check for ascii > '@'
        if (ch < 91) { // check for ascii < '[' 
            return 1;
        }
    }
    // check for lower ASCII Letter a-z
    if (ch > 96) { // check for ascii > '`'
        if (ch < 123) { // check for ascii < '{' 
            return 1;
        }
    }
    return 0;
}
