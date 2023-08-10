int convert_to_bin_err;
int convert_to_bin(ADDRESSPTR ptr) {
    ADDRESSPTR p;
    byte index, flag, ch;
    int result;

    convert_to_bin_err = 0;
    p = ptr;
    index = 0;
    result = 0;
    ch = peek(p);
    while (ch != 0) {
        ch = upchar(ch);
        if (ch > 64) {
            if (ch < 71) {
                ch = ch - 55;
            }
        }
        if (ch > 47) {
            if (ch < 58) {
                ch = ch - 48;
            }
        }
        if (ch > 15) {
            convert_to_bin_err = 1;
            return 0;
        }
        result = result + ch;
        p = p + 1;
        index = index + 1;
        ch = peek(p);
        if (ch != 0) {
            shiftleft(result,4);
        }
    }
    return result;
}
