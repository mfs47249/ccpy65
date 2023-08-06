

int main(int argc, ADDRESSPTR argv) {
    byte i, z, x, w;
    longlong sum, a;
    longlong counter;

    a = 0 - 5;
    a = 0x222222 - 5;
    a = 0xF23456789ABCDE00 - 3;
    a = 10;
    i = 0;
    sum = 10;
    sum = a + 20;
    writeln("a:", a);
    counter = 0;
    while (sum < (a - 200000)) {
        sum = sum - 1;
        counter = counter + 1;
    }
    writeln("counter:", counter);
    while (i < 0x40) {
        sum = sum - 1;
        if (sum < a) {
            write("true");
        }
        writeln("i:", i, " sum:", sum);
        i = i + 1;
    }
    writeln("ureg0:", _unireg0)
    writeln("i:", i, " sum:", sum, " a:", a);
}