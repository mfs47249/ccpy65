byte isnumber(char ch) {
    // check for 0-9
    if (ch > 47) { // check for ascii > '/'
        if (ch < 58) { // check for ascii < ':' 
            return 1;
        }
    }
    return 0;
}