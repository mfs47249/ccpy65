from preprocessor import preprocessor
from dotoken import dotoken
from storetokens import storetokens, objects

from os.path import exists, join
from argparse import ArgumentParser
import sys
import inspect as insp

class filedata:
    ch = ' '
    lasttoken = ''
    debug = False
    debugscanner = False
    debuggetch = False
    debugpreprocessor = False
    alphaset = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','_']
    alphaset += ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    numberset = ['0','1','2','3','4','5','6','7','8','9','.']
    octalset = ['0','1','2','3','4','5','6','7']
    hexnumberset = ['$','0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','a','b','c','d','e','f','.']
    whitespace = [' ', '\t', '\a', '\n']
    specialchars = [' ','!','"','§','$','%','&','/','\\','(',')','=','?','´','`','^','°','@',',',';','.',':','-','_','{','}','[',']' ]


    def __init__(self, fp, fd, debugflag=False):
        self.fp = fp
        self.fd = fd
        self.idx = 0
        self.debug = debugflag
        self.debugwhitespace = False
        self.linenumber = 1
        self.column = 1

    def getfname(self, frame):
        classname = __class__.__name__
        funcname = insp.getframeinfo(frame).function
        return classname + '.' + funcname

    def getfilepath(self):
        return self.fp

    def getch(self, debug=False):
        if self.debuggetch:
            print("fp: %30s, idx: %08d:  %s" % (self.fp, self.idx, self.fd[self.idx]))
        if self.idx < len(self.fd):
            achar = self.fd[self.idx]
        else:
            achar = ''
        self.idx += 1
        self.ch = achar
        self.column += 1
        if achar == '\n':
            self.linenumber += 1
            self.column = 1
        return achar

    def ungetch(self):
        self.idx -= 1
        self.column -= 1
        if self.column < 1:
            self.column = 0
        self.ch = self.fd[self.idx]
        return self.ch

    def printdata(self):
        print("Filepath = %s" % self.fp)
        self.idx = 0
        while self.idx < len(self.fd):
            self.getch(debug=True)
        self.idx = 0  # reset filepointer to beginning

    def processpreprocessor(self):
        while self.ch != '\n':
            self.lasttoken += self.ch
            self.ch = self.getch()
        self.ch = ' '
        if self.debugpreprocessor:
            print("%30s, lasttoken:'%s'" % (insp.getframeinfo(insp.currentframe()).function, self.lasttoken))
        prepro.processline(self.lasttoken)
        return self.lasttoken

    def processstartblock(self):
        self.getch()
        self.lasttoken = "startblock"
        tokens.addtoken(self.lasttoken, self.lasttoken, self.linenumber)
        if self.debugscanner:
            print("%30s, lasttoken:'%s'" % (self.getfname(insp.currentframe()), self.lasttoken))
        return

    def processendblock(self):
        self.lasttoken = "endblock"
        tokens.addtoken(self.lasttoken, self.lasttoken, self.linenumber)
        if self.debugscanner:
            print("%30s, lasttoken:'%s'" % (self.getfname(insp.currentframe()), self.lasttoken))
        return

    def processsquareopen(self):
        self.lasttoken = "squareopen"
        tokens.addtoken(self.lasttoken, self.lasttoken, self.linenumber)
        if self.debugscanner:
            print("%30s, lasttoken:'%s'" % (self.getfname(insp.currentframe()), self.lasttoken))
        return

    def processsquareclose(self):
        self.lasttoken = "squareclose"
        tokens.addtoken(self.lasttoken, self.lasttoken, self.linenumber)
        if self.debugscanner:
            print("%30s, lasttoken:'%s'" % (self.getfname(insp.currentframe()), self.lasttoken))
        return


    def processunknown(self):
        self.lasttoken = "unknown"
        tokens.addtoken(self.lasttoken, self.lasttoken, self.linenumber)
        if self.debugscanner:
            print("%30s, lasttoken:'%s'" % (self.getfname(insp.currentframe()), self.lasttoken))
        return

    def processopenbracket(self):
        self.lasttoken = "openbracket"
        tokens.addtoken(self.lasttoken, self.lasttoken, self.linenumber)
        if self.debugscanner:
            print("%30s, lasttoken:'%s'" % (self.getfname(insp.currentframe()), self.lasttoken))
        return
        
    def processclosebracket(self):
        self.lasttoken = "closebracket"
        tokens.addtoken(self.lasttoken, self.lasttoken, self.linenumber)
        if self.debugscanner:
            print("%30s, lasttoken:'%s'" % (self.getfname(insp.currentframe()), self.lasttoken))
        return

    def processsemicolon(self):
        self.lasttoken = "semicolon"
        tokens.addtoken(self.lasttoken, self.lasttoken, self.linenumber)
        if self.debugscanner:
            print("%30s, lasttoken:'%s'" % (self.getfname(insp.currentframe()), self.lasttoken))
        return

    def processcolon(self):
        self.lasttoken = "colon"
        tokens.addtoken(self.lasttoken, self.lasttoken, self.linenumber)
        return

    def processhash(self):
        self.lasttoken = "hash"
        if self.column == 2:
            hashitem = ""
            nextchar = self.getch()
            while nextchar in self.alphaset:
                hashitem += nextchar
                nextchar = self.getch()
            if hashitem == "include":
                nextchar = self.getch()
                while nextchar != "<":
                    nextchar = self.getch()
                includefile = ""
                nextchar = self.getch()
                while nextchar != ">":
                    includefile += nextchar
                    nextchar = self.getch()
                self.lasttoken = "doincludefile"
                self.lastincludefile = includefile
                tokens.addtoken(includefile, "preprocessor", self.linenumber)
                return
            else:
                for i in hashitem:
                    self.ungetch()
                self.lasttoken = "hash"
        tokens.addtoken(self.lasttoken, self.lasttoken, self.linenumber)
        return

    def processstar(self):
        new_t_type = ""
        new_t_value = ""
        nextchar = self.getch()
        if nextchar == '*':
            self.lasttoken = "starstar" # was pointerpointer
            new_t_type = "starstar"
            new_t_value = "pointerpointer"
        elif nextchar == ' ':
            self.lasttoken = "star"
            new_t_type = "star"
            new_t_value = "pointer"
        else:
            self.lasttoken = "star" # was "pointer"
            new_t_type = "star"
            new_t_value = "pointer"
            self.ungetch()
        tokens.addtoken(new_t_type, new_t_value, self.linenumber)
        if self.debugscanner:
            print("%30s, lasttoken:'%s'" % (self.getfname(insp.currentframe()), self.lasttoken))
        return
    
    def processpointer(self):
        last_token = "nextalphaispointer"
        tokens.addtoken(last_token, last_token, self.linenumber)
        if self.debugscanner:
            print("%30s, lasttoken:'%s'" % (self.getfname(insp.currentframe()), self.lasttoken))
        return


    def processplus(self):
        nextchar = self.getch()
        if nextchar == '+':
            self.lasttoken = "plusplussign"
        else:
            self.ungetch()
            self.lasttoken = "plussign"
        tokens.addtoken(self.lasttoken, self.lasttoken, self.linenumber)
        if self.debugscanner:
            print("%30s, lasttoken:'%s'" % (self.getfname(insp.currentframe()), self.lasttoken))
        return

    def processminus(self):
        nextchar = self.getch()
        if nextchar == '-':
            self.lasttoken = "minusminussign"
        else:
            self.ungetch()
            self.lasttoken = "minussign"
        tokens.addtoken(self.lasttoken, self.lasttoken, self.linenumber)
        if self.debugscanner:
            print("%30s, lasttoken:'%s'" % (self.getfname(insp.currentframe()), self.lasttoken))
        return

    def processequal(self):
        nextchar = self.getch()
        if nextchar == '=':
            self.lasttoken = "equalequal"
        elif nextchar == '<':
            self.lasttoken = "equalsmaller"
        elif nextchar == '>':
            self.lasttoken = "equalgreater"
        else:
            self.ungetch()
            self.lasttoken = "equals"
        tokens.addtoken(self.lasttoken, self.lasttoken, self.linenumber)
        if self.debugscanner:
            print("%30s, lasttoken:'%s'" % (self.getfname(insp.currentframe()), self.lasttoken))
        return

    def processsmaller(self):
        nextchar = self.getch()
        if nextchar == '=':
            self.lasttoken = "smallerequal"
        else:
            self.ungetch()
            self.lasttoken = "smaller"
        tokens.addtoken(self.lasttoken, self.lasttoken, self.linenumber)
        if self.debugscanner:
            print("%30s, lasttoken:'%s'" % (self.getfname(insp.currentframe()), self.lasttoken))
        return

    def processgreater(self):
        nextchar = self.getch()
        if nextchar == '=':
            self.lasttoken = "greaterequal"
        else:
            self.ungetch()
            self.lasttoken = "greater"
        tokens.addtoken(self.lasttoken, self.lasttoken, self.linenumber)
        if self.debugscanner:
            print("%30s, lasttoken:'%s'" % (self.getfname(insp.currentframe()), self.lasttoken))
        return

    def processnot(self):
        nextchar = self.getch()
        if nextchar == '=':
            self.lasttoken = "notequal"
        else:
            self.lasttoken = "not"
            self.ungetch()
        tokens.addtoken(self.lasttoken, self.lasttoken, self.linenumber)
        if self.debugscanner:
            print("%30s, lasttoken:'%s'" % (self.getfname(insp.currentframe()), self.lasttoken))
        return

    def processcomma(self):
        self.lasttoken = "comma"
        tokens.addtoken(self.lasttoken, self.lasttoken, self.linenumber)
        if self.debugscanner:
            print("%30s, lasttoken:'%s'" % (self.getfname(insp.currentframe()), self.lasttoken))
        return

    def processnumber(self):
        self.lasttoken += self.ch
        character = self.ch
        while self.getch() in self.numberset:
            self.lasttoken += self.ch
        if self.ch == 'x':
            self.lasttoken = ""
            while self.getch() in self.hexnumberset:
                self.lasttoken += self.ch
            self.lasttoken = "%d" % int(self.lasttoken, 16)
        tokens.addtoken(self.lasttoken, "number", self.linenumber)
        if self.debugscanner:
            print("%30s, lasttoken:'%s'" % (self.getfname(insp.currentframe()), self.lasttoken))
        self.ungetch()
        return self.lasttoken

    def processampersand(self):
        self.lasttoken = "ampersand"
        tokens.addtoken(self.lasttoken, self.lasttoken, self.linenumber)
        if self.debugscanner:
            print("%30s, lasttoken:'%s'" % (self.getfname(insp.currentframe()), self.lasttoken))
        return

    def processpercentchar(self):
        self.lasttoken = "percent"
        tokens.addtoken(self.lasttoken, self.lasttoken, self.linenumber)
        if self.debugscanner:
            print("%30s, lasttoken:'%s'" % (self.getfname(insp.currentframe()), self.lasttoken))
        return


    def processdollarsign(self):
        self.lasttoken = "dollarsign"
        tokens.addtoken(self.lasttoken, self.lasttoken, self.linenumber)
        if self.debugscanner:
            print("%30s, lasttoken:'%s'" % (self.getfname(insp.currentframe()), self.lasttoken))
        return
        # previous implementation skipped, because hexnumbers in c are defined by 0x...
        while self.ch in self.hexnumberset:
            self.lasttoken += self.ch
            self.ch = self.getch()
        tokens.addtoken(self.lasttoken, "hexnumber", self.linenumber)
        if self.debugscanner:
            print("%30s, lasttoken:'%s'" % (self.getfname(insp.currentframe()), self.lasttoken))
        return self.lasttoken


    def isinlist(self, value, values):
        found = False
        for v in values:
            if v == value:
                return True
        return False

    def processalpha(self):
        self.lasttoken += self.ch
        while self.getch() in self.alphaset + self.numberset:
            self.lasttoken += self.ch
        stok = stokens.get(self.lasttoken)
        if stok != None:
            attribs = stok.getattributes()
            if self.isinlist("mnemonic", attribs):
                tokens.addtoken(self.lasttoken, "mnemonic", self.linenumber)
            else:
                tokens.addtoken(self.lasttoken, "alpha", self.linenumber)
        else:
            tokens.addtoken(self.lasttoken, "alpha", self.linenumber)
        if self.debugscanner:
            print("%30s, lasttoken:'%s'" % (self.getfname(insp.currentframe()), self.lasttoken))
        self.ungetch()
        return self.lasttoken

    def processstartchar(self):
        self.lasttoken = "charconst"
        if self.debugscanner:
            print("%30s, lasttoken:'%s'" % (self.getfname(insp.currentframe()), self.lasttoken))
        return

    def processstartstring(self):
        self.lasttoken = ""
        achar = self.getch()
        while achar != '"' and achar in self.alphaset + self.numberset + self.specialchars:
            self.lasttoken += achar
            achar = self.getch()
        tokens.addtoken(self.lasttoken, "type_stringconst", self.linenumber)
        if self.debugscanner:
            print("%30s, lasttoken:'%s'" % (self.getfname(insp.currentframe()), self.lasttoken))
        return self.lasttoken

    def processslashchar(self):
        achar = self.getch()
        if achar == '*':
            while True:
                while achar != '*':
                    achar = self.getch()
                achar = self.getch()
                if achar == '/':
                    break
        elif achar == '/':
            while True:
                achar = self.getch()
                if achar == '\n' or achar == '\a':
                    break
        else:
            self.lasttoken = "slash"
            tokens.addtoken(self.lasttoken, self.lasttoken, self.linenumber)
            if self.debugscanner:
                print("%30s, lasttoken:'%s'" % (self.getfname(insp.currentframe()), self.lasttoken))
        return self.lasttoken

    def processdata(self, instance):
        self.idx = 0
        while self.idx < len(self.fd):
            while self.getch() in self.whitespace:
                self.lasttoken = ''
                if self.debugwhitespace:
                    print("whitespace:'%s'" % self.ch)
            if False and self.debugscanner:
                print("next char is:'%s'" % self.ch)
            if self.ch == '#':
                self.processhash()
                # self.processpreprocessor()
            elif self.ch in self.numberset:
                self.processnumber()
            elif self.ch in self.alphaset:
                self.processalpha()
            elif self.ch == '&':
                self.processampersand()
            elif self.ch == '$':
                self.processdollarsign()
            elif self.ch == '{':
                self.processstartblock()
            elif self.ch == '}':
                self.processendblock()
            elif self.ch == '[':
                self.processsquareopen()
            elif self.ch == ']':
                self.processsquareclose()
            elif self.ch == ';':
                self.processsemicolon()
            elif self.ch == '(':
                self.processopenbracket()
            elif self.ch == ')':
                self.processclosebracket()
            elif self.ch == '*':
                nextch = self.getch()
                if nextch in self.whitespace:
                    self.ungetch()
                    self.processstar()
                else:
                    self.ungetch()
                    self.processpointer()
            elif self.ch == '=':
                self.processequal()
            elif self.ch == ':':
                self.processcolon()
            elif self.ch == '<':
                self.processsmaller()
            elif self.ch == '>':
                self.processgreater()
            elif self.ch == '!':
                self.processnot()
            elif self.ch == ',':
                self.processcomma()
            elif self.ch == '+':
                self.processplus()
            elif self.ch == '-':
                self.processminus()
            elif self.ch == '"':
                self.processstartstring()
            elif self.ch == "'":
                self.processstartchar()
            elif self.ch == "/":
                self.processslashchar()
            elif self.ch == "%":
                self.processpercentchar()
            else:
                print("character not tokenize, last ch read was:%s" % (self.ch))
            if self.lasttoken == "doincludefile":
                print("#include <%s>" % self.lastincludefile)
                fullpath = instance.searchincludepathsforfile(self.lastincludefile)
                ifd = instance.readsinglefile(self.lastincludefile)
                ifd.processdata(instance)
            if self.debugscanner:
                print("lasttoken: %s" % (self.lasttoken))
            self.lasttoken = ""

