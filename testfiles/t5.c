#include <factorial.c>
#include <printsubtable.c>


long main(int argc, ADDRESSPTR argv) {
    ADDRESSPTR s;
    long i, max, xd;
    ADDRESSPTR p;
    wozfloat x,y;

    println("Calculating 100 x");
    max = 100;
    i = 0;
    x = real(100);
    y = x / 1000;
    while (i < max) {
        p = adr("_userstack");
        s = getintataddress(p);
        println("Userstack:", s, " iterations:", i, " wfloat:", xd);
        factorialtest();
        i = i + 1;
        x = x + y;
        xd = integer(x);
    }
}