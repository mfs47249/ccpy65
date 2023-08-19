
void printuptime(long interval) {
    longlong ticks;
    longlong usec;
    longlong timeval;
    longlong timeinusec;
    longlong time_in_sec;
    longlong days, hours, minutes, seconds;

    timeval = gettimer();
    usec = timeval;
    ticks = timeval;
    and(usec, 0xFFFF);
    shiftright(ticks, 16);
    timeinusec = (ticks * interval) + usec;
    //println("Uptime time is, in usec:", timeinusec);
    seconds = timeinusec / 1000000;
    minutes = seconds / 60;
    hours = minutes / 60;
    days = hours / 24;
    seconds = seconds - (minutes * 60);
    minutes = minutes - (hours * 60);
    hours = hours - (days * 24);
    //time_in_sec = (timeinusec / 1000000) - (minutes * 60);
    println("usec:" timeinusec, " days:", days, " hours:", hours, " minutes:", minutes, " sec:", seconds);
}


void main(int argc, int *argv) {
    int doit;
    long ti;
    char ch;
    int readcount;

    ti = 50000;
    settimer(ti);
    doit = 1;
    println("Starting...");
    while (doit) {
        readcount = avail();
        if (readcount > 0) {
            ch = getch();
            if (ch == 13) {
                printuptime(ti);
                lcddata(41);
            }
            if (ch == 3) {
                doit = 0;
            }
            lcddata(ch);
        }
    }
    _JMP $8000;
}