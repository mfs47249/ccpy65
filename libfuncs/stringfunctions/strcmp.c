
int strcmp(ADDRESSPTR a, ADDRESSPTR b) {
    ADDRESSPTR p,q,
    char x,y;

    p = a;
    q = b;
    strcmploop:
        x = peek(p);
        y = peek(q);
        if (x == y) {
            p = p + 1;
            q = q + 1;
            if (x == 0) {
                if (y == 0) {
                    return 0;
                }
            }
        } else {
            if (x > y) {
                return 1;
            } else {
                return -1;
            }
        }
    goto strcmploop;
}
