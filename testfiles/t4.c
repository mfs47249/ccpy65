#include <printregisters.c>

#include <printsubtable.c>

int main(int argc, ADDRESSPTR argv) {
    byte i, z, x, w;
    long sum, a;
    long counter;

    println("a:", a);
    //sevensegmentptr = adr(counter);
    sum = 2000;
    counter = 0;
    while (sum < 0x10000) {
        sum = sum - 1;
        counter = counter + 1;
    }
    printregisters();
    println("i:", i, " sum:", sum, " a:", a);
}