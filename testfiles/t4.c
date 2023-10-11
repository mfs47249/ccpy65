
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

    a = 0;
    while (a < 20000) {
        b = iterate(1000);
        println("iterations = ", a);
        a = a + 1;
    }
    println("Ende");
}