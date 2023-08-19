
int main(int argc, char ADDRESSPTR) {
    int retval, state;
    int chars_to_read;
    byte idx, in;
    char ch, inchar;
    ADDRESSPTR funcptr;
    longlong timerinterval;

    timerinterval = 50000;
    settimer(timerinterval);
    state = 0;
    retval = 0;
    println("Serialtest:");
    inchar = 0x20;
    while (retval == 0) {
        chars_to_read = avail();
        if (chars_to_read > 0) {
            ch = getch();
            in = ch;
            println(in);
        }
    }
    return retval;
}