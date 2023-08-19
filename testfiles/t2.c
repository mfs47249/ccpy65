#include <convert_to_bin.c>



char hexbuffer[16];

void main(int argc, int *argv) {
    int count, result;
    byte error;
    char ch;
    ADDRESSPTR error_ptr;
    long test, timerinterval;

    timerinterval = 1000;
    settimer(timerinterval);
    error_ptr = adr(error);
    count = 0;
    while (count < 127) {
        ch = count;
        strcpy(hexbuffer,ch);
        result = hex_to_long(hexbuffer, error_ptr);
        printlnhex("buf:", hexbuffer, " result:", result, " error:", error);
        count = count + 1;
    }

    strcpy(hexbuffer, "DE");
    test = hex_to_long(hexbuffer, error_ptr);
    printlnhex("value:", test, " error:", error);
    strcpy(hexbuffer, "01234");
    test = hex_to_long(hexbuffer, error_ptr);
    printlnhex("value:", test, " error:", error);
    strcpy(hexbuffer, "4711");
    test = hex_to_long(hexbuffer, error_ptr);
    printlnhex("value:", test, " error:", error);
    strcpy(hexbuffer, "11");
    test = hex_to_long(hexbuffer, error_ptr);
    printlnhex("value:", test, " error:", error);
    strcpy(hexbuffer, "DAE");
    test = hex_to_long(hexbuffer, error_ptr);
    printlnhex("value:", test, " error:", error);
    strcpy(hexbuffer, "012a34");
    test = hex_to_long(hexbuffer, error_ptr);
    printlnhex("value:", test, " error:", error);
    strcpy(hexbuffer, "471 1");
    test = hex_to_long(hexbuffer, error_ptr);
    printlnhex("value:", test, " error:", error);
    strcpy(hexbuffer, "feedc0de");
    test = hex_to_long(hexbuffer, error_ptr);
    printlnhex("value:", test, " error:", error);

}

/* END OF PROGRAM */