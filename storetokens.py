class objects:
    oname = ""
    otype = ""
    ovalue = ""
    oaddr = 0
    precedence = 0
    oattributes = []
    obuildin = False

    def __init__(self, objectname, objecttype):
        self.oname = objectname
        self.otype = objecttype
        self.funcdata = None
        self.namespace = "global"
        self.ovalue = ""
        self.oattributes = []
        self.obuildin = False
        self.osize = -1
        self.oaddr = 0
        self.scratch = ""
        self.temppointer = False

    def setprecedence(self, pres):
        self.precedence = pres

    def getprecedence(self):
        return self.precedence

    def settemppointer(self):
        self.temppointer = True

    def cleartemppointer(self):
        retval = self.temppointer
        self.temppointer = False
        return retval

    def getscratch(self):
        return self.scratch

    def setscratch(self, scratchdata):
        self.scratch = scratchdata

    def getnamespace(self):
        return self.namespace

    def setnamespace(self, namespace):
        self.namespace = namespace

    def getsize(self):
        return self.osize

    def setsize(self, size):
        self.osize = size

    def getfuncdata(self):
        return self.funcdata

    def setfuncdata(self, obj):
        self.funcdata = obj

    def getname(self):
        return self.oname

    def getvarname(self):
        return self.oname

    def getnamewithnamespace(self):
        if self.oname[0] == '_':
            result = self.namespace + self.oname
        else:
            result = self.namespace + '_' + self.oname
        return result
    
    def getnamespacename(self):
        return self.getnamewithnamespace()

    def gettype(self):
        return self.otype

    def getvalue(self):
        return self.ovalue

    def setaddress(self, addr):
        self.oaddr = addr

    def getaddress(self):
        return self.oaddr

    def getattributstring(self):
        attr = ""
        for a in self.oattributes:
            attr += a + ','
        attr = attr[:-1]
        return attr

    def getattributes(self):
        return self.oattributes

    def getattributehash(self):
        rethash =  dict([[t,True] for t in self.oattributes])
        return rethash

    def buildin(self):
        return self.obuildin
    
    def setbuildin(self, buildin):
        self.obuildin = buildin

    def setvalue(self, value):
        self.ovalue = value

    def addattribute(self, attribute):
        self.oattributes.append(attribute)

    def addattributes(self, attrs):
        for a in attrs:
            self.oattributes.append(a)

    def getinfo(self):
        return "Value:%20s, Name:'%20s', adr:$%4x Attribs:%s" % (self.otype, self.oname, self.getaddress(), self.getattributstring())

class storetokens:
    vartokens = []

    def __init__(self):
        self.namespace = "global"
        self.addtype("byte", "type_byte", True, 1)
        self.addtype("char", "type_char", True, 1)
        self.addtype("int", "type_integer", True, 2)
        self.addtype("short", "type_short", True, 2)
        self.addtype("long", "type_long", True, 4)
        self.addtype("longlong", "type_longlong", True, 8)
        self.addtype("superlong", "type_superlong", True, 16)
        self.addtype("wozfloat", "type_wozfloat", True, 4)
        self.addtype("kimfloat", "type_kimfloat", True, 18)
        self.addtype("float", "type_float", True, 4)
        self.addtype("double", "type_double", True, 8)
        self.addtype("string", "type_charpointer", True, 2)
        self.addb("chararray", "type_chararray", True)
        self.addb("signed", "signed_modifier", True)
        self.addb("unsigned", "unsigned_modifier", True)
        self.addb("auto", "type_auto", True)
        self.addb("break", "statement_break", True)
        self.addb("const", "constant", True)
        self.addb("case", "statement_break", True)
        self.addb("continue", "statement_continue", True)
        self.addb("default", "statement_default", True)
        self.addb("do", "statement_do", True)
        self.addb("register", "type_register", True)
        self.addb("return", "statement_return", True)
        self.addb("static", "statement_static", True)
        self.addb("struct", "statement_struct", True)
        self.addb("switch", "statement_switch", True)
        self.addb("type", "type_type", True)
        self.addb("typedef", "type_typedef", True)
        self.addb("union", "type_union", True)
        self.addb("void", "type_void", True)
        self.addb("volatile", "type_volatile", True)
        self.addb("while", "statement_while", True)
        self.addb("if", "statement_if", True)
        self.addb("else", "statement_else", True)
        self.addb("enum", "type_enum", True)
        self.addb("extern", "statement_extern", True)
        self.addb("for", "statement_for", True)
        self.addb("goto", "statement_goto", True)
        self.addtype("pointer", "type_pointer", True, 2)
        self.addtype("ADDRESSPTR", "type_varpointer", True, 2)
        self.addtype("pointerpointer", "type_pointerpointer", True, 2)
        self.addmne("_LABEL")
        self.addmne("_LEABYNAME")
        self.addmne("_ADC")
        self.addmne("_ASL")
        self.addmne("_BCC")
        self.addmne("_AND")
        self.addmne("_BCC")
        self.addmne("_BCS")
        self.addmne("_BEQ")
        self.addmne("_BIT")
        self.addmne("_BMI")
        self.addmne("_BNE")
        self.addmne("_BPL")
        self.addmne("_BRK")
        self.addmne("_BVC")
        self.addmne("_BVS")
        self.addmne("_CLC")
        self.addmne("_CLD")
        self.addmne("_CLI")
        self.addmne("_CLV")
        self.addmne("_CMP")
        self.addmne("_CPX")
        self.addmne("_CPY")
        self.addmne("_DEC")
        self.addmne("_DEX")
        self.addmne("_DEY")
        self.addmne("_EOR")
        self.addmne("_INC")
        self.addmne("_INX")
        self.addmne("_INY")
        self.addmne("_JMP")
        self.addmne("_JSR")
        self.addmne("_LDA")
        self.addmne("_LDX")
        self.addmne("_LDY")
        self.addmne("_LSR")
        self.addmne("_NOP")
        self.addmne("_ORA")
        self.addmne("_PHA")
        self.addmne("_PHP")
        self.addmne("_PLA")
        self.addmne("_PLP")
        self.addmne("_ROL")
        self.addmne("_ROR")
        self.addmne("_RTI")
        self.addmne("_RTS")
        self.addmne("_SBC")
        self.addmne("_SEC")
        self.addmne("_SED")
        self.addmne("_SEI")
        self.addmne("_STA")
        self.addmne("_STX")
        self.addmne("_STY")
        self.addmne("_TAX")
        self.addmne("_TAY")
        self.addmne("_TSX")
        self.addmne("_TXA")
        self.addmne("_TXS")
        self.addmne("_TYA")
        # additonal 65c02 opcodes
        self.addmne("_STZ")   # store zero
        self.addmne("_PHX")   # push X
        self.addmne("_PHY")   # push Y
        self.addmne("_PLX")   # pop X
        self.addmne("_PLY")   # pop Y
        self.addmne("_BRA")   # unconditional branch

    def setnamespace(self, namespace):
        self.namespace = namespace

    def addmne(self, mnemonic):
        obj = objects(mnemonic, "mnemonic")
        obj.setbuildin(True)
        obj.addattribute("mnemonic")
        self.vartokens.append(obj)

    def add(self, name, externtype):
        obj = objects(name, externtype)
        self.vartokens[name] = obj

    def addb(self, buildinname, buildintype, bulidin):
        obj = objects(buildinname, buildintype)
        obj.setbuildin(bulidin)
        self.vartokens.append(obj)

    def addtype(self, buildinname, buildintype, bulidin, size):
        obj = objects(buildinname, buildintype)
        obj.setbuildin(bulidin)
        obj.setsize(size)
        self.vartokens.append(obj)

    def addblock(self, name, namespace):
        obj = objects(name, "block")
        obj.setbuildin(False)
        obj.setsize(0)
        obj.setnamespace(namespace)
        self.vartokens.append(obj)

    def addwithattributes(self, newname, newtype, attrib):
        vartype = self.get(newtype)
        obj = objects(newname, newtype)
        obj.setbuildin(False)
        varpointer = False
        for a in attrib:
            if a == "type_varpointer":
                varpointer = True
        if varpointer:
            obj.setsize(2)
        elif vartype != None:
            varsize = vartype.getsize()
            obj.setsize(varsize)
        for a in attrib:
            obj.addattribute(a)
        self.vartokens.append(obj)
        return obj

    def getwithnamespace(self, stokenname, namespace):
        retlist = list()
        for r in self.vartokens:
            if r.oname == stokenname:
                retlist.append(r)
        if len(retlist) == 0:
            return None
        if len(retlist) == 1:
            found = retlist[0]
            if found.getnamespace() != namespace:
                return None
            return retlist[0]
        detailedlist = list()
        for r in retlist:
            if namespace == r.namespace:
                detailedlist.append(r)
        if len(detailedlist) == 1:
            return detailedlist[0]
        return None

    def get(self, stokenname):
        retlist = list()
        for r in self.vartokens:
            if r.oname == stokenname:
                retlist.append(r)
        if len(retlist) == 0:
            return None
        if len(retlist) == 1:
            return retlist[0]
        detailedlist = list()
        for r in retlist:
            if self.namespace == r.namespace:
                detailedlist.append(r)
        if len(detailedlist) == 1:
            return detailedlist[0]
        return None

    def olgget(self, stokenname):
        return self.get(stokenname)

    def detailtype(self, tokentype, tokenvalue):
        x = self.get(tokenvalue)
        if x == None:
            return tokentype
        else:
            return x.gettype()

    def getinfoontoken(self, token):
        o = self.get(token)
        return "Value:%20s, Name:'%20s', Attribs:%s" % (o.otype, o.oname, o.getattributstring())

    def listall(self, buildin=False):
        for o in self.vartokens:
            if o.obuildin == buildin:
                print("Value:%20s, Name:'%20s', Attribs:%s" % (o.otype, o.oname, o.getattributstring()))
            if o.obuildin != buildin:
                print("Value:%20s, Name:'%20s', Space:%20s, Addr:%04x: Attribs:%s" % (o.otype, o.oname, o.namespace, o.oaddr, o.getattributstring()))

            