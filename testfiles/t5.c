#include <factorial.c>
#include <printsubtable.c>


long main(int argc, ADDRESSPTR argv) {
    ADDRESSPTR s;
    long i, max;
    ADDRESSPTR p;

    println("Calculating 100 x");
    max = 100;
    i = 0;
    while (i < max) {
        p = adr("_userstack");
        s = getintataddress(p);
        println("Userstack:", s, " iterations:", i);
        factorialtest();
        i = i + 1;
    }
}