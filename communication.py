#!/usr/bin/python3
import serial
import time
import sys
import argparse

# communication.py is a helper script for copy the binary program a.out to the mini computer
# It relies on the wozmon Monitorprogram (see Ben Eaters Video on YouTube about the wozmon)

# The script trys to execute commands for put data into memory and get data from memory:
#  Getting Data with:
#    0200.0300
#  gets the data from memory 0200 to 0300
#  Putting Data with:
#    0200:01 02 03 04 05 06
#  puts the byte 01,02,03,04,05,06 from the memory location 0200 into memory of the system
#
# Communication is slow an unsave. Communication errors sometimes stop the communication
# you can simple type reset on the minicomputer, if the minicomputer resets to the wozmon
# monitor, the transfer will continue.

    

def grepcode(data, search):
    searchlist = list()
    datalist = list()
    print("len(data):%d" % len(data))
    for d in data:
        datalist.append(int(d))
    for s in search:
        searchlist.append(s)
    dindex = 0
    while (dindex < (len(datalist) + len(search))):
        sindex = 0
        found = True
        for s in searchlist:
            if (searchlist[sindex] != datalist[dindex+sindex]):
                found = False
                break
            else:
                sindex += 1
        if found:
            return dindex
        dindex += 1
    return -1



class storageitem:

    def __init__(self, address, data):
        self.address = address
        self.data = data

    def getaddress(self):
        return self.address

    def getdata(self):
        return self.data

    def getbyte(self,address):
        baseadr = address % 8

class datastore:
    asciitab = ["nul", "soh", "stx", "etx", "eot", "enq", "ack", "bel",
                "bs", "ht", "lf", "vt", "ff", "cr", "so", "si",
                "dle", "dc1", "dc2", "dc3", "dc4", "nak", "syn", "etb",
                "can", "em", "sub", "esc", "fs", "gs", "rs", "us",
                " ", "!", "\"", "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/",
                "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", ";", "<", "=", ">", "?",
                "@",'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
                "[", "\\", "]", "^", "_", "`",
                'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
                "{", "|", "}", "~", "del"]

    def __init__(self):
        self.storage = dict()

    def returnletter(self, number):
        if number > len(self.asciitab) - 1:
            return " . "
        else:
            x = "%3s" % self.asciitab[number]
            return x

    def listdata(self):
        for d in self.storage:
            print("Address:%s (%04X) Data:" % (d,d), end="")
            for x in self.storage[d].getdata():
                print(" %s" % x, end="")
            print("   ", end="")
            for x in self.storage[d].getdata():
                try:
                    b = int("0x%s" % x, base=16)
                except:
                    b = "ERR"
                print(" %s" % self.returnletter(b), end="")
            print()

    def getmemdump(self, memdump):
        for l in memdump:
            linevals = l.split()
            if len(linevals) > 8:
                adr = linevals[0]
                try:
                    address = int("0x%s" % adr[0:4], base=16)
                except:
                    print("\nerror in converting hexaddress to int, line is:%s" % linevals)
                    return False
                data = list()
                for idx in [1,2,3,4,5,6,7,8]:
                    data.append(linevals[idx])
                s = storageitem(address, data)
                self.storage[address] = s
        return True

    def putdata(self, address, data):
        cmd = "%04X: " % address
        for d in data:
            cmd += "%s" % d
        return cmd

    def returncmds(self, newaddress):
        adr = newaddress
        commands = list()
        for s in self.storage:
            item = self.storage[s]
            address = item.getaddress()
            data = item.getdata()
            commands.append(self.putdata(adr, data))
            adr += 8
        return commands
        
    def insertbinfile(self, startaddress, length, byte_array):
        index = 0
        address = startaddress
        while index < length:
            #print("%d, (%04X):" % (address, address), end="")
            data = list()
            for i in [0,1,2,3,4,5,6,7]:
                # print("%02X " % byte_array[index+i], end="")
                data.append("%02X " % byte_array[index+i])
            s = storageitem(address, data)
            self.storage[address] = s
            # print()
            index += 8
            address += 8

    def checkdata(self, startaddress, endaddress):
        checkaddress = startaddress
        while checkaddress < endaddress:
            try:
                sobj = self.storage[checkaddress]
            except KeyError as e:
                print("\ncheckdata address:%d (%04X) not found" % (checkaddress, checkaddress))
                return False
            data = sobj.getdata()
            if len(data) == 8:
                for d in data:
                    try:
                        b = int("0x%s" % d, base=16)
                    except:
                        print("\nerror in data at address: %04X, data is:" % checkaddress, end="")
                        for d in data:
                            print("%s," % d, end="")
                        print()
                        return False
            else:
                return False
            checkaddress += 8
        return True
        

