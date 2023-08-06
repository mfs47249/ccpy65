
// #include <factorial.c>
// #include <itoa.c>

longlong getmicroseconds(longlong interval) {
    longlong ticks;
    longlong usec;
    longlong timeval;
    longlong timeinusec;

    timeval = gettimer();
    usec = timeval;
    ticks = timeval;
    and(usec, 0xFFFF);
    shiftright(ticks, 16);
    // printlnhex("timeval:", timeval, " usec:", usec, " ticks:", ticks);
    timeinusec = (ticks * interval) + usec;
    return timeinusec;
}

int main(int argc, ADDRESSPTR argv)  { 
    longlong counter;
    longlong time;
    longlong time_in_sec;
    long c1;
    longlong newvalue;

    c1 = 0;
    newvalue = 10000;
    settimer(newvalue);
    counter = 0;
    while (counter < 10) {
        counter = counter + 1;
        time = getmicroseconds(newvalue);
        time_in_sec = time / 100000;
        println("count:", counter, " time in usec:", time, " sec:", time_in_sec);
    }
/*
    counter = 1;
    while (counter < 5) {
        time = gettimer();
        printlnhex("Counter:", time);
        counter = counter + 1;
        // wait();
    }
    */
    //factorialtest();
    return time;
}