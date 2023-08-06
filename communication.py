#!/usr/bin/python3
import serial
import time
import sys

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
        self.serconn = serial.Serial(port=device, baudrate=19200, bytesize=8, stopbits=2, parity='N', timeout=1, xonxoff=0, rtscts=0)
        self.isopen = self.serconn.is_open

    def close(self):
        self.serconn.close()

    def writedata(self, sendline):
        tosystem = sendline + "\r"
        self.serconn.write(tosystem.encode())
        self.serconn.flush()

    def readdata(self, termstring):
        dlines = list()
        linecount = 0
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
            except UnicodeDecodeError as e:
                print("\nerror at decode at line: %s" % r)
                return list()
            dlines.append(receiveddata)
            linecount += 1
        return dlines

    def commoperation(self):
        self.writedata('8000.8007')
        result = self.readdata()
        for l in result:
            print(l)

    def putcommand(self, cmd):
        cmd = cmd.strip()
        # print("commnd:%s" % cmd)
        termstring = cmd[0:5]
        startaddress = int("0x%s" % cmd[0:4], base=16)
        isok = False
        while not isok:
            self.writedata(cmd)
            result = self.readdata(termstring)
            endaddress = startaddress + 8
            checkcmd = "%04X.%04X" % (startaddress, endaddress)
            self.writedata(checkcmd)
            termstring = "%04X:" % endaddress
            result = self.readdata(termstring)
            found = ""
            for l in result:
                if len(l) > 28:
                    found = l.strip()
            if len(result) < 2:
                isok = False
            else:
                # print("%s,%s" % (cmd, found))
                if cmd == found:
                    isok = True
                else:
                    isok = False
        print(found)

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
        self.writedata(command)
        return self.readdata(termstring)

    def garbage(self):
        try:
            ser.write(b'\n\r')
            ser.write(b'8000.A000\n\r')
            ser.flush()
            s = "none"
            while True:
                try:
                    s = ser.readline()
                except OSError as e:
                    print("----------------- OSError ----------------------")
                    print(e)
                print(s)
                if len(s) < 2:
                    ser.write(b"8000.A000\n\r")
                    ser.flush()
        except KeyboardInterrupt:
            ser.close()
            print("Keyboard Interrupt, closeing serial connection")

        print(ser.is_open)
        ser.close()


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



address = 0x0200

towritedata = open("C:\\Users\\mf\\src\\asmtest\\a.out", "rb")
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
    comm = SerialConn("COM4")
except:
    print("Problems to open the serial connection, is your terminal program running?")
    sys.exit(1)
for c in cmds:
    comm.putcommand(c)
    #time.sleep(0.1)
comm.close()

sys.exit(0)
stor = datastore()
# comm.commoperation()
address = 0x8000
lastaddress = 0x8790
dist = 32
while address < lastaddress:
    endaddr = str("%04X" % (address + dist - 8)) + ':'
    print("(%04X,%04X);" % (address, address + dist),flush=True,end="")
    fromhost = comm.getmemorylinesat(address, dist - 1, endaddr)
    if len(fromhost) == 0:
        print("\nError during communication, at address:%04X" % address)
        # empty buffer until timeout
        comm.emptybuffer()
    else:
        checkok = stor.getmemdump(fromhost)
        if checkok:
            checkok = stor.checkdata(address, address + dist)
            if checkok:
                address += dist
print()
checkok = stor.checkdata(address, lastaddress)
if not checkok:
    print("check is not ok, data is invalid")
    sys.exit(1)
stor.listdata()

print("done")