class SerialConn:
    serconn = None

    def __init__(self, device):
        self.device = device
        self.openserial(self.device)
    
    def openserial(self,device):
        self.serconn = serial.Serial(port=device, baudrate=19200, bytesize=8, stopbits=2, parity='O', timeout=1, xonxoff=0, rtscts=0)
        self.isopen = self.serconn.is_open

    def close(self):
        self.serconn.close()

    def writedata_lf(self, sendline):
        tosystem = sendline + "\r"
        self.serconn.write(tosystem.encode())
        self.serconn.flush()

    def writedata(self,sendline):
        tosystem = sendline
        dosend = True
        while dosend:
            try:
                # error in write on serial should never happen, put it does on my windows system
                # for solving the "permission denied" error on writing to the serial port on windows
                # we close the connection and open a new one, this solves the problem the hard way
                self.serconn.write(tosystem.encode())
                dosend = False
            except:
                print("error in Serial write command")
                self.close()
                time.sleep(2)
                self.openserial(self.device)
                dosend = True
        self.serconn.flush()

    def writedataraw(self,sendline):
        tosystem = sendline
        self.serconn.write(tosystem)
        self.serconn.flush

    def readdata(self, termstring):
        dlines = list()
        linecount = 0
        receiveddata = "no data"
        try:
            r = self.serconn.readline()
            receiveddata = r.decode("ascii").strip()
        except:
            return list()
        dlines.append(receiveddata)
        linecount += 1
        while len(receiveddata) > 0 and not receiveddata.startswith(termstring):
            try:
                r = self.serconn.readline()
                receiveddata = r.decode("ascii").strip()
                # print("Termstring:%s Received:%s Len():%d" % (str(termstring), str(receiveddata), len(receiveddata)))
                if len(receiveddata) == 0:
                    self.writedata_lf("wozmon")
            except UnicodeDecodeError as e:
                print("\nerror at decode at line: %s" % r)
                return list()
            dlines.append(receiveddata)
            linecount += 1
        return dlines

    def putcommand(self, length, cmd):
        cmd = cmd.strip()
        # print("commnd:%s" % cmd)
        termstring = cmd[0:5]
        startaddress = int("0x%s" % cmd[0:4], base=16)
        isok = False
        while not isok:
            self.writedata_lf(cmd)
            result = self.readdata(termstring)
            endaddress = startaddress + 8
            checkcmd = "%04X.%04X" % (startaddress, endaddress)
            self.writedata_lf(checkcmd)
            termstring = "%04X:" % endaddress
            result = self.readdata(termstring)
            found = ""
            for l in result:
                if len(l) > 28:
                    found = l.strip()
            if len(result) < 2:
                isok = False
            else:
                if cmd == found:
                    isok = True
                else:
                    print("cmd differs:%s,%s" % (cmd, found))
                    isok = False
        print("%04x,%s" % (length, found))

    def emptybuffer(self):
        result = "***"
        while result != "":
            try:
                tosystem = "\r"
                self.serconn.write(tosystem.encode())
                self.serconn.flush()
                r = self.serconn.readline()
                result = r.decode("ascii").strip()
                print(result)
            except UnicodeDecodeError as e:
                print("\nemptybuffer:%s" % e)

    def getmemorylinesat(self, address, distance, termstring):
        startaddr = address
        endaddr = address + distance
        hexstart = "%04X" % startaddr
        hexend = "%04X" % endaddr
        command = "%s.%s" % (hexstart, hexend)
        self.writedata_lf(command)
        return self.readdata(termstring)

    def putdata(self, start, length, data, startpattern):
        datavalues = list()
        packetlength = 64
        for d in data:
            datavalues.append(int(d))
        print("starting transfer of data with length:%04x" % length)
        pointer = start
        count = 0
        while count < length:
            packetdata = ""
            checksum = 0
            for d in range(packetlength):
                item = datavalues[d+count]
                packetdata += "%02X " % item
                checksum += item
            packetdata = packetdata[:-1]
            checksum = checksum & 0xFFFF
            headerchecksum = (packetlength + pointer) & 0xFFFF
            sendpacket = "%s%02X %04X %04X %s %04X" % (startpattern, packetlength, pointer, headerchecksum, packetdata, checksum)
            sendfailed = True
            while sendfailed:
                if True:
                    self.writedata(sendpacket)
                    # print(sendpacket)
                    # time.sleep(0.1)
                    status = self.getstatus()
                    if status.find("OK") >= 0:
                        print("Max:%04X Status of %04X OK, Message is:%s" % (length + start, pointer, status))
                        sendfailed = False
                    else:
                        print("Max:%04X Status of %04X NOT OK, Messages is:%s" % (length + start, pointer, status))
                        sendfailed = True
                else:
                    sendfailed = False
                    print(sendpacket)
            pointer = pointer + packetlength
            count = count + packetlength

    def getstatus(self):
        error = 0
        receiveddata = "no data"
        try:
            r = self.serconn.readline()
        except:
            return "SerialException in getstatus"
        try:
            receiveddata = r.decode("ascii").strip()
        except:
            return "error during decode in getstatus"
        return receiveddata

    def putbyterange(self):
        # for this test function, the receiving program looks like this:
        # byte in, retval, chars_to_read;
        # char ch;
        # println("Serialtest:");
        # retval = 0;
        # while (retval == 0) {
        #     chars_to_read = avail();
        #     if (chars_to_read > 0) {
        #         ch = getch();
        #         in = ch;
        #         println(in);
        #     }
        # }
        # the program receives one byte and converts it to a hex value to
        # send it back with a cr+lf at the end of line
        print("putbyterange")
        s = bytearray()
        for i in range(256):
            s.append(i)
        idx = 0
        while idx < len(s):
            # self.writedataraw(x)
            i = 0
            t = bytearray()
            t.append(s[idx+i])
            readcount = 1
            while readcount > 0:
                readcount = self.serconn.inWaiting()
                y = self.serconn.read(readcount)
            self.serconn.write(t)   # write bytearray with one item
            time.sleep(0.05)
            y = self.serconn.readline().decode("ascii").strip()
            if t[0] != y:
                print("out:%02X in:%s" % (t[0], y))
            idx += 1
        print("End")

