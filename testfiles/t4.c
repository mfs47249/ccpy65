
int iterate(int n) {
    int x;

    x = n;
    while (x > 1) {
        x = x - 1;
    }
    return x;
}


int main(int argc, char *argv) {
    int a, b;
    ADDRESSPTR p;

    a = 0;
    p = 0x7832;
    while (1) {
        // b = iterate(1000);
        // println("iterations = ", a);
        poke(p,a);
        a = a + 1;
    }
    println("Ende");
}
