byte asmtest(byte input) {
    byte result;

    result = input;
    if (input > 0x20) {
        _LDY   #asmtest_result;
        _LDA   (_userstack),Y;
        _ORA   #$80;
        _STA   (_userstack),Y;
    }
    return result;
}

int test1(int x) {
    int a;

    a = 1;
    return a;
}

int testfunc0() {
    int b;

    b = 1 + 2 - 4 * test1(b) - 1000 * 200 + 5 / 2;
    b = 1 + test1(b);
    print("in0:", b, "                  ");
    return b;
}

int testfunc1(int in1) {
    int b;

    print("in1:", in1, "                  ");
    b = in1;
    return b;
}

int testfunc2(int in1, int in2) {
    int b;

    print("in1:", in1, " in2:", in2, "         ");
    b = in1 + in2;
    return b;
}

int testfunc3(int in1, int in2, int in3) {
    int b;

    print("in1:", in1, " in2:", in2, " in3:", in3);
    b = in1 + in2 + in3;
    return b;
}

int infiniterecursion(int r) {
    int a;

    println("infinite recursion called with:", r)
    a = infiniterecursion(1 + r);
    return a;
}

void main(int argc, int *argv) {
    int a, b, c, d, e, funcarg;
    byte bvalue;
    char cvalue;

    funcarg = 0x1234;
    funcarg = 0x1000;
    b = 5;
    /* a = (a + b / d - e) * (a + b / d - e) * (a + b / d - e) * (a + b / d - e); */
    while (b > 0) {
        a = b;
        // a = a + testfunc0();
        // println(" res, tf0:", a);
        if (a == b) {
            a = a + testfunc1(funcarg);
            println(" res, tf1:", a);
            a = a + testfunc2(funcarg, 0x100);
            println(" res, tf2:", a);
            a = a + testfunc3(funcarg, 0x100, 0x10);
            println(" res, tf3:", a);
            // a = a + testfunc4(funcarg, 0x100, 0x10, 0x1);
            // println(" res, tf3:", a);
            /* a = testfunc(funcarg + 10); */
            println("nach funktionsaufruf,a:", a);
        }
        // else
        if (1) {
            print("a:", a);
        }
        b = b - 1;
    }
    bvalue = 0x41;
    println("bvalue:", bvalue);
    cvalue = bvalue;
    println("cvalue:", cvalue);
    bvalue = 0x41;
    bvalue = asmtest(bvalue);
    println("bvalue:", bvalue);
    cvalue = asmtest(bvalue);
    println("cvalue:", cvalue);
    /* a = infiniterecursion(1); */
}

/* END OF PROGRAM */