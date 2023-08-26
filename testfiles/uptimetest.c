
void printuptime(long interval) {
    longlong ticks;
    longlong usec;
    longlong timeval;
    longlong timeinusec;
    longlong time_in_sec;
    longlong days, hours, minutes, seconds;

    timeval = gettimer();
    println("timeval:", timeval);
    usec = timeval;
    ticks = timeval;
    and(usec, 0xFFFF);
    shiftright(ticks, 16);
    timeinusec = (ticks * 10000) + usec;
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


void lcdxy(byte x, byte y) {
    byte send;
    byte command;

    send = 0x80;  //  command is set ddramaddress
    if (y == 0) {
        command = send + 0 + x;
    }
    if (y == 1) {
        command = send + 0x40 + x;
    }
    printhex("cmd:", command);
    lcdcommand(command);
}

void main(int argc, int *argv) {
    int doit;
    long ti;
    char ch;
    byte temp;
    int readcount;
    char message[20];

    ti = 10000;
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
            if (ch == 'A') {
                lcdcommand(1); // clear screen of lcd
                strcpy(message, "Hallo LCD!");
                adr(message);
                lcdstring("Hallo Welt");
            }
            if (ch == 'B') {
                lcdcommand(2); // return home

            }
            if (ch < 'Z') {
                if (ch > 'C') {
                    temp = ch - 'C';
                    println("ord(temp):", temp);
                }
            }
            lcddata(ch);
        }
    }
    _JMP $8000;
}