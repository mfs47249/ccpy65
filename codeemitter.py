import sys
import random, string

   
from storetokens import storetokens, objects


registerconvert = { 
            "_unireg0_0" : "_unireg0_0",
            "_unireg0_1" : "_unireg0_1",
            "_unireg0_2" : "_unireg0_2",
            "_unireg0_3" : "_unireg0_3",
            "_unireg0_4" : "_uniregA_0",
            "_unireg0_5" : "_uniregA_1",
            "_unireg0_6" : "_uniregA_2",
            "_unireg0_7" : "_uniregA_3",

            "_unireg1_0" : "_unireg1_0",
            "_unireg1_1" : "_unireg1_1",
            "_unireg1_2" : "_unireg1_2",
            "_unireg1_3" : "_unireg1_3",
            "_unireg1_4" : "_uniregB_0",
            "_unireg1_5" : "_uniregB_1",
            "_unireg1_6" : "_uniregB_2",
            "_unireg1_7" : "_uniregB_3",

            "_unireg2_0" : "_unireg2_0",
            "_unireg2_1" : "_unireg2_1",
            "_unireg2_2" : "_unireg2_2",
            "_unireg2_3" : "_unireg2_3",
            "_unireg2_4" : "_uniregC_0",
            "_unireg2_5" : "_uniregC_1",
            "_unireg2_6" : "_uniregC_2",
            "_unireg2_7" : "_uniregC_3",

            "_unireg3_0" : "_unireg3_0",
            "_unireg3_1" : "_unireg3_1",
            "_unireg3_2" : "_unireg3_2",
            "_unireg3_3" : "_unireg3_3",
            "_unireg3_4" : "_uniregD_0",
            "_unireg3_5" : "_uniregD_1",
            "_unireg3_6" : "_uniregD_2",
            "_unireg3_7" : "_uniregD_3",

            "_unireg4_0" : "_unireg4_0",
            "_unireg4_1" : "_unireg4_1",
            "_unireg4_2" : "_unireg4_2",
            "_unireg4_3" : "_unireg4_3",
            "_unireg4_4" : "_uniregE_0",
            "_unireg4_5" : "_uniregE_1",
            "_unireg4_6" : "_uniregE_2",
            "_unireg4_7" : "_uniregE_3",

            "_unireg5_0" : "_unireg5_0",
            "_unireg5_1" : "_unireg5_1",
            "_unireg5_2" : "_unireg5_2",
            "_unireg5_3" : "_unireg5_3",
            "_unireg5_4" : "_uniregF_0",
            "_unireg5_5" : "_uniregF_1",
            "_unireg5_6" : "_uniregF_2",
            "_unireg5_7" : "_uniregF_3",

            "_unireg6_0" : "_unireg6_0",
            "_unireg6_1" : "_unireg6_1",
            "_unireg6_2" : "_unireg6_2",
            "_unireg6_3" : "_unireg6_3",
            "_unireg6_4" : "_uniregG_0",
            "_unireg6_5" : "_uniregG_1",
            "_unireg6_6" : "_uniregG_2",
            "_unireg6_7" : "_uniregG_3",
            
            "_unireg7_0" : "_unireg7_0",
            "_unireg7_1" : "_unireg7_1",
            "_unireg7_2" : "_unireg7_2",
            "_unireg7_3" : "_unireg7_3",
            "_unireg7_4" : "_uniregH_0",
            "_unireg7_5" : "_uniregH_1",
            "_unireg7_6" : "_uniregH_2",
            "_unireg7_7" : "_uniregH_3",
}

class varobject:
    def __init__(self, funcname, varname, vartype, namespace):
        self.namespace = namespace
        self.funcname = funcname
        self.varname = varname
        self.vartype = vartype
        self.varaddress = 0
        self.stoken = None

    def setstoken(self, token):
        self.stoken = token

    def getstoken(self):
        return self.stoken

    def setnamespace(self, nspace):
        self.namespace = nspace

    def getnamespace(self):
        return self.namespace

    def setvaradress(self, address):
        self.varaddress = address

    def getaddress(self):
        return self.varaddress

    def getfuncname(self):
        return self.funcname

    def getvarname(self):
        return self.varname

    def getvartype(self):
        return self.vartype

    def getnamespacename(self):
        return self.funcname + '_' + self.varname

    def getnamewithnamespace(self):
        return self.funcname + '_' + self.varname


class funcdef:
    def __init__(self, functionname, type_return, stoken):
        self.functionname = functionname
        self.namespace = "global"
        self.type_return = type_return
        self.arg_objects = list()
        self.funcstoken = stoken
        self.argaddress = 0
        self.subroutine = ""
        # self.printinfo()
    
    def printinfo(self):
        print("Name:%s, Type:%s, Adress:%d" % (self.functionname, self.type_return, self.argaddress))

    def addvar(self, funcname, varname, vartype, namespace):
        varo = varobject(funcname, varname, vartype, namespace)
        varo.setvaradress(self.argaddress)
        self.arg_objects.append(varo)

    def getvar(self):
        return self.arg_objects

    def getfuncname(self):
        return self.functionname

    def getreturntype(self):
        return self.type_return

    def getargaddress(self):
        return self.argaddress

    def setargaddress(self, newaddress):
        self.argaddress = newaddress

    def setsubroutine(self, routinename):
        self.subroutine = routinename

    def getsubroutine(self):
        return self.subroutine

class codeline:
    linelabel = ""
    lineopcode = ""
    linevalue = ""
    linecomment = ""

    def __init__(self, label,opcode,value,comment):
        self.linelabel = label
        self.lineopcode = opcode
        self.linevalue = value
        self.linecomment = comment
    
    def getcodeline(self):
        assemblerline = self.linelabel + self.lineopcode + self.linevalue + self.linecomment
        return assemblerline

class subroutine:
    sourcelineno = 0
    assemblerline = ""
    codelines = []
    subroutinename = ""

    def __init__(self, subroutinename):
        self.codelines = []
        self.subroutinename = subroutinename
        startline = codeline(subroutinename, "", "", "")
        self.codelines.append(startline)

    def getname(self):
        return self.subroutinename

    def appendcodeline(self, label,opcode,value,comment):
        oneline = codeline(label,opcode,value,comment)
        self.codelines.append(oneline)

    
    def debugoutall(self):
        for x in self.codelines:
            assemblerline = x.linelabel + x.lineopcode + x.linevalue + x.linecomment
            print(assemblerline)

    def getlist(self):
        return self.codelines

class codeemitter:
    assemberline = 0
    labelwidth = 30
    opcodeswidth = 10
    valueswidth = 25
    linelabel = ""
    lineopcode = ""
    linevalue = ""
    linecomment = ""
    assemblerline = ""
    labelcount = 0
    outfilepath = "aout.s"
    varstartaddress = 0
    internalvarcounter = 0
    expr_stack_index = "_unireg7"
    debug_espression = False
    subroutinebuffer = []
    createsubroutine = False
    actualsubroutine = None
    createvirtsub = True

    def __init__(self, assemblerpath, stokens, blocks, log):
        self.stokens = stokens
        self.clearoutput()
        self.outfilepath = assemblerpath
        self.varstartaddress = 0
        self.internalvarcounter = self.varstartaddress
        self.log = log
        self.opset6502_save_register = False
        self.blocks = blocks
        self.blocks.setactivefunctionname("global")
        self.eval_sizeforvar = 18       # max longlong value
        self.kim_precvalue = 10         # kimath precision value
        self.kim_extradigit = 2         # kimath extra value

    def pushcpureg(self, startcomment=""):
        self.createcode("PHA","",startcomment)
        self.createcode("TXA", "","push everything on stack for save")
        self.createcode("PHA", "","save x-register")
        self.createcode("TYA")
        self.createcode("PHA", "","save y-register")

    def popcpureg(self):
        self.createcode("PLA","", "restore y-register")
        self.createcode("TAY")
        self.createcode("PLA","", "restore x-register")
        self.createcode("TAX")
        self.createcode("PLA","", "restore accu")

    def randomword(self, length):
        prefix = self.blocks.getactivefunctionname() + '_'
        letters = string.ascii_lowercase
        randomstring = prefix + ''.join(random.choice(letters) for i in range(length))
        return randomstring

    def randomconst(self, length):
        prefix = "virtsub_"
        letters = string.ascii_lowercase
        randomstring = prefix + ''.join(random.choice(letters) for i in range(length))
        return randomstring

    def checkhash(self, hash, value):
        try:
            res = hash[value]
            return True
        except KeyError as e:
            return False

    def isnotglobalfunc(self):
        return self.blocks.getactivefunctionname() != "global"

    def openoutfilepath(self, assemblerpath):
        self.outfilepath = assemblerpath
        self.assemblerout = open(self.outfilepath, "w")

    def close(self):
        self.assemblerout()

    def clearoutput(self):
        fmtstr = "%%-%ds" % self.labelwidth
        self.linelabel = fmtstr % ""
        fmtstr = "%%-%ds" % self.opcodeswidth
        self.lineopcode = fmtstr % ""
        fmtstr = "%%-%ds" % self.valueswidth
        self.linevalue = fmtstr % ""
        self.linecomment = ""

    def getvaraddress(self):
        return self.internalvarcounter

    def setvaraddress(self, newaddress):
        self.internalvarcounter = newaddress

    def setvarstart(self, startaddress):
        self.varstartaddress = startaddress
        self.internalvarcounter = self.varstartaddress

    def setlabel(self, labelname):
        fmtstr = "%%-%ds" % self.labelwidth
        self.linelabel = fmtstr % (labelname + ':')

    def setname(self, labelname):
        fmtstr = "%%-%ds" % self.labelwidth
        self.linelabel = fmtstr % (labelname)

    def setopcode(self, lineopcode):
        fmtstr = "%%-%ds" % self.opcodeswidth
        self.lineopcode = fmtstr % (lineopcode)

    def setvalue(self, linevalue):
        newvalue = str(linevalue)
        if len(newvalue) > 0 and newvalue[0] == '=':
            newvalue = '#' + newvalue[1:]
        fmtstr = "%%-%ds" % self.valueswidth
        self.linevalue = fmtstr % (newvalue)

    def setcomment(self, comment):
        self.linecomment = ";%s" % comment

    def addstring(self, stringname, string):
        self.actualsubroutine = subroutine(stringname)
        self.createsubroutine = True
        self.nonewsub = False
        self.createcode("ASCIIZ", string, "String added name:%s" % stringname)
        self.createsubroutine = False
        self.subroutinebuffer.append(self.actualsubroutine)
        self.actualsubroutine = None

    def startconvertedsubroutine(self, subname):
        if subname == "pfloatMX_w":
            xxx = 0
        self.createsubroutine = True
        for sub in self.subroutinebuffer:
            if sub.getname() == subname:
                self.nonewsub = True
                return
        self.nonewsub = False
        self.actualsubroutine = subroutine(subname)

    def stopconvertedsubroutine(self, noreturn=False):
        if self.nonewsub:
            self.createsubroutine = False
            return
        if not noreturn:
            self.createcode("RTS", "", "End automated Subroutine %s" % self.actualsubroutine.getname())
        self.createsubroutine = False
        self.subroutinebuffer.append(self.actualsubroutine)
        self.actualsubroutine = None

    def createassemberline(self):
        if self.createsubroutine:
            if self.nonewsub:
                return
            self.actualsubroutine.appendcodeline(self.linelabel, self.lineopcode, self.linevalue, self.linecomment)
        else:
            self.assemblerline = self.linelabel + self.lineopcode + self.linevalue + self.linecomment
            self.assemblerout.write(self.assemblerline + '\n')
        return self.assemblerline

    def handlesubroutines(self):
        for subroutine in self.subroutinebuffer:
            print("Append subroutinename:%s" % subroutine.getname())
            for oneline in subroutine.getlist():
                self.assemblerout.write(oneline.getcodeline() + '\n')

    def createlabel(self, label, opcode="", value="", comment=""):
        self.setlabel(label)
        self.setopcode(opcode)
        self.setvalue(value)
        self.setcomment(comment)
        return self.createassemberline()

    def createcode(self, code, value="", comment="", name=""):
        self.setname(name+' ')
        self.setopcode(code)
        self.setvalue(value)
        self.setcomment(comment)
        self.createassemberline()

    def createdefinition(self, name, code, value):
        self.setname(name+' ')
        self.setopcode(code)
        self.setvalue(value)
        self.createassemberline()

    def createcomment(self, comment):
        self.setname("; %s" % comment)
        self.setopcode("")
        self.setvalue("")
        self.setcomment("")
        self.createassemberline()

    def insertinline(self, opcode, arguments, linenumber, name="", comment="inline assembler from souceline:%d"):
        if opcode == "LABEL":
            self.setname(arguments)
            self.setopcode("")
            self.setvalue("")
            self.setcomment(comment % linenumber)
            self.createassemberline()
        elif opcode == "LEABYNAME":
            names = arguments.split(",")
            self.leabyname(names[0], names[1])
        else:
            self.setname(name)
            self.setopcode(opcode)
            self.setvalue(arguments)
            self.setcomment(comment % linenumber)
            self.createassemberline()

    def constintstatement(self, name, value, attributes):
        attribstr = ""
        for a in attributes:
            attribstr += a + ','
        attribstr = attribstr[:-1]
        self.createcode("","","CONSTINTSTATEMENT (name:%s, value:%s, attribs=%s)" % (name, value, attribstr))
        self.setname(name)
        self.setopcode("=")
        self.setvalue(value)
        self.setcomment("const %s = %s with %s"%(name,value,attribstr))
        return self.createassemberline()
    
    def constfloatstatement(self, name, value, attributes):
        attribstr = ""
        for a in attributes:
            attribstr += a + ','
        attribstr = attribstr[:-1]
        self.createcode("","","CONSTFLOATSTATEMENT (name:%s, value:%s, attribs=%s)" % (name, value, attribstr))
        self.setname(name)
        self.setopcode(".ASCIIZ")
        self.setvalue('"' + value + '"')
        self.setcomment("const %s = %s with %s"%(name,value,attribstr))
        return self.createassemberline()

    def constcharstatement(self, name, value, attributes):
        attribstr = ""
        for a in attributes:
            attribstr += a + ','
        attribstr = attribstr[:-1]
        fullname = self.blocks.getactivefunctionname() + '_' + name
        label = self.randomword(8)
        self.createcode("JMP",label ,"CONSTCHARSTATEMENT (name:%s, value:%s, attribs=%s)" % (fullname, value, attribstr))
        self.clearoutput()
        self.setcomment("const %s = \"%s\" with %s"%(fullname,value,attribstr))
        self.createassemberline()
        self.clearoutput()
        self.setname(fullname)
        self.setopcode(".ASCIIZ")
        self.setvalue('"' + value + '"')
        self.createassemberline()
        self.createcode("","","end of constcharstatement", name=label)
        return 

    def conststatement(self, name, value, attributes):
        attribstr = ""
        for a in attributes:
            attribstr += a + ','
        attribstr = attribstr[:-1]
        self.createcode("","","CONSTSTATEMENT (name:%s, value:%s, attribs=%s)" % (name, value, attribstr))
        self.setname(name)
        self.setopcode("EQU")
        self.setvalue("#" + value)
        self.setcomment("const %s = %s with %s"%(name,value,attribstr))
        return self.createassemberline()

    def createdebugout(self, string, cr=False):
        stringlabel = self.randomword(8)
        debuglabelend = self.randomword(8)
        createdebugloop = self.randomword(8)
        self.createcode("LDY", "#0")
        self.createcode("LDA", "%s,Y" % stringlabel, name=createdebugloop)
        self.createcode("BEQ", debuglabelend)
        self.createcode("JSR", "_OUTPUTCHAR")
        self.createcode("INY")
        self.createcode("JMP", createdebugloop)
        self.setname(stringlabel+' ')
        self.setopcode(".ASCIIZ")
        self.setvalue('"%s"' % string)
        self.setcomment("debugstring")
        self.createassemberline()
        self.createcode("byte","0","end of string c-like")
        if cr:
            self.createcode("JSR", "_OUTPUTCRLF", "end of debougoutput", name=debuglabelend)
        else:
            self.createcode("NOP", "", "end of debougoutput", name=debuglabelend)

    def printwozfloatMXininteger(self, wozfloatreg):
        m2loop = self.randomword(8)
        m2bkloop = self.randomword(8)
        m2rsloop = self.randomword(8)
        subsalt = self.randomconst(8)
        convertedsubname = "pfloatMX_w"
        if False and self.createvirtsub:
            self.createcode("","","Calling printwozfloatMXininteger as virtual Subroutine")
            self.startconvertedsubroutine(convertedsubname)
        self.createcode("LDX", "#7", "Printing wozfloat register M%d" % wozfloatreg)
        self.createcode("LDA", "X2,X", name=m2bkloop)
        self.createcode("STA", "_scratchregister,X")
        self.createcode("DEX")
        self.createcode("BPL", m2bkloop)
        if wozfloatreg == 1:
            self.createcode("JSR", "wozFIX")
            self.createcode("LDA", "M1")
            self.createcode("JSR", "_OUTHEX", "call write a hex byte")
            self.createcode("LDA", "M1_1")
            self.createcode("JSR", "_OUTHEX", "call write a hex byte")
        elif wozfloatreg == 2:
            self.createcode("LDX", "#3")
            self.createcode("LDA", "X2,X", name=m2loop)
            self.createcode("STA", "X1,X")
            self.createcode("DEX")
            self.createcode("BPL", m2loop)
            self.createcode("JSR", "wozFIX")
            self.createcode("LDA", "M1")
            self.createcode("JSR", "_OUTHEX", "call write a hex byte")
            self.createcode("LDA", "M1_1")
            self.createcode("JSR", "_OUTHEX", "call write a hex byte")
        self.createcode("JSR", "_OUTPUTCRLF", "end of print wozfloat registers")
        self.createcode("LDX", "#7")
        self.createcode("LDA", "_scratchregister,X", name=m2rsloop)
        self.createcode("STA", "X2,X")
        self.createcode("DEX")
        self.createcode("BPL", m2rsloop)
        if False and yself.createvirtsub:
            self.stopconvertedsubroutine()
            self.createcode("JSR", convertedsubname)

    def copyreg(self, fromregistername, toregistername):
        fromtoken = self.stokens.get(fromregistername)
        totoken = self.stokens.get(toregistername)
        if totoken.getsize() < fromtoken.getsize():
            copysize = totoken.getsize()
        else:
            copysize = fromtoken.getsize()
        for index in range(copysize):
            self.createcode("LDA", "%s" % (registerconvert[fromregistername+'_'+str(index)]),"COPYREG, from:%s to:%s" % (fromregistername, toregistername))
            self.createcode("STA", "%s" % (registerconvert[toregistername+'_'+str(index)]))

    def outputatreg(self,registername, size, onlyvalue=False, cr=False, shortinfo=""):
        outregloop1 = self.randomword(8)
        outregloop2 = self.randomword(8)
        #self.pushcpureg("save register bevor printing")
        if not onlyvalue:
            self.createdebugout("%s,ADR:" % shortinfo, cr=False)
            self.createcode("LDX", "#%d" %  1, "OUTPUTATREG: Output *reg:%s")
            self.createcode("LDA", "%s,x" % registername, name=outregloop1)
            self.createcode("JSR", "_OUTHEX")
            self.createcode("DEX")
            self.createcode("BPL", outregloop1)
            self.createdebugout(" STACK:", cr=False)
        self.createcode("LDY", "#%d" % (int(size) - 1))
        self.createcode("LDX", "#%d" %  (int(size) - 1))
        self.createcode("LDA", "(%s),y" % registername, name=outregloop2)
        self.createcode("JSR", "_OUTHEX")
        self.createcode("DEY")
        self.createcode("DEX")
        self.createcode("BPL", outregloop2)
        self.createcode("LDA", "#$20")
        self.createcode("JSR", "_OUTPUTCHAR")
        if cr:
            self.createcode("JSR", "_OUTPUTCRLF")
        #self.popcpureg()
        return

    def createdumpevalstack(self, shortinfo, callinfo):
        # _ureg7 is evaluationstackpointer, one element on the stack takes 8 byte (long-value)
        # _ureg7 will be loaded in begindoevaluate() from stackpointer
        # evaluation stack starts at stackpointer
        loop1 = self.randomword(8)
        size = 8
        if self.debug_evalstack:
            self.createcode("NOP","",callinfo)
            self.pushcpureg("CREATEDUMPEVALSTACK: show content of evaluation stack for debugging")
            self.copyreg("_unireg7","_unireg2")
            self.outputatreg("_unireg2", size, onlyvalue=False, cr=False, shortinfo=shortinfo)
            self.createcode("NOP","","",name=loop1)
            self.createcode("CLC","","add size for var to _unireg2")
            self.createcode("LDA", "_unireg2_0")
            self.createcode("ADC", "#%d" % self.eval_sizeforvar)
            self.createcode("STA", "_unireg2_0")
            self.createcode("LDA", "_unireg2_1")
            self.createcode("ADC", "#0")
            self.createcode("STA", "_unireg2_1")
            self.outputatreg("_unireg2", size, onlyvalue=True, cr=False)
            self.createcode("LDA", "_unireg2_0")
            self.createcode("CMP", "_userstack_0")
            self.createcode("BNE", loop1)
            self.createcode("LDA", "_unireg2_1")
            self.createcode("CMP", "_userstack_1")
            self.createcode("BNE", loop1)
            self.createcode("JSR", "_OUTPUTCRLF")
            self.popcpureg()
            return
        # return registers back from stack

    def varstatement(self, stoken, t_type, t_value, isinarguments=False):
        attributes = stoken.getattributes()
        attributhash = stoken.getattributehash()
        iscpureg = False
        attribstr = ""
        for a in attributes:
            attribstr += a + ','
            if a == "cpuregister":
                iscpureg = True
        attribstr = attribstr[:-1]
        name = stoken.getname()
        if False:
            self.createcode("","","VARSTATEMENT (stoken=%s, t_type=%s, t_value=%s, attribs=%s)" % (name, t_type, t_value, attribstr))
        if isinarguments:
            infunction = self.blocks.lastfunction()
            baseaddress = infunction.getargaddress()
            print("True , varname:%20s, vartype:%10s, %20s, Addr:%04x, Activefunc:%s" % (t_value, t_type, self.blocks.getactivefunctionname(), baseaddress, self.blocks.getactivefunctionname()))
        else:
            baseaddress = self.internalvarcounter
            print("False, varname:%20s, vartype:%10s, %20s, Addr:%04x, Activefunc:%s" % (t_value, t_type, self.blocks.getactivefunctionname(), baseaddress, self.blocks.getactivefunctionname()))
        namespace = self.blocks.getactivefunctionname()
        typetoken = self.stokens.getwithnamespace(t_type, namespace)
        if typetoken == None:
            namespace =  "global"
            typetoken = self.stokens.getwithnamespace(t_type, namespace)
            if typetoken == None:
                print("type not found")
                sys.exit(1)
        if iscpureg:
            funcvarname = t_value
        else:
            funcvarname = self.blocks.getactivefunctionname() + '_' + t_value
        if self.checkhash(attributhash, "type_varpointer"):
            varsize = 2
        elif self.checkhash(attributhash, "type_chararray"):
            varsize = stoken.getsize()
        else:
            varsize = typetoken.getsize()
        adr = "$%04x" % baseaddress
        hexidx = "%04x" % baseaddress
        varindex = 0
        varidx = "_%d" % varindex
        self.log.writelog("codeemitter/varstatement", "name is:%20s, adr=:$%4x" % (stoken.getname(), baseaddress))
        stoken.setaddress(baseaddress)
        self.setcomment("define var %s = %s sizeof(%d) with %s"%(t_type, t_value, varsize, attribstr))
        self.createdefinition(funcvarname, "=", adr)
        self.createdefinition(funcvarname + varidx, "=", adr)
        self.setcomment("define var name:%s sizeof(%d) baseadress:$%4x" % (t_value, varsize, baseaddress))
        if varsize < 9 or self.checkhash(attributhash, "type_superlong"):
            baseaddress += 1
            varindex += 1
            varsize -= 1
            while varsize > 0:
                adr = "$%04x" % baseaddress
                hexidx = "_%04x" % baseaddress
                varidx = "_%d" % varindex
                self.createdefinition(funcvarname + varidx, "=", adr)
                # the following line inserts varname + _xxxx where xxxx is the address
                # this following line should be eliminated in  the future, becaus this
                # makes no sense....
                # self.createdefinition(funcvarname + hexidx, "=", adr)
                varsize -= 1
                baseaddress += 1
                varindex += 1
        else:
            baseaddress += varsize
        if isinarguments:
            infunction.setargaddress(baseaddress)
        else:
            self.internalvarcounter = baseaddress
        return
