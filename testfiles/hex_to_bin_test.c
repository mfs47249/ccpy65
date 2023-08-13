#include <convert_to_bin.c>

char buffer[128];

int main() {
    ADDRESSPTR cptr;
    long result;
    char tchar;

    cptr = adr(buffer);
    tchar = 0;
    strcpy(buffer, "89ABCDEF");
    while (tchar != 3) {
        result = hex_to_int(cptr);
        printlnhex("tchar:", tchar, " result:", result);
        tchar = tchar + 1;
    }



}