datatransfer = "normal"
pars = argparse.ArgumentParser()
pars.add_argument("--startaddress", help="set startaddress to download the data")
pars.add_argument("--woz", help="set wozmon monitor program for download data", action="store_true")
pars.add_argument("--fastmode", help="setting communication to fast method", action="store_true")
pars.add_argument("--testmode", help="set specific testmode")
args = pars.parse_args()
if not args:
    print("no arguments given, setting downloadaddress to 0x0200")
    print("and setting download method to bb-communication")
    address = 0x0200 # address to upload to
if args.woz:
    datatransfer = "wozmode"
else:
    wozmon_communication = False
if args.startaddress:
    address = "%04X" % args.startaddress
else:
    address = 0x200
if args.testmode:
    datatransfer = args.testmode
if args.fastmode:
    datatransfer = "fastmode"

print("sys.platform is:%s" % sys.platform)
# Microsoft Windows Version of Path on my Computer (insert your path here)
if sys.platform == "win32":
    print("open data for win32 platform")
    towritedata = open("C:\\Users\\mf\\github\\ccpy65\\asmtest\\a.out", "rb")
if sys.platform == "cygwin":
    print("open data for win32 platform with cygwin")
    towritedata = open("C:\\Users\\mf\\github\\ccpy65\\asmtest\\a.out", "rb")
# Apple Macintosh Version of Path on my Computer
if sys.platform == "darwin":
    towritedata = open("/Users/mf/github/ccpy65/asmtest/a.out", "rb")
if sys.platform == "linux":
    towritedata = open("/home/mf/github/ccpy65/asmtest/a.out", "rb")
#
newdata = towritedata.read()
towritedata.close()
length = grepcode(newdata, [0xFE, 0xED, 0xC0, 0xDE])
print("length is:%d (0x%04X)" % (length, length))
if (length == -1):
    print("Pattern not found, exit")
    sys.exit(0)
writedata = datastore()
writedata.insertbinfile(address, length, newdata)
checkok = writedata.checkdata(address, address+length)
if not checkok:
    print("check is not ok, data is invalid")
    sys.exit(1)
cmds = writedata.returncmds(address)
try:
    # this is the windows version of my serial connection 
    if sys.platform == "win32":
        comm = SerialConn("COM4")
    # this is the apple macintosh version of my serial connection
    if sys.platform == "darwin":
        comm = SerialConn("/dev/cu.usbserial-14230")
    if sys.platform == "linux":
        comm = SerialConn("/dev/ttyS0")
    if sys.platform == "cygwin":
        comm = SerialConn("/dev/ttyS3")
except:
    print("Problems to open the serial connection, is your terminal program running?")
    sys.exit(1)
if datatransfer == "fastmode":
    comm.putdata(address, length, newdata, "+")
elif datatransfer == "wozmode":
    for c in cmds:
        comm.putcommand(address + length, c)
elif datatransfer == "normal":
    comm.putdata(address, length, newdata, "*")
elif datatransfer == "byterange":
    print("putbyterange called")
    comm.putbyterange()
else:
    print("unknown datatransfer mode: %s" % datatransfer)
comm.close()
print("done")
