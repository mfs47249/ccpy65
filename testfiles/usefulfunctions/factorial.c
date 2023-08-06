longlong factorial(longlong factor) {
    longlong a;

    if (factor == 0) {
        return 1;
    }
    a = factor * factorial(factor - 1);
    return a;
}


void factorialtest() {
    longlong fa, fb;

    fb = 0;
    while (fb < 21) {
        fa = factorial(fb);
        println("n:", fb, "  n!:", fa);
        fb = fb + 1;
    }
}

/*  Result of factorialtest should be:
    https://en.wikipedia.org/wiki/Factorial

0 	1
1 	1
2 	2
3 	6
4 	24
5 	120
6 	720
7 	5040
8 	40320
9 	362880
10 	3628800
11 	39916800
12 	479001600
13 	6227020800
14 	87178291200
15 	1307674368000
16 	20922789888000
17 	355687428096000
18 	6402373705728000
19 	121645100408832000
20 	2432902008176640000

*/