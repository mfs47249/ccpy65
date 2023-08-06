const char pi = "03141592653589701";   // "3.1415926535897";
const char euler = "2.718281828459045";
const char test = "100"; // 3.764E3

#include <factorial.c>


int main(int argc, char *argv) {
    kimfloat test1, test2;
    long x, y;
    char buffer[64];

    factorialtest();
    kim_clrx();
    kim_clry();
    kim_clrz();
    kim_uploadx(pi);
    kim_uploadx(test);
    kim_uploady(test);
    x = adr(_memarea);
    printlnhex("bufferadr:", x);
    kim_ustres(buffer);
    x = 0;
    while (x < 10) {
        kim_uploadx(test);
        kim_uploady(test);
        kim_ustres(buffer);
        println(buffer);
        x = x + 1;
    }
    return 0;
}