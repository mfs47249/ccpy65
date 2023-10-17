#include <factorial.c>
#include <printsubtable.c>


long main(int argc, ADDRESSPTR argv) {
    ADDRESSPTR s, p, f1, f2;
    long i, max, sum;

    println("Calculating 100 x");
    f1 = adr("programstart");
    f2 = adr("kima_konst");
    max = 10000;
    i = 0;
    while (i < max) {
        p = f1;
        sum = 0;
        while (p < f2) {
            sum = sum + peek(p);
            p = p + 1;
        }
        println("i:", i, " f1:", f1, " f2:", f2, " sum:", sum);
        p = adr("_userstack");
        s = getintataddress(p);
        //Okrintln("Userstack:", s, " iterations:", i);
        // _JSR $AC63;
        factorialtest();
        i = i + 1;
    }
}