# ---------------------------- push and pop functions for evaluate ------------------------------
    def debugoutunireg(self, do, registerno,  message):
        if not do:
            return
        self.createdebugout("u%d-%s" % (registerno, message))
        self.createcode("LDA", "_unireg%d_1" % registerno)
        self.createcode("JSR", "_OUTHEX")
        self.createcode("LDA", "_unireg%d_0" % registerno)
        self.createcode("JSR", "_OUTHEX")
        self.createcode("LDA", "#\" \"")
        self.createcode("JSR", "_OUTPUTCHAR")
        self.createcode("LDY", "#3")
        for x in range(4):
            self.createcode("TYA")
            self.createcode("PHA")
            self.createcode("LDA", "(_unireg%d_0),Y" % registerno)
            self.createcode("JSR", "_OUTHEX")
            self.createcode("PLA")
            self.createcode("TAY")
            self.createcode("DEY")
        self.createcode("JSR", "_OUTPUTCRLF")

    def begindoevaluate(self, useopsize, expression, stackdepthneeded):
        self.log.writelog("codeemitter/begindoevaluate", "useopsize is:%d, expression:%s, stackdepth:%d" % (useopsize, expression, stackdepthneeded))
        self.debug_evalstack = False
        self.eval_opsize = useopsize
        print("opsize for expression:%s is:%d" % (expression, useopsize))
        new_eval_stacksize = self.eval_sizeforvar * stackdepthneeded
        if new_eval_stacksize > self.eval_stacksize:
            self.eval_stacksize = new_eval_stacksize
        self.createcode("","","BEGINDOEVALUATE: Expression: %s, Stackdepth:%d, Stacklength:%d" % (expression, stackdepthneeded, new_eval_stacksize))
        self.createcode("LDA", "_userstack_0", "Copy userstack to unireg7")
        self.createcode("STA", "_unireg7_0")
        self.createcode("LDA", "_userstack_1")
        self.createcode("STA", "_unireg7_1")
        if self.debug_espression:
            self.createdebugout("BEGINDOEVALUATE: %s, stackdepth:%d" % (expression, stackdepthneeded), cr=True)
        self.debugoutunireg(self.debug_espression, 7, "begin eval before correction:")
        if False:
            self.createcode("LDA", "#%d" % (self.eval_stacksize + 16), "Load sum of stackspace needet for complete operation")
            self.createcode("JSR", "subaccufrom_unireg7", "subtract from ureg7")
        else:
            namespace = self.blocks.getactivefunctionname()
            evalstackend = "%s_sflast" % namespace
            self.createcode("LDA", "#%s" % evalstackend)
            self.createcode("JSR", "addaccuto_unireg7")
        self.debugoutunireg(self.debug_espression, 7, "begin eval bei exit:")

    def pushvaluetostack(self, fromtoken):
        debug = self.debug_espression
        self.createcode("LDA", "#%d" % self.eval_sizeforvar, "PUSHVALUETOSTACK add stack for one var")
        self.createcode("JSR", "subaccufrom_unireg7", "sub from ureg7")
        avalue = fromtoken.getvalue()
        aaddr = fromtoken.getaddress()
        asize = self.eval_opsize
        byteindex = 0
        ureg = self.expr_stack_index + "_%d" % byteindex
        self.log.writelog("codeemitter/pushvaluetostack", "value:%08x" % int(avalue))

        if asize == 1:
            hexvalue = "%02x" % int(avalue)
            indx = 0
            idxlist = [ 0 ]
        if asize == 2:
            hexvalue = "%04x" % int(avalue)
            indx = 2
            idxlist = [ 2, 0 ]
        if asize == 4:
            hexvalue = "%08x" % int(avalue)
            indx = 6
            idxlist = [ 6, 4, 2, 0 ]
        if asize == 8:
            hexvalue = "%016x" % int(avalue)
            indx = 14
            idxlist = [ 14, 12, 10, 8, 6, 4, 2, 0]
        oldhexbyte = "--"
        self.createcode("LDY","#0","Value:%s" % avalue)
        for idx in idxlist:
            hexbyte = hexvalue[indx:indx+2]
            if hexbyte != oldhexbyte:
                self.createcode("LDA", "#$%s" % hexbyte, "Load from Value:%s" % hexvalue)
            self.createcode("STA", "(%s),Y" % ureg, "store byte to stack")
            if idx > 0:
                self.createcode("INY","","adjust to next byte")
            aaddr += 1
            indx -= 2
            oldhexbyte = hexbyte
        #
        # self.createcode("JSR", "_OUTAT_UNIREG7")
        if debug:
            self.debugoutunireg(debug, 6, "push val, bei exit:")
            self.debugoutunireg(debug, 7, "push val, bei exit:")
        #
        print("pushvalue to stack called with Value:%s" % str(avalue))

    def pushvartostack(self, fromtoken):
        debug = self.debug_espression
        name = fromtoken.getnamewithnamespace()
        self.createcode("LDA", "#%d" % self.eval_sizeforvar, "PUSHVARTOSTACK with Name:%s" % name)
        self.createcode("JSR", "subaccufrom_unireg7", "sub from ureg7")
        namespace = self.blocks.getactivefunctionname()
        avalue = fromtoken.getvalue()
        name = fromtoken.getnamewithnamespace()
        namespace = fromtoken.getnamespace()
        source_attr = fromtoken.getattributehash()
        addr = fromtoken.getaddress()
        if name == "global_strtok_laststring":
            x = 0
        self.log.writelog("codeemitter/pushvartostack", "name:%s" % (name))
        if self.checkhash(source_attr, "isargument") and namespace == fromtoken.getnamespace():
            frame0 = "_framepointer_0"
            frame1 = "_framepointer_1"
        else:
            frame0 = "_userstack_0"
            frame1 = "_userstack_1"
        if namespace == "global":
            self.createcode("LDA", "#<%s" % name)
            self.createcode("STA", "%s" % "_unireg6_0")
            self.createcode("LDA", "#>%s" % name)
            self.createcode("STA", "%s" % "_unireg6_1")
        else:
            self.createcode("CLC")
            self.createcode("LDA", "%s" % frame0)
            self.createcode("ADC", "#%s" % name )
            self.createcode("STA", "%s" % "_unireg6_0")
            self.createcode("LDA", "%s" % frame1)
            self.createcode("ADC", "#0")
            self.createcode("STA", "%s" % "_unireg6_1")
        convertedsubname = "pushvaronstack_"+str(fromtoken.getsize()) # + '_' + subsalt
        if self.createvirtsub:
            self.createcode("","","Calling PUSHVARONSTACK as virtual Subroutine")
            self.startconvertedsubroutine(convertedsubname)
        indx = 0
        self.createcode("LDY","#0")
        while indx < fromtoken.getsize():
            self.createcode("LDA", "(%s),Y" % "_unireg6_0", "copy from:%s" % name)
            self.createcode("STA", "(%s),Y" % "_unireg7_0")
            indx += 1
            if indx < fromtoken.getsize():
                self.createcode("INY","","adjust to next byte")
        if self.createvirtsub:
            self.stopconvertedsubroutine()
            self.createcode("JSR", convertedsubname)
        print("pushvar to stack called with Variable:%s" % str(name))

    def popvarfromstack(self, fromtoken, ptr_a_dest=False, ptr_a_source=False, lineno=0):
        debug = self.debug_espression
        namespace = self.blocks.getactivefunctionname()
        avalue = fromtoken.getvalue()
        name = fromtoken.getnamewithnamespace()
        destnamespace = fromtoken.getnamespace()
        destname = fromtoken.getname()
        dest_attr = fromtoken.getattributehash()
        ureg = self.expr_stack_index
        destsize = fromtoken.getsize()
        self.log.writelog("codeemitter/popvarfromstack", "dest:%s" % (name))
        if name == "recurse_a":
            xxxx = 0
        if self.checkhash(dest_attr, "isargument") and namespace == fromtoken.getnamespace():
            frame_0 = "_framepointer_0"
            frame_1 = "_framepointer_1"
        else:
            frame_0 = "_userstack_0"
            frame_1 = "_userstack_1"
        if destnamespace == "global":
            indx = 0
            self.createcode("LDY", "#0", "POPVARFROMSTACK GLOBAL to Name:%s, size:%d" % (name, destsize))
            for x in range(destsize):
                self.createcode("LDA", "(%s),Y" % ureg, "copy from:%s" % ureg)
                try:
                    self.createcode("STA", "%s" % (registerconvert[destname + '_' + str(x)]))
                except KeyError:
                    self.createcode("STA", "%s" % name + '_' + str(x))
                if x < destsize - 1:
                    self.createcode("INY")
        else:
            indx = 0
            self.createcode("CLC","","POPVARFROMSTACK LOCAL to Name:%s" % name)
            self.createcode("LDA", frame_0, "destination size for token:%s is:%d bytes" % (destname, destsize))
            self.createcode("ADC", "#%s" % name)
            self.createcode("STA", "_unireg6_0")
            self.createcode("LDA", frame_1)
            self.createcode("ADC", "#0")
            self.createcode("STA", "_unireg6_1")
            convertedsubname = "popvarfromstack_"+str(destsize) # + '_' + subsalt
            if self.createvirtsub:
                self.createcode("","","Calling POPVARFROMSTACK as virtual Subroutine")
                self.startconvertedsubroutine(convertedsubname)
            self.createcode("LDY","#0")
            while indx < destsize:
                self.createcode("LDA", "(%s),Y" % ureg, "copy from:%s" % ureg)
                self.createcode("STA", "(_unireg6_0),Y", "copy to returntoken")
                indx += 1
                if indx < destsize:
                    self.createcode("INY","","adjust to next byte")
            if self.createvirtsub:
                self.stopconvertedsubroutine()
                self.createcode("JSR", convertedsubname)
        #

    def addonstack(self, options):
        debug = self.debug_espression
        size = self.eval_opsize
        self.log.writelog("codeemitter/addonstack", "size:%s" % (size))
        # ----------------------------------------
        subsalt = self.randomconst(8)
        if options == "wozfloat":
            convertedsubname = "addonstack_woz_"+str(self.eval_opsize) # + '_' + subsalt
        else:
            convertedsubname = "addonstack_"+str(self.eval_opsize) # + '_' + subsalt
        if self.createvirtsub:
            self.createcode("","","Calling ADDONSTACK as virtual Subroutine")
            self.startconvertedsubroutine(convertedsubname)
        # ----------------------------------------
        self.createcode("","","ADDONSTACK")
        # set pointer for 2nd stackmember in unireg6
        #
        self.createcode("CLC")
        self.createcode("LDA", "_unireg7_0")
        self.createcode("ADC", "#%d" % self.eval_sizeforvar)
        self.createcode("STA", "_unireg6_0")
        self.createcode("LDA", "_unireg7_1")
        self.createcode("ADC", "#0")
        self.createcode("STA", "_unireg6_1")
        #
        if debug:
            self.debugoutunireg(debug, 6, "add, vor calc:")
            self.debugoutunireg(debug, 7, "add, vor calc:")
        #
        if options == "wozfloat":
            wozacploop1 = self.randomword(8)
            wozacploop2 = self.randomword(8)
            wozacpbackloop = self.randomword(8)
            # copy first stackitem to woz register 1
            self.createcode("LDY", "#3", "4 bytes to copy, M1 and X1")
            self.createcode("LDA", "(_unireg7_0),Y", "load first value from stack", name=wozacploop1)
            self.createcode("STA", "X1,Y")
            self.createcode("DEY")
            self.createcode("BPL", wozacploop1)
            # copy second
            self.createcode("LDY", "#3", "4 bytes to copy, M2 and X2")
            self.createcode("LDA", "(_unireg6_0),Y", "load first value from stack", name=wozacploop2)
            self.createcode("STA", "X2,Y")
            self.createcode("DEY")
            self.createcode("BPL", wozacploop2)
            # add with wozadd
            self.createcode("JSR", "wozFADD")
            # copy result from wot register 2 to resultpointer
            self.createcode("LDY", "#3", "4 bytes to copy, M1 and X1")
            self.createcode("LDA", "X1,Y", "load first value from stack", name=wozacpbackloop)
            self.createcode("STA", "(_unireg6_0),Y")
            self.createcode("DEY")
            self.createcode("BPL", wozacpbackloop)
        elif size == 1:
            self.createcode("LDY", "#0")
            self.createcode("CLC")
            self.createcode("LDA", "(_unireg7_0),Y")
            self.createcode("ADC", "(_unireg6_0),Y")
            self.createcode("STA", "(_unireg6_0),Y")
        elif size == 2 or size == 4 or size == 8:
            self.createcode("LDY", "#0")
            self.createcode("CLC")
            for x in range(size):
                self.createcode("LDA", "(_unireg7_0),Y")
                self.createcode("ADC", "(_unireg6_0),Y")
                self.createcode("STA", "(_unireg6_0),Y")
                if x < size - 1:
                    self.createcode("INY")
        else:
            pass
        self.createcode("LDA", "#%d" % self.eval_sizeforvar, "add stack for two var")
        self.createcode("JSR", "addaccuto_unireg7", "add from ureg7")
        # ----------------------------------------
        if self.createvirtsub:
            self.stopconvertedsubroutine()
            self.createcode("JSR", convertedsubname)

    def subonstack(self, options):
        debug = self.debug_espression
        subsalt = self.randomconst(8)
        if options == "wozfloat":
            convertedsubname = "subonstack_woz_"+str(self.eval_opsize) # + '_' + subsalt
        else:
            convertedsubname = "subonstack_"+str(self.eval_opsize) # + '_' + subsalt
        if self.createvirtsub:
            self.createcode("","","Calling SUBONSTACK as virtual Subroutine")
            self.startconvertedsubroutine(convertedsubname)
        self.createcode("","","SUBONSTACK")
        size = self.eval_opsize
        self.log.writelog("codeemitter/subonstack", "size:%s" % (size))
        #
        self.createcode("CLC")
        self.createcode("LDA", "_unireg7_0")
        self.createcode("ADC", "#%d" % self.eval_sizeforvar)
        self.createcode("STA", "_unireg6_0")
        self.createcode("LDA", "_unireg7_1")
        self.createcode("ADC", "#0")
        self.createcode("STA", "_unireg6_1")
        #
        self.debugoutunireg(debug, 6, "sub, vor calc:")
        self.debugoutunireg(debug, 7, "sub, vor calc:")
        #
        if options == "wozfloat":
            wozscploop1 = self.randomword(8)
            wozscploop2 = self.randomword(8)
            wozscpbackloop = self.randomword(8)
            #self.createcode("JSR", "_OUTAT_UNIREG6")
            #self.createcode("JSR", "_OUTAT_UNIREG7")
            #self.createcode("JSR", "wozmon")
            # copy first stackitem to woz register 1
            self.createcode("LDY", "#3", "4 bytes to copy, M1 and X1")
            self.createcode("LDA", "(_unireg7_0),Y", "load first value from stack", name=wozscploop1)
            self.createcode("STA", "X1,Y")
            self.createcode("DEY")
            self.createcode("BPL", wozscploop1)
            # copy second
            self.createcode("LDY", "#3", "4 bytes to copy, M2 and X2")
            self.createcode("LDA", "(_unireg6_0),Y", "load first value from stack", name=wozscploop2)
            self.createcode("STA", "X2,Y")
            self.createcode("DEY")
            self.createcode("BPL", wozscploop2)
            # sub with wozsub
            self.createcode("JSR", "wozFSUB")
            # self.printwozfloatMXininteger(2)
            # copy result from woz register 2 to resultpointer
            self.createcode("LDY", "#3", "4 bytes to copy, M1 and X1")
            self.createcode("LDA", "X1,Y", "load first value from stack", name=wozscpbackloop)
            self.createcode("STA", "(_unireg6_0),Y")
            self.createcode("DEY")
            self.createcode("BPL", wozscpbackloop)
        elif size == 1:
            self.createcode("LDY", "#0")
            self.createcode("SEC")
            self.createcode("LDA", "(_unireg6_0),Y")
            self.createcode("SBC", "(_unireg7_0),Y")
            self.createcode("STA", "(_unireg6_0),Y")
        elif size == 2:
            self.createcode("LDY", "#0")
            self.createcode("SEC")
            self.createcode("LDA", "(_unireg6_0),Y")
            self.createcode("SBC", "(_unireg7_0),Y")
            self.createcode("STA", "(_unireg6_0),Y")
            self.createcode("INY")
            self.createcode("LDA", "(_unireg6_0),Y")
            self.createcode("SBC", "(_unireg7_0),Y")
            self.createcode("STA", "(_unireg6_0),Y")
        elif size == 4 or size == 8:
            self.createcode("LDY", "#0")
            self.createcode("SEC")
            for x in range(size):
                self.createcode("LDA", "(_unireg6_0),Y")
                self.createcode("SBC", "(_unireg7_0),Y")
                self.createcode("STA", "(_unireg6_0),Y")
                if x < size:
                    self.createcode("INY")
        else:
            pass
        self.createcode("LDA", "#%d" % self.eval_sizeforvar, "add stack for two var")
        self.createcode("JSR", "addaccuto_unireg7", "add from ureg7")
        if self.createvirtsub:
            self.stopconvertedsubroutine()
            self.createcode("JSR", convertedsubname)

    def mulonstack(self, options):
        # ----------------------------------------
        subsalt = self.randomconst(8)
        if options == "wozfloat":
            convertedsubname = "mulonstack_woz_"+str(self.eval_opsize)
        else:
            convertedsubname = "mulonstack_"+str(self.eval_opsize)
        if self.createvirtsub:
            self.createcode("","","Calling MULONSTACK as virtual Subroutine")
            self.startconvertedsubroutine(convertedsubname)
        # ----------------------------------------
        self.createcode("","","MULONSTACK")
        debug = self.debug_espression
        size = self.eval_opsize
        self.log.writelog("codeemitter/mulonstack", "size:%s" % (size))
        # set pointer for 2nd stackmember in unireg6
        #
        self.createcode("CLC")
        self.createcode("LDA", "_unireg7_0")
        self.createcode("ADC", "#%d" % self.eval_sizeforvar)
        self.createcode("STA", "_unireg6_0")
        self.createcode("LDA", "_unireg7_1")
        self.createcode("ADC", "#0")
        self.createcode("STA", "_unireg6_1")
        #
        L1 = self.randomword(8)
        L2 = self.randomword(8)
        L3 = self.randomword(8)
        CP1 = self.randomword(8)
        CP2 = self.randomword(8)
        if options == "wozfloat":
            wozscploop1 = self.randomword(8)
            wozscploop2 = self.randomword(8)
            wozscpbackloop = self.randomword(8)
            # copy first stackitem to woz register 1
            self.createcode("LDY", "#3", "4 bytes to copy, M1 and X1")
            self.createcode("LDA", "(_unireg7_0),Y", "load first value from stack", name=wozscploop1)
            self.createcode("STA", "X2,Y")
            self.createcode("DEY")
            self.createcode("BPL", wozscploop1)
            # copy second
            self.createcode("LDY", "#3", "4 bytes to copy, M2 and X2")
            self.createcode("LDA", "(_unireg6_0),Y", "load first value from stack", name=wozscploop2)
            self.createcode("STA", "X1,Y")
            self.createcode("DEY")
            self.createcode("BPL", wozscploop2)
            # sub with wozsub
            #self.printwozfloatMXininteger(1)
            #self.printwozfloatMXininteger(2)
            self.createcode("JSR", "wozFMUL")
            #self.printwozfloatMXininteger(1)
            #self.printwozfloatMXininteger(2)
            # copy result from woz register 1 to resultpointer
            # self.createcode("JSR", "_OUTAT_UNIREG6")
            self.createcode("LDY", "#3", "4 bytes to copy, M1 and X1")
            self.createcode("LDA", "X1,Y", "load first value from stack", name=wozscpbackloop)
            self.createcode("STA", "(_unireg6_0),Y")
            self.createcode("DEY")
            self.createcode("BPL", wozscpbackloop)
            # self.createcode("JSR", "_OUTAT_UNIREG6")
            # self.createcode("JMP", "wozmon")
        elif size == 1:
            self.createcode("LDY", "#0")
            self.createcode("LDA", "(_unireg7_0),Y")
            self.createcode("STA", "_unireg0_0", "store multiplicant in unireg0")
            self.createcode("LDA", "(_unireg6_0),Y")
            self.createcode("STA", "_unireg1_0", "store multiplicator in unireg1")
            self.createcode("TYA","","set result to 0")
            self.createcode("LDX", "#8", "this is for 8bit only, result will be 16bit of course")
            self.createcode("LSR", "_unireg0_0", "get low bit of multiplicant", name=L1)
            self.createcode("BCC", L2)
            self.createcode("CLC","","if bit is 1, add Multiplicator")
            self.createcode("ADC", "_unireg1_0","add to multiplicator")
            self.createcode("ROR", "A", "shift out the carry bit...", name=L2)
            self.createcode("ROR", "_scratchregister_0", "...and shift it into result")
            self.createcode("DEX")
            self.createcode("BNE", L1)
            self.createcode("INY")
            self.createcode("STA", "(_unireg6_0),Y")
            self.createcode("LDA", "_scratchregister_0")
            self.createcode("DEY")
            self.createcode("STA", "(_unireg6_0),Y")
        elif size == 2:
            self.createcode("LDY", "#0")
            self.createcode("LDA", "(_unireg7_0),Y")
            self.createcode("STA", "_unireg0_0", "store LSB multiplicant in unireg0")
            self.createcode("LDA", "(_unireg6_0),Y")
            self.createcode("STA", "_unireg1_0", "store LSB multiplicant in unireg0")
            self.createcode("INY")
            self.createcode("LDA", "(_unireg7_0),Y")
            self.createcode("STA", "_unireg0_1", "store MSB multiplicant in unireg0")
            self.createcode("LDA", "(_unireg6_0),Y")
            self.createcode("STA", "_unireg1_1", "store LSB multiplicant in unireg0")
            # ---------------- basic multiplication routine for 16bit -------------------
            self.createcode("LDA", "#0")
            self.createcode("STA", "_scratchregister_0")
            self.createcode("STA", "_scratchregister_1")
            self.createcode("STA", "_scratchregister_2")
            self.createcode("STA", "_scratchregister_3")
            self.createcode("LDX", "#16", "there are 16 bits in _unireg1")
            self.createcode("LSR", "_unireg1_1", "get low bit of unireg1",name=L1)
            self.createcode("ROR", "_unireg1_0")
            self.createcode("BCC", L2)
            self.createcode("TAY")
            self.createcode("CLC")
            self.createcode("LDA", "_unireg0_0")
            self.createcode("ADC", "_scratchregister_2")
            self.createcode("STA", "_scratchregister_2")
            self.createcode("TYA")
            self.createcode("ADC", "_unireg0_1")
            # --------------------------------------LOOP L2 ---------------------------
            self.createcode("ROR", "A", "", name=L2)
            self.createcode("ROR", "_scratchregister_2")
            self.createcode("ROR", "_scratchregister_1")
            self.createcode("ROR", "_scratchregister_0")
            self.createcode("DEX")
            self.createcode("BNE", L1)
            self.createcode("STA", "_scratchregister_3")
            # -----------------end of multiplication ----------------------------------
            self.createcode("LDY", "#0")
            self.createcode("LDX", "#3")
            self.createcode("LDA", "_scratchregister,Y","",name=L3)
            self.createcode("STA", "(_unireg6_0),Y")
            self.createcode("INY")
            self.createcode("DEX")
            self.createcode("BPL", L3)
        elif size == 4:
            self.createcode("LDY", "#3")
            self.createcode("LDA", "(_unireg7_0),Y",name=CP1)
            self.createcode("STA", "_unireg0,Y")
            self.createcode("LDA", "(_unireg6_0),Y")
            self.createcode("STA", "_unireg1,Y")
            self.createcode("DEY")
            self.createcode("BPL", CP1)
            # ---------------- basic multiplication routine for 16bit -------------------
            self.createcode("LDA", "#0")
            # ---------------- clear upper half of result
            self.createcode("STA", "_scratchregister_4", "clear result")
            self.createcode("STA", "_scratchregister_5", "clear result")
            self.createcode("STA", "_scratchregister_6", "clear result")
            self.createcode("STA", "_scratchregister_7", "clear result")
            self.createcode("LDX", "#32", "there are 32 bits in _unireg1")
            # ----------------------------- LOOP L1 ----------------------------------
            self.createcode("LSR", "_unireg1_3", "get low bit of unireg1",name=L1)
            self.createcode("ROR", "_unireg1_2")
            self.createcode("ROR", "_unireg1_1")
            self.createcode("ROR", "_unireg1_0")
            self.createcode("BCC", L2)
            self.createcode("LDA", "_scratchregister_4")
            self.createcode("CLC")
            self.createcode("ADC", "_unireg0_0")
            self.createcode("STA", "_scratchregister_4")
            self.createcode("LDA", "_scratchregister_5")
            self.createcode("ADC", "_unireg0_1")
            self.createcode("STA", "_scratchregister_5")
            self.createcode("LDA", "_scratchregister_6")
            self.createcode("ADC", "_unireg0_2")
            self.createcode("STA", "_scratchregister_6")
            self.createcode("LDA", "_scratchregister_7")
            self.createcode("ADC", "_unireg0_3")
            # ----------------------------- LOOP L2 -----------------------------------
            self.createcode("ROR", "A", "", name=L2)
            self.createcode("STA", "_scratchregister_7")
            self.createcode("ROR", "_scratchregister_6")
            self.createcode("ROR", "_scratchregister_5")
            self.createcode("ROR", "_scratchregister_4")
            self.createcode("ROR", "_scratchregister_3")
            self.createcode("ROR", "_scratchregister_2")
            self.createcode("ROR", "_scratchregister_1")
            self.createcode("ROR", "_scratchregister_0")
            self.createcode("DEX")
            self.createcode("BNE", L1)
            # -----------------end of multiplication ----------------------------------
            self.createcode("LDY", "#0")
            self.createcode("LDX", "#7")
            self.createcode("LDA", "_scratchregister,Y","",name=CP2)
            self.createcode("STA", "(_unireg6_0),Y")
            self.createcode("INY")
            self.createcode("DEX")
            self.createcode("BPL", CP2)
        elif size == 8:
            self.createcode("LDY", "#7")
            self.createcode("LDA", "(_unireg7_0),Y",name=CP1)
            self.createcode("STA", "_unireg0,Y")
            self.createcode("LDA", "(_unireg6_0),Y")
            self.createcode("STA", "_unireg1,Y")
            self.createcode("DEY")
            self.createcode("BPL", CP1)
            # ---------------- basic multiplication routine for 16bit -------------------
            # ---------------- clear lower half of result
            self.createcode("LDA", "#0")
            self.createcode("STA", "_scratchregister_0", "clear result")
            self.createcode("STA", "_scratchregister_1", "clear result")
            self.createcode("STA", "_scratchregister_2", "clear result")
            self.createcode("STA", "_scratchregister_3", "clear result")
            self.createcode("STA", "_scratchregister_4", "clear result")
            self.createcode("STA", "_scratchregister_5", "clear result")
            self.createcode("STA", "_scratchregister_6", "clear result")
            self.createcode("STA", "_scratchregister_7", "clear result")
            # self.createcode("LDX", "#64", "there are 64 bits in _unireg1")
            # ---------------- clear upper half of result
            self.createcode("STA", "_scratchregister_8", "clear result")
            self.createcode("STA", "_scratchregister_9", "clear result")
            self.createcode("STA", "_scratchregister_10", "clear result")
            self.createcode("STA", "_scratchregister_11", "clear result")
            self.createcode("STA", "_scratchregister_12", "clear result")
            self.createcode("STA", "_scratchregister_13", "clear result")
            self.createcode("STA", "_scratchregister_14", "clear result")
            self.createcode("STA", "_scratchregister_15", "clear result")
            self.createcode("LDX", "#64", "there are 64 bits in _unireg1")
            # ----------------------------- LOOP L1 ----------------------------------
            self.createcode("LSR", registerconvert["_unireg1_7"], "get low bit of unireg1",name=L1)
            self.createcode("ROR", registerconvert["_unireg1_6"])
            self.createcode("ROR", registerconvert["_unireg1_5"])
            self.createcode("ROR", registerconvert["_unireg1_4"])
            self.createcode("ROR", registerconvert["_unireg1_3"])
            self.createcode("ROR", registerconvert["_unireg1_2"])
            self.createcode("ROR", registerconvert["_unireg1_1"])
            self.createcode("ROR", registerconvert["_unireg1_0"])
            self.createcode("BCC", L2)
            self.createcode("LDA", "_scratchregister_8")
            self.createcode("CLC")
            self.createcode("ADC", registerconvert["_unireg0_0"])
            self.createcode("STA", "_scratchregister_8")
            self.createcode("LDA", "_scratchregister_9")
            self.createcode("ADC", registerconvert["_unireg0_1"])
            self.createcode("STA", "_scratchregister_9")
            self.createcode("LDA", "_scratchregister_10")
            self.createcode("ADC", registerconvert["_unireg0_2"])
            self.createcode("STA", "_scratchregister_10")
            self.createcode("LDA", "_scratchregister_11")
            self.createcode("ADC", registerconvert["_unireg0_3"])
            self.createcode("STA", "_scratchregister_11")
            self.createcode("LDA", "_scratchregister_12")
            self.createcode("ADC", registerconvert["_unireg0_4"])
            self.createcode("STA", "_scratchregister_12")
            self.createcode("LDA", "_scratchregister_13")
            self.createcode("ADC", registerconvert["_unireg0_5"])
            self.createcode("STA", "_scratchregister_13")
            self.createcode("LDA", "_scratchregister_14")
            self.createcode("ADC", registerconvert["_unireg0_6"])
            self.createcode("STA", "_scratchregister_14")
            self.createcode("LDA", "_scratchregister_15")
            self.createcode("ADC", registerconvert["_unireg0_7"])
            # ----------------------------- LOOP L2 -----------------------------------
            self.createcode("ROR", "A", "", name=L2)
            self.createcode("STA", "_scratchregister_15")
            self.createcode("ROR", "_scratchregister_14")
            self.createcode("ROR", "_scratchregister_13")
            self.createcode("ROR", "_scratchregister_12")
            self.createcode("ROR", "_scratchregister_11")
            self.createcode("ROR", "_scratchregister_10")
            self.createcode("ROR", "_scratchregister_9")
            self.createcode("ROR", "_scratchregister_8")
            self.createcode("ROR", "_scratchregister_7")
            self.createcode("ROR", "_scratchregister_6")
            self.createcode("ROR", "_scratchregister_5")
            self.createcode("ROR", "_scratchregister_4")
            self.createcode("ROR", "_scratchregister_3")
            self.createcode("ROR", "_scratchregister_2")
            self.createcode("ROR", "_scratchregister_1")
            self.createcode("ROR", "_scratchregister_0")
            self.createcode("DEX")
            self.createcode("BNE", L1)
            # -----------------end of multiplication ----------------------------------
            self.createcode("LDY", "#0")
            self.createcode("LDX", "#7")
            self.createcode("LDA", "_scratchregister,Y","",name=CP2)
            self.createcode("STA", "(_unireg6_0),Y")
            self.createcode("INY")
            self.createcode("DEX")
            self.createcode("BPL", CP2)
        else:
            pass
        self.createcode("LDA", "#%d" % self.eval_sizeforvar, "add stack for two var")
        self.createcode("JSR", "addaccuto_unireg7", "add from ureg7")
        # ----------------------------------------
        if self.createvirtsub:
            self.stopconvertedsubroutine()
            self.createcode("JSR", convertedsubname)
        return

    def divonstack(self, options):
        # ----------------------------------------
        subsalt = self.randomconst(8)
        if options == "wozfloat":
            convertedsubname = "divonstack_woz_"+str(self.eval_opsize)
        else:
            convertedsubname = "divonstack_"+str(self.eval_opsize)
        if self.createvirtsub:
            self.createcode("","","Calling DIVONSTACK as virtual Subroutine")
            self.startconvertedsubroutine(convertedsubname)
        # ----------------------------------------
        self.createcode("","","DIVONSTACK")
        debug = self.debug_espression
        size = self.eval_opsize
        self.log.writelog("codeemitter/divonstack", "size:%s" % (size))
        # set pointer for 2nd stackmember in unireg6
        #
        self.createcode("CLC")
        self.createcode("LDA", "_unireg7_0")
        self.createcode("ADC", "#%d" % self.eval_sizeforvar)
        self.createcode("STA", "_unireg6_0")
        self.createcode("LDA", "_unireg7_1")
        self.createcode("ADC", "#0")
        self.createcode("STA", "_unireg6_1")
        #
        DO_NXT_BIT = self.randomword(8)
        SUBT = self.randomword(8)
        RSULT = self.randomword(8)
        NXT = self.randomword(8)
        CP1 = self.randomword(8)
        CP2 = self.randomword(8)
        CLEAR = self.randomword(8)
        if debug:
            self.debugoutunireg(debug, 6, "div, vor div:")
            self.debugoutunireg(debug, 7, "div, vor div:")
        if options == "wozfloat":
            wozdivcploop1 = self.randomword(8)
            wozdivcploop2 = self.randomword(8)
            wozdivcpbackloop = self.randomword(8)
            # copy first stackitem to woz register 1
            self.createcode("LDY", "#3", "4 bytes to copy, M1 and X1")
            self.createcode("LDA", "(_unireg6_0),Y", "load first value from stack", name=wozdivcploop1)
            self.createcode("STA", "X2,Y")
            self.createcode("DEY")
            self.createcode("BPL", wozdivcploop1)
            # copy second
            self.createcode("LDY", "#3", "4 bytes to copy, M2 and X2")
            self.createcode("LDA", "(_unireg7_0),Y", "load first value from stack", name=wozdivcploop2)
            self.createcode("STA", "X1,Y")
            self.createcode("DEY")
            self.createcode("BPL", wozdivcploop2)
            self.createcode("JSR", "wozFDIV")
            self.createcode("LDY", "#3", "4 bytes to copy, M1 and X1")
            self.createcode("LDA", "X1,Y", "load first value from stack", name=wozdivcpbackloop)
            self.createcode("STA", "(_unireg6_0),Y")
            self.createcode("DEY")
            self.createcode("BPL", wozdivcpbackloop)
        elif size == 1:
            pass
        elif size == 2:
            # copy input for divider and quotient from stack into registers 0 and 1
            self.createcode("LDY", "#3")
            self.createcode("LDA", "(_unireg6_0),Y",name=CP1)
            self.createcode("STA", "_unireg0,Y")
            self.createcode("LDA", "(_unireg7_0),Y")
            self.createcode("STA", "_unireg1,Y")
            self.createcode("DEY")
            self.createcode("BPL", CP1)
            # divide unireg0 unireg1
            self.createcode("LDA", "#0", "init reminder (_scratchregister) to 0")
            self.createcode("STA", "_scratchregister_0")
            self.createcode("STA", "_scratchregister_1")
            self.createcode("LDX", "#16", "16bit integer used")
            self.createcode("ASL", "_unireg0_0", "Shift hi bit of num1 into reminder",name=DO_NXT_BIT)
            self.createcode("ROL", "_unireg0_1", "vacating the lo bit, which will be used for the quotient")
            self.createcode("ROL", "_scratchregister_0")
            self.createcode("ROL", "_scratchregister_1")
            self.createcode("LDA", "_scratchregister_0")
            self.createcode("SEC","","Trial subtraction")
            self.createcode("SBC", "_unireg1_0")
            self.createcode("TAY")
            self.createcode("LDA", "_scratchregister_1")
            self.createcode("SBC", "_unireg1_1")
            self.createcode("BCC", NXT)
            self.createcode("STA", "_scratchregister_1")
            self.createcode("STY", "_scratchregister_0")
            self.createcode("INC", "_unireg0_0", "and record a 1 in the quotient")
            self.createcode("DEX", name=NXT)
            self.createcode("BNE", DO_NXT_BIT)
            # last step ist copy back _unireg0 (dividend) into return var to stack
            self.createcode("LDY", "#0")
            self.createcode("LDX", "#3")
            self.createcode("LDA", "_unireg0,Y","",name=CP2)
            self.createcode("STA", "(_unireg6_0),Y")
            self.createcode("INY")
            self.createcode("DEX")
            self.createcode("BPL", CP2)
            #
            # -------------------------------------------------  end of 16bit divide ------------------------
            #
        elif size == 4 or size == 8:
            # copy input for divider and quotient from stack into registers 0 and 1
            self.createcode("LDA", "#0")
            self.createcode("LDX", "#8")
            self.createcode("STA", "_scratchregister_7,X", name=CLEAR)
            self.createcode("DEX")
            self.createcode("BNE", CLEAR)
            self.createcode("LDY", "#7")
            self.createcode("LDA", "(_unireg6_0),Y",name=CP1)
            self.createcode("STA", "_unireg0,Y")
            self.createcode("LDA", "(_unireg7_0),Y")
            self.createcode("STA", "_scratchregister,Y")
            self.createcode("DEY")
            self.createcode("BPL", CP1)
            # divide unireg0 unireg1
            self.createcode("LDY", "#64")
            self.createcode("ASL", "_unireg0_0", name=DO_NXT_BIT)
            self.createcode("ROL", "_unireg0_1")
            self.createcode("ROL", "_unireg0_2")
            self.createcode("ROL", "_unireg0_3")
            self.createcode("ROL", registerconvert["_unireg0_4"])
            self.createcode("ROL", registerconvert["_unireg0_5"])
            self.createcode("ROL", registerconvert["_unireg0_6"])
            self.createcode("ROL", registerconvert["_unireg0_7"])
            self.createcode("ROL", "_scratchregister_8")
            self.createcode("ROL", "_scratchregister_9")
            self.createcode("ROL", "_scratchregister_10")
            self.createcode("ROL", "_scratchregister_11")
            self.createcode("ROL", "_scratchregister_12")
            self.createcode("ROL", "_scratchregister_13")
            self.createcode("ROL", "_scratchregister_14")
            self.createcode("ROL", "_scratchregister_15")
            self.createcode("LDX", "#0")
            self.createcode("LDA", "#8")
            self.createcode("STA", "_zpscratch_0")
            self.createcode("SEC")
            self.createcode("LDA", "_scratchregister_8,X", "subtract divider from", name=SUBT)
            self.createcode("SBC", "_scratchregister_0,X", "partial dividend and")
            self.createcode("STA", "_unireg2_0,X", "save")
            self.createcode("INX")
            self.createcode("DEC", "_zpscratch_0")
            self.createcode("BNE", SUBT)
            self.createcode("BCC", NXT, "branch to next bit")
            self.createcode("INC", "_unireg0_0", "if result = or -")
            self.createcode("LDX", "#8", "Put subtractor result")
            self.createcode("LDA", "_unireg2_0-1,X","into partial dividend", name=RSULT)
            self.createcode("STA", "_scratchregister_7,X")
            self.createcode("DEX")
            self.createcode("BNE", RSULT)
            self.createcode("DEY","","",name=NXT)
            self.createcode("BNE",DO_NXT_BIT)
            # last step ist copy back  _unireg0 (remainder) into return var to stack
            self.createcode("LDY", "#0")
            self.createcode("LDX", "#7")
            self.createcode("LDA", "_unireg0,Y","",name=CP2)
            self.createcode("STA", "(_unireg6_0),Y")
            self.createcode("INY")
            self.createcode("DEX")
            self.createcode("BPL", CP2)
        else:
            pass
        if debug:
            self.debugoutunireg(debug, 6, "div, nach div:")
            self.debugoutunireg(debug, 7, "div, nach div:")
        self.createcode("LDA", "#%d" % self.eval_sizeforvar, "add stack for two var")
        self.createcode("JSR", "addaccuto_unireg7", "add from ureg7")
        # ----------------------------------------
        if self.createvirtsub:
            self.stopconvertedsubroutine()
            self.createcode("JSR", convertedsubname)
        return

    def modonstack(self, options):
        self.createcode("","","MODONSTACK")
        debug = self.debug_espression
        size = self.eval_opsize
        self.log.writelog("codeemitter/modonstack", "size:%s" % (size))
        # set pointer for 2nd stackmember in unireg6
        #
        self.createcode("CLC")
        self.createcode("LDA", "_unireg7_0")
        self.createcode("ADC", "#%d" % self.eval_sizeforvar)
        self.createcode("STA", "_unireg6_0")
        self.createcode("LDA", "_unireg7_1")
        self.createcode("ADC", "#0")
        self.createcode("STA", "_unireg6_1")
        #
        DO_NXT_BIT = self.randomword(8)
        SUBT = self.randomword(8)
        RSULT = self.randomword(8)
        NXT = self.randomword(8)
        CP1 = self.randomword(8)
        CP2 = self.randomword(8)
        CLEAR = self.randomword(8)
        if size == 1:
            pass
        if size == 2:
            # copy input for divider and quotient from stack into registers 0 and 1
            self.createcode("LDY", "#3")
            self.createcode("LDA", "(_unireg6_0),Y",name=CP1)
            self.createcode("STA", "_unireg0,Y")
            self.createcode("LDA", "(_unireg7_0),Y")
            self.createcode("STA", "_unireg1,Y")
            self.createcode("DEY")
            self.createcode("BPL", CP1)
            # divide unireg0 unireg1
            self.createcode("LDA", "#0", "init reminder (_scratchregister) to 0")
            self.createcode("STA", "_scratchregister_0")
            self.createcode("STA", "_scratchregister_1")
            self.createcode("LDX", "#16", "16bit integer used")
            self.createcode("ASL", "_unireg0_0", "Shift hi bit of num1 into reminder",name=DO_NXT_BIT)
            self.createcode("ROL", "_unireg0_1", "vacating the lo bit, which will be used for the quotient")
            self.createcode("ROL", "_scratchregister_0")
            self.createcode("ROL", "_scratchregister_1")
            self.createcode("LDA", "_scratchregister_0")
            self.createcode("SEC","","Trial subtraction")
            self.createcode("SBC", "_unireg1_0")
            self.createcode("TAY")
            self.createcode("LDA", "_scratchregister_1")
            self.createcode("SBC", "_unireg1_1")
            self.createcode("BCC", NXT)
            self.createcode("STA", "_scratchregister_1")
            self.createcode("STY", "_scratchregister_0")
            self.createcode("INC", "_unireg0_0", "and record a 1 in the quotient")
            self.createcode("DEX", name=NXT)
            self.createcode("BNE", DO_NXT_BIT)
            # last step ist copy back _unireg0 (dividend) or _scratchregister (remainder) into return var to stack
            self.createcode("LDY", "#0")
            self.createcode("LDX", "#3")
            self.createcode("LDA", "_unireg0,Y","",name=CP2)
            #self.createcode("LDA", "_scratchregister_0,Y","",name=CP2)
            self.createcode("STA", "(_unireg6_0),Y")
            self.createcode("INY")
            self.createcode("DEX")
            self.createcode("BPL", CP2)
            #
            # -------------------------------------------------  end of 16bit divide ------------------------
            #
        if size == 4 or size == 8:
            # copy input for divider and quotient from stack into registers 0 and 1
            self.createcode("LDA", "#0")
            self.createcode("LDX", "#8")
            self.createcode("STA", "_scratchregister_7,X", name=CLEAR)
            self.createcode("DEX")
            self.createcode("BNE", CLEAR)
            self.createcode("LDY", "#7")
            self.createcode("LDA", "(_unireg6_0),Y",name=CP1)
            self.createcode("STA", "_unireg0,Y")
            self.createcode("LDA", "(_unireg7_0),Y")
            self.createcode("STA", "_scratchregister,Y")
            self.createcode("DEY")
            self.createcode("BPL", CP1)
            # divide unireg0 unireg1
            self.createcode("LDY", "#64")
            self.createcode("ASL", "_unireg0_0", name=DO_NXT_BIT)
            self.createcode("ROL", "_unireg0_1")
            self.createcode("ROL", "_unireg0_2")
            self.createcode("ROL", "_unireg0_3")
            self.createcode("ROL", registerconvert["_unireg0_4"])
            self.createcode("ROL", registerconvert["_unireg0_5"])
            self.createcode("ROL", registerconvert["_unireg0_6"])
            self.createcode("ROL", registerconvert["_unireg0_7"])
            self.createcode("ROL", "_scratchregister_8")
            self.createcode("ROL", "_scratchregister_9")
            self.createcode("ROL", "_scratchregister_10")
            self.createcode("ROL", "_scratchregister_11")
            self.createcode("ROL", "_scratchregister_12")
            self.createcode("ROL", "_scratchregister_13")
            self.createcode("ROL", "_scratchregister_14")
            self.createcode("ROL", "_scratchregister_15")
            self.createcode("LDX", "#0")
            self.createcode("LDA", "#8")
            self.createcode("STA", "_zpscratch_0")
            self.createcode("SEC")
            self.createcode("LDA", "_scratchregister_8,X", "subtract divider from", name=SUBT)
            self.createcode("SBC", "_scratchregister_0,X", "partial dividend and")
            self.createcode("STA", "_unireg2_0,X", "save")
            self.createcode("INX")
            self.createcode("DEC", "_zpscratch_0")
            self.createcode("BNE", SUBT)
            self.createcode("BCC", NXT, "branch to next bit")
            self.createcode("INC", "_unireg0_0", "if result = or -")
            self.createcode("LDX", "#8", "Put subtractor result")
            self.createcode("LDA", "_unireg2_0-1,X","into partial dividend", name=RSULT)
            self.createcode("STA", "_scratchregister_7,X")
            self.createcode("DEX")
            self.createcode("BNE", RSULT)
            self.createcode("DEY","","",name=NXT)
            self.createcode("BNE",DO_NXT_BIT)
            # last step ist copy back _unireg0 (dividend) or _scratchregister (remainder) into return var to stack
            self.createcode("LDY", "#0")
            self.createcode("LDX", "#7")
            #self.createcode("LDA", "_unireg0,Y","",name=CP2)
            self.createcode("LDA", "_scratchregister,Y","",name=CP2)
            self.createcode("STA", "(_unireg6_0),Y")
            self.createcode("INY")
            self.createcode("DEX")
            self.createcode("BPL", CP2)
        else:
            pass
        self.createcode("LDA", "#%d" % self.eval_sizeforvar, "add stack for two var")
        self.createcode("JSR", "addaccuto_unireg7", "add from ureg7")
        return

    def equalstack(self, options):
        # ----------------------------------------
        subsalt = self.randomconst(8)
        convertedsubname = "equalonstack_"+str(self.eval_opsize) # + '_' + subsalt
        if self.createvirtsub:
            self.createcode("","","Calling EQUALONSTACK as virtual Subroutine")
            self.startconvertedsubroutine(convertedsubname)
        # ----------------------------------------
        self.createcode("","","EQUALSTACK")
        size = self.eval_opsize
        self.log.writelog("codeemitter/equalonstack", "size:%s" % (size))
        #
        self.createcode("CLC")
        self.createcode("LDA", "_unireg7_0")
        self.createcode("ADC", "#%d" % self.eval_sizeforvar)
        self.createcode("STA", "_unireg6_0")
        self.createcode("LDA", "_unireg7_1")
        self.createcode("ADC", "#0")
        self.createcode("STA", "_unireg6_1")
        #
        label = self.randomword(8)
        exitlabel = self.randomword(8)
        self.createcode("LDY", "#0")
        for x in range(size):
            self.createcode("LDA", "(_unireg6_0),Y")
            self.createcode("CMP", "(_unireg7_0),Y")
            self.createcode("BNE", label)
            if x < size-1:
                self.createcode("INY")
        self.createcode("LDA", "#1")
        self.createcode("LDY", "#0")
        self.createcode("STA","(_unireg6_0),Y")
        self.createcode("LDA", "#0")
        for x in range(size-1):
            self.createcode("INY")
            self.createcode("STA","(_unireg6_0),Y")
        self.createcode("JMP", exitlabel)
        self.createcode("LDY", "#0", name=label)
        self.createcode("TYA")
        self.createcode("STA","(_unireg6_0),Y")
        for x in range(size-1):
            self.createcode("INY")
            self.createcode("STA","(_unireg6_0),Y")
        self.createcode("", "", "exit check for equal", name=exitlabel)
        self.createcode("LDA", "#%d" % self.eval_sizeforvar, "add stack for two var")
        self.createcode("JSR", "addaccuto_unireg7", "add from ureg7")
        # ----------------------------------------
        if self.createvirtsub:
            self.stopconvertedsubroutine()
            self.createcode("JSR", convertedsubname)

    def notequalstack(self, options):
        # ----------------------------------------
        subsalt = self.randomconst(8)
        convertedsubname = "notequalonstack_"+str(self.eval_opsize) # + '_' + subsalt
        if self.createvirtsub:
            self.createcode("","","Calling NOTEQUALONSTACK as virtual Subroutine")
            self.startconvertedsubroutine(convertedsubname)
        # ----------------------------------------
        self.createcode("","","NOTEQUALSTACK")
        size = self.eval_opsize
        self.log.writelog("codeemitter/notequalonstack", "size:%s" % (size))
        #
        self.createcode("CLC")
        self.createcode("LDA", "_unireg7_0")
        self.createcode("ADC", "#%d" % self.eval_sizeforvar)
        self.createcode("STA", "_unireg6_0")
        self.createcode("LDA", "_unireg7_1")
        self.createcode("ADC", "#0")
        self.createcode("STA", "_unireg6_1")
        #
        label = self.randomword(8)
        exitlabel = self.randomword(8)
        self.createcode("LDY", "#0")
        for x in range(size):
            self.createcode("LDA", "(_unireg6_0),Y")
            self.createcode("CMP", "(_unireg7_0),Y")
            self.createcode("BNE", label)
            if x < size-1:
                self.createcode("INY")
        self.createcode("LDY", "#0")
        self.createcode("TYA")
        self.createcode("STA","(_unireg6_0),Y")
        self.createcode("LDA", "#0")
        for x in range(size-1):
            self.createcode("INY")
            self.createcode("STA","(_unireg6_0),Y")
        self.createcode("JMP", exitlabel)
        self.createcode("LDY", "#0", name=label)
        self.createcode("LDA", "#1")
        self.createcode("STA","(_unireg6_0),Y")
        self.createcode("TYA")
        for x in range(size-1):
            self.createcode("INY")
            self.createcode("STA","(_unireg6_0),Y")
        self.createcode("", "", "exit check for equal", name=exitlabel)
        self.createcode("LDA", "#%d" % self.eval_sizeforvar, "add stack for two var")
        self.createcode("JSR", "addaccuto_unireg7", "add from ureg7")
        # ----------------------------------------
        if self.createvirtsub:
            self.stopconvertedsubroutine()
            self.createcode("JSR", convertedsubname)

    def smallerstack(self, options):
        # ----------------------------------------
        subsalt = self.randomconst(8)
        convertedsubname = "smalleronstack_"+str(self.eval_opsize) # + '_' + subsalt
        if self.createvirtsub:
            self.createcode("","","Calling SMALLERONSTACK as virtual Subroutine")
            self.startconvertedsubroutine(convertedsubname)
        # ----------------------------------------
        self.createcode("","","EQUALSMALLER TEST")
        size = self.eval_opsize
        self.log.writelog("codeemitter/smalleronstack", "size:%s" % (size))
        #
        self.createcode("CLC")
        self.createcode("LDA", "_unireg7_0")
        self.createcode("ADC", "#%d" % self.eval_sizeforvar)
        self.createcode("STA", "_unireg6_0")
        self.createcode("LDA", "_unireg7_1")
        self.createcode("ADC", "#0")
        self.createcode("STA", "_unireg6_1")
        #
        label = self.randomword(8)
        exitlabel = self.randomword(8)
        endcode = self.randomword(8)
        lessthenlabel = self.randomword(8)
        higherthenlabel = self.randomword(8)
        samethenlabel = self.randomword(8)
        checkbranch = self.randomword(8)
        label2 = self.randomword(8)
        label3 = self.randomword(8)
        if size == 1:  #  tested ok!
            self.createcode("LDY", "#0", "checking most sigificant byte with signed algorithm")
            self.createcode("SEC", "", "prepare carry for SBC")
            self.createcode("LDA", "(_unireg6_0),Y")
            self.createcode("SBC", "(_unireg7_0),Y", "A-NUM")
            self.createcode("BVC", label, "if V is 0, N eor V, otherwise N eor V = N eor 1")
            self.createcode("EOR", "#$80", "A = A eor $80, and N = N eor 1")
            self.createcode("BMI", lessthenlabel,"if the N flag is 1, then (signed) < NUM(signed) and BMI will branch", name=label)
            self.createcode("LDA", "#0", "not less")
            self.createcode("JMP", endcode)
            self.createcode("LDA", "#1", name=lessthenlabel)
            self.createcode("JMP", endcode)
            self.createcode("STA", "(_unireg6_0),Y", name=endcode)
        if size == 2: # maybe ok ;-)
            self.createcode("LDY", "#1", "checking high byte with signed algorithm")
            self.createcode("SEC", "", "prepare carry for SBC")
            self.createcode("LDA", "(_unireg6_0),Y")
            self.createcode("SBC", "(_unireg7_0),Y", "A-NUM")
            self.createcode("BVC", label, "if V is 0, N eor V, otherwise N eor V = N eor 1")
            self.createcode("EOR", "#$80", "A = A eor $80, and N = N eor 1")
            self.createcode("BMI", lessthenlabel,"if the N flag is 1, then (signed) < NUM(signed) and BMI will branch", name=label)
            self.createcode("BVC", label2)
            self.createcode("EOR", "#$80")
            self.createcode("BNE", label3, name=label2)
            self.createcode("DEY")
            self.createcode("LDA", "(_unireg6_0),Y")
            self.createcode("SBC", "(_unireg7_0),Y")
            self.createcode("BCC", lessthenlabel)
            self.createcode("LDA", "#0", name=label3)
            self.createcode("JMP", endcode)
            self.createcode("LDA", "#1", name=lessthenlabel)
            self.createcode("LDY", "#0", name=endcode)
            self.createcode("STA", "(_unireg6_0),Y")
        if size == 4:
            self.createcode("LDY", "#3", "checking high byte with signed algorithm")
            self.createcode("SEC", "", "prepare carry for SBC")
            self.createcode("LDA", "(_unireg6_0),Y")
            self.createcode("SBC", "(_unireg7_0),Y", "A-NUM")
            self.createcode("BVC", label, "if V is 0, N eor V, otherwise N eor V = N eor 1")
            self.createcode("EOR", "#$80", "A = A eor $80, and N = N eor 1")
            self.createcode("BMI", lessthenlabel,"if the N flag is 1, then (signed) < NUM(signed) and BMI will branch", name=label)
            self.createcode("BVC", label2)
            self.createcode("EOR", "#$80")
            self.createcode("BNE", label3, name=label2)
            for x in range(3):
                self.createcode("DEY")
                self.createcode("LDA", "(_unireg6_0),Y")
                self.createcode("SBC", "(_unireg7_0),Y")
                self.createcode("BCC", lessthenlabel)
                self.createcode("BNE", label3)
            #
            self.createcode("LDA", "#0", name=label3)
            self.createcode("JMP", endcode)
            self.createcode("LDA", "#1", name=lessthenlabel)
            self.createcode("LDY", "#0", name=endcode)
            self.createcode("STA", "(_unireg6_0),Y")
        if size == 8:
            self.createcode("LDY", "#7", "checking high byte with signed algorithm")
            self.createcode("SEC", "", "prepare carry for SBC")
            self.createcode("LDA", "(_unireg6_0),Y")
            self.createcode("SBC", "(_unireg7_0),Y", "A-NUM")
            self.createcode("BVC", label, "if V is 0, N eor V, otherwise N eor V = N eor 1")
            self.createcode("EOR", "#$80", "A = A eor $80, and N = N eor 1")
            self.createcode("BMI", lessthenlabel,"if the N flag is 1, then (signed) < NUM(signed) and BMI will branch", name=label)
            self.createcode("BVC", label2)
            self.createcode("EOR", "#$80")
            self.createcode("BNE", label3, name=label2)
            for x in range(7):
                self.createcode("DEY")
                self.createcode("LDA", "(_unireg6_0),Y")
                self.createcode("SBC", "(_unireg7_0),Y")
                self.createcode("BCC", lessthenlabel)
                self.createcode("BNE", label3)
            #
            self.createcode("LDA", "#0", name=label3)
            self.createcode("JMP", endcode)
            self.createcode("LDA", "#1", name=lessthenlabel)
            self.createcode("LDY", "#0", name=endcode)
            self.createcode("STA", "(_unireg6_0),Y")
        self.createcode("", "", "exit check for equal", name=exitlabel)
        self.createcode("LDA", "#%d" % self.eval_sizeforvar, "add stack for two var")
        self.createcode("JSR", "addaccuto_unireg7", "add from ureg7")
        # ----------------------------------------
        if self.createvirtsub:
            self.stopconvertedsubroutine()
            self.createcode("JSR", convertedsubname)

    def greaterstack(self, options):
        # ----------------------------------------
        subsalt = self.randomconst(8)
        convertedsubname = "greateronstack_"+str(self.eval_opsize) # + '_' + subsalt
        if self.createvirtsub:
            self.createcode("","","Calling GREATERONSTACK as virtual Subroutine")
            self.startconvertedsubroutine(convertedsubname)
        # ----------------------------------------
        self.createcode("","","EQUALGREATER TEST")
        size = self.eval_opsize
        self.log.writelog("codeemitter/greateronstack", "size:%s" % (size))
        #
        self.createcode("CLC")
        self.createcode("LDA", "_unireg7_0")
        self.createcode("ADC", "#%d" % self.eval_sizeforvar)
        self.createcode("STA", "_unireg6_0")
        self.createcode("LDA", "_unireg7_1")
        self.createcode("ADC", "#0")
        self.createcode("STA", "_unireg6_1")
        #
        label = self.randomword(8)
        exitlabel = self.randomword(8)
        endcode = self.randomword(8)
        greaterthenlabel = self.randomword(8)
        higherthenlabel = self.randomword(8)
        samethenlabel = self.randomword(8)
        checkbranch = self.randomword(8)
        label1 = self.randomword(8)
        label2 = self.randomword(8)
        label3 = self.randomword(8)
        if size == 1:  # testet ok
            self.createcode("LDY", "#0", "checking byte with signed algorithm")
            self.createcode("SEC", "", "prepare carry for SBC")
            self.createcode("LDA", "(_unireg6_0),Y")
            self.createcode("SBC", "(_unireg7_0),Y", "A-NUM")
            self.createcode("BVC", label, "if V is 0, N eor V, otherwise N eor V = N eor 1")
            self.createcode("EOR", "#$80", "A = A eor $80, and N = N eor 1")
            self.createcode("BPL", greaterthenlabel,"if the N flag is 1, then (signed) < NUM(signed) and BMI will branch", name=label)
            self.createcode("LDA", "#0", "not less", name=samethenlabel)
            self.createcode("JMP", endcode)
            self.createcode("BEQ", samethenlabel, name=greaterthenlabel)
            self.createcode("LDA", "#1")
            self.createcode("JMP", endcode)
            self.createcode("STA", "(_unireg6_0),Y", name=endcode)
        if size == 2: # maybe ok ;-)
            self.createcode("LDY", "#1", "checking high byte with signed algorithm")
            self.createcode("SEC", "", "prepare carry for SBC")
            self.createcode("LDA", "(_unireg7_0),Y")
            self.createcode("SBC", "(_unireg6_0),Y", "A-NUM")
            self.createcode("BVC", label, "if V is 0, N eor V, otherwise N eor V = N eor 1")
            self.createcode("EOR", "#$80", "A = A eor $80, and N = N eor 1")
            self.createcode("BMI", label1,"if the N flag is 1, then (signed) < NUM(signed) and BMI will branch", name=label)
            self.createcode("BVC", label2)
            self.createcode("EOR", "#$80")
            self.createcode("BNE", label3, name=label2)
            self.createcode("DEY")
            self.createcode("LDA", "(_unireg7_0),Y")
            self.createcode("SBC", "(_unireg6_0),Y")
            self.createcode("BCC", label1)
            self.createcode("LDA", "#0", name=label3)
            self.createcode("JMP", endcode)
            self.createcode("LDA", "#1", name=label1)
            self.createcode("LDY", "#0", name=endcode)
            self.createcode("STA", "(_unireg6_0),Y")
        if size == 4:
            self.createcode("LDY", "#3", "checking high byte with signed algorithm")
            self.createcode("SEC", "", "prepare carry for SBC")
            self.createcode("LDA", "(_unireg7_0),Y")
            self.createcode("SBC", "(_unireg6_0),Y", "A-NUM")
            self.createcode("BVC", label, "if V is 0, N eor V, otherwise N eor V = N eor 1")
            self.createcode("EOR", "#$80", "A = A eor $80, and N = N eor 1")
            self.createcode("BMI", label1,"if the N flag is 1, then (signed) < NUM(signed) and BMI will branch", name=label)
            self.createcode("BVC", label2)
            self.createcode("EOR", "#$80")
            self.createcode("BNE", label3, name=label2)
            for x in range(3):
                self.createcode("DEY")
                self.createcode("LDA", "(_unireg7_0),Y")
                self.createcode("SBC", "(_unireg6_0),Y")
                self.createcode("BCC", label1)
                self.createcode("BNE", label3)
            self.createcode("BEQ", label3, "if lobyte is equal, then return false, for >")
            self.createcode("LDA", "#0", name=label3)
            self.createcode("JMP", endcode)
            self.createcode("LDA", "#1", name=label1)
            self.createcode("LDY", "#0", name=endcode)
            self.createcode("STA", "(_unireg6_0),Y")
        if size == 8:
            self.createcode("LDY", "#7", "checking high byte with signed algorithm")
            self.createcode("SEC", "", "prepare carry for SBC")
            self.createcode("LDA", "(_unireg7_0),Y")
            self.createcode("SBC", "(_unireg6_0),Y", "A-NUM")
            self.createcode("BVC", label, "if V is 0, N eor V, otherwise N eor V = N eor 1")
            self.createcode("EOR", "#$80", "A = A eor $80, and N = N eor 1")
            self.createcode("BMI", label1,"if the N flag is 1, then (signed) < NUM(signed) and BMI will branch", name=label)
            self.createcode("BVC", label2)
            self.createcode("EOR", "#$80")
            self.createcode("BNE", label3, name=label2)
            for x in range(7):
                self.createcode("DEY")
                self.createcode("LDA", "(_unireg7_0),Y")
                self.createcode("SBC", "(_unireg6_0),Y")
                self.createcode("BCC", label1)
                self.createcode("BNE", label3)
            self.createcode("BEQ", label3, "if lobyte is equal, then return false, for >")
            self.createcode("LDA", "#0", name=label3)
            self.createcode("JMP", endcode)
            self.createcode("LDA", "#1", name=label1)
            self.createcode("LDY", "#0", name=endcode)
            self.createcode("STA", "(_unireg6_0),Y")
        self.createcode("", "", "exit check for equal", name=exitlabel)
        self.createcode("LDA", "#%d" % self.eval_sizeforvar, "add stack for two var")
        self.createcode("JSR", "addaccuto_unireg7", "add from ureg7")
        # ----------------------------------------
        if self.createvirtsub:
            self.stopconvertedsubroutine()
            self.createcode("JSR", convertedsubname)

    def equalgreaterstack(self, options):
        # ----------------------------------------
        subsalt = self.randomconst(8)
        convertedsubname = "eqgreateronstack_"+str(self.eval_opsize) # + '_' + subsalt
        if self.createvirtsub:
            self.createcode("","","Calling EQUALGREATERONSTACK as virtual Subroutine")
            self.startconvertedsubroutine(convertedsubname)
        # ----------------------------------------
        self.createcode("","","EQUALGREATERSTACK TEST")
        size = self.eval_opsize
        self.log.writelog("codeemitter/equalgreateronstack", "size:%s" % (size))
        #
        self.createcode("CLC")
        self.createcode("LDA", "_unireg7_0")
        self.createcode("ADC", "#%d" % self.eval_sizeforvar)
        self.createcode("STA", "_unireg6_0")
        self.createcode("LDA", "_unireg7_1")
        self.createcode("ADC", "#0")
        self.createcode("STA", "_unireg6_1")
        #
        label = self.randomword(8)
        exitlabel = self.randomword(8)
        greaterthenlabel = self.randomword(8)
        endcode = self.randomword(8)
        label1 = self.randomword(8)
        label2 = self.randomword(8)
        label3 = self.randomword(8)
        if size == 1: # tested ok!
            self.createcode("LDY", "#0", "checking byte with signed algorithm")
            self.createcode("SEC", "", "prepare carry for SBC")
            self.createcode("LDA", "(_unireg6_0),Y")
            self.createcode("SBC", "(_unireg7_0),Y", "A-NUM")
            self.createcode("BVC", label, "if V is 0, N eor V, otherwise N eor V = N eor 1")
            self.createcode("EOR", "#$80", "A = A eor $80, and N = N eor 1")
            self.createcode("BPL", greaterthenlabel,"if the N flag is 1, then (signed) < NUM(signed) and BMI will branch", name=label)
            self.createcode("LDA", "#0", "less")
            self.createcode("JMP", endcode)
            self.createcode("LDA", "#1", name=greaterthenlabel)
            self.createcode("JMP", endcode)
            self.createcode("STA", "(_unireg6_0),Y", name=endcode)
        if size == 2:  # maybe ok ;-)
            self.createcode("LDY", "#1", "checking high byte with signed algorithm")
            self.createcode("SEC", "", "prepare carry for SBC")
            self.createcode("LDA", "(_unireg7_0),Y")
            self.createcode("SBC", "(_unireg6_0),Y", "A-NUM")
            self.createcode("BVC", label, "if V is 0, N eor V, otherwise N eor V = N eor 1")
            self.createcode("EOR", "#$80", "A = A eor $80, and N = N eor 1")
            self.createcode("BMI", label1,"if the N flag is 1, then (signed) < NUM(signed) and BMI will branch", name=label)
            self.createcode("BVC", label2)
            self.createcode("EOR", "#$80")
            self.createcode("BNE", label3, name=label2)
            self.createcode("DEY")
            self.createcode("LDA", "(_unireg7_0),Y")
            self.createcode("SBC", "(_unireg6_0),Y")
            self.createcode("BCC", label1)
            self.createcode("BEQ", label1, "if lobyte is equal, then return true, for >=")
            self.createcode("LDA", "#0", name=label3)
            self.createcode("JMP", endcode)
            self.createcode("LDA", "#1", name=label1)
            self.createcode("LDY", "#0", name=endcode)
            self.createcode("STA", "(_unireg6_0),Y")
        if size == 4:
            self.createcode("LDY", "#3", "checking high byte with signed algorithm")
            self.createcode("SEC", "", "prepare carry for SBC")
            self.createcode("LDA", "(_unireg7_0),Y")
            self.createcode("SBC", "(_unireg6_0),Y", "A-NUM")
            self.createcode("BVC", label, "if V is 0, N eor V, otherwise N eor V = N eor 1")
            self.createcode("EOR", "#$80", "A = A eor $80, and N = N eor 1")
            self.createcode("BMI", label1,"if the N flag is 1, then (signed) < NUM(signed) and BMI will branch", name=label)
            self.createcode("BVC", label2)
            self.createcode("EOR", "#$80")
            self.createcode("BNE", label3, name=label2)
            for x in range(3):
                self.createcode("DEY")
                self.createcode("LDA", "(_unireg7_0),Y")
                self.createcode("SBC", "(_unireg6_0),Y")
                self.createcode("BCC", label1)
                self.createcode("BNE", label3)
            self.createcode("BEQ", label1, "if lobyte is equal, then return true, for >=")
            self.createcode("LDA", "#0", name=label3)
            self.createcode("JMP", endcode)
            self.createcode("LDA", "#1", name=label1)
            self.createcode("LDY", "#0", name=endcode)
            self.createcode("STA", "(_unireg6_0),Y")
        if size == 8:
            self.createcode("LDY", "#7", "checking high byte with signed algorithm")
            self.createcode("SEC", "", "prepare carry for SBC")
            self.createcode("LDA", "(_unireg7_0),Y")
            self.createcode("SBC", "(_unireg6_0),Y", "A-NUM")
            self.createcode("BVC", label, "if V is 0, N eor V, otherwise N eor V = N eor 1")
            self.createcode("EOR", "#$80", "A = A eor $80, and N = N eor 1")
            self.createcode("BMI", label1,"if the N flag is 1, then (signed) < NUM(signed) and BMI will branch", name=label)
            self.createcode("BVC", label2)
            self.createcode("EOR", "#$80")
            self.createcode("BNE", label3, name=label2)
            for x in range(7):
                self.createcode("DEY")
                self.createcode("LDA", "(_unireg7_0),Y")
                self.createcode("SBC", "(_unireg6_0),Y")
                self.createcode("BCC", label1)
                self.createcode("BNE", label3)
            self.createcode("BEQ", label1, "if lobyte is equal, then return true, for >=")
            self.createcode("LDA", "#0", name=label3)
            self.createcode("JMP", endcode)
            self.createcode("LDA", "#1", name=label1)
            self.createcode("LDY", "#0", name=endcode)
            self.createcode("STA", "(_unireg6_0),Y")
        self.createcode("", "", "exit check for equal", name=exitlabel)
        self.createcode("LDA", "#%d" % self.eval_sizeforvar, "add stack for two var")
        self.createcode("JSR", "addaccuto_unireg7", "add from ureg7")
        # ----------------------------------------
        if self.createvirtsub:
            self.stopconvertedsubroutine()
            self.createcode("JSR", convertedsubname)
    
    def equalsmallerstack(self, options):
        # ----------------------------------------
        subsalt = self.randomconst(8)
        convertedsubname = "eqsmalleronstack_"+str(self.eval_opsize) # + '_' + subsalt
        if self.createvirtsub:
            self.createcode("","","Calling EQUALSMALLERONSTACK as virtual Subroutine")
            self.startconvertedsubroutine(convertedsubname)
        # ----------------------------------------
        size = self.eval_opsize
        self.log.writelog("codeemitter/equalsmalleronstack", "size:%s" % (size))
        #
        self.createcode("CLC")
        self.createcode("LDA", "_unireg7_0")
        self.createcode("ADC", "#%d" % self.eval_sizeforvar)
        self.createcode("STA", "_unireg6_0")
        self.createcode("LDA", "_unireg7_1")
        self.createcode("ADC", "#0")
        self.createcode("STA", "_unireg6_1")
        #
        label = self.randomword(8)
        exitlabel = self.randomword(8)
        lessthenlabel = self.randomword(8)
        endcode = self.randomword(8)
        label2 = self.randomword(8)
        label3 = self.randomword(8)
        self.createcode("","","EQUALSMALLERSTACK TEST opsize:%d" % size)
        if size == 1: # tested ok !
            self.createcode("LDY", "#0", "checking with signed algorithm")
            self.createcode("SEC", "", "prepare carry for SBC")
            self.createcode("LDA", "(_unireg6_0),Y")
            self.createcode("SBC", "(_unireg7_0),Y", "A-NUM")
            self.createcode("BVC", label, "if V is 0, N eor V, otherwise N eor V = N eor 1")
            self.createcode("EOR", "#$80", "A = A eor $80, and N = N eor 1")
            self.createcode("BMI", lessthenlabel,"if the N flag is 1, then (signed) < NUM(signed) and BMI will branch", name=label)
            self.createcode("BEQ", lessthenlabel, "we are in lessequal, so equal is also true")
            self.createcode("LDA", "#0", "not less")
            self.createcode("JMP", endcode)
            self.createcode("LDA", "#1", name=lessthenlabel)
            self.createcode("JMP", endcode)
            self.createcode("STA", "(_unireg6_0),Y", name=endcode)
        if size == 2: # maybe ok ;-)
            self.createcode("LDY", "#1", "checking high byte with signed algorithm")
            self.createcode("SEC", "", "prepare carry for SBC")
            self.createcode("LDA", "(_unireg6_0),Y")
            self.createcode("SBC", "(_unireg7_0),Y", "A-NUM")
            self.createcode("BVC", label, "if V is 0, N eor V, otherwise N eor V = N eor 1")
            self.createcode("EOR", "#$80", "A = A eor $80, and N = N eor 1")
            self.createcode("BMI", lessthenlabel,"if the N flag is 1, then (signed) < NUM(signed) and BMI will branch", name=label)
            self.createcode("BVC", label2)
            self.createcode("EOR", "#$80")
            self.createcode("BNE", label3, name=label2)
            self.createcode("DEY")
            self.createcode("LDA", "(_unireg6_0),Y")
            self.createcode("SBC", "(_unireg7_0),Y")
            self.createcode("BCC", lessthenlabel)
            self.createcode("BEQ", lessthenlabel, "if values are equal return true, because we are in =<")
            self.createcode("LDA", "#0", name=label3)
            self.createcode("JMP", endcode)
            self.createcode("LDA", "#1", name=lessthenlabel)
            self.createcode("LDY", "#0", name=endcode)
            self.createcode("STA", "(_unireg6_0),Y")
        if size == 4:
            self.createcode("LDY", "#3", "checking high byte with signed algorithm")
            self.createcode("SEC", "", "prepare carry for SBC")
            self.createcode("LDA", "(_unireg6_0),Y")
            self.createcode("SBC", "(_unireg7_0),Y", "A-NUM")
            self.createcode("BVC", label, "if V is 0, N eor V, otherwise N eor V = N eor 1")
            self.createcode("EOR", "#$80", "A = A eor $80, and N = N eor 1")
            self.createcode("BMI", lessthenlabel,"if the N flag is 1, then (signed) < NUM(signed) and BMI will branch", name=label)
            self.createcode("BVC", label2)
            self.createcode("EOR", "#$80")
            self.createcode("BNE", label3, name=label2)

            for x in range(3):
                self.createcode("DEY")
                self.createcode("LDA", "(_unireg6_0),Y")
                self.createcode("SBC", "(_unireg7_0),Y")
                self.createcode("BCC", lessthenlabel)
                self.createcode("BNE", label3)
            self.createcode("BEQ", lessthenlabel, "if values are equal return true, because we are in =<")
            self.createcode("LDA", "#0", name=label3)
            self.createcode("JMP", endcode)
            self.createcode("LDA", "#1", name=lessthenlabel)
            self.createcode("LDY", "#0", name=endcode)
            self.createcode("STA", "(_unireg6_0),Y")
        if size == 8:
            self.createcode("LDY", "#7", "checking high byte with signed algorithm")
            self.createcode("SEC", "", "prepare carry for SBC")
            self.createcode("LDA", "(_unireg6_0),Y")
            self.createcode("SBC", "(_unireg7_0),Y", "A-NUM")
            self.createcode("BVC", label, "if V is 0, N eor V, otherwise N eor V = N eor 1")
            self.createcode("EOR", "#$80", "A = A eor $80, and N = N eor 1")
            self.createcode("BMI", lessthenlabel,"if the N flag is 1, then (signed) < NUM(signed) and BMI will branch", name=label)
            self.createcode("BVC", label2)
            self.createcode("EOR", "#$80")
            self.createcode("BNE", label3, name=label2)
            
            for x in range(7):
                self.createcode("DEY")
                self.createcode("LDA", "(_unireg6_0),Y")
                self.createcode("SBC", "(_unireg7_0),Y")
                self.createcode("BCC", lessthenlabel)
                self.createcode("BNE", label3)
            self.createcode("BEQ", lessthenlabel, "if values are equal return true, because we are in =<")
            self.createcode("LDA", "#0", name=label3)
            self.createcode("JMP", endcode)
            self.createcode("LDA", "#1", name=lessthenlabel)
            self.createcode("LDY", "#0", name=endcode)
            self.createcode("STA", "(_unireg6_0),Y")
        self.createcode("", "", "exit check for equal", name=exitlabel)
        self.createcode("LDA", "#%d" % self.eval_sizeforvar, "add stack for two var")
        self.createcode("JSR", "addaccuto_unireg7", "add from ureg7")
        # ----------------------------------------
        if self.createvirtsub:
            self.stopconvertedsubroutine()
            self.createcode("JSR", convertedsubname)
    
    def pushregistertouserstack(self, regname, options):
        subpushreg = self.randomconst(8)
        convertedsubname = "pushreg%s" % (regname)
        if self.createvirtsub:
            self.createcode("","","Calling pushregistertouserstack as virtual Subroutine")
            self.startconvertedsubroutine(convertedsubname)
        self.createcode("SEC")
        self.createcode("LDA", "_userstack_0")
        self.createcode("SBC", "#8")
        self.createcode("STA", "_userstack_0")
        self.createcode("LDA", "_userstack_1")
        self.createcode("SBC", "#0")
        self.createcode("STA", "_userstack_1")
        #
        #self.createcode("JSR", "_OUT_UNIREG7")
        #self.createcode("JSR", "_OUTPUTCRLF")
        #self.createcode("JSR", "_OUT_USERSTACK")
        #

        self.createcode("LDY", "#7")
        self.createcode("LDA", "%s,Y" % regname, name=subpushreg)
        self.createcode("STA", "(_userstack_0),Y")
        self.createcode("DEY")
        self.createcode("BPL", subpushreg)

        if self.createvirtsub:
            self.stopconvertedsubroutine()
            self.createcode("JSR", convertedsubname)
        #self.createcode("JMP", "wozmon")

    def popregisterfromuserstack(self, regname, options):
        subpopreg = self.randomconst(8)
        convertedsubname = "popreg%s" % (regname)
        if self.createvirtsub:
            self.createcode("","","Calling popregisterfromuserstack as virtual Subroutine")
            self.startconvertedsubroutine(convertedsubname)
        #self.createcode("JSR", "_OUT_USERSTACK")
        self.createcode("LDY", "#7")
        self.createcode("LDA", "(_userstack),Y", name=subpopreg)
        self.createcode("STA", "%s,Y" % regname)
        self.createcode("DEY")
        self.createcode("BPL", subpopreg)
        #self.createcode("JSR", "_OUT_UNIREG7")
        #self.createcode("JSR", "_OUTPUTCRLF")

        self.createcode("LDA", "#8")
        self.createcode("CLC")
        self.createcode("ADC", "_userstack_0")
        self.createcode("STA", "_userstack_0")
        self.createcode("LDA", "#0")
        self.createcode("ADC", "_userstack_1")
        self.createcode("STA", "_userstack_1")
        if self.createvirtsub:
            self.stopconvertedsubroutine()
            self.createcode("JSR", convertedsubname)
        #self.createcode("JMP", "wozmon")

    def funcfromexpression(self, functoken, options):
        fctname = functoken.getname()
        if fctname == "testfunc1":
            xxxxx = 0
        fctdata = functoken.getfuncdata()
        fctargs = fctdata.arg_objects
        fctarglen = len(fctargs)
        fctsize = functoken.getsize()
        
        debug = self.debug_espression
        size = self.eval_opsize
        self.log.writelog("codeemitter/funcfromexpression", "size:%s, functionname:%s" % (size, fctname))
        self.createcode("","","FUNCFROMEXPRESSION: %s" % fctname)
        #
        # self.createcode("JSR", "_OUTAT_UNIREG7")
        # set pointer for 2nd stackmember in unireg6
        #
        if False: # subract to adjust Stack
            correctsize = 0 # int(self.eval_sizeforvar*fctarglen)
            self.createcode("SEC")
            self.createcode("LDA", "_unireg7_0")
            self.createcode("SBC", "#%d" % correctsize)
            self.createcode("STA", "_unireg6_0")
            self.createcode("LDA", "_unireg7_1")
            self.createcode("SBC", "#0")
            self.createcode("STA", "_unireg6_1")
        else:
            # set pointer in unireg6 from unireg7, wich is the top of stack, modifiy unireg6 for more then 1 argument
            self.createcode("LDA", "_unireg7_0")
            self.createcode("STA", "_unireg6_0")
            self.createcode("LDA", "_unireg7_1")
            self.createcode("STA", "_unireg6_1")
        # self.createcode("JSR", "_OUTAT_UNIREG6")
        # unireg7 and now unireg6 points to beginning of data, where every 8 byte starts a new parameter
        # self.createcode("JSR", "_OUT_UNIREG7")
        # self.createcode("JSR", "wozmon")
        if fctarglen > 0:
            # set framepointer to beginning of local vars of called function, if function has parameter
            stackcorrection = 8   # stack will differ by 8 bytes because of popunireg7 later
            stackframelength = "#%s_sflast+%d" % (fctname, stackcorrection)
            self.createcode("SEC", "", "CREATEFUNCTIONCALL for: %s" % fctname)
            self.createcode("LDA", "_userstack_0", "SET FRAMEPOINTER to end of called function")
            self.createcode("SBC", stackframelength, "for having access to parameters")
            self.createcode("STA", "_framepointer_0", "store in framepointer lo byte")
            self.createcode("LDA", "_userstack_1", "load userstack hi-byte")
            self.createcode("SBC", "#0", "subtract with carry")
            self.createcode("STA", "_framepointer_1", "save to framepointer hi byte")
        if len(fctargs) == 0:
            varsize = fctsize
        argcount = 0
        for arg in fctargs:
            loadfuncloop = self.randomword(8)    
            varname = arg.getvarname()
            vartype = arg.getvartype()
            varnamespace = arg.getnamespace()
            vartoken = self.stokens.getwithnamespace(varname, varnamespace)
            varnamewithnamespace = vartoken.getnamewithnamespace()
            varsize = vartoken.getsize()
            varaddress = arg.getaddress()
            #self.createcode("JSR", "_OUTAT_UNIREG6")
            #self.createcode("JSR", "_OUT_FRAMEPOINTER")
            #self.createcode("JMP", "wozmon")
            #
            self.createcode("CLC")
            self.createcode("LDA", "_framepointer_0")
            self.createcode("ADC", "#%s" % varnamewithnamespace, "add offet of var %s to pointer" %  varname)
            self.createcode("STA", "_unireg5_0")
            self.createcode("LDA", "_framepointer_1")
            self.createcode("ADC", "#0")
            self.createcode("STA", "_unireg5_1")
            self.createcode("LDY", "#%d" % (varsize - 1))
            self.createcode("LDA", "(_unireg6),Y", "Load from source (stack)", name=loadfuncloop)
            self.createcode("STA", "(_unireg5),Y", "Store to destination")
            self.createcode("DEY")
            self.createcode("BPL", loadfuncloop)
            # one item from stack copied, correct stack to next item by adding size for entry
            # self.createcode("JSR", "_OUTAT_FRAMEPOINTER")
            # self.createcode("JMP", "wozmon")
            #
            argcount += 1
            if len(fctargs) > argcount:
                self.createcode("CLC")
                self.createcode("LDA", "_unireg6_0")
                self.createcode("ADC", "#8")
                self.createcode("STA", "_unireg6_0")
                self.createcode("LDA", "_unireg6_1")
                self.createcode("ADC", "#0")
                self.createcode("STA", "_unireg6_1")
        # call function
        # A T T E N T I O N: using pushregister to user stack will put framepointer out of scope
        # see stackcorrection at the beginning for handling this problem
        self.pushregistertouserstack("_unireg7", None)
        self.createcode("JSR", fctname, "call function")
        self.popregisterfromuserstack("_unireg7", None)
        if fctarglen == 0:
            # function without a parameter creates a new stackentry
            # subracting the for create this entry
            self.createcode("SEC")
            self.createcode("LDA", "_unireg7_0")
            self.createcode("SBC", "#8")
            self.createcode("STA", "_unireg7_0")
            self.createcode("LDA", "_unireg7_1")
            self.createcode("SBC", "#0")
            self.createcode("STA", "_unireg7_1")
        # print result from _unireg0
        # self.createcode("JSR", "_OUT_UNIREG7")
        # copy from _unireg0 to position at _unireg7
        resultloop = self.randomword(8)  
        self.createcode("LDY", "#%d" % (varsize - 1))
        self.createcode("LDA", "_unireg0,Y", "Load from source (stack)", name=resultloop)
        self.createcode("STA", "(_unireg7),Y", "Store to destination")
        self.createcode("DEY")
        self.createcode("BPL", resultloop)
        # -------------------------------- END OF CODE ------------------------------
        if fctarglen == 0:
            fctarglen = 0
        self.createcode("LDA", "#%d" % int(self.eval_sizeforvar * (fctarglen  - 1)), "add stack")
        self.createcode("JSR", "addaccuto_unireg7", "add from ureg7")
        # ----------------------------------------
        # self.createcode("JSR", "_OUTAT_UNIREG7")
        #self.createcode("JMP", "wozmon")

    def internalfuncfromexpression(self,functoken, options):
        fctname = functoken.getname()
        if fctname == "testfunc1":
            xxxxx = 0
        fctdata = functoken.getfuncdata()
        fctargs = fctdata.arg_objects
        fctarglen = len(fctargs)
        fctsize = functoken.getsize()
        
        debug = self.debug_espression
        size = self.eval_opsize
        self.log.writelog("codeemitter/internalfuncfromexpression", "size:%s, functionname:%s" % (size, fctname))
        self.createcode("","","INTERNALFUNCFROMEXPRESSION: %s" % fctname)
        #
        # self.createcode("JSR", "_OUTAT_UNIREG7")
        # set pointer for 2nd stackmember in unireg6
        #
        if False: # subract to adjust Stack
            correctsize = 0 # int(self.eval_sizeforvar*fctarglen)
            self.createcode("SEC")
            self.createcode("LDA", "_unireg7_0")
            self.createcode("SBC", "#%d" % correctsize)
            self.createcode("STA", "_unireg6_0")
            self.createcode("LDA", "_unireg7_1")
            self.createcode("SBC", "#0")
            self.createcode("STA", "_unireg6_1")
        else:
            # set pointer in unireg6 from unireg7, wich is the top of stack, modifiy unireg6 for more then 1 argument
            self.createcode("LDA", "_unireg7_0")
            self.createcode("STA", "_unireg6_0")
            self.createcode("LDA", "_unireg7_1")
            self.createcode("STA", "_unireg6_1")
        # self.createcode("JSR", "_OUTAT_UNIREG6")
        # unireg7 and now unireg6 points to beginning of data, where every 8 byte starts a new parameter
        # self.createcode("JSR", "_OUT_UNIREG7")
        # self.createcode("JSR", "wozmon")
        varsize = fctsize
        argcount = 0
        for arg in fctargs:
            loadfuncloop = self.randomword(8)    
            varname = arg.getvarname()
            vartype = arg.getvartype()
            varnamespace = arg.getnamespace()
            vartoken = self.stokens.getwithnamespace(varname, varnamespace)
            varnamewithnamespace = vartoken.getnamewithnamespace()
            tokenvarsize = vartoken.getsize()
            varaddress = arg.getaddress()
            #self.createcode("JSR", "_OUTAT_UNIREG6")
            #self.createcode("JSR", "_OUT_FRAMEPOINTER")
            #self.createcode("JMP", "wozmon")
            #
            self.createcode("LDY", "#%d" % (fctsize - 1))
            self.createcode("LDA", "(_unireg6),Y", "Load source from stack", name=loadfuncloop)
            if varnamespace == "global":
                self.createcode("STA", "%s,Y" % varname)
            else:
                self.createcode("STA", "%s,Y" % varnamewithnamespace)
            self.createcode("DEY")
            self.createcode("BPL", loadfuncloop)
        self.intfunc_tofloat(functoken, fctargs)
        resultloop = self.randomword(8)  
        self.createcode("LDY", "#%d" % (varsize - 1), "after infunc_tofloat, copy back result")
        if varnamespace == "global":
            self.createcode("LDA", "%s,Y" % varname, "Load from source (stack)", name=resultloop)
        else:
            self.createcode("LDA", "%s,Y" % varnamewithnamespace, "Load from source (stack)", name=resultloop)
        self.createcode("STA", "(_unireg7),Y", "Store to destination")
        self.createcode("DEY")
        self.createcode("BPL", resultloop)
        # -------------------------------- END OF CODE ------------------------------
        if fctarglen == 0:
            fctarglen = 0
        self.createcode("LDA", "#%d" % int(self.eval_sizeforvar * (fctarglen  - 1)), "add stack")
        self.createcode("JSR", "addaccuto_unireg7", "add from ureg7")

    # COPYVAR
    def copyvar(self, destvartoken, sourcevartok, ptr_a_dest=False, ptr_a_source=False, lineno=0):
        namespace = self.blocks.getactivefunctionname()
        sourcenamespace = sourcevartok.getnamespace()
        sourcevarname = sourcenamespace + '_' + sourcevartok.getname()
        destnamespace = destvartoken.getnamespace()
        destvarname = destnamespace + '_' + destvartoken.getname()
        destaddr = destvartoken.getaddress()
        destsize = destvartoken.getsize()
        sourceaddr = sourcevartok.getaddress()
        sourcesize = sourcevartok.getsize()
        destsize = destvartoken.getsize()
        unireg6token = self.stokens.get("_unireg6")
        unireg7token = self.stokens.get("_unireg7")
        label1 = self.randomword(8)
        source_size = sourcevartok.getsize()
        source_attr = sourcevartok.getattributehash()
        destisregister = sourceisregister = False
        if self.checkhash(source_attr, "cpuregister"):
            sourcevarname = sourcevartok.getname()
            sourceisregister = True
        dest_size = destvartoken.getsize()
        dest_attr = destvartoken.getattributehash()
        if self.checkhash(dest_attr, "cpuregister"):
            destvarname = destvartoken.getname()
            destisregister = True
        # access to parameter from inside the function uses _userstack instead of _framepointer
        if self.checkhash(dest_attr, "isargument"): # and namespace == sourcenamespace:
            destframetok = self.stokens.get("_framepointer")
            destframe0 = "_framepointer_0"
            destframe1 = "_framepointer_1"
        else:
            destframetok = self.stokens.get("_userstack")
            destframe0 = "_userstack_0"
            destframe1 = "_userstack_1"
        # access to parameter from inside the function uses _userstack instead of _framepointer
        if self.checkhash(source_attr, "isargument"): # and namespace == destnamespace:
            sourceframetok = self.stokens.get("_framepointer")
            sourceframe0 = "_framepointer_0"
            sourceframe1 = "_framepointer_1"
        else:
            sourceframetok = self.stokens.get("_userstack")
            sourceframe0 = "_userstack_0"
            sourceframe1 = "_userstack_1"
        if sourcevartok.cleartemppointer():
            ptr_a_source = True
        if destvartoken.cleartemppointer():
            ptr_a_dest = True
        if destvarname == "memdump_p":
            iii = 0
        if sourcevarname == "global_closebracket":
            iii = 0
        self.createcode("","","---COPYVAR (%d) (sourcename:%s, destname=%s, srcsize:%d, dstsize:%d, srcregister:%s, destregister:%s)" % (lineno, sourcevarname, destvarname, source_size, dest_size, sourceisregister, destisregister))
        if self.checkhash(source_attr, "type_stringconst"):
            if destnamespace == "global":
                idx = 0
                self.createcode("LDA", "#<%s" % sourcevarname, "CONSTSTRING handling, stringaddress to register, load lobyte of address")
                self.createcode("STA", "%s_%d" % (destvarname, idx))
                idx += 1
                self.createcode("LDA", "#>%s" % sourcevarname, "load hi-byte address for string constant")
                self.createcode("STA", "%s_%d" % (destvarname, idx))
            else:
                self.createcode("LDA", "#<%s" % sourcevarname, "CONSTSTRING handling, stringaddress to register, load lobyte of address")
                self.createcode("LDY", "#%s" % destvarname, "set pointer to destination address")
                self.createcode("STA", "(%s),Y" % destframe0, "save lo byte")
                self.createcode("INY","", "jump to hi byte")
                self.createcode("LDA", "#>%s" % sourcevarname, "load hi-byte address for string constant")
                self.createcode("STA", "(%s),Y" % destframe0, "save hi byte")
            return
        if sourcenamespace == "global" and destnamespace == "global": # global global
            self.createcode("NOP", "", "COPYVAR GLOBAL GLOBAL")
            if dest_size != source_size:
                print("SRC:%s, DST:%s, sourcesize <> destsize (%d,%d)" % (sourcevarname, destvarname, source_size, dest_size))
                sys.exit(1)
            copysize = 0
            if dest_size < source_size:
                copysize = source_size
            else:
                copysize = dest_size
            for x in range(copysize):
                if sourceisregister:
                    srcregister = "%s_%d" % (sourcevarname, x)
                    srcregister = registerconvert[srcregister]
                    self.createcode("LDA", srcregister)
                else:
                    self.createcode("LDA", "%s,%d" % (sourcevarname, x))
                if destisregister:
                    destregister = "%s_%d" % (destvarname, x)
                    destregister = registerconvert[destregister]
                    self.createcode("STA", destregister)
                else:
                    self.createcode("STA", "%s_%d" % (destvarname, x))
            
        if sourcenamespace == "global" and destnamespace != "global": # global local
            self.createcode("NOP", "", "COPYVAR GLOBAL LOKAL src:%s, dest:%s, srcsize:%d, destsize:%s" % (sourcevarname, destvarname, source_size, dest_size))
            if dest_size < source_size:
                print("SRC:%s, DST:%s, sourcesize <> destsize (%d,%d)" % (sourcevarname, destvarname, source_size, dest_size))
                if sourceisregister:
                    print("SRC is register, ignoring size")
                else:
                    if self.checkhash(source_attr, "type_chararray"):
                        pass
                    else:
                        sys.exit(1)
            idx = 0
            if self.checkhash(source_attr, "type_chararray"):
                if dest_size == 2:
                    self.createcode("LDA", "#<%s" % sourcevarname, "copy from chararray:(%s) called" % sourcevarname)
                    self.createcode("LDY", "#%s" % destvarname, "load offset for destination")
                    self.createcode("STA", "(%s),Y" % destframe0, "store data to ptr")
                    self.createcode("LDA", "#>%s" % sourcevarname)
                    self.createcode("INY", "", "switch to next byte")
                    self.createcode("STA", "(%s),Y" % destframe0, "store date")
            elif dest_size == 1:
                self.createcode("LDA", sourcevarname, "load global char")
                self.createcode("LDY", "#%s" % destvarname, "load offset for destination")
                self.createcode("STA", "(%s),Y" % destframe0, "store data to ptr")
            elif dest_size == 2:
                self.createcode("LDA", sourcevarname, "copy int value")
                self.createcode("LDY", "#%s" % destvarname, "load offset for destination")
                self.createcode("STA", "(%s),Y" % destframe0, "store data to ptr")
                sourceaddr += 1
                idx += 1
                self.createcode("LDA", "%s_%d" % (sourcevarname, idx))
                self.createcode("INY", "", "switch to next byte")
                self.createcode("STA", "(%s),Y" % destframe0, "store date")
            elif dest_size == 4 or dest_size == 8:
                self.createcode("LDY", "#%s" % destvarname, "load offset for destination")
                for x in range(dest_size):
                    if sourceisregister:
                        sourceregister = "%s_%d" % (sourcevarname, x)
                        sourceregister = registerconvert[sourceregister]
                    else:
                        sourceregister = "%s_%d" % (sourcevarname, x)
                    self.createcode("LDA", "%s" % sourceregister, "copy global long value")
                    self.createcode("STA", "(%s),Y" % destframe0, "store data to ptr")
                    self.createcode("INY")
                    sourceaddr += 1
            else:
                print("unknown destination size in COPYVAR global to local")
                sys.exit(1)
        if sourcenamespace != "global" and destnamespace == "global": # local global
            self.createcode("","","COPYVAR local to global, source:%s, dest:%s" % (sourcevarname, destvarname))
            if dest_size == 1 or destisregister:
                if ptr_a_source:
                    if source_size == 1:
                        self.createcode("LDY", "#%s" % sourcevarname, "Load offset for %s" % sourcevarname)
                        self.createcode("LDA", "(%s),Y" % sourceframe0, "Pointer read operation")
                        self.createcode("STA", "_unireg7_0", "save address lo in register 7")
                        self.createcode("INY", "", "switch to hi byte")
                        self.createcode("LDA", "(%s),Y" % sourceframe0, "load hi address")
                        self.createcode("STA", "_unireg7_1", "save address lo in register 7")
                        self.createcode("LDY", "#0", "index is 0")
                        self.createcode("LDA", "(_unireg7),Y", "load from memoryaddress")
                        self.createcode("STA", destvarname, "Save to global address")
                else:
                    if source_size == 1:
                        self.createcode("LDY", "#%s" % sourcevarname, "load byte source (local,global)")
                        self.createcode("LDA", "(%s),Y" % sourceframe0, "load local var")
                        self.createcode("STA", destvarname, "save to destination")
                    elif source_size == 2:
                        self.createcode("LDY", "#%s" % sourcevarname, "load int source (local,global)")
                        self.createcode("LDA", "(%s),Y" % sourceframe0, "load local var")
                        self.createcode("STA", destvarname, "save to destination")
                        self.createcode("INY", "", "switch to next byte")
                        self.createcode("LDA", "(%s),Y" % sourceframe0, "load local var")
                        destaddr += 1
                        self.createcode("STA", "%s_1" % (destvarname), "save to destination")
                    elif source_size == 4 or source_size == 8:
                        self.createcode("LDY", "#%s" % sourcevarname, "load int source (local,global)")
                        for idx in range(source_size):
                            self.createcode("LDA", "(%s),Y" % sourceframe0, "load local var")
                            computeddestvarname = "%s_%d" % (destvarname, idx)
                            self.createcode("STA", "%s" % registerconvert[computeddestvarname], "save to destination")
                            if idx < source_size:
                                self.createcode("INY", "", "switch to next byte")
                    else:
                        self.createcode("NOP","", "not implemented")
        if sourcenamespace != "global" and destnamespace != "global": # local local
            if dest_size == 1 or destisregister:
                if ptr_a_dest:
                    pass
                else:
                    pass
                if ptr_a_source:
                    self.createcode("LDY", "#%s" % sourcevarname, "load index, copy from %s to %s" % (sourcevarname, destvarname))
                    self.createcode("LDA", "(%s),Y" % sourceframe0, "load from userstack")
                    self.createcode("STA", "_unireg0_0", "save address lo in register 0")
                    self.createcode("INY", "", "switch to hi byte")
                    self.createcode("LDA", "(%s),Y" % sourceframe0, "load hi address")
                    self.createcode("STA", "_unireg0_1", "save address lo in register 0")
                    self.createcode("LDY", "#0", "load index for destination")
                    self.createcode("LDA", "(_unireg0),Y", "load date from memoryaddress")
                    self.createcode("LDY", "#%s" % destvarname, "Load Index")
                    self.createcode("STA", "(%s),Y" % destframe0, "store in local var")
                else:
                    self.createcode("LDY", "#%s" % sourcevarname, "load index, copy from %s to %s" % (sourcevarname, destvarname))
                    self.createcode("LDA", "(%s),Y" % sourceframe0, "load from local var")
                    self.createcode("LDY", "#%s" % destvarname, "load index for destination")
                    self.createcode("STA", "(%s),Y" % destframe0, "save to local var")
            elif dest_size == 2 or destisregister:
                if ptr_a_dest:
                    self.createcode("LDY", "#%s" % sourcevarname, "load sourcevar (local,local)")
                    self.createcode("LDA", "(%s),Y" % sourceframe0, "load from sourcevar into accu")
                    self.createcode("PHA", "", "push accu to stack for later use")
                    self.createcode("LDY", "#%s" % destvarname, "load indexpt")
                    self.createcode("LDA", "(%s),Y" % destframe0, "load lo address from sourcevarname")
                    self.createcode("STA", "_unireg7_0", "store lo address to register 7")
                    self.createcode("INY","","increment pointer")
                    self.createcode("LDA", "(%s),Y" % destframe0, "load hi address from sourcevarname")
                    self.createcode("STA", "_unireg7_1", "store hi address to register 7")
                    self.createcode("PLA", "", "sourcedata from stack")
                    self.createcode("LDX", "#0", "index = 0")
                    self.createcode("STA", "(_unireg7,X)", "store sourcedata to destinationptr")
                elif ptr_a_source:
                    print("copyvar local -- local ptr_a_source not implemented")
                    sys.exit(1)
                else:
                    source_offset = sourcevartok.getaddress()
                    source_offset = 0
                    dest_offset = destvartoken.getaddress()
                    dest_offset = 0
                    firstelement = False
                    count = dest_size
                    for x in range(source_size):
                        if not firstelement:
                            self.createcode("LDY", "#%s" % (sourcevarname), "load index, copy from %s to %s" % (sourcevarname, destvarname))
                        else:
                            self.createcode("LDY", "#%s_%d" % (sourcevarname, source_offset), "load index, copy from %s to %s" % (sourcevarname, destvarname))
                        self.createcode("LDA", "(%s),Y" % (sourceframe0), "load from local var")
                        if not firstelement:
                            self.createcode("LDY", "#%s_%d" % (destvarname, dest_offset), "load index for destination")
                        else:
                            self.createcode("LDY", "#%s_%d" % (destvarname, dest_offset), "load index for destination")
                        self.createcode("STA", "(%s),Y" % (destframe0), "save to local var")
                        source_offset += 1
                        dest_offset += 1
                        firstelement = True
                        count -= 1
                        if count == 0:
                            break
            elif dest_size == 4 or destisregister:
                if ptr_a_source:
                    if self.checkhash(source_attr, "type_byte"):
                        self.createcode("LDY", "#%s" % sourcevarname, "CPYV: len(dst) = %d, src_type = %s" % (dest_size, "type_byte"))
                        self.createcode("LDA", "(%s),Y" % sourceframe0)
                        self.createcode("STA", "_scratchregister_0")
                        self.createcode("INY")
                        self.createcode("LDA", "(%s),Y" % sourceframe0)
                        self.createcode("STA", "_scratchregister_1")
                        self.createcode("LDY", "#0")
                        self.createcode("LDA", "(_scratchregister_0),Y")
                        self.createcode("LDY", "#%s" % destvarname)
                        self.createcode("STA", "(%s),Y" % destframe0)
                        self.createcode("INY")
                        self.createcode("LDA", "#0")
                        self.createcode("STA", "(%s),Y" % destframe0)
                        self.createcode("INY")
                        self.createcode("STA", "(%s),Y" % destframe0)
                        self.createcode("INY")
                        self.createcode("STA", "(%s),Y" % destframe0)
                    pass
                else:
                    self.createcode("NOP","","Copy S-Size:%d to D-Size:%d" % (sourcesize, destsize))
                    offset = 0
                    for x in range(source_size):
                        self.createcode("LDY", "#%s_%d" % (sourcevarname, offset), "load index, copy from %s to %s" % (sourcevarname, destvarname))
                        self.createcode("LDA", "(%s),Y" % (sourceframe0), "load from local var")
                        self.createcode("LDY", "#%s_%d" % (destvarname, offset), "load index for destination")
                        self.createcode("STA", "(%s),Y" % (destframe0), "save to local var")
                        self.createcode("INY")
                        offset += 1
            elif dest_size == 8 or destisregister:
                if ptr_a_source:
                    pass
                else:
                    offset = 0
                    for x in range(source_size):
                        self.createcode("NOP","","Copy S-Size:%d to D-Size:%d" % (sourcesize, destsize))
                        self.createcode("LDY", "#%s_%d" % (sourcevarname, offset), "load index, copy from %s to %s" % (sourcevarname, destvarname))
                        self.createcode("LDA", "(%s),Y" % (sourceframe0), "load from local var")
                        self.createcode("LDY", "#%s_%d" % (destvarname, offset), "load index for destination")
                        self.createcode("STA", "(%s),Y" % (destframe0), "save to local var")
                        self.createcode("INY")
                        offset += 1
        self.createcode("", "", "END-COPYVAR (%d) (sourcename:%s, destname=%s, srcsize:%d, dstsize:%d, srcregister:%s, destregister:%s)" % (lineno, sourcevarname, destvarname, source_size, dest_size, sourceisregister, destisregister))
    # Load Effective Address of varname into destregname

    def addvartovar__(self, dest, op1, op2):
        op1_name = op1.getname()
        op1_value = op1.getvalue()
        op1_adr = op1.getaddress()
        op1_attributes = op1.getattributes()
        self.log.writelog("codeemitter/addvartovar", "name is:%20s, adr=:$%4x" % (op1_name, op1_adr))
        op2_name = op2.getname()
        op2_value = op2.getvalue()
        op2_adr = op2.getaddress()
        op2_attributes = op2.getattributes()
        self.log.writelog("codeemitter/addvartovar", "name is:%20s, adr=:$%4x" % (op2_name, op2_adr))
        dest_name = dest.getname()
        dest_value = dest.getvalue()
        dest_adr = dest.getaddress()
        dest_attributes = dest.getattributes()
        self.log.writelog("codeemitter/addvartovar", "name is:%20s, adr=:$%4x" % (dest_name, dest_adr))
        self.createcode("","","ADDVARTOVAR (stoken=%s, t_type=%s, t_value=%s, attribs=%s)" % (name, t_type, t_value, attribstr))
        attribhash = {}
        for a in op1_attributes:
            attribhash[a] = True
        if self.checkhash(attribhash, "type_byte"):
            self.createcomment("codeemitter/addvartovar")
            self.createcode("CLC", "", "clear carry flag before add something")
            # load accu with constant value
            self.setname("")
            self.setopcode("LDA")
            self.setvalue(int(t_value))
            self.setcomment("assign var %s = %s with %s"%(op1_name,op1_value,op1_attributes))
            self.createassemberline()
            # add accu with variable / register
            self.setname("")
            self.setopcode("ADC")
            self.setvalue(name)
            self.setcomment("add accu to var: %s = %s with %s"%(dest_name,dest_value,dest_attributes))
            self.createassemberline()
            # store accu in variable / register
            self.setopcode("STA")
            self.setvalue(dest_name)
            self.setcomment("store byte value of: %s" % dest_name)
            self.createassemberline()
        elif self.checkhash(attribhash, "type_integer"):
            self.createcomment("codeemitter/addvartovar/type_long:" + "dest:%s, op1:%s, op2%s" % (dest_name,op1_name,op2_name))
            self.createcode("LDA", lobyte, "load word(%d,$%4X) lobyte (%X) in accu" % (x, x, lobyte))
            self.createcode("STA", name, "store lobyte from %s to address: $%4x" % (name, adr))
            self.createcode("LDA", hibyte, "load hibyte (%X) in accu" % hibyte)
            adr += 1
            self.createcode("STA", name + "_%4x" % adr, "store hibyte to $%4x" % adr)
        elif self.checkhash(attribhash, "type_long"):
            debug = "codeemitter/addvartovar/type_long"
            self.log.writelog(debug, "name is:%20s, adr=:$%08x" % (op1_name, op1_adr))
            self.createcomment("codeemitter/addvartovar/type_long:" + "dest:%s, op1:%s, op2:%s" % (dest_name,op1_name,op2_name))
            self.createcode("CLC", "", "clear carry flag before adding")
            indx = 6
            for idx in [0,2,4,6]:
                if idx == 0:
                    self.createcode("LDA", op1_name, "load byte from op1:%s" % op1_name)
                    self.createcode("ADC", op2_name, "add byte from op2:%s" % op2_name)
                    self.createcode("STA", dest_name, "store accu in destination:%s" % dest_name)
                else:
                    self.createcode("LDA", op1_name + "_%04x" % op1_adr, "load byte from op1:%s" % op1_name)
                    self.createcode("ADC", op2_name + "_%04x" % op2_adr, "add byte from op2:%s" % op2_name)
                    self.createcode("STA", dest_name + "_%04x" % dest_adr, "store accu in destination:%s" % dest_name)
                op1_adr += 1
                op2_adr += 1
                dest_adr += 1
                indx -= 2
        elif self.checkhash(attribhash, "type_longlong"):
            self.log.writelog("codeemitter/addconsttovar/type_longlong", "name is:%20s, adr=:$%04x" % (stoken.getname(), adr))
            x = int(t_value)
            hexvalue_hi = int(x / 0x100000000)
            hexvalue_lo = int((x & 0xFFFFFFFF) % 0xFFFFFFFF)
            hexvalue = "%08x" % hexvalue_hi + "%08x" % hexvalue_lo
            for idx in [0, 2, 4, 6, 8, 10, 12, 14 ]:
                self.createcode("LDA", '$' + hexvalue[idx:idx+2], "load word(%d,$%s)" % (x, hexvalue))
                if idx == 0:
                    self.createcode("STA", name, "store lobyte from %s to address: $%04x" % (name, adr))
                else:
                    self.createcode("STA", name + "_%04x" % adr, "store lobyte from %s to address: $%04x" % (name, adr))
                adr += 1
        return
        
    def assignvaluetovariable(self, stoken, t_type, t_value):
        attribstr = ""
        attribhash = dict()
        attributes = stoken.getattributes()
        cpuregister = False
        for a in attributes:
            attribstr += a + ','
            if a == "cpuregister":
                cpuregister = True
            attribhash[a] = True
        attribstr = attribstr[:-1]
        destnamespace = stoken.getnamespace()
        name = stoken.getname()
        if cpuregister:
            funcvarname = name
        else:
            funcvarname = destnamespace + '_' + name
        value = stoken.getvalue()
        adr = stoken.getaddress()
        self.log.writelog("codeemitter/assignvaluetovar", "name is:%20s, adr=:$%4x" % (stoken.getname(), adr))
        attribstr = ""
        attribhash = {}
        cpuregister = False
        for a in attributes:
            attribstr += a + ','
            if a == "cpuregister":
                cpuregister = True
            attribhash[a] = True
        attribstr = attribstr[:-1]
        dest_attr = stoken.getattributehash()
        if self.checkhash(dest_attr, "isargument"): # and namespace == destnamespace:
            destframe0 = "_framepointer"
            destframe1 = "_framepointer_1"
        else:
            destframe0 = "_userstack"
            destframe1 = "_userstack_1"
        self.log.writelog("codeemitter/assignvaluetovar", "Name:%s Hash:%s" % (name, attribhash))
        self.createcode("","","start assignvaluetovariable(stoken=%s, t_type=%s, t_value=%s, attribs=%s)" % (name, t_type, t_value, attribstr))
        if name == "_unireg5":
            xxxxxx = name
        if True:
            if self.checkhash(attribhash, "type_integer") or self.checkhash(attribhash, "type_pointer") or self.checkhash(attribhash, "type_varpointer"):
                x = "%04x" % int(t_value)
                hibyte = x[0:2]
                lobyte = x[2:4]
                if destnamespace == "global":
                    self.createcode("LDA", "#$" + lobyte, "load word(%s,$%s) lobyte (%s) in accu" % (t_value, x, lobyte))
                    self.createcode("STA", funcvarname, "store lobyte from %s to address: $%4x" % (name, adr))
                    self.createcode("LDA", "#$" + hibyte, "load hibyte (%s) in accu" % hibyte)
                    self.createcode("STA", funcvarname + "_1", "store hibyte to $%4x" % adr)
                else:
                    self.createcode("LDA", "#$" + lobyte, "load word(%s,$%s) lobyte (%s) in accu" % (t_value, x, lobyte))
                    self.createcode("LDY", "#%s" % funcvarname, "load index for name:%s" % destnamespace)
                    self.createcode("STA", "(%s),Y" % destframe0 , "store relative to framepointer")
                    self.createcode("LDA", "#$" + hibyte, "load hibyte (%s) in accu" % hibyte)
                    self.createcode("INY", "", "add pointer to hi-byte")
                    self.createcode("STA", "(%s),Y" % destframe0, "store hibyte")
            elif self.checkhash(attribhash, "cpuregister"):
                self.log.writelog("codeemitter/assignvaluetovar/cpuregister", "name is:%20s, adr=:$%04x" % (stoken.getname(), adr))
                x = "%016x" % int(t_value)
                byte_0 = x[0:2]
                byte_1 = x[2:4]
                byte_2 = x[4:6]
                byte_3 = x[6:8]
                byte_4 = x[8:10]
                byte_5 = x[10:12]
                byte_6 = x[12:14]
                byte_7 = x[14:16]
                if destnamespace == "global":
                    index = 0
                    indx = 14
                    oldhexbyte = "--"
                    for idx in [0,2,4,6,8,10,12,14]:
                        hexbyte = x[indx:indx+2]
                        if hexbyte != oldhexbyte:
                            self.createcode("LDA", "#$%s" % hexbyte, "Load %s from Value:%s, Index:%d" % (hexbyte, x, idx))
                        realregister = registerconvert["%s_%d" % (funcvarname, index)]
                        self.createcode("STA", "%s" % realregister, "store byte to global var")
                        indx -= 2
                        index += 1
                        oldhexbyte = hexbyte
                else:
                    print("cpuregister not global, something went wrong")
                    sys.exit(1)
            elif self.checkhash(attribhash, "type_byte") or self.checkhash(attribhash, "type_char"):
                if destnamespace == "global":
                    self.setname("")
                    self.setopcode("LDA")
                    self.setvalue("#" + str(int(t_value)))
                    self.setcomment("assign var %s = %s with %s"%(name,value,attribstr))
                    self.createassemberline()
                    self.setopcode("STA")
                    self.setvalue(funcvarname)
                    self.setcomment("store byte value of: %s" % name)
                    self.createassemberline()
                else:
                    self.createcode("LDY", "#%s" % funcvarname, "load index")
                    self.createcode("LDA", "#%d" % int(t_value), "load constant to accu")
                    self.createcode("STA", "(%s),Y" % destframe0, "store data in local var")
            elif self.checkhash(attribhash, "type_long"):
                self.log.writelog("codeemitter/assignvaluetovar/type_long", "name is:%20s, adr=:$%08x" % (stoken.getname(), adr))
                x = "%08x" % int(t_value)
                if destnamespace == "global":
                    index = 0
                    indx = 6
                    oldhexbyte = "--"
                    for idx in [0,2,4,6]:
                        hexbyte = x[indx:indx+2]
                        if hexbyte != oldhexbyte:
                            self.createcode("LDA", "#$%s" % hexbyte, "Load %s from Value:%s" % (hexbyte, x))
                        self.createcode("STA", "%s_%d" % (funcvarname, index), "store byte to global var")
                        indx -= 2
                        index += 1
                        oldhexbyte = hexbyte
                else:
                    self.createcode("LDY","#%s" % funcvarname,"Value:%s" % value)
                    indx = 6
                    oldhexbyte = "--"
                    for idx in [0,2,4,6]:
                        hexbyte = x[indx:indx+2]
                        if hexbyte != oldhexbyte:
                            self.createcode("LDA", "#$%s" % hexbyte, "Load %s from Value:%s" % (hexbyte, x))
                        self.createcode("STA", "(%s),Y" % destframe0, "store byte to stack")
                        indx -= 2
                        self.createcode("INY","","adjust to next byte")
                        oldhexbyte = hexbyte
            elif self.checkhash(attribhash, "type_longlong"):
                self.log.writelog("codeemitter/assignvaluetovar/type_longlong", "name is:%20s, adr=:$%08x" % (stoken.getname(), adr))
                x = "%016x" % int(t_value)
                byte_0 = x[0:2]
                byte_1 = x[2:4]
                byte_2 = x[4:6]
                byte_3 = x[6:8]
                byte_4 = x[8:10]
                byte_5 = x[10:12]
                byte_6 = x[12:14]
                byte_7 = x[14:16]
                if destnamespace == "global":
                    index = 0
                    indx = 14
                    oldhexbyte = "--"
                    for idx in [0,2,4,6,8,10,12,14]:
                        hexbyte = x[indx:indx+2]
                        if hexbyte != oldhexbyte:
                            self.createcode("LDA", "#$%s" % hexbyte, "Load %s from Value:%s" % (hexbyte, x))
                        self.createcode("STA", "%s_%d" % (funcvarname, index), "store byte to global var")
                        indx -= 2
                        index += 1
                        oldhexbyte = hexbyte
                else:
                    self.createcode("LDY","#%s" % funcvarname,"Value:%s" % value)
                    indx = 14
                    oldhexbyte = "--"
                    for idx in [0,2,4,6,8,10,12,14]:
                        hexbyte = x[indx:indx+2]
                        if hexbyte != oldhexbyte:
                            self.createcode("LDA", "#$%s" % hexbyte, "Load %s from Value:%s" % (hexbyte, x))
                        self.createcode("STA", "(%s),Y" % destframe0, "store byte to stack")
                        if idx < 14:
                            self.createcode("INY","","adjust to next byte")
                        indx -= 2
                        oldhexbyte = hexbyte
        else:
            pass    
        return

    def createfunctioncall(self, functionobj, arglist, line=0):
        debug = False
        functionname = functionobj.getname()
        functiondata = functionobj.getfuncdata()
        destinationargs = functiondata.getvar()
        destindex = 0
        # print("funccall:%s argc:%d, argv:%s" % (functionname, len(arglist), argv))
        if len(arglist) > 0:
            # set framepointer to beginning of local vars of called function, if function has parameter
            stackframelength = "#%s_sflast" % functionname
            self.createcode("SEC", "", "CREATEFUNCTIONCALL for: %s" % functionname)
            self.createcode("LDA", "_userstack_0", "SET FRAMEPOINTER to end of called function")
            self.createcode("SBC", stackframelength, "for having access to parameters")
            self.createcode("STA", "_framepointer_0", "store in framepointer lo byte")
            self.createcode("LDA", "_userstack_1", "load userstack hi-byte")
            self.createcode("SBC", "#0", "subtract with carry")
            self.createcode("STA", "_framepointer_1", "save to framepointer hi byte")
        for arg in arglist:
            if arg == None:
                print("arguments in function call is empty, function to be called is:%s" % functionname)
            elif isinstance(arg, list):
                if arg[0] == "number":
                    destobject = destinationargs[destindex]
                    destinationname = destobject.getvarname()
                    destinationnamespace = destobject.getnamespace()
                    deststok = self.stokens.getwithnamespace(destinationname, destinationnamespace)
                    destsize = deststok.getsize()
                    destvarname = deststok.getnamewithnamespace()
                    self.assignvaluetovariable(deststok, "number", arg[1])
            else:
                sourcestok = arg
                sourcevarname = arg.getnamewithnamespace()
                sourcesize = sourcestok.getsize()
                dest = destinationargs[destindex]
                deststok = self.stokens.getwithnamespace(dest.getvarname(), dest.getnamespace())
                destsize = deststok.getsize()
                destvarname = deststok.getnamewithnamespace()
                self.insertinline("NOP", "", line, comment="source:" + sourcevarname + "    dest:"+deststok.getnamewithnamespace()+" (%d)")
                # copy the sourcetoken from the caller to the destination to the called function, calculate the future framepointer
                self.copyvar(deststok, sourcestok)
            destindex = destindex + 1
        # call function
        if debug:
                self.createdebugout("in %s do call of function:%s" % (self.blocks.getactivefunctionname(), functionname))
        self.insertinline("JSR", functionname, line, comment="call function (%d)")
        # set framepoint back to userstack. Only if framepointer was set before
        if len(arglist) > 0:
            self.createcode("LDA", "_userstack_0", "Load User-Stack lo byte")
            self.createcode("STA", "_framepointer_0", "Save Userstack lo in framepointer")
            self.createcode("LDA", "_userstack_1", "Load User-Stack lo byte")
            self.createcode("STA", "_framepointer_1", "Save Userstack lo in framepointer")

    def internalfunctioncall(self, functionobj, arglist, line=0):
        debug = False
        functionname = functionobj.getname()
        functiondata = functionobj.getfuncdata()
        functionsubroutine = functiondata.getsubroutine()
        destinationargs = functiondata.getvar()
        destindex = 0
        if len(arglist) > 0:
            # set framepointer to beginning of local vars of called function
            namespace = self.blocks.getactivefunctionname()
            stackframelength = "#%s_sflast" % namespace
            self.createcode("SEC", "", "CREATEFUNCTIONCALL for: %s" % functionname)
            self.createcode("LDA", "_userstack_0", "load userstack lo-byte")
            self.createcode("SBC", stackframelength, "subtract stackframelength")
            self.createcode("STA", "_framepointer_0", "store in framepointer lo byte")
            self.createcode("LDA", "_userstack_1", "load userstack hi-byte")
            self.createcode("SBC", "#0", "subtract with carry")
            self.createcode("STA", "_framepointer_1", "save to framepointer hi byte")
        for arg in arglist:
            if arg == None:
                print("arguments in function call is empty, function to be called is:%s" % functionname)
            elif isinstance(arg, list):
                if arg[0] == "number":
                    dest = destinationargs[destindex]
                    deststok = self.stokens.getwithnamespace(dest.getvarname(), dest.getnamespace())
                    destsize = deststok.getsize()
                    destvarname = deststok.getnamewithnamespace()
                    self.assignvaluetovariable(deststok, "number", arg[1])
            else:
                sourcestok = arg
                sourcevarname = arg.getnamewithnamespace()
                sourcesize = sourcestok.getsize()
                dest = destinationargs[destindex]
                deststok = self.stokens.getwithnamespace(dest.getvarname(), dest.getnamespace())
                destsize = deststok.getsize()
                destvarname = deststok.getnamewithnamespace()
                self.insertinline("NOP", "", line, comment="source:" + sourcevarname + "    dest:"+deststok.getnamewithnamespace()+" (%d)")
                # copy the sourcetoken from the caller to the destination to the called function, calculate the future framepointer
                self.copyvar(deststok, sourcestok)
            destindex += 1
        # call function
        if debug:
            self.createdebugout("in %s do call of function:%s" % (self.blocks.getactivefunctionname(), functionname))
        self.createcode("JSR", functionsubroutine, "internalfunction:%s, call subroutine:%s" % (functionname, functionsubroutine))

    def intfunc_logical(self, functionobj, arglist, line=0):
        functionname = functionobj.getname()
        functiondata = functionobj.getfuncdata()
        functionsubroutine = functiondata.getsubroutine()
        destinationargs = functiondata.getvar()
        if len(arglist) != 2:
            print("internal function %s() must be called with two arguments" % functionname)
            sys.exit(1)
        sourcestok = arglist[0]
        value = arglist[1]
        if isinstance(value, list):
            if value[0] == "number":
                operand = value[1]
            else:
                print("internal function %s(var, const) must be call with number constant on the second argument" % functionname)
        else:
            print("internal function %s() must be called with %s(var, const)" % (functionname, functionname))
            sys.exit(1)
        sourcesize = sourcestok.getsize()
        sourcenamespace = sourcestok.getnamespace()
        source_attr = sourcestok.getattributehash()
        sourcename = sourcestok.getname()
        sourcenamewithnamespace = sourcestok.getnamewithnamespace()
        sourcevalue = sourcestok.getvalue()
        sourcetype = sourcestok.gettype()
        if self.checkhash(source_attr, "isargument"):
            frame0 = "_framepointer_0"
            frame1 = "_framepointer_1"
        else:
            frame0 = "_userstack_0"
            frame1 = "_userstack_1"
        if self.checkhash(source_attr, "type_byte"):
            hexoperand = "%08x" % int(operand)
            byteoperand = "%s" % hexoperand[6:8]
            self.createcode("LDY", "#%s" % sourcenamewithnamespace, "operation:%s with operand:%s" % (functionname, hexoperand))
            self.createcode("LDA", "(%s),Y" % frame0)
            if functionname == "and":
                self.createcode("AND", "#$%s" % byteoperand, "do logical AND on bytevalue")
            elif functionname == "or":
                self.createcode("ORA", "#$%s" % byteoperand, "do logical OR on bytevalue")
            elif functionname == "shiftright":
                for c in range(int(operand)):
                    self.createcode("LSR", "", "do logical shift right on bytevalue")
            elif functionname == "shiftleft":
                for c in range(int(operand)):
                    self.createcode("ASL", "", "do arithmetic shift left on bytevalue")
            elif functionname == "rotateright":
                for c in range(int(operand)):
                    self.createcode("LSR", "", "do logical rotate right on bytevalue")
            elif functionname == "rotateleft":
                for c in range(int(operand)):
                    self.createcode("ASL", "", "do arithmetic rotate left on bytevalue")
            self.createcode("STA", "(%s),Y" % frame0)
        elif self.checkhash(source_attr, "type_integer"):
            if functionname == "and" or functionname == "or":
                hexoperand = "%04x" % int(operand)
                self.createcode("LDY", "#%s" % sourcenamewithnamespace, "operation:%s with operand:%s" % (functionname, hexoperand))
                self.createcode("LDA", "(%s),Y" % frame0, "copy variable %s to scrath register" % sourcenamewithnamespace)
                self.createcode("STA", "_scratchregister_0")
                self.createcode("INY")
                self.createcode("LDA", "(%s),Y" % frame0)
                self.createcode("STA", "_scratchregister_1")
                byteoperand = "%s" % hexoperand[0:2]
                if functionname == "and":
                    self.createcode("AND", "#$%s" % byteoperand)
                if functionname == "or":
                    self.createcode("ORA", "#$%s" % byteoperand)
                self.createcode("STA", "_scratchregister_1")
                self.createcode("DEY")
                self.createcode("LDA", "_scratchregister_0")
                byteoperand = "%s" % hexoperand[2:4]
                if functionname == "and":
                    self.createcode("AND", "#$%s" % byteoperand)
                if functionname == "or":
                    self.createcode("ORA", "#$%s" % byteoperand)
                self.createcode("STA", "_scratchregister_0")
                self.createcode("STA", "(%s),Y" % frame0, "copy back to var:%s" % sourcenamewithnamespace)
                self.createcode("LDA", "_scratchregister_1")
                self.createcode("INY")
                self.createcode("STA", "(%s),Y" % frame0, "copy back to var:%s" % sourcenamewithnamespace)
            else:
                self.createcode("LDY", "#%s" % sourcenamewithnamespace, "operation:%s with operand:%d" % (functionname, int(operand)))
                self.createcode("LDA", "(%s),Y" % frame0, "copy variable %s to scrath register" % sourcenamewithnamespace)
                self.createcode("STA", "_scratchregister_0")
                self.createcode("INY")
                self.createcode("LDA", "(%s),Y" % frame0)
                self.createcode("STA", "_scratchregister_1")
                if functionname == "shiftright":
                    for x in range(int(operand)):
                        self.createcode("LSR", "_scratchregister_1", "shift right, fill carry with bit 0")
                        self.createcode("ROR", "_scratchregister_0", "rotate right, get bit 7 from carry flag")
                if functionname == "shiftleft":
                    for x in range(int(operand)):
                        self.createcode("ASL", "_scratchregister_0", "shift left fill carry with bit 0")
                        self.createcode("ROL", "_scratchregister_1", "rotate left, get bit 7 from carry flag")
                if functionname == "rotateright":
                    for x in range(int(operand)):
                        self.createcode("LDA", "_scratchregister_0")
                        self.createcode("LSR", "A", "bit 0 ist now in the carry flag")
                        self.createcode("ROR", "_scratchregister_1")
                        self.createcode("ROR", "_scratchregister_0", "get bit 7 from carry flag, round:%d" % x)
                if functionname == "rotateleft":
                    for x in range(int(operand)):
                        self.createcode("LDA", "_scratchregister_1", "load value for check bit 7")
                        self.createcode("ASL", "", "bit 7 ist now in the carry flag")
                        self.createcode("ROL", "_scratchregister_0", "shift right, fill carry with bit 0")
                        self.createcode("ROL", "_scratchregister_1", "rotate right, get bit 7 from carry flag")
                self.createcode("LDY", "#%s" % sourcenamewithnamespace)
                self.createcode("LDA", "_scratchregister_0")
                self.createcode("STA", "(%s),Y" % frame0)
                self.createcode("INY")
                self.createcode("LDA", "_scratchregister_1")
                self.createcode("STA", "(%s),Y" % frame0)
        elif self.checkhash(source_attr, "type_long"):
            if functionname == "and" or functionname == "or":
                hexoperand = "%08x" % int(operand)
                self.createcode("LDY", "#%s" % sourcenamewithnamespace, "operation:%s with operand:%s" % (functionname, hexoperand))
                for x in [6,4,2,0]:
                    self.createcode("LDA", "(%s),Y" % frame0, "copy variable %s to scrath register" % sourcenamewithnamespace)
                    if functionname == "and":
                        self.createcode("AND", "#$%s" % hexoperand[x:x+2], "and with %s" % hexoperand[x:x+2])
                    if functionname == "or":
                        self.createcode("OR", "#$%s" % hexoperand[x:x+2], "or with %s" % hexoperand[x:x+2])
                    self.createcode("STA", "(%s),Y" % frame0)
                    if x > 0:
                        self.createcode("INY")
            else:
                self.createcode("LDY", "#%s" % sourcenamewithnamespace, "operation:%s with operand:%d" % (functionname, int(operand)))
                for x in range(4):
                    self.createcode("LDA", "(%s),Y" % frame0, "copy variable %s to scrath register" % sourcenamewithnamespace)
                    self.createcode("STA", "_scratchregister_%d" % x,"store in scratch at pos %d" % x)
                    if x < 4:
                        self.createcode("INY")
                if functionname == "shiftright":
                    for x in range(int(operand)):
                        self.createcode("LSR", "_scratchregister_3", "shift right, fill carry with bit 0")
                        self.createcode("ROR", "_scratchregister_2", "rotate right, get bit 7 from carry flag")
                        self.createcode("ROR", "_scratchregister_1", "rotate right, get bit 7 from carry flag")
                        self.createcode("ROR", "_scratchregister_0", "rotate right, get bit 7 from carry flag")
                if functionname == "shiftleft":
                    for x in range(int(operand)):
                        self.createcode("ASL", "_scratchregister_0", "shift left fill carry with bit 0")
                        self.createcode("ROL", "_scratchregister_1", "rotate left, get bit 7 from carry flag")
                        self.createcode("ROL", "_scratchregister_2", "rotate left, get bit 7 from carry flag")
                        self.createcode("ROL", "_scratchregister_3", "rotate left, get bit 7 from carry flag")
                if functionname == "rotateright":
                    for x in range(int(operand)):
                        self.createcode("LDA", "_scratchregister_0")
                        self.createcode("LSR", "A", "bit 0 ist now in the carry flag")
                        self.createcode("ROR", "_scratchregister_3")
                        self.createcode("ROR", "_scratchregister_2")
                        self.createcode("ROR", "_scratchregister_1")
                        self.createcode("ROR", "_scratchregister_0", "get bit 7 from carry flag, round:%d" % x)
                if functionname == "rotateleft":
                    for x in range(int(operand)):
                        self.createcode("LDA", "_scratchregister_3", "load value for check bit 7")
                        self.createcode("ASL", "", "bit 7 ist now in the carry flag")
                        self.createcode("ROL", "_scratchregister_0", "shift right, fill carry with bit 0")
                        self.createcode("ROL", "_scratchregister_1", "rotate right, get bit 7 from carry flag")
                        self.createcode("ROL", "_scratchregister_2", "rotate right, get bit 7 from carry flag")
                        self.createcode("ROL", "_scratchregister_3", "rotate right, get bit 7 from carry flag")
                self.createcode("LDY", "#%s" % sourcenamewithnamespace)
                for x in range(4):
                    self.createcode("LDA", "_scratchregister_%d" % x,"load from scratch at pos %d" % x)
                    self.createcode("STA", "(%s),Y" % frame0, "copy scratch %s to var" % sourcenamewithnamespace)
                    if x < 4:
                        self.createcode("INY")
        elif self.checkhash(source_attr, "type_longlong"):
            if functionname == "and" or functionname == "or":
                hexoperand = "%016x" % int(operand)
                self.createcode("LDY", "#%s" % sourcenamewithnamespace, "operation:%s with operand:%s" % (functionname, hexoperand))
                for x in [14,12,10,8,6,4,2,0]:
                    self.createcode("LDA", "(%s),Y" % frame0, "copy variable %s to scrath register" % sourcenamewithnamespace)
                    if functionname == "and":
                        self.createcode("AND", "#$%s" % hexoperand[x:x+2], "and with %s" % hexoperand[x:x+2])
                    if functionname == "or":
                        self.createcode("OR", "#$%s" % hexoperand[x:x+2], "or with %s" % hexoperand[x:x+2])
                    self.createcode("STA", "(%s),Y" % frame0)
                    if x > 0:
                        self.createcode("INY")
            else:
                self.createcode("LDY", "#%s" % sourcenamewithnamespace, "operation:%s with operand:%d" % (functionname, int(operand)))
                for x in range(8):
                    self.createcode("LDA", "(%s),Y" % frame0, "copy variable %s to scrath register" % sourcenamewithnamespace)
                    self.createcode("STA", "_scratchregister_%d" % x,"store in scratch at pos %d" % x)
                    if x < 8:
                        self.createcode("INY")
                if functionname == "shiftright":
                    for x in range(int(operand)):
                        self.createcode("LSR", "_scratchregister_7", "shift right, fill carry with bit 0")
                        self.createcode("ROR", "_scratchregister_6", "rotate right, get bit 7 from carry flag")
                        self.createcode("ROR", "_scratchregister_5", "rotate right, get bit 7 from carry flag")
                        self.createcode("ROR", "_scratchregister_4", "rotate right, get bit 7 from carry flag")
                        self.createcode("ROR", "_scratchregister_3", "rotate right, get bit 7 from carry flag")
                        self.createcode("ROR", "_scratchregister_2", "rotate right, get bit 7 from carry flag")
                        self.createcode("ROR", "_scratchregister_1", "rotate right, get bit 7 from carry flag")
                        self.createcode("ROR", "_scratchregister_0", "rotate right, get bit 7 from carry flag")
                if functionname == "shiftleft":
                    for x in range(int(operand)):
                        self.createcode("ASL", "_scratchregister_0", "shift left fill carry with bit 0")
                        self.createcode("ROL", "_scratchregister_1", "rotate left, get bit 7 from carry flag")
                        self.createcode("ROL", "_scratchregister_2", "rotate left, get bit 7 from carry flag")
                        self.createcode("ROL", "_scratchregister_3", "rotate left, get bit 7 from carry flag")
                        self.createcode("ROL", "_scratchregister_4", "rotate left, get bit 7 from carry flag")
                        self.createcode("ROL", "_scratchregister_5", "rotate left, get bit 7 from carry flag")
                        self.createcode("ROL", "_scratchregister_6", "rotate left, get bit 7 from carry flag")
                        self.createcode("ROL", "_scratchregister_7", "rotate left, get bit 7 from carry flag")
                if functionname == "rotateright":
                    for x in range(int(operand)):
                        self.createcode("LDA", "_scratchregister_0")
                        self.createcode("LSR", "A", "bit 0 ist now in the carry flag")
                        self.createcode("ROR", "_scratchregister_7")
                        self.createcode("ROR", "_scratchregister_6")
                        self.createcode("ROR", "_scratchregister_5")
                        self.createcode("ROR", "_scratchregister_4")
                        self.createcode("ROR", "_scratchregister_3")
                        self.createcode("ROR", "_scratchregister_2")
                        self.createcode("ROR", "_scratchregister_1")
                        self.createcode("ROR", "_scratchregister_0", "get bit 7 from carry flag, round:%d" % x)
                if functionname == "rotateleft":
                    for x in range(int(operand)):
                        self.createcode("LDA", "_scratchregister_7", "load value for check bit 7")
                        self.createcode("ASL", "", "bit 7 ist now in the carry flag")
                        self.createcode("ROL", "_scratchregister_0", "rotate left, fill carry with bit 0")
                        self.createcode("ROL", "_scratchregister_1", "rotate left, get bit 7 from carry flag")
                        self.createcode("ROL", "_scratchregister_2", "rotate left, get bit 7 from carry flag")
                        self.createcode("ROL", "_scratchregister_3", "rotate left, get bit 7 from carry flag")
                        self.createcode("ROL", "_scratchregister_4", "rotate left, fill carry with bit 0")
                        self.createcode("ROL", "_scratchregister_5", "rotate left, get bit 7 from carry flag")
                        self.createcode("ROL", "_scratchregister_6", "rotate left, get bit 7 from carry flag")
                        self.createcode("ROL", "_scratchregister_7", "rotate left, get bit 7 from carry flag")
                self.createcode("LDY", "#%s" % sourcenamewithnamespace)
                for x in range(8):
                    self.createcode("LDA", "_scratchregister_%d" % x,"load from scratch at pos %d" % x)
                    self.createcode("STA", "(%s),Y" % frame0, "copy scratch %s to var" % sourcenamewithnamespace)
                    if x < 8:
                        self.createcode("INY")
        else:
            print("not implementet for data type: %s" % source_attr)
            sys.exit(1)
            
    def intfunc_print(self, functionobj, arglist, line=0):
        functionname = functionobj.getname()
        functiondata = functionobj.getfuncdata()
        functionsubroutine = functiondata.getsubroutine()
        destinationargs = functiondata.getvar()
        for sourcestok in arglist:
            if isinstance(sourcestok, list):
                if sourcestok[0] == "number":
                    print("internal function write() must be called with var, not with number")
                    print("arglist is:", arglist)
                    sys.exit(1)
            sourcesize = int(sourcestok.getsize())
            sourcenamespace = sourcestok.getnamespace()
            source_attr = sourcestok.getattributehash()
            sourcename = sourcestok.getname()
            sourcenamewithnamespace = sourcestok.getnamewithnamespace()
            sourcevalue = sourcestok.getvalue()
            sourcetype = sourcestok.gettype()
            if self.checkhash(source_attr, "isargument"):
                frame0 = "_framepointer_0"
                frame1 = "_framepointer_1"
            else:
                frame0 = "_userstack_0"
                frame1 = "_userstack_1"
            if self.checkhash(source_attr, "cpuregister"):
                cpuregister = True
            else:
                cpuregister = False
            if sourcetype == "type_stringconst":
                loop = self.randomword(8)
                endloop = self.randomword(8)
                stringlabel = self.randomword(8)
                dochar = self.randomword(8)
                self.createcode("LDY", "#0", "internal write called with stringconstant")
                self.createcode("LDA", "%s,Y" % stringlabel, name=loop)
                self.createcode("BEQ", endloop)
                self.createcode("CMP", "#$5C", "check for backsladh")
                self.createcode("BNE", dochar)
                self.createcode("INY")
                self.createcode("LDA", "%s,Y" % stringlabel)
                self.createcode("BEQ", endloop)
                self.createcode("CMP", "#'n'")
                self.createcode("BNE", dochar)
                self.createcode("JSR", "_OUTPUTCRLF")
                self.createcode("INY")
                self.createcode("JMP", loop)
                self.createcode("JSR", "_OUTPUTCHAR", name=dochar)
                self.createcode("INY")
                self.createcode("JMP", loop)
                self.addstring(stringlabel, "\"%s\"" % sourcevalue)
                self.createcode("", "", "end of writeloop", name=endloop)
            elif self.checkhash(source_attr, "type_chararray"):
                sourceaddress = sourcestok.getaddress()
                endofstring = self.randomword(8)
                outloop = self.randomword(8)
                if sourcenamespace == "global":
                    self.createcode("LDX", "#0", "write: with var %s from type chararray called" % sourcenamewithnamespace)
                    self.createcode("LDA", "%s,X" % sourcenamewithnamespace, "Load from Address %04x" % sourceaddress, name=outloop)
                    self.createcode("BEQ", endofstring)
                    self.createcode("JSR", "_OUTPUTCHAR")
                    self.createcode("INX")
                    self.createcode("JMP", outloop)
                    self.createcode("","","End of output Stringvar", name=endofstring)
                else:
                    self.createcode("LDY", "#%s" % (sourcenamewithnamespace), "write: called with chararray %s" % sourcenamewithnamespace)
                    self.createcode("LDX", "#0")
                    self.createcode("LDA", "(%s),Y" % frame0, "Load Accu until char is #$00", name=outloop)
                    self.createcode("BEQ", endofstring)
                    self.createcode("JSR", "_OUTPUTCHAR")
                    self.createcode("INX")
                    self.createcode("INY")
                    self.createcode("JMP", outloop)
                    self.createcode("","","End of ouput Stringvar", name=endofstring)
            # long and longlong
            elif self.checkhash(source_attr, "type_long") or self.checkhash(source_attr, "type_longlong"):
                outloop_long = self.randomword(8)
                if cpuregister:
                    if functionname == "printhex" or functionname == "printlnhex":
                        for idx in [7,6,5,4,3,2,1,0]:
                            realregname = registerconvert[sourcename + '_' + str(idx)]
                            self.createcode("LDA", realregname)
                            self.createcode("JSR", "_OUTHEX")
                    else:
                        self.createcode("LDX", "#7")
                        self.createcode("LDA", "%s,X" % sourcename, name=outloop_long)
                        self.createcode("STA", "%s,X" % "_unireg0,X")
                        self.createcode("DEX")
                        self.createcode("BPL", outloop_long)
                        # self.createcode("LDA", "#0")
                        # self.createcode("STA", "global_memarea", "clear memory, if there is something from the prev. output")
                        self.createcode("JSR", "_UNIREG0_DECIMAL")
                        self.createcode("JSR", "_prt_global_memarea")

                else:
                    if functionname == "printhex" or functionname == "printlnhex":
                        self.createcode("LDY", "#%s+%d" % (sourcenamewithnamespace, sourcesize-1), "internal write called with long var")
                        self.createcode("LDX", "#%d" % (sourcesize - 1))
                        self.createcode("LDA", "(%s),Y" % frame0, "Load Accu", name=outloop_long)
                        self.createcode("JSR", "_OUTHEX")
                        self.createcode("DEY")
                        self.createcode("DEX")
                        self.createcode("BPL", outloop_long)
                    else:
                        self.createcode("LDY", "#%s+%d" % (sourcenamewithnamespace, sourcesize-1), "internal write called with long var")
                        self.createcode("LDX", "#%d" % (sourcesize - 1))
                        self.createcode("LDA", "(%s),Y" % frame0, "Load Accu", name=outloop_long)
                        self.createcode("STA", "%s,X" % "_unireg0", "Store Accu in _unireg0")
                        self.createcode("DEY")
                        self.createcode("DEX")
                        self.createcode("BPL", outloop_long)
                        self.createcode("JSR", "_UNIREG0_DECIMAL")
                        self.createcode("JSR", "_prt_global_memarea")
            # integer
            elif self.checkhash(source_attr, "type_integer") or self.checkhash(source_attr, "type_varpointer") or self.checkhash(source_attr, "type_pointer"):
                if cpuregister:
                    self.createcode("LDA", sourcename + '_1')
                    self.createcode("JSR", "_OUTHEX")
                    self.createcode("LDA", sourcename + '_0')
                    self.createcode("JSR", "_OUTHEX")
                else:
                    self.createcode("LDY", "#%s_1" % sourcenamewithnamespace, "internal write called with int or pointer")
                    self.createcode("LDA", "(%s),Y" % frame0)
                    self.createcode("JSR", "_OUTHEX", "call write a hex byte")
                    self.createcode("DEY")
                    self.createcode("LDA", "(%s),Y" % frame0)
                    self.createcode("JSR", "_OUTHEX", "call write a hex byte")
            elif self.checkhash(source_attr, "type_integer_bcd"):
                self.createcode("LDY", "#%s" % sourcenamewithnamespace, "internal write called with int or pointer")
                self.createcode("LDA", "(%s),Y" % frame0)
                self.createcode("STA", "_scratchregister_0")
                self.createcode("INY")
                self.createcode("LDA", "(%s),Y" % frame0)
                self.createcode("STA", "_scratchregister_1")
                self.createcode("JSR", "_BIN2BCD")
                self.createcode("LDA", "global_memarea+2")
                self.createcode("JSR", "_OUTBCD", "call write a hex byte")
                self.createcode("LDA", "global_memarea+1")
                self.createcode("JSR", "_OUTBCD", "call write a hex byte")
                self.createcode("LDA", "global_memarea+0")
                self.createcode("JSR", "_OUTBCD", "call write a hex byte")
            # byte
            elif self.checkhash(source_attr, "type_byte"):
                self.createcode("LDY", "#%s" % sourcenamewithnamespace, "internal write called with byte var")
                self.createcode("LDA", "(%s),Y" % frame0)
                self.createcode("JSR", "_OUTHEX", "call write a hex byte")
            elif self.checkhash(source_attr, "type_char"):
                self.createcode("LDY", "#%s" % sourcenamewithnamespace, "internal write called with byte var")
                self.createcode("LDA", "(%s),Y" % frame0)
                self.createcode("JSR", "_OUTPUTCHAR")
            elif self.checkhash(source_attr, "type_wozfloat"):
                self.createcode("LDY", "#%s" % sourcenamewithnamespace, "internal print with wozfloat argument")
                self.createcode("LDA", "(%s),Y" % frame0)
                self.createcode("STA", "X1")
                self.createcode("INY")
                self.createcode("LDA", "(%s),Y" % frame0)
                self.createcode("STA", "M1")
                self.createcode("INY")
                self.createcode("LDA", "(%s),Y" % frame0)
                self.createcode("STA", "M1_1")
                self.createcode("INY")
                self.createcode("LDA", "(%s),Y" % frame0)
                self.createcode("STA", "M1_2")
                self.createcode("JSR", "wozFIX")
                self.createcode("LDA", "M1")
                self.createcode("JSR", "_OUTHEX", "call write a hex byte")
                self.createcode("LDA", "M1_1")
                self.createcode("JSR", "_OUTHEX", "call write a hex byte")
            else:
                if self.checkhash(source_attr, "isargument"):
                    frame0 = "_framepointer_0"
                    frame1 = "_framepointer_1"
                else:
                    frame0 = "_userstack_0"
                    frame1 = "_userstack_1"
                dest = destinationargs[0]
                deststok = self.stokens.getwithnamespace(dest.getvarname(), dest.getnamespace())
                destsize = deststok.getsize()
                dest_attr = deststok.getattributehash()
        if functionname == "println" or functionname == "printlnhex":
            self.createcode("JSR", "_OUTPUTCRLF", "write a crlf if functionname is println")
    # strcpy, strcat
    def intfunc_strcpy(self, functionobj, arglist, line=0): # is also strcat
        functionname = functionobj.getname()
        functiondata = functionobj.getfuncdata()
        functionsubroutine = functiondata.getsubroutine()
        destinationargs = functiondata.getvar()
        argindex = 0
        stringpointer = self.stokens.get("_unireg0")
        stringpointername = stringpointer.getname()
        destinationpointer = self.stokens.get("_unireg1")
        destinationpointername = destinationpointer.getname()
        for sourcestok in arglist:
            appendlabel = self.randomword(8)
            stringlabel = self.randomword(8)
            nextcopy = self.randomword(8)
            stringcopied = self.randomword(8)
            if isinstance(sourcestok, list):
                if arg[0] == "number":
                    print("internal function write() must be called with var, not with number")
                    sys.exit(1)
            sourcesize = int(sourcestok.getsize())
            sourcenamespace = sourcestok.getnamespace()
            source_attr = sourcestok.getattributehash()
            sourcename = sourcestok.getname()
            sourcenamewithnamespace = sourcestok.getnamewithnamespace()
            sourcevalue = sourcestok.getvalue()
            sourcetype = sourcestok.gettype()
            if sourcename == "_memarray":
                x = 0
            if self.checkhash(source_attr, "isargument"):
                frame0 = "_framepointer_0"
                frame1 = "_framepointer_1"
            else:
                frame0 = "_userstack_0"
                frame1 = "_userstack_1"
            if argindex == 0:
                # the first argument ist the destination of the copy operation, but here it is just another source
                # this is a little confusing
                if self.checkhash(source_attr, "type_chararray"):
                    targettoken = sourcestok
                    if sourcenamespace == "global":
                        # if source is a global var, set stringpointer (_unireg0, see oabove) to address of var
                        targettokenaddress = targettoken.getaddress()
                        # if global, we know the address
                        hexaddress = "%04x" % targettokenaddress
                        idx = 0
                        self.createcode("LDA", "#$%s" % hexaddress[2:4], "strcpy: destination is global, address direct")
                        self.createcode("STA", "%s_%d" % (stringpointername, idx))
                        idx += 1
                        self.createcode("LDA", "#$%s" % hexaddress[0:2])
                        self.createcode("STA", "%s_%d" % (stringpointername, idx))
                    else:
                        # if source is a local var on the stack, calculate the address and store it in stringpointer
                        # set framepointer to beginning of local vars of called function
                        namespace = self.blocks.getactivefunctionname()
                        stackframelength = "#%s_sflast" % namespace
                        idx = 0
                        self.createcode("SEC", "", "%s: for: argument:%s" % (functionname, sourcenamewithnamespace))
                        self.createcode("LDA", "_userstack_0", "load userstack lo-byte")
                        self.createcode("SBC", stackframelength, "subtract stackframelength")
                        self.createcode("STA", "_framepointer_0", "store in framepointer lo byte")
                        self.createcode("LDA", "_userstack_1", "load userstack hi-byte")
                        self.createcode("SBC", "#0", "subtract with carry")
                        self.createcode("STA", "_framepointer_1", "save to framepointer hi byte")
                        self.createcode("CLC")
                        self.createcode("LDA", "#%s" % sourcenamewithnamespace)
                        self.createcode("ADC", frame0)
                        self.createcode("STA", "%s_%d" % (stringpointername, idx))
                        idx += 1
                        self.createcode("LDA", "#0")
                        self.createcode("ADC", frame1)
                        self.createcode("STA", "%s_%d" % (stringpointername, idx))
                        # in destvarname (usually _unireg0) is the address
                else:
                    print("Error in strcpy, var:%s must be from type chararray" % sourcenamewithnamespace)
                    sys.exit(1)
            else:
                # argindex > 0, these are the sourcees from wich to copy/cat
                if self.checkhash(source_attr, "type_char"):
                    searchzero = self.randomword(8)
                    if sourcenamespace == "global":
                        self.createcode("LDA", "%s" % sourcenamewithnamespace)
                    else:
                        self.createcode("LDY", "#%s" % sourcenamewithnamespace)
                        self.createcode("LDA", "(%s),Y" % frame0)
                    self.createcode("PHA")
                    if functionname == "strcat":
                        self.createcode("LDY", "#0", "strcat: search for end of text in destination")
                        self.createcode("LDA", "(%s),Y" % stringpointername, name=searchzero)
                        self.createcode("BEQ", appendlabel)
                        self.createcode("INY")
                        self.createcode("JMP", searchzero)
                    elif functionname == "strcpy":
                        self.createcode("LDY", "#0", "strcpy: copy to beginning of char array")
                    else:
                        print("something was going wrong inside strcpy/strcat functionname not known: %s" % functionname)
                        print("calling with: %s" % sourcenamewithnamespace)
                        sys.exit(1)
                    self.createcode("PLA", name=appendlabel)
                    self.createcode("STA", "(%s),Y" % stringpointername)
                    self.createcode("INY")
                    self.createcode("LDA", "#0")
                    self.createcode("STA", "(%s),Y" % stringpointername)
                elif self.checkhash(source_attr, "type_chararray") \
                    or self.checkhash(source_attr, "type_stringconst") \
                    or self.checkhash(source_attr, "type_varpointer"):
                    searchzero = self.randomword(8)
                    # first set write pointer to first or end of existing string
                    if functionname == "strcat":
                        self.createcode("LDY", "#0", "strcat: search for end of text in destination")
                        self.createcode("LDA", "(%s),Y" % stringpointername, name=searchzero)
                        self.createcode("BEQ", appendlabel)
                        self.createcode("INY")
                        self.createcode("JMP", searchzero)
                    elif functionname == "strcpy":
                        self.createcode("LDY", "#0", "strcpy: copy to beginning of char array")
                    else:
                        print("error in strcpy, strcat...  unknown funktionname:%s" % functionname)
                        sys.exit(1)
                    #
                    # write pointer is at the start of the following write operation
                    #
                    if self.checkhash(source_attr, "type_stringconst"):
                        self.addstring(stringlabel, "\"%s\"" % sourcevalue)
                        self.createcode("LDX", "#0", name=appendlabel)
                        self.createcode("LDA", "%s,X" % stringlabel, name=nextcopy)
                        self.createcode("STA", "(%s),Y" % stringpointername)
                        self.createcode("BEQ", stringcopied)
                        self.createcode("INX")
                        self.createcode("INY")
                        self.createcode("JMP", nextcopy)
                        self.createcode("", name=stringcopied)
                    elif self.checkhash(source_attr, "type_varpointer"):
                        self.createcode("PHY", "", "save pointer to destination string")
                        self.createcode("LDY", "#%s" % sourcenamewithnamespace, "argument is var_pointer")
                        self.createcode("LDA", "(%s),Y" % frame0)
                        self.createcode("STA", "_zpscratch_0", "store pointer in zpscratch")
                        self.createcode("INY")
                        self.createcode("LDA", "(%s),Y" % frame0)
                        self.createcode("STA", "_zpscratch_1", "store pointer in zpscratch")
                        self.createcode("PLY")

                        self.createcode("LDX", "#0", name=appendlabel)
                        self.createcode("PHY","","complicate use of X and Y in (zp),Y :-(", name=nextcopy)
                        self.createcode("TXA")
                        self.createcode("TAY")
                        self.createcode("LDA", "(_zpscratch),Y")
                        self.createcode("PLY")
                        self.createcode("STA", "(%s),Y" % stringpointername)
                        self.createcode("LDA", "(%s),Y" % stringpointername, "Load again, because flags are lost")
                        self.createcode("BEQ", stringcopied)
                        self.createcode("INX")
                        self.createcode("INY")
                        self.createcode("JMP", nextcopy)
                        self.createcode("", name=stringcopied)
                    # type_chararray
                    else:
                        if sourcenamespace == "global":
                            self.createcode("LDX", "#0", name=appendlabel)
                            self.createcode("LDA", "%s,X" % sourcenamewithnamespace, name=nextcopy)
                            self.createcode("STA", "(%s),Y" % stringpointername)
                            self.createcode("BEQ", stringcopied)
                            self.createcode("INX")
                            self.createcode("INY")
                            self.createcode("JMP", nextcopy)
                            self.createcode("", name=stringcopied)
                        else:
                            # set destination pointer to destinationpoint register
                            self.createcode("CLC")
                            self.createcode("LDA", "frame0")
                            self.createcode("ADC", "#%d" % sourcenamewithnamespace)
                            self.createcode("STA", "%s" % destinationpointername)
                            self.createcode("LDA", "frame1")
                            self.createcode("ADC", "#0")
                            self.createcode("STA", "%s+1" % destinationpointername)
                            #
                            self.createcode("LDY", "#0")
                            self.createcode("LDA", "(%s),Y" % sourcenamewithnamespace, name=nextcopy)
                            self.createcode("STA", "(%s),Y" % destinationpointername)
                            print("strcpy, strcat....   type_chararray copy not implementet")
                            sys.exit(1)
                else:
                    print("%s: not implementet for var:%s  type:%s" % (functionname, sourcenamewithnamespace, source_attr))
                    sys.exit(1)
                nexttoken = targettoken

            argindex = argindex + 1

    # strlen
    def intfunc_strlen(self, functionobj, arglist, line=0): 
        functionname = functionobj.getname()
        functiondata = functionobj.getfuncdata()
        functionsubroutine = functiondata.getsubroutine()
        destinationargs = functiondata.getvar()
        for sourcestok in arglist:
            if isinstance(sourcestok, list):
                if arg[0] == "number":
                    print("internal function write() must be called with var, not with number")
                    sys.exit(1)
            sourcesize = int(sourcestok.getsize())
            sourcenamespace = sourcestok.getnamespace()
            source_attr = sourcestok.getattributehash()
            sourcename = sourcestok.getname()
            sourcenamewithnamespace = sourcestok.getnamewithnamespace()
            sourcevalue = sourcestok.getvalue()
            sourcetype = sourcestok.gettype()
            if self.checkhash(source_attr, "isargument"):
                frame0 = "_framepointer_0"
                frame1 = "_framepointer_1"
            else:
                frame0 = "_userstack_0"
                frame1 = "_userstack_1"
            # there may be a better solution, because strlen should return a byte as result, so clearing _unireg0 should not needed
            self.createcode("LDA", "#0","strlen(%s), setting _unireg0 to 0" % sourcenamewithnamespace)
            self.createcode("STA", "_unireg0_1")
            self.createcode("STA", "_unireg0_2")
            self.createcode("STA", "_unireg0_3")
            if sourcetype == "type_stringconst":
                loop = self.randomword(8)
                endloop = self.randomword(8)
                stringlabel = self.randomword(8)
                dochar = self.randomword(8)
                self.createcode("LDY", "#0", "internal strlen called with stringconstant")
                self.createcode("LDA", "%s,Y" % sourcenamewithnamespace, name=loop)
                self.createcode("BEQ", endloop)
                self.createcode("INY")
                self.createcode("JMP", loop)
                self.createcode("STY", "_unireg0_0", "Store Count into unireg0_0 only a byte", name=endloop)
            elif self.checkhash(source_attr, "type_chararray"):
                sourceaddress = sourcestok.getaddress()
                endofstring = self.randomword(8)
                outloop = self.randomword(8)
                if sourcenamespace == "global":
                    self.createcode("LDX", "#0", "strlen: with var %s from type chararray called" % sourcenamewithnamespace)
                    self.createcode("LDA", "%s,X" % sourcenamewithnamespace, "Load from Address %04x" % sourceaddress, name=outloop)
                    self.createcode("BEQ", endofstring)
                    self.createcode("INX")
                    self.createcode("JMP", outloop)
                    self.createcode("STX","_unireg0_0","Store Count into unireg0_0 only a byte", name=endofstring)
                else:
                    self.createcode("LDY", "#%s" % (sourcenamewithnamespace), "write: called with chararray %s" % sourcenamewithnamespace)
                    self.createcode("LDX", "#0")
                    self.createcode("LDA", "(%s),Y" % frame0, "Load Accu until char is #$00", name=outloop)
                    self.createcode("BEQ", endofstring)
                    self.createcode("INX")
                    self.createcode("INY")
                    self.createcode("JMP", outloop)
                    self.createcode("STX","_unireg0_0","Store Count into unireg0_0 only a byte", name=endofstring)
            elif self.checkhash(source_attr, "type_varpointer"):
                endofstring = self.randomword(8)
                outloop = self.randomword(8)
                if sourcenamespace == "global":
                    print("%s called with global var not yet implemented" % functionname)
                    sys.exit(1)
                else:
                    self.createcode("LDY", "#%s" % (sourcenamewithnamespace), "strlen() called with varpointer %s" % sourcenamewithnamespace)
                    self.createcode("LDA", "(%s),Y" % frame0)
                    self.createcode("STA", "_zpscratch_0", "load lobyte of address pointer in zpscratch")
                    self.createcode("INY")
                    self.createcode("LDA", "(%s),Y" % frame0, "load highbyte of address pointer in zpscratch")
                    self.createcode("STA", "_zpscratch_1")
                    # search for end of string terminater (0)
                    self.createcode("LDY", "#0")
                    self.createcode("LDA", "(_zpscratch),Y", "Load Accu until char is #$00", name=outloop)
                    self.createcode("BEQ", endofstring)
                    self.createcode("INY")
                    self.createcode("JMP", outloop)
                    self.createcode("STY","_unireg0_0","Store Count into unireg0_0 only a byte", name=endofstring)
            else:
                print("datatype not valid in internal function %s(), datatype was:%s" % (functionname, source_attr))
                sys.exit(1)

    # gettimer, _getstack6502, peek, poke, adr
    def intfunc_adr(self, functionobj, arglist, line=0):
        debug = False
        functionname = functionobj.getname()
        functiondata = functionobj.getfuncdata()
        functionsubroutine = functiondata.getsubroutine()
        destinationargs = functiondata.getvar()
        if (functionname == "gettimer" or functionname == "_getstack6502") and len(arglist) > 0:
            print("internal function %s has no argument" % functionname)
            sys.exit(1)
        if len(arglist) > 1:
            if functionname == "poke":
                if len(arglist) != 2:
                    print("internal function %s(a,b) has two arguments not %d!" % (functionname, len(arglist)))
                    print("error is in line: %d" % line)
                    sys.exit(1)
            else:
                print("internal function %s() has only one argument, arg was called with %d args: %s" % (functionname, len(arglist), arglist))
                print("error is in line: %d" % line)
                sys.exit(1)
        if functionname == "adr" or functionname == "settimer" or functionname == "peek" or functionname == "poke":
            arg = arglist[0]
            if isinstance(arg, list):
                if arg[0] == "number":
                    print("internal function %s() must be called with var, not with number" % functionname)
                    sys.exit(1)
            sourcestok = arg
            sourcesize = sourcestok.getsize()
            sourcenamespace = sourcestok.getnamespace()
            sourcevarname = arg.getnamewithnamespace()
            sourcetype = sourcestok.gettype()
            source_attr = sourcestok.getattributehash()
            source_name = sourcestok.getname()
        if functionname == "poke":
            arg = arglist[1]
            if isinstance(arg, list):
                if arg[0] == "number":
                    sourcevarname_2_isconstant = True
                    sourcevarname_2_constant = arg[1]
                    sourcetype_2 = "int"
                else:
                    print("internal function %s() must be called with var, not with number" % functionname)
                    sys.exit(1)
            else:
                sourcestok_2 = arg
                sourcesize_2 = sourcestok_2.getsize()
                sourcenamespace_2 = sourcestok_2.getnamespace()
                sourcevarname_2 = arg.getnamewithnamespace()
                sourcetype_2 = sourcestok_2.gettype()
                source_attr_2 = sourcestok_2.getattributehash()
                source_name_2 = sourcestok_2.getname()
                sourcevarname_2_isconstant = False

        dest = destinationargs[0]
        destination_name = dest.getvarname()
        destination_namespace = dest.getnamespace()
        deststok = self.stokens.getwithnamespace(dest.getvarname(), dest.getnamespace())
        destvarname = deststok.getname()
        destsize = deststok.getsize()
        dest_attr = deststok.getattributehash()
        if functionname == "adr" or functionname == "settimer" or functionname == "peek" or functionname == "poke":
            if self.checkhash(source_attr, "isargument"):
                frame0 = "_framepointer_0"
                frame1 = "_framepointer_1"
            else:
                frame0 = "_userstack_0"
                frame1 = "_userstack_1"
        if functionname == "adr":
            if self.checkhash(source_attr, "funcdefinition"): 
                idx = 0
                self.createcode("LDA", "#<%s" % source_name, "adr(%s) called" % source_name)
                self.createcode("STA", "%s_%d" % (destvarname, idx))
                idx += 1
                self.createcode("LDA", "#>%s" % source_name)
                self.createcode("STA", "%s_%d" % (destvarname, idx))
                idx += 1
                self.createcode("LDA", "#0")
                self.createcode("STA", "%s_%d" % (destvarname, idx))
                idx += 1
                self.createcode("STA", "%s_%d" % (destvarname, idx))
            elif sourcetype == "type_stringconst":
                idx = 0
                self.createcode("LDA", "#<%s" % sourcevarname, "adr(source:" + sourcevarname + ") dest:" + destvarname)
                self.createcode("STA", "%s_%d" % (destvarname, idx), "ADR handling, stringaddress to register, load lobyte of address")
                idx += 1
                self.createcode("LDA", "#>%s" % sourcevarname, "load hi-byte address for string constant")
                self.createcode("STA", "%s_%d" % (destvarname, idx))
                idx += 1
                self.createcode("LDA", "#0")
                self.createcode("STA", "%s_%d" % (destvarname, idx))
                idx += 1
                self.createcode("STA", "%s_%d" % (destvarname, idx))
            elif sourcenamespace == "global":
                idx = 0
                self.createcode("LDA", "#<%s" % sourcevarname, "adr(%s) called" % sourcevarname)
                self.createcode("STA", "%s_%d" % (destvarname, idx))
                idx += 1
                self.createcode("LDA", "#>%s" % sourcevarname)
                self.createcode("STA", "%s_%d" % (destvarname, idx))
                idx += 1
                self.createcode("LDA", "#0")
                self.createcode("STA", "%s_%d" % (destvarname, idx))
                idx += 1
                self.createcode("STA", "%s_%d" % (destvarname, idx))
            else:
                namespace = self.blocks.getactivefunctionname()
                stackframelength = "#%s_sflast" % namespace
                idx = 0
                self.createcode("CLC")
                self.createcode("LDA", "#%s" % sourcevarname)
                self.createcode("ADC", frame0)
                self.createcode("STA", "%s_%d" % (destvarname, idx))
                idx += 1
                self.createcode("LDA", "#0")
                self.createcode("ADC", frame1)
                self.createcode("STA", "%s_%d" % (destvarname, idx))
                idx += 1
                self.createcode("LDA", "#0")
                self.createcode("STA", "%s_%d" % (destvarname, idx))
                idx += 1
                self.createcode("STA", "%s_%d" % (destvarname, idx))
        elif functionname == "_getstack6502":
            self.createcode("TSX")
            self.createcode("STX", destvarname)
            self.createcode("LDA", "#$01")
            self.createcode("STA", "%s_%d" % (destvarname, 1))
        elif functionname == "gettimer":
            self.createcode("SEI")
            self.createcode("LDA", "VIAT1CL")
            self.createcode("STA", "%s_0" % destvarname)
            self.createcode("LDA", "VIAT1CH")
            self.createcode("STA", "%s_1" % destvarname)
            self.createcode("LDA", "global_tickscounter_0")
            self.createcode("STA", "%s_2" % destvarname)
            self.createcode("LDA", "global_tickscounter_1")
            self.createcode("STA", "%s_3" % destvarname)
            reg_4 = registerconvert["%s_4" % destvarname]
            reg_5 = registerconvert["%s_5" % destvarname]
            reg_6 = registerconvert["%s_6" % destvarname]
            reg_7 = registerconvert["%s_7" % destvarname]
            self.createcode("LDA", "global_tickscounter_2")
            self.createcode("STA", reg_4)
            self.createcode("LDA", "global_tickscounter_3")
            self.createcode("STA", reg_5)
            self.createcode("LDA", "#0")
            self.createcode("STA", reg_6)
            self.createcode("STA", reg_7)
            self.createcode("CLI")
            self.createcode("SEC")
            self.createcode("LDA", "t1interval_0", "Load initial value")
            self.createcode("SBC", "%s_0" % destvarname, "subtract low byte of t1-low-counter")
            self.createcode("STA", "%s_0" % destvarname)
            self.createcode("LDA", "t1interval_1", "Load initial value")
            self.createcode("SBC", "%s_1" % destvarname, "subtract high byte of t1-high-counter")
            self.createcode("STA", "%s_1" % destvarname)
        elif functionname == "settimer":
            if sourcetype == "int" or sourcetype == "long" or sourcetype == "longlong":
                idx = 0
                self.createcode("LDY", "#%s_0" % sourcevarname, "get Value of %s" % sourcevarname)
                self.createcode("LDA", "(%s),Y" % frame0)
                self.createcode("STA", "VIAT1CL", "set Timer Latch Low Byte")
                self.createcode("STA", "t1interval_0", "save value of Low Byte")
                self.createcode("LDY", "#%s_1" % sourcevarname, "get Value of %s" % sourcevarname)
                self.createcode("LDA", "(%s),Y" % frame0)
                self.createcode("STA", "VIAT1CH", "set Timer Latch High Byte")
                self.createcode("STA", "t1interval_1", "save value of high Byte")
            else:
                print("functionname %s needs int or long or longlong variable, called with:%s" % (functionname, sourcetype))
                sys.exit(1)
        elif functionname == "peek":
            if sourcetype == "int" or sourcetype == "long" or sourcetype == "longlong" or sourcetype == "ADDRESSPTR":
                self.createcode("LDY", "#%s" % sourcevarname, "peek, get Value of %s" % sourcevarname)
                self.createcode("LDA", "(%s),Y" % frame0)
                self.createcode("STA", "_zpscratch_0", "save for indirect access")
                self.createcode("INY")
                self.createcode("LDA", "(%s),Y" % frame0)
                self.createcode("STA", "_zpscratch_1", "save for indirect access")
                self.createcode("LDY", "#0")
                self.createcode("LDA", "(_zpscratch),Y")
                self.createcode("STA", "%s_0" % destvarname, "usally in _unireg0") 
        elif functionname == "poke":
            if sourcetype == "int" or sourcetype == "long" or sourcetype == "longlong" or sourcetype == "ADDRESSPTR":
                if sourcetype_2 == "byte" or sourcetype_2 == "int" or sourcetype_2 == "char":
                    # get address, where to put the second parameter
                    self.createcode("LDY", "#%s" % sourcevarname, "poke, get Value of %s" % sourcevarname)
                    self.createcode("LDA", "(%s),Y" % frame0)
                    self.createcode("STA", "_zpscratch_0", "save for indirect access")
                    self.createcode("INY")
                    self.createcode("LDA", "(%s),Y" % frame0)
                    self.createcode("STA", "_zpscratch_1", "save for indirect access")
                    # load second parameter to store at address given from the first parameter
                    if sourcevarname_2_isconstant:
                        hexvalue = "%02X" % int(sourcevarname_2_constant)
                        self.createcode("LDA", "#$%s" % hexvalue, "load constant %s in accu" % sourcevarname_2_constant)
                        self.createcode("STA", "(_zpscratch)", "store byte into address")
                        pass
                    else:
                        self.createcode("LDY", "#%s" % sourcevarname_2, "poke, get Value of %s" % sourcevarname_2)
                        self.createcode("LDA", "(%s),Y" % frame0)
                        self.createcode("LDY", "#0")
                        self.createcode("STA", "(_zpscratch),Y", "store byte into address")
                else:
                    print("function %s needs byte or int as second parameter, %s was given" % (functionname, sourcetype_2))
                    sys.exit(1)
            else:
                print("functionname %s needs int or long or longlong variable, called with:%s" % (functionname, sourcetype))
                sys.exit(1)
        else:
            print("functionname %s unknown for routine 'adr'" % functionname)
            sys.exit(1)
    
    # getch(), avail()
    def intfunc_sizeof(self, functionobj, arglist, line=0):
        debug = False
        functionname = functionobj.getname()
        functiondata = functionobj.getfuncdata()
        functionsubroutine = functiondata.getsubroutine()
        destinationargs = functiondata.getvar()
        if len(arglist) > 1:
            print("internal function sizeof(varname) has only one argument, arg was called with %d args: %s" % (len(arglist), arglist))
            sys.exit(1)
        if len(arglist) == 0 and functionname == "sizeof":
            print("internal function sizeof(varname) has only one argument, arg was called with %d args: %s" % (len(arglist), arglist))
            sys.exit(1)
        if functionname == "getch":
            dest = destinationargs[0]
            deststok = self.stokens.getwithnamespace(dest.getvarname(), dest.getnamespace())
            destvarname = deststok.getname()
            destsize = deststok.getsize()
            dest_attr = deststok.getattributehash()
            idx = 0
            self.createcode("JSR", "_INPUT_WAIT", "getch() called")
            self.createcode("STA", "%s_%d" % (destvarname, idx), "getch()")
            idx += 1
            self.createcode("LDA", "#0")
            self.createcode("STA", "%s_%d" % (destvarname, idx))
            idx += 1
            self.createcode("STA", "%s_%d" % (destvarname, idx))
            idx += 1
            self.createcode("STA", "%s_%d" % (destvarname, idx))
        elif functionname == "avail":
            dest = destinationargs[0]
            deststok = self.stokens.getwithnamespace(dest.getvarname(), dest.getnamespace())
            destvarname = deststok.getname()
            destsize = deststok.getsize()
            dest_attr = deststok.getattributehash()
            idx = 0
            self.createcode("JSR", "_INPUT_AVAIL", "avail() called")
            self.createcode("STA", "%s_%d" % (destvarname, idx), "getch()")
            idx += 1
            self.createcode("LDA", "#0")
            self.createcode("STA", "%s_%d" % (destvarname, idx))
            idx += 1
            self.createcode("STA", "%s_%d" % (destvarname, idx))
            idx += 1
            self.createcode("STA", "%s_%d" % (destvarname, idx))

        else:
            arg = arglist[0]
            if isinstance(arg, list):
                if arg[0] == "number":
                    print("internal function sizeof() must be called with var, not with number")
                    sys.exit(1)
            sourcestok = arg
            sourcesize = sourcestok.getsize()
            sourcenamespace = sourcestok.getnamespace()
            sourcevarname = arg.getnamewithnamespace()
            sourcetype = sourcestok.gettype()
            source_attr = sourcestok.getattributehash()
            dest = destinationargs[0]
            deststok = self.stokens.getwithnamespace(dest.getvarname(), dest.getnamespace())
            destvarname = deststok.getname()
            destsize = deststok.getsize()
            dest_attr = deststok.getattributehash()
            if self.checkhash(source_attr, "isargument"):
                frame0 = "_framepointer_0"
                frame1 = "_framepointer_1"
            else:
                frame0 = "_userstack_0"
                frame1 = "_userstack_1"
            hexsize = "%08x" % sourcesize
            idx = 0
            self.createcode("LDA", "#$%s" % hexsize[6:8], "sizeof(%s) called" % sourcevarname)
            self.createcode("STA", "%s_%d" % (destvarname, idx), "sizeof() is %d bytes" % sourcesize)
            idx += 1
            self.createcode("LDA", "#$%s" % hexsize[4:6])
            self.createcode("STA", "%s_%d" % (destvarname, idx))
            idx += 1
            self.createcode("LDA", "#$%s" % hexsize[2:4])
            self.createcode("STA", "%s_%d" % (destvarname, idx))
            idx += 1
            self.createcode("LDA", "#$%s" % hexsize[0:2])
            self.createcode("STA", "%s_%d" % (destvarname, idx))

    def intfunc_lcd(self, functionobj, arglist, line=0):
        debug = False
        functionname = functionobj.getname()
        functiondata = functionobj.getfuncdata()
        functionsubroutine = functiondata.getsubroutine()
        destinationargs = functiondata.getvar()
        if (functionname == "lcdcommand" or functionname == "lcddata") and len(arglist) > 1:
            print("internal function %s has only one argument" % functionname)
            sys.exit(1)
        arg = arglist[0]
        argumenttype = "var"
        if isinstance(arg, list):
            if arg[0] == "number":
                value = arg[1]
                argumenttype = "const"
            else:
                print("internal function %s() must be called with var, not with number" % functionname)
                sys.exit(1)
        else:
            sourcestok = arg
            sourcesize = sourcestok.getsize()
            sourcenamespace = sourcestok.getnamespace()
            sourcevarname = arg.getnamewithnamespace()
            sourcetype = sourcestok.gettype()
            source_attr = sourcestok.getattributehash()
            source_name = sourcestok.getname()
            argumenttype = "var"
            if self.checkhash(source_attr, "isargument"):
                frame0 = "_framepointer_0"
                frame1 = "_framepointer_1"
            else:
                frame0 = "_userstack_0"
                frame1 = "_userstack_1"
        if functionname == "lcdcommand":
            if argumenttype == "const":
                self.createcode("LDA", "#%s" % value)
                self.createcode("JSR", "lcd_instruction")
            elif argumenttype == "var":
                pass
            else:
                print("internal function %s() must be called with const or var" % functionname)
        elif functionname == "lcddata":
            if argumenttype == "const":
                self.createcode("LDA", "#%s" % value)
                self.createcode("JSR", "print_lcdchar")
            elif argumenttype == "var":
                self.createcode("LDY","#%s" % sourcevarname)
                self.createcode("LDA","(%s),Y" % frame0)
                self.createcode("JSR", "print_lcdchar")
            else:
                print("internal function %s() must be called with const or var" % functionname)
        


    def intfunc_tofloat(self, functionobj, arglist, line=0):
        debug = False
        functionname = functionobj.getname()
        functiondata = functionobj.getfuncdata()
        functionsubroutine = functiondata.getsubroutine()
        destinationargs = functiondata.getvar()
        dest = destinationargs[0]
        destination_name = dest.getvarname()
        destination_namespace = dest.getnamespace()
        deststok = self.stokens.getwithnamespace(dest.getvarname(), dest.getnamespace())
        destvarname = deststok.getname()
        destsize = deststok.getsize()
        dest_attr = deststok.getattributehash()
        if len(arglist) != 1:
            print("internal function %s(x) has only one argument, arg was called with %d args: %s" % (functionname, len(arglist), arglist))
            sys.exit(1)
        value = arglist[0]
        if isinstance(value, list):
            if value[0] == "number":
                operand = value[1]
            else:
                print("internal function %s(var, const) must be call with number constant or variable" % functionname)
                sys.exit(1)
            # argument is integer constant or float
            if functionname == "real":
                x = "%04x" % int(operand)
                hibyte = x[0:2]
                lobyte = x[2:4]
                # Load M1 with 16bit integer value
                self.createcode("LDA", "#$%s" % lobyte, "calling internal real(%s) function" % operand)
                self.createcode("STA", "M1+1")
                self.createcode("LDA", "#$%s" % hibyte)
                self.createcode("STA", "M1")
                destvarname = "_unireg0" # workaround becaus we can not know if we are called from expression or not
            elif functionname == "integer":
                print("internal functionname integer() not implemented with const argument")
                sys.exit(1)
            elif functionname == "log":
                print("internal functionname log() not implemented with const argument")
                sys.exit(1)
            elif functionname == "log10":
                print("internal functionname log10() not implemented with const argument")
                sys.exit(1)
            elif functionname == "exp":
                print("internal functionname exp() not implemented with const argument")
                sys.exit(1)
            else:
                print("internal function %s is unknown" % functionname)
                sys.exit(1)
        else:
            sourcestok = arglist[0]
            sourcenamespace = sourcestok.getnamespace()
            sourcevarnamewithnamespace = sourcestok.getnamewithnamespace()
            sourcevarname = sourcestok.getvarname()
            # sourcevarnamenamespacename = sourcestok.getnamespacename()
            vartoken = self.stokens.getwithnamespace(sourcevarname, sourcenamespace)
            source_attr = vartoken.getattributehash()
            if self.checkhash(source_attr, "isargument"):
                frame0 = "_framepointer_0"
                frame1 = "_framepointer_1"
            else:
                frame0 = "_userstack_0"
                frame1 = "_userstack_1"
        if functionname == "real":
            if not isinstance(value, list):
                if sourcenamespace == "global":
                    if sourcevarname != "X1":
                        self.createcode("LDA", "%s_0" % sourcevarname, "calling internal real(%s)" % sourcevarname)
                        self.createcode("STA", "M1+1")
                        self.createcode("LDA", "%s_1" % sourcevarname)
                        self.createcode("STA", "M1")
                    else:
                        self.createcode("LDA", "%s" % sourcevarname, "calling internal real(%s)" % sourcevarname)
                        self.createcode("STA", "M1+1")
                else:
                    destvarname = "_unireg0" # in case of real() is not in an expression, the returnvalue is in reg 0
                    self.createcode("LDY", "#%s" % sourcevarnamewithnamespace, "calling internal real(%s)" % sourcevarnamewithnamespace)
                    self.createcode("LDA", "(%s),Y" % frame0)
                    self.createcode("STA", "M1+1", "store in M1")
                    self.createcode("INY")
                    self.createcode("LDA", "(%s),Y" % frame0)
                    self.createcode("STA", "M1")
            self.createcode("JSR", "wozFLOAT", "calling wozFLOAT() to convert integer to wozfloat")
            # self.createcode("JSR", "_OUT_M1")
            # self.createcode("JMP", "wozmon")
            if destvarname != "X1":
                idx = 0
                self.createcode("LDA", "X1_0")
                self.createcode("STA", "%s_%d" % (destvarname, idx))
                idx += 1
                self.createcode("LDA", "M1_0")
                self.createcode("STA", "%s_%d" % (destvarname, idx))
                idx += 1
                self.createcode("LDA", "M1_1")
                self.createcode("STA", "%s_%d" % (destvarname, idx))
                idx += 1
                self.createcode("LDA", "M1_2")
                self.createcode("STA", "%s_%d" % (destvarname, idx))
            else:
                xxx = destvarname
        elif functionname == "integer":
            if sourcenamespace == "global":
                if sourcevarname != "X1":
                    self.createcode("LDA", "#%s_0" % sourcevarname)
                    self.createcode("STA", "X1")
                    self.createcode("LDA", "#%s_1" % sourcevarname, "integer(%s) called" % sourcevarname)
                    self.createcode("STA", "M1+0")
                    self.createcode("LDA", "#%s_2" % sourcevarname)
                    self.createcode("STA", "M1+1")
                    self.createcode("LDA", "#%s_3" % sourcevarname)
                    self.createcode("STA", "M1+2")
            else:
                self.createcode("LDY", "#%s" % sourcevarnamewithnamespace, "integer(%s) called" % sourcevarnamewithnamespace)
                self.createcode("LDA", "(%s),Y" % frame0)
                self.createcode("STA","X1")
                self.createcode("INY")
                self.createcode("LDA", "(%s),Y" % frame0)
                self.createcode("STA","M1+0")
                self.createcode("INY")
                self.createcode("LDA", "(%s),Y" % frame0)
                self.createcode("STA","M1+1")
                self.createcode("INY")
                self.createcode("LDA", "(%s),Y" % frame0)
                self.createcode("STA","M1+2")
                destvarname = "_unireg0" # workaround, if not called from expression
            self.createcode("JSR", "wozFIX")
            if destvarname != "X1":
                idx = 0
                self.createcode("LDA", "M1_1")
                self.createcode("STA", "%s_%d" % (destvarname, idx))
                idx += 1
                self.createcode("LDA", "M1_0")
                self.createcode("STA", "%s_%d" % (destvarname, idx))
                idx += 1
                self.createcode("LDA", "#0")
                self.createcode("STA", "%s_%d" % (destvarname, idx))
                idx += 1
                self.createcode("STA", "%s_%d" % (destvarname, idx))
            else: # destvarname = X1
                self.createcode("LDA", "M1_1", "destvarname = %s" % destvarname)
                self.createcode("STA", "X1", "save lo byte")
                # M1_0 content is ok
                self.createcode("LDA", "#0")
                self.createcode("STA", "M1_1")
                self.createcode("STA", "M1_2")                    
        elif functionname == "log":
            if sourcenamespace == "global":
                if sourcevarname != "X1":
                    self.createcode("LDA", "#%s_0" % sourcevarname)
                    self.createcode("STA", "X1")
                    self.createcode("LDA", "#%s_1" % sourcevarname, "log(%s) called" % sourcevarname)
                    self.createcode("STA", "M1+0")
                    self.createcode("LDA", "#%s_2" % sourcevarname)
                    self.createcode("STA", "M1+1")
                    self.createcode("LDA", "#%s_3" % sourcevarname)
                    self.createcode("STA", "M1+2")
            else:
                self.createcode("LDY", "#%s" % sourcevarnamewithnamespace, "log(%s) called" % sourcevarnamewithnamespace)
                self.createcode("LDA", "(%s),Y" % frame0)
                self.createcode("STA","X1")
                self.createcode("INY")
                self.createcode("LDA", "(%s),Y" % frame0)
                self.createcode("STA","M1+0")
                self.createcode("INY")
                self.createcode("LDA", "(%s),Y" % frame0)
                self.createcode("STA","M1+1")
                self.createcode("INY")
                self.createcode("LDA", "(%s),Y" % frame0)
                self.createcode("STA","M1+2")
                destvarname = "_unireg0" # workaround, see above
            self.createcode("JSR", "wozLOG")
            if destvarname != "X1":
                idx = 0
                self.createcode("LDA", "X1_0")
                self.createcode("STA", "%s_%d" % (destvarname, idx))
                idx += 1
                self.createcode("LDA", "M1_0")
                self.createcode("STA", "%s_%d" % (destvarname, idx))
                idx += 1
                self.createcode("LDA", "M1_1")
                self.createcode("STA", "%s_%d" % (destvarname, idx))
                idx += 1
                self.createcode("LDA", "M1_2")
                self.createcode("STA", "%s_%d" % (destvarname, idx))
        elif functionname == "log10":
            if sourcenamespace == "global":
                if sourcevarname != "X1":
                    self.createcode("LDA", "#%s_0" % sourcevarname)
                    self.createcode("STA", "X1")
                    self.createcode("LDA", "#%s_1" % sourcevarname, "log10(%s) called" % sourcevarname)
                    self.createcode("STA", "M1+0")
                    self.createcode("LDA", "#%s_2" % sourcevarname)
                    self.createcode("STA", "M1+1")
                    self.createcode("LDA", "#%s_3" % sourcevarname)
                    self.createcode("STA", "M1+2")
                else:
                    xxx = sourcevarname
            else:
                self.createcode("LDY", "#%s" % sourcevarnamewithnamespace, "log10(%s) called" % sourcevarnamewithnamespace)
                self.createcode("LDA", "(%s),Y" % frame0)
                self.createcode("STA","X1")
                self.createcode("INY")
                self.createcode("LDA", "(%s),Y" % frame0)
                self.createcode("STA","M1+0")
                self.createcode("INY")
                self.createcode("LDA", "(%s),Y" % frame0)
                self.createcode("STA","M1+1")
                self.createcode("INY")
                self.createcode("LDA", "(%s),Y" % frame0)
                self.createcode("STA","M1+2")
                destvarname = "_unireg0" # workaround, see above
            self.createcode("JSR", "wozLOG10")
            if destvarname != "X1":
                idx = 0
                self.createcode("LDA", "X1_0")
                self.createcode("STA", "%s_%d" % (destvarname, idx))
                idx += 1
                self.createcode("LDA", "M1_0")
                self.createcode("STA", "%s_%d" % (destvarname, idx))
                idx += 1
                self.createcode("LDA", "M1_1")
                self.createcode("STA", "%s_%d" % (destvarname, idx))
                idx += 1
                self.createcode("LDA", "M1_2")
                self.createcode("STA", "%s_%d" % (destvarname, idx))
        elif functionname == "exp":
            if sourcenamespace == "global":
                if sourcevarname != "X1":
                    self.createcode("LDA", "#%s_0" % sourcevarname)
                    self.createcode("STA", "X1")
                    self.createcode("LDA", "#%s_1" % sourcevarname, "exp(%s) called" % sourcevarname)
                    self.createcode("STA", "M1+0")
                    self.createcode("LDA", "#%s_2" % sourcevarname)
                    self.createcode("STA", "M1+1")
                    self.createcode("LDA", "#%s_3" % sourcevarname)
                    self.createcode("STA", "M1+2")
                else:
                    xxx = sourcevarname
            else:
                self.createcode("LDY", "#%s" % sourcevarnamewithnamespace, "exp(%s) called" % sourcevarnamewithnamespace)
                self.createcode("LDA", "(%s),Y" % frame0)
                self.createcode("STA","X1")
                self.createcode("INY")
                self.createcode("LDA", "(%s),Y" % frame0)
                self.createcode("STA","M1+0")
                self.createcode("INY")
                self.createcode("LDA", "(%s),Y" % frame0)
                self.createcode("STA","M1+1")
                self.createcode("INY")
                self.createcode("LDA", "(%s),Y" % frame0)
                self.createcode("STA","M1+2")
                destvarname = "_unireg0" # workaround, see above
            self.createcode("JSR", "wozEXP")
            if destvarname != "X1":
                idx = 0
                self.createcode("LDA", "X1_0")
                self.createcode("STA", "%s_%d" % (destvarname, idx))
                idx += 1
                self.createcode("LDA", "M1_0")
                self.createcode("STA", "%s_%d" % (destvarname, idx))
                idx += 1
                self.createcode("LDA", "M1_1")
                self.createcode("STA", "%s_%d" % (destvarname, idx))
                idx += 1
                self.createcode("LDA", "M1_2")
                self.createcode("STA", "%s_%d" % (destvarname, idx))

# --------------------------------- KIMA FUNCTIONS ------------------------------------
    def emitsetkimaprec(self):
        self.createcode("LDA", "#%s" % int(self.kim_precvalue))
        self.createcode("STA", "kima_prec")
        self.createcode("LDA", "#%s" % int(self.kim_extradigit))
        self.createcode("STA", "kima_extra")
        self.createcode("JSR", "kima_iprec")

    def intfunc_kima(self, functionobj, arglist, line=0):
        debug = False
        functionname = functionobj.getname()
        functiondata = functionobj.getfuncdata()
        functionsubroutine = functiondata.getsubroutine()
        destinationargs = functiondata.getvar()
        dest = destinationargs[0]
        destination_name = dest.getvarname()
        destination_namespace = dest.getnamespace()
        deststok = self.stokens.getwithnamespace(dest.getvarname(), dest.getnamespace())
        destvarname = deststok.getname()
        destsize = deststok.getsize()
        dest_attr = deststok.getattributehash()
        if functionname == "kim_clrx" or functionname == "kim_clry" or functionname == "kim_clrz" \
                or functionname == "kim_savxy" or functionname == "kim_rclxy":
            numofargs = 0
        elif functionname == "kim_iprec":
            numofargs = 2
        elif functionname == "kim_ploadx" or functionname == "kim_ploady" or functionname == "kim_uploadx" \
                or functionname == "kim_uploady" or functionname == "kim_dechex" or functionname == "kim_ustres":
            numofargs = 1
        else:
            print("internal function %s(x) different args, arg was called with %d args: %s" % (functionname, len(arglist), arglist))
            sys.exit(1)
        if len(arglist) != numofargs:
            print("internal function %s(x) has only one argument, arg was called with %d args: %s" % (functionname, len(arglist), arglist))
            sys.exit(1)
        for value in arglist:
            if isinstance(value, list):
                if value[0] == "number":
                    operand = value[1]
                else:
                    print("internal function %s(var, const) must be call with number constant or variable" % functionname)
                    sys.exit(1)
                # argument is integer constant or float
                if functionname == "kim_uploadx" or functionname == "kim_uploady":
                    x = "%04x" % int(operand)
                    hibyte = x[0:2]
                    lobyte = x[2:4]
                    # Load M1 with 16bit integer value
                    self.createcode("LDA", "#$%s" % lobyte, "calling internal real(%s) function" % operand)
                    self.createcode("STA", "M1+1")
                    self.createcode("LDA", "#$%s" % hibyte)
                    self.createcode("STA", "M1")
                else:
                    print("internal function %s is unknown" % functionname)
                    sys.exit(1)
            else:
                sourcestok = value
                sourcenametype = sourcestok.gettype()
                sourcenamespace = sourcestok.getnamespace()
                sourcevarnamewithnamespace = sourcestok.getnamewithnamespace()
                sourcevarname = sourcestok.getvarname()
                # sourcevarnamenamespacename = sourcestok.getnamespacename()
                vartoken = self.stokens.getwithnamespace(sourcevarname, sourcenamespace)
                source_attr = vartoken.getattributehash()
                if self.checkhash(source_attr, "isargument"):
                    frame0 = "_framepointer_0"
                    frame1 = "_framepointer_1"
                else:
                    frame0 = "_userstack_0"
                    frame1 = "_userstack_1"
        if functionname == "kim_clrx":
            self.createcode("JSR", "kima_clrx")
        elif functionname == "kim_clry":
            self.createcode("JSR", "kima_clry")
        elif functionname == "kim_clrz":
            self.createcode("JSR", "kima_clrz")
        elif functionname == "kim_uploadx" or functionname == "kim_uploady":
            # define precision
            self.emitsetkimaprec()
            if sourcenametype == "type_stringconst":
                if sourcenamespace == "global":
                    if functionname == "kim_uploadx":
                        self.createcode("LDA", "#<%s" % sourcevarnamewithnamespace)
                        self.createcode("STA", "kima_argxl")
                        self.createcode("LDA", "#>%s" % sourcevarnamewithnamespace)
                        self.createcode("STA", "kima_argxh")
                        self.createcode("JSR", "kima_uloadx")
                    elif functionname == "kim_uploady":
                        self.createcode("LDA", "#<%s" % sourcevarnamewithnamespace)
                        self.createcode("STA", "kima_argyl")
                        self.createcode("LDA", "#>%s" % sourcevarnamewithnamespace)
                        self.createcode("STA", "kima_argyh")
                        self.createcode("JSR", "kima_uloady")
                    else:
                        print("unknown functionname in kim_uploadx or kim_uploady")
                        sys.exit(1)
        elif functionname == "kim_ustres":
            if self.checkhash(source_attr, "type_chararray"):
                sourceaddress = sourcestok.getaddress()
                endofstring = self.randomword(8)
                outloop = self.randomword(8)
                mantissaispositive = self.randomword(8)
                copymantissaloop = self.randomword(8)
                if sourcenamespace == "global":
                    self.createcode("LDA", "#<%s" % sourcevarnamewithnamespace, "Load from Address %04x" % sourceaddress)
                    self.createcode("STA", "kima_resl")
                    self.createcode("LDA", "#>%s" % sourcevarnamewithnamespace)
                    self.createcode("STA", "kima_resh")
                    self.createcode("JSR", "kima_ustres")
                else:
                    self.createcode("LDX", "#0")
                    self.createcode("LDA", "#<global_memarea", "Load  Address memadrea for analyses")
                    self.createcode("STA", "kima_resl", "Store in resl for transfer")
                    self.createcode("LDA", "#>global_memarea", "Load  Address memadrea for analyses")
                    self.createcode("STA", "kima_resh", "Store in resh for transfer")
                    self.createcode("JSR", "kima_ustres", "transfer and convert to unpacked format to global_memarea")
                    self.createcode("BIT", "global_memarea", "read sign of mantissa and exponent")
                    self.createcode("BPL", mantissaispositive)
                    self.createcode("LDA", "#'-'")
                    self.createcode("STA", "global_memarea+24,X", "store string in temp area")
                    self.createcode("INX")
                    self.createcode("LDY", "#0", "count number of bytes for mantissa in Y-Reg", name=mantissaispositive)
                    self.createcode("INY", "", "correct pointer to first byte in mantissa")
                    self.createcode("LDA", "global_memarea,X", name=copymantissaloop)
                    self.createcode("STA", "global_memarea+24,Y", "store string in temp area")
                    self.createcode("INY")
                    self.createcode("TYA")
                    self.createcode("CMP", "kima_prec")
                    self.createcode("BPL", copymantissaloop)
                    self.createcode("LDA", "#0")
                    self.createcode("STA", "global_memarea+24,Y")
                    self.createcode("JSR", "wozmon")


                    self.createcode("LDA", "#<%s" % sourcevarnamewithnamespace, "Load from Address %04x" % sourceaddress)
                    self.createcode("LDA", frame0)
                    self.createcode("ADC", "#%s" % sourcevarnamewithnamespace)
                    self.createcode("STA", "kima_resl")
                    self.createcode("LDA", frame1)
                    self.createcode("ADC", "#0")
                    self.createcode("STA", "kima_resh")
                    self.createcode("JSR", "kima_ustres")

    def startfunctionarguments(self, stoken, name, value, attributes):
        if self.opset6502_save_register:
            self.createcode("PHA", "", "---STARTFUNCTIONARGUMENTS retval:%s  funcname:%s with %s" % (name,value,attribstr), name=value)
            self.createcode("TXA", "", "store Register X to Accu")
            self.createcode("PHA", "", "push accu to stack")
            self.createcode("TYA", "", "store Register Y to Accu")
            self.createcode("PHA", "", "store accu to stack")
        else:
            self.createcode("", "", "---STARTFUNCTIONARGUMENTS retval:%s  funcname:%s" % (name,value), name=value)
        if False:
            self.createcode("LDA", "_userstack_0", "Load User-Stack lo byte")
            self.createcode("STA", "_framepointer_0", "Save Userstack lo in framepointer")
            self.createcode("LDA", "_userstack_1", "Load User-Stack lo byte")
            self.createcode("STA", "_framepointer_1", "Save Userstack lo in framepointer")
        return

    def stopfunctionarguments(self, name, value, attributes, istnotglobal):
        attribstr = ""
        for a in attributes:
            attribstr += a + ','
        attribstr = attribstr[:-1]
        if self.opset6502_save_register:
            self.createcode("PLA","","restore accu from stack")
            self.createcode("TAY","","copy accu to Y")
            self.createcode("PLA","","restore accu from stack")
            self.createcode("TAX","","copy accu to X")
            self.createcode("PLA","","STOPFUNCTIONARGUMENTS %s = %s with %s" % (name,value,attribstr))
        else:
            self.createcode("","","STOPFUNCTIONARGUMENTS %s = %s with %s" % (name,value,attribstr))
        frameoffsetforvars = self.blocks.lastfunction().getargaddress()
        framelast = self.blocks.getactivefunctionname() + "_sframe"
        self.constintstatement(framelast, frameoffsetforvars, ["constvalue"])
        return

    def startblock(self, name, value, attributes, line=0):
        attribstr = ""
        for a in attributes:
            attribstr += a + ','
        attribstr = attribstr[:-1]
        self.setname("")
        self.setopcode("NOP")
        self.setvalue("")
        self.setcomment("---STARTBLOCK args %s = %s with %s" % (name,value,attribstr))
        self.createassemberline()
        if self.opset6502_save_register:
            self.createcode("TXA","","store registers for functionbody")
            self.createcode("PHA","","store registers for functionbody")
            self.createcode("TYA","", "store registers for functionbody")
            self.createcode("PHA","","store registers for functionbody")
        #self.createcode("JSR", "_OUT_USERSTACK")

        namespace = self.blocks.getactivefunctionname()
        stackframelength = "#%s_sflast" % namespace#ä
         # correct the stackpointer for this function to point to the beginning of locals
        self.insertinline("LDA", stackframelength,line,comment="set length of stackframe (%d)")
        self.insertinline("JSR", "setunireg7fromaccu", line, comment="make space on stack (%d)")
        self.insertinline("JSR", "subu7fromuserstack", line)
        if False:
            self.createcode("LDA", "_userstack_0")
            self.createcode("STA", "_framepointer_0")
            self.createcode("LDA", "_userstack_1")
            self.createcode("STA", "_framepointer_1")
        self.eval_stacksize = 0
        #self.createcode("JSR", "_OUT_USERSTACK")
        return

    def endblock(self, name, value, attributes, line=0):
        namespace = self.blocks.getactivefunctionname()
        attribstr = ""
        for a in attributes:
            attribstr += a + ','
        attribstr = attribstr[:-1]
        userstack = self.stokens.get("_userstack")
        adruserstack = userstack.getaddress()
        stackframelength = "#%s_sflast" % namespace
        exitlabel = namespace + "_exitlabel"
        self.createcode(" ", "", "ENDBLOCK name:%s = %s with %s" % (name,value,attribstr), name=exitlabel)
        self.insertinline("LDA", stackframelength, line, comment="correct stackpointer, remove stackframe (%d)")
        self.insertinline("JSR", "setunireg7fromaccu", line)
        self.insertinline("JSR", "addu7touserstack", line)
        if self.opset6502_save_register:
            self.createcode("PLA","","restore registers")
            self.createcode("TAY","","restore registers")
            self.createcode("PLA","","restore registers")
            self.createcode("TAX","","restore registers")
        self.insertinline("RTS", "", line)
        # define memory for expressionstack
        stoken = self.stokens.addwithattributes("eval_stack_mem", "chararray", ["type_chararray", "vardefinition"])
        stoken.setsize(self.eval_stacksize)
        self.varstatement(stoken, "chararray", "Eval_Stk", isinarguments= True)
        #
        stackoffsetforvars = self.blocks.lastfunction().getargaddress()
        stackframelast = self.blocks.getactivefunctionname() + "_sflast"
        self.constintstatement(stackframelast, stackoffsetforvars, ["constvalue"])
        return

    def opensquarebracket(self, name, value, attributes):
        attribstr = ""
        for a in attributes:
            attribstr += a + ','
        attribstr = attribstr[:-1]
        self.setname("")
        self.setopcode("")
        self.setvalue("")
        self.setcomment("openbracket args %s = %s with %s" % (name,value,attribstr))
        return self.createassemberline()

    def closesquarebracket(self, name, value, attributes):
        attribstr = ""
        for a in attributes:
            attribstr += a + ','
        attribstr = attribstr[:-1]
        self.setname("")
        self.setopcode("")
        self.setvalue("")
        self.setcomment("closebracket args %s = %s with %s" % (name,value,attribstr))
        return self.createassemberline()

    def reservememory(self, stok):
        name = stok.getname()
        value = stok.getvalue()
        self.setname("")
        self.setopcode("")
        self.setvalue("")
        self.setcomment("reserve array memory args %s = %s" % (name,value))
        self.createassemberline()
        return

    def startlabel(self, labeltoken, called_type, called_name):
        self.setname(called_name)
        self.setopcode("NOP")
        self.setvalue("")
        self.setcomment("defined label:%s type:%s" % (called_name, called_type))
        self.createassemberline()

    def jumptolabel(self, t_type, t_value):
        self.createcode("JMP",t_value,"execute goto statement to label:%s" % t_value)

    def exitfromfunction(self):
        exitlabel = self.blocks.getactivefunctionname() + "_exitlabel"
        self.createcode("JMP", exitlabel)

    def do_afterif(self, ifobject):
        internlabel = ifobject.getname() + ''.join(random.choice(string.ascii_lowercase) for i in range(4))
        doafteriflabel = "%s_%s" % (internlabel, ''.join(random.choice(string.ascii_lowercase) for i in range(4)))
        ifobject.setfuncdata(doafteriflabel)
        self.createcode("LDA", "_unireg0_0", "do_afterif() load result from if from unireg0")
        self.createcode("BNE", internlabel)
        self.createcode("JMP", doafteriflabel)
        self.createcode("", "","do_afterif",  name=internlabel)

    def end_afterif(self, ifobject):
        doafteriflabel = ifobject.getfuncdata()
        self.createcode("NOP", "", "end do_afterif()", name=doafteriflabel)

    def do_whileexpression(self):
        namespace = self.blocks.getactivefunctionname()
        dowhileexprlabel = "%s_while_%s" % (namespace, ''.join(random.choice(string.ascii_lowercase) for i in range(4)))
        self.createcode("NOP","","do_whileexpression",name=dowhileexprlabel)
        return dowhileexprlabel

    def do_afterwhile(self, whileobject):
        namespace = self.blocks.getactivefunctionname()
        doafterwhileblocklabel = "%s_%s_%s" % (whileobject.getname(), namespace, ''.join(random.choice(string.ascii_lowercase) for i in range(4)))
        doafterwhilelabel = "%s_%s_%s" % (whileobject.getname(), namespace, ''.join(random.choice(string.ascii_lowercase) for i in range(4)))
        whileobject.setscratch(doafterwhilelabel)
        self.createcode("NOP", "", "start do_afterwhile()  ")
        self.createcode("LDA", "_unireg0_0", "load result from while from unireg0")
        self.createcode("BNE", doafterwhileblocklabel)
        self.createcode("JMP", doafterwhilelabel)
        self.createcode("NOP", "","do_afterwhileblocklabel",  name=doafterwhileblocklabel)
        
    def end_afterwhile(self, whileobject):
        namespace = self.blocks.getactivefunctionname()
        dowhileexprlabel = whileobject.getfuncdata()
        doafterwhilelabel = whileobject.getscratch()
        self.createcode("JMP",dowhileexprlabel, "end do_afterwhile()")
        self.createcode("NOP","","end_afterwhile",name=doafterwhilelabel)

    def close(self):
        print("Codeemitter Close")

    def __del__(self):
        self.close()



