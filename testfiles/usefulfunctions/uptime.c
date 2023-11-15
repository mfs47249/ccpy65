
void printuptime() {
    longlong timeval;
    long ticks;
    long days, hours, minutes, seconds;

    timeval = 0;
    //println("Uptime time is, in usec:", timeinusec);
    timeval = gettimer();
    shiftright(timeval, 16);
    seconds = timeval / 100;
    minutes = seconds / 60;
    hours = minutes / 60;
    days = hours / 24;
    seconds = seconds - (minutes * 60);
    minutes = minutes - (hours * 60);
    hours = hours - (days * 24);
    //time_in_sec = (timeinusec / 1000000) - (minutes * 60);
    println("days:", days, " hours:", hours, " minutes:", minutes, " sec:", seconds);
}