class findinincludelist:
    incllist = []

    def __init__(self, includedirs):
        includedirs.append(".")
        for icldir in includedirs:
            self.incllist.append(icldir)
    
    def findfile(self, filename):
        for includepath in self.incllist:
            checkpath = join(includepath, filename)
            if  exists(checkpath):
                return checkpath
        return None

    def getlist(self):
        return self.incllist

class initsystem:
    ccargs = []
    fil = []
    debugflag = False
    allfiles = []
    filedatalist = []
    includefiles = []
    filedatalist = []
    outfilepath = "aout.s"
    varstart = 0x8000
    heapstart = 0x6000
    progstart = 0x0200

    def __init__(self):
        ap = ArgumentParser(description="ccpy65: accept the following options:")
        ap.add_argument("-V", "--version", help="show version info", action="store_true")
        ap.add_argument("--debug", help="set debugmode on", action="store_true")
        ap.add_argument("--debug2", help="set debugoption 2 on", action="store_true")
        ap.add_argument("-v", "--verbosity", help="set verbosity level to 0 < N < 10")
        ap.add_argument("-f", "--file", help="use file for input")
        ap.add_argument("-o", "--outfile", help="namepath for output file")
        ap.add_argument("-I", "--include", action="append", help="include path")
        ap.add_argument("-s", "--varstart", help="set startaddress of varmemory (decimal), above memory is reserved for global var,\n below is reserved for stack until heapstart")
        ap.add_argument("-g", "--heapstart", help="set startaddress of heap (decimal), heap will be reserved\n below until codesegment ist reached")
        ap.add_argument("-p", "--progstart", help="set start of program")
        ap.add_argument("files", type=str, nargs="+", help="list of files")
        self.ccargs = vars(ap.parse_args())
        if self.ccargs["debug"] == True:
            self.debugflag = True
            print("debugging is true")
            print("Arguments are:")
            print(self.ccargs)
        if self.ccargs["file"] != None:
            self.allfiles.append(self.ccargs["file"])
            self.readfile(self.allfiles)
        if self.ccargs["include"] != None:
            if self.debugflag:
                print("include dirs set:")
                print(self.ccargs["include"])
        if self.ccargs["outfile"] != None:
            self.outfilepath = self.ccargs['outfile']
        if self.ccargs["varstart"] != None:
            a_varstart = self.ccargs['varstart']
            if a_varstart[0:2] == "0x":
                print("varstart is a hex number")
                self.varstart = int(a_varstart, 16)
            else:
                self.varstart = int(a_varstart)
            print("varstart is:%04X, decimal:%d" % (self.varstart, self.varstart))
        if self.ccargs["heapstart"] != None:
            a_heapstart = self.ccargs['heapstart']
            if a_heapstart[0:2] == "0x":
                print("heapstart is a hex number")
                self.heapstart = int(a_heapstart, 16)
            else:
                self.heapstart = int(a_heapstart)
            print("Heap Start is:%04X, decimal:%d" % (self.heapstart, self.heapstart))
        if self.ccargs["progstart"] != None:
            a_progstart = self.ccargs['progstart']
            if a_progstart[0:2] == "0x":
                print("progstart is a hex number")
                self.progstart = int(a_progstart, 16)
            else:
                self.progstart = int(a_progstart)
            print("Program Start is:%04X, decimal:%d" % (self.progstart, self.progstart))

        self.searchincludepath()
        if len(self.includefiles) > 0:
            self.readfile(self.includefiles)

    def getdebugflag(self):
        return self.debugflag

    def getoutfilepath(self):
        return self.outfilepath

    def getvarstart(self):
        return self.varstart

    def getprogstart(self):
        return self.progstart

    def searchincludepath(self):
        self.fil = findinincludelist(self.ccargs["include"])
        for onefile in self.ccargs['files']:
            if self.debugflag:
                print("search for file: %s" % onefile)
            ifile = self.fil.findfile(onefile)
            print("includefile found: %s" % ifile)
            self.includefiles.append(ifile)
      
    def searchincludepathsforfile(self, filename):
        self.fil = findinincludelist(self.ccargs["include"])
        ifile = self.fil.findfile(filename)
        return ifile

    def readfile(self, allfiles):
        if self.debugflag:
            for filepath in allfiles:
                print("readfile called, filepath is: %s" % filepath)
        for filepath in allfiles:
            of = open(filepath, "r")
            lines = of.read()
            self.filedatalist.append(filedata(filepath, lines, debugflag=self.debugflag))
            of.close()

    def readsinglefile(self, singlefile):
        if self.debugflag:
            print("readsinglefile called, filepath is: %s" % singlefile)
        ifile = self.searchincludepathsforfile(singlefile)
        of = open(ifile, "r")
        lines = of.read()
        sfd = filedata(filepath, lines, debugflag=self.debugflag)
        of.close()
        return sfd

    def getfiledatalist(self):
        return self.filedatalist
    
    def printcontent(self):
        for fd in self.filedatalist:
            fd.printdata()

    def getfil(self):
        return self.fil


if __name__ == "__main__":
    instance = initsystem()
    prepro = preprocessor(searchpath=instance.getfil().getlist(), debugflag=instance.getdebugflag())
    tokens = dotoken(debugflag=instance.getdebugflag())
    stokens = tokens.getstokens()
    fdl = instance.getfiledatalist()
    for fd in fdl:
        filepath = fd.getfilepath()
        tokens.setfilename(filepath)
        fd.processdata(instance)
    # tokens.listtokens()
    # tokens.listall()
    tokens.emit(instance.getvarstart(), instance.getprogstart(), instance.getoutfilepath())
    tokens.close()
    # tokens.listalluserdefined()