from storetokens import storetokens, objects
from codeemitter import codeemitter, funcdef
from cclogger import cclogger
from expressions import expressions
from initasm import initasm
from blockstack import handleblocks
import ast
import sys

class token:
    index = -1
    filename = ""
    linenumber = 0
    tokentype = ""
    tokenvalue = ""

    def __init__(self, idx):
        self.index = idx

    def setindex(self,idx):
        self.index = idx
    
    def printtoken(self):
        print("%5d: %10s: %15s: %20s" % (self.index, self.filename, self.tokenvalue, self.tokentype))


    def isalpha(self):
        return self.tokentype == "alpha"
    
    def isnumber(self):
        return self.tokentype == "number"

    def ishexnumber(self):
        return self.tokentype == "hexnumber"

    def setfilename(self,filename):
        self.filename = filename

    def setlinenumber(self, linenumber):
        self.linenumber = linenumber
    
    def settype(self,tokentype):
        self.tokentype = tokentype

    def setvalue(self,tokenvalue):
        self.tokenvalue = tokenvalue
    
    def getindex(self):
        return self.index
    
    def getfilename(self):
        return self.filename

    def getlinenumber(self):
        return self.linenumber
    
    def gettype(self):
        return self.tokentype
    
    def getvalue(self):
        return self.tokenvalue

    def __del__(self):
        return
        print("token close:", end="")
        self.printtoken()

class dotoken:
    tokenlist = list()
    filename = "unset"
    index = 0
    eof = False
    t_type = "none"
    t_value = "none"
    unsigned_modifier = False
    signed_modifier = False


    def __init__(self, debugflag=False):
        self.stokens = storetokens()
        self.log = cclogger("dotoken.log")
        self.blocks = handleblocks(self.stokens)
        self.code = codeemitter("aout.s", self.stokens, self.blocks, self.log)
        self.expressions = expressions(self.log, self.stokens, self.code)
        self.debug = debugflag
        self.const_modifiers = [ "unsigned_modifier", "signed_modifier", "type_float", "type_double"]
        self.typedef_modifiers = [  "type_char", "type_integer", "type_float",
                                    "type_double", "unsigned_modifier", "signed_modifier"]
        self.int_types = [ "type_integer", "type_byte", "type_long", "type_longlong", "type_userint", "type_varpointer" ]
        self.type_buildins = [  "type_integer", "type_float", "type_wozfloat", "type_kimfloat", "type_char", "type_double", "type_void", "type_long", "type_longlong",
                                "type_byte", "type_register", "type_auto", "type_short", "type_typedef", "type_type",
                                "type_uniion", "type_volatile", "type_enum", "type_pointer", "type_varpointer", "type_pointerpointer"]
        #self.int_modifiers = [ "unsigned_modifier", "signed_modifier", "type_pointer", "type_pointerpointer" ]
        self.int_modifiers = [ "unsigned_modifier", "signed_modifier" ]
        if self.debug:
            self.log.writelog("dotoken/init", "%30s, do token init:" % (self.func_name()))

    def getstokens(self):
        return self.stokens

    def func_name(self):
        classname = __class__.__name__
        funcname = sys._getframe(1).f_code.co_name
        return classname + '.' + funcname

    def isbuildin_old(self, alpha):
        if alpha == "int":
            return True

    def debugout(self, out):
        self.log.writelog("dotoken/debugout", "%s" % out)

    def setfilename(self, filename):
        self.filename = filename

    def listtokens(self):
        self.log.writelog("dotoken/listtoken:", "%5s: %30s: %20s: %20s: %6s" % ("index", "Filename", "Token Type", "Token Value:", "Addr:"))
        for t in self.tokenlist:
            index = t.getindex()
            filename = t.getfilename()
            tokentype = t.gettype()
            tokenvalue = t.getvalue()
            attribs = t.getattributstring()
            addr = t.getaddress()
            if attribs.find("vardefinition") > -1:
                self.log.writelog("dotoken/listtoken:", "%5d: %30s: %20s: %20s: %04x: %s" % (index, filename, tokentype, tokenvalue, addr, attribs))
            else:
                self.log.writelog("dotoken/listtoken:", "%5d: %30s: %20s: %20s: %s" % (index, filename, tokentype, tokenvalue, attribs))

    def addtoken(self, tokenvalue, tokentype, linenumber):
        newtoken = token(self.index)
        newtoken.setfilename(self.filename)
        detailed = self.stokens.detailtype(tokentype, tokenvalue)
        newtoken.settype(detailed)
        # newtoken.settype(tokentype)
        newtoken.setvalue(tokenvalue)
        newtoken.setlinenumber(linenumber)
        self.tokenlist.append(newtoken)
        self.index += 1
    
    def nexttoken(self):
        if self.index >= len(self.tokenlist):
            self.eof = True
            return
        self.t = self.tokenlist[self.index]
        self.t_type = self.t.gettype()
        self.t_value = self.t.getvalue()
        self.t_isalpha = self.t.isalpha()
        self.t_isnumber = self.t.isnumber()
        self.t_ishexnumber = self.t.ishexnumber()
        self.t_linenumber = self.t.getlinenumber()
        self.log.writelog("nexttoken", "token is:%20s, value:%s" % (self.t_type, self.t_value))
        self.index += 1
        if self.t_type == "semicolon":
            self.stmtstartpos = self.index

    def gettokentypeatnext(self):
        # index points to the next token
        return self.tokenlist[self.index].gettype()


    def listall(self):
        self.stokens.listall(buildin=-1)

    def listalluserdefined(self):
        self.stokens.listall(buildin=0)

    def undostmt(self):
        self.index = self.stmtstartpos

    def isinlist(self, value, values):
        found = False
        for v in values:
            if v == value:
                return True
        return False

    def do_modifier(self):
        attributes = []
        while self.isinlist(self.t_type, self.int_modifiers):
        # while self.isinlist(self.t_type, self.int_types):
            attributes.append(self.t_type)
            self.nexttoken()
        return attributes
    
    def do_expression(self, foundtoken): # selects type of function or expression
        foundtokennamespace = foundtoken.getnamewithnamespace()
        foundtokenname = foundtoken.getname()
        if foundtokenname == "println":
            xxxx = 1
        # foundtoken is the left hand side of the expression, attrib "type_varpointer" means: *var = ...
        leftsidetoken = None # foundtoken
        pointeraccess = False
        self.nexttoken()
        if self.t_type == "nextalphaispointer":
            pointeraccess = True
            self.nexttoken()
        if self.t_type == "ampersand":
            pointeraccess = True
            self.nexttoken()
        if self.t_type == "number" or self.t_type == "openbracket":
            var_type = self.t_type
            var_value = self.t_value
            # namespace = self.code.getactivefunctionname()
            self.nexttoken()
            if self.t_type == "semicolon":
                self.log.writelog("dotoken/do_expression constantvalue", "Type:%s, Value:%s" % (var_type, var_value))
                self.code.assignvaluetovariable(foundtoken, var_type, var_value)
            else:
                self.log.writelog("dotoken/do_expression do_expression const first", "Type:%s, Value:%s" % (var_type, var_value))
                destinationname = foundtoken.getname()
                namespace = self.blocks.getactivefunctionname()
                self.expressions.add(pointeraccess, namespace, var_type, var_value)
                while self.t_type != "semicolon" and self.t_type != "startblock":
                    self.expressions.add(pointeraccess, namespace, self.t_type, self.t_value)
                    self.nexttoken()
                self.expressions.listall()
                self.expressions.generate(foundtoken, self.t_linenumber)
        elif self.t_type == "alpha" or self.t_type == "pointer":
            namespace = self.blocks.getactivefunctionname()
            if self.t_type == "pointer":
                self.nexttoken()
                var_type = self.t_type
                var_value = self.t_value
                pointeraccess = True
            if self.t_type == "openbracket":
                var_type = self.t_type
                var_value = self.t_value
                #stoken = self.stokens.addwithattributes(called_name, called_type, attributes)
            leftsidetoken = foundtoken
            self.log.writelog("dotoken/do_expression","t_type:%s,  t_value:%s" % (self.t_type, self.t_value))
            if self.t_value == namespace:  # if namespace == tokenname --> functiondefinition of this function --> global
                foundtoken = self.stokens.getwithnamespace(self.t_value, "global")
                if foundtoken != None:
                    if self.isinlist("funcdefinition", foundtoken.getattributes()):
                        print("function %s found" % self.t_value)
            else:
                foundtoken = self.stokens.getwithnamespace(self.t_value, namespace)
                if foundtoken == None:
                    foundtoken = self.stokens.getwithnamespace(self.t_value, "global")
                    if foundtoken == None:
                        foundtoken = self.stokens.getwithnamespace(self.t_value, "_INTERNAL")
            if foundtoken == None:
                self.stokens.listall()
                print("identifier: %s not found in namespace '%s', 'global' and '_INTERNAL', terminating in line number %d" % (self.t_value, namespace, self.t_linenumber))
                sys.exit(1)
            self.log.writelog("dotoken/do_expression do_expression id first", "Type:%s, Value:%s" % (self.t_type, self.t_value))
            destinationname = foundtoken.getname()
            destinationattrs = foundtoken.getattributes()
            namespace = self.blocks.getactivefunctionname()
            if self.isinlist("funcdefinition", destinationattrs) and self.do_functioncall(foundtoken, False): # should now fall in to expression.py
                returntoken = self.stokens.get("_unireg0")
                self.code.copyvar(leftsidetoken, returntoken, ptr_a_dest=False, ptr_a_source=False, lineno=self.t_linenumber)
            elif self.isinlist("internalfunc", destinationattrs) and self.do_functioncall(foundtoken, False):
                returntoken = self.stokens.get("_unireg0")
                self.code.copyvar(leftsidetoken, returntoken, ptr_a_dest=False, ptr_a_source=False, lineno=self.t_linenumber)
            else:
                self.expressions.add(pointeraccess, namespace, self.t_type, self.t_value)
                self.nexttoken()
                while self.t_type != "semicolon":
                    self.expressions.add(pointeraccess, namespace, self.t_type, self.t_value)
                    self.nexttoken()
                    if self.t_type == "nextalphaispointer":
                        self.nexttoken()
                        var_type = self.t_type
                        var_value = self.t_value
                        pointeraccess = True
                self.expressions.listall()
                self.expressions.generate(leftsidetoken, self.t_linenumber)

    def do_returnstatement(self, ttype, tvalue):
        if ttype == "statement_return":
            unireg0 = self.stokens.get("_unireg0")
            self.do_expression(unireg0)
            self.code.exitfromfunction()

    def do_constant(self):
        attributes = []
        constantname = ""
        self.nexttoken()
        while True:
            if self.isinlist(self.t_type, self.int_modifiers):
                attributes.append(self.t_type)
                self.nexttoken()
            if self.isinlist(self.t_type, self.int_types):
                self.nexttoken()
                if self.t_type == "alpha":
                    constantname = self.t_value
                    self.nexttoken()
                    if self.t_type == "equals":
                        self.nexttoken()
                        if self.t_type == "number":
                            constantvalue = self.t_value
                            if constantvalue.find('.') >= 0:
                                newconsttype = "floatvalue"
                                newconstsizeof = "long_size"  # if value is float
                                if constantvalue.find('d') >= 0:
                                    newconsttype = "doublevalue"
                                    newconstsizeof = "longlong_size" # if value is double, signed with a 'd' at the end
                            else:
                                newconsttype = "intvalue"
                                if int(constantvalue) < 256:
                                    newconstsizeof = "byte_size"
                                elif int(constantvalue) < 65535:
                                    newconstsizeof = "word_size"
                                elif int(constantvalue) < 4294967296:
                                    newconstsizeof = "long_size"
                                elif int(constantvalue) < 18446744073709551616:
                                    newconstsizeof = "longlong_size"
                            attributes.append("constvalue")
                            attributes.append(newconsttype)
                            attributes.append(newconstsizeof)
                            objattr = attributes
                            self.stokens.addwithattributes(constantname, constantvalue, objattr)
                            self.code.constintstatement(constantname, constantvalue, objattr)
                            attributes = []
                            self.nexttoken()
                            if self.t_type == "comma":
                                self.nexttoken()
                            elif self.t_type == "semicolon":
                                break
            elif self.t_type == "type_float" or self.t_type == "type_double" or self.t_type == "type_char":
                self.nexttoken()
                if self.t_type == "alpha":
                    constantname = self.t_value
                    self.nexttoken()
                    if self.t_type == "equals":
                        self.nexttoken()
                        if self.t_type == "number" or self.t_type == "type_stringconst":
                            constantvalue = self.t_value
                            attributes.append(self.t_type)
                            if self.t_type == "number":
                                newtoken = self.stokens.addwithattributes(constantname, self.t_type, attributes)
                                newtoken.setvalue(constantvalue)
                                newtoken.setnamespace(self.blocks.getactivefunctionname())
                                newtoken.setsize(len(constantvalue))
                                self.code.constfloatstatement(constantname, constantvalue, attributes)
                            if self.t_type == "type_stringconst":
                                newtoken = self.stokens.addwithattributes(constantname, self.t_type, attributes)
                                newtoken.setvalue(constantvalue)
                                newtoken.setnamespace(self.blocks.getactivefunctionname())
                                newtoken.setsize(len(constantvalue))
                                self.code.constcharstatement(constantname, constantvalue, attributes)
                            self.nexttoken()
                            if self.t_type == "comma":
                                self.nexttoken()
                            elif self.t_type == "semicolon":
                                break
            elif self.t_type == "type_charpointer":
                value = self.t_value
                if value == "string":
                    self.nexttoken()
                    stringname = self.t_value
                    self.nexttoken()
                    if self.t_type == "equals":
                        self.nexttoken()
                        thestring = self.t_value
                        self.nexttoken()
                        if self.t_type == "semicolon":
                            self.stokens.addwithattributes(stringname, thestring, attributes)
                            self.code.constcharstatement(stringname, thestring, attributes)
                            break
                        else:
                            self.log.writelog("dotoken/do_constant", "Error in string Constant")
                            self.log.writelog("dotoken/do_constant","Line number: %d" % self.t_linenumber)
                            sys.exit()

                    
            else:
                self.log.writelog("dotoken/do_constant","Error in const Definition: %s, %s" % (self.t_type, self.t_value))
                self.log.writelog("dotoken/do_constant","Line number: %d" % self.t_linenumber)
                sys.exit(1)
        
    def do_varfuncs(self, attrib, isinargs):
        attributes = attrib
        isinarguments = isinargs
        pointer_flag = []
        self.log.writelog("dotoken/do_varfuncs","varfuncs:%s" % self.t_type)
        called_attributes = attributes
        called_type = self.t_value
        if self.t_linenumber == 53:
            xxx = 0
        if self.isinlist(self.t_type, self.type_buildins):
            attributes.append(self.t_type)
            self.nexttoken()
        if self.t_type == "nextalphaispointer":
            attributes.append("type_varpointer")
            self.nexttoken()
        if self.isinlist(self.t_type, self.int_modifiers):
            attributes.append(self.t_type)
            self.nexttoken()
        if self.t_type == "alpha":
            called_name = self.t_value
            self.log.writelog("dotoken/do_varfunc", "do_varfuncs: %s, value: %s" % (called_type, called_name))
            self.nexttoken()
            if self.t_type == "openbracket":
                # start function definition after "funcname("
                attributes.append("funcdefinition")
                isinarguments = True
                self.log.writelog ("dotoken/do_func", "do_funcs openbracket: %s, oldvalue: %s" % (called_type, called_name))
                stoken = self.stokens.addwithattributes(called_name, called_type, attributes)
                nspace = self.blocks.getactivefunctionname()
                stoken.setnamespace(nspace)
                funcobj = funcdef(called_name, called_type, stoken)
                stoken.setfuncdata(funcobj)
                blockobject = self.blocks.beginblock("function", funcobj)
                self.code.startfunctionarguments(stoken, called_type, called_name, attributes)
                self.log.writelog("dotoken/do_func", "name:%s, type:%s" % (called_name, called_type))
                self.nexttoken()
                attributes = self.do_modifier()
                self.do_varfuncs(attributes, self.code.isnotglobalfunc())
                self.log.writelog("dotoken/do_func", "do_func terminated func:%s" % self.t_type)
            else:
                if isinarguments:
                    # continue function definition inside parameter until ")" is reached
                    self.log.writelog ("1 dotoken/do_funcarg", "do_var: %s, value: %s" % (called_type, called_name))
                    while 1:
                        self.log.writelog ("2 dotoken/do_funcarg", "do_var: %s, value: %s" % (self.t_type, self.t_value))
                        if self.t_type == "comma":
                            self.log.writelog ("3 dotoken/do_funcarg", "do_var_comma: %s, value: %s" % (self.t_type, self.t_value))
                            thisfunction = self.blocks.getlastfunkstack()
                            thisfunction.addvar(self.blocks.getactivefunctionname(), called_name, called_type, self.blocks.getactivefunctionname())
                            stoken = self.stokens.addwithattributes(called_name, called_type, attributes)
                            stoken.addattribute("isargument")
                            stoken.setnamespace(self.blocks.getactivefunctionname())
                            self.code.varstatement(stoken, called_type, called_name, self.code.isnotglobalfunc())
                            self.log.writelog("4 dotoken/do_funcarg", "None")
                            self.nexttoken()
                            attributes = self.do_modifier()
                            self.log.writelog("5a dotoken/do_funcarg", "after comma: %s, value: %s" % (self.t_type, self.t_value))
                            called_type = self.t_value
                            called_name = self.t_value
                            if self.isinlist(self.t_type, self.type_buildins):
                                attributes.append(self.t_type)
                            self.nexttoken()
                            if self.t_type == "alpha":
                                called_name = self.t_value
                            self.log.writelog ("5b dotoken/do_funcarg", "do_var: %s, value: %s" % (called_type, called_name))
                        elif self.t_type == "closebracket":
                            thisfunction = self.blocks.getlastfunkstack()
                            thisfunction.addvar(self.blocks.getactivefunctionname(), called_name, called_type, self.blocks.getactivefunctionname())
                            stoken = self.stokens.addwithattributes(called_name, called_type, attributes)
                            stoken.addattribute("isargument")
                            stoken.setnamespace(self.blocks.getactivefunctionname())
                            self.code.varstatement(stoken, called_type, called_name, self.code.isnotglobalfunc())
                            self.log.writelog("6 dotoken/do_funcarg", "NOne")
                            if self.t_type == "closebracket":
                                self.code.stopfunctionarguments(self.t_type, self.t_value, attributes, self.code.isnotglobalfunc())
                                self.log.writelog("7 dotoken/do_funcarg", "none")
                            break
                        elif self.t_type == "star":
                            pointer_flag = ['type_pointer']
                        elif self.t_type == "pointer":
                            pointer_flag = ['type_pointerpointer']
                        elif self.t_type == "alpha":
                            called_name = self.t_value
                        self.nexttoken()
                else:
                    # ----------------- do var definition -----------------
                    self.log.writelog ("10 dotoken/do_var", "do_var: %s, value: %s" % (called_type, called_name))
                    attributes.append("vardefinition")
                    while 1:
                        if self.isinlist(self.t_type, self.int_modifiers):
                            attributes.append(self.t_type)
                            self.nexttoken()
                        self.log.writelog ("11 dotoken/do_var", "do_var: %s, value: %s" % (self.t_type, self.t_value))
                        if self.t_type == "comma":
                            self.log.writelog ("12 dotoken/do_var", "do_var_comma: %s, value: %s" % (self.t_type, self.t_value))
                            stoken = self.stokens.addwithattributes(called_name, called_type, attributes)
                            stoken.setnamespace(self.blocks.getactivefunctionname())
                            self.code.varstatement(stoken, called_type, called_name, self.code.isnotglobalfunc())
                            self.log.writelog("13 dotoken/do_var","None")
                        elif self.t_type == "semicolon" or self.t_type == "closebracket":
                            stoken = self.stokens.getwithnamespace(called_name, self.blocks.getactivefunctionname())
                            if stoken == None:
                                stoken = self.stokens.addwithattributes(called_name, called_type, attributes)
                                stoken.setnamespace(self.blocks.getactivefunctionname())
                                self.code.varstatement(stoken, called_type, called_name, self.code.isnotglobalfunc())
                            if self.t_type == "closebracket":
                                self.code.stopfunctionarguments(self.t_type, self.t_value, attributes, self.code.isnotglobalfunc())
                            break
                        elif self.t_type == "type_pointer":
                            pointer_flag = ['type_pointer']
                        elif self.t_type == "nextalphaispointer":
                            pointer_flag = ['type_pointer']
                        elif self.t_type == "alpha":
                            called_name = self.t_value
                        elif self.t_type == "squareopen":
                            self.code.opensquarebracket(called_type, called_name, attributes)
                            self.nexttoken()
                            if self.t_type == "number":
                                if called_type == "char":
                                    attributes.append("type_chararray")
                                    stoken = self.stokens.addwithattributes(called_name, called_type, attributes)
                                    stoken.setnamespace(self.blocks.getactivefunctionname())
                                    stoken.setsize(int(self.t_value))
                                    self.code.varstatement(stoken, called_type, called_name, self.code.isnotglobalfunc())
                                    self.code.reservememory(stoken)
                            else:
                                self.log.writelog("dotoken/alloc_array", "Memory value not given as constant")
                                print("dotoken/alloc_array" + " Memory value not given as constant")
                                sys.exit(1)
                        elif self.t_type == "squareclose":
                            self.code.closesquarebracket(self.t_type, self.t_value, attributes)
                        self.nexttoken()

    def do_functioncall(self, foundtoken, doanyway):
        namespace = self.blocks.getactivefunctionname()
        functiontocall = foundtoken.getname()
        if functiontocall == "real":
            x = 0
        arglist = list()
        storedindex = self.index
        indexatbeginning = self.index # mark beginning for undo 
        var_found = ""
        self.nexttoken()
        token_type = self.t_type
        token_value = self.t_value
        index = 0
        registerindex = 0
        while token_type != "closebracket":
            if token_type == "comma":
                var_found += ","
            elif token_value == "openbracket":
                # mark beginning of expression in parameter
                storedindex = self.index
            else:
                var_found += token_value # only for debugging
                if token_type == "number":
                    numberobj = [ token_type, token_value ]
                    arglist.append(numberobj)
                elif token_type == "alpha":
                    tokenobj = self.stokens.getwithnamespace(token_value, namespace)
                    if tokenobj == None:
                        tokenobj = self.stokens.getwithnamespace(token_value, "global")
                        if tokenobj == None:
                            ln = self.t_linenumber
                            print("No var '%s' found for parameter in function call of: %s in line:%s" % (token_value,functiontocall,ln))
                            sys.exit(1)
                    arglist.append(tokenobj)
                elif token_type == "type_stringconst":
                    constantname = "%s_conststring_%d" % (namespace, index)
                    attributes = []
                    attributes.append(token_type)
                    newtoken = self.stokens.addwithattributes(constantname, token_type, attributes)
                    newtoken.setvalue(token_value)
                    newtoken.setnamespace(self.blocks.getactivefunctionname())
                    newtoken.setsize(len(token_value))
                    arglist.append(newtoken)
                else:
                    print("tokentype:%s and Value:%s does not match, doing expression for this section" % (token_type, token_value))
                    self.index = storedindex
                    self.nexttoken()
                    pointeraccess = False
                    destinationregister = "_unireg%d" % registerindex
                    destinationregister = self.stokens.getwithnamespace(destinationregister, "global")
                    while self.t_type != "colon" and self.t_type != "closebracket":
                        self.expressions.add(pointeraccess, namespace, self.t_type, self.t_value)
                        self.nexttoken()
                    self.expressions.listall()
                    self.expressions.generate(destinationregister, self.t_linenumber)
                    arglist = list()
                    arglist.append(destinationregister)
            if self.t_type != "closebracket":
                self.nexttoken()
            token_type = self.t_type
            token_value = self.t_value
            index += 1
        self.nexttoken()
        token_type = self.t_type
        token_value = self.t_value
        if doanyway or token_value == "semicolon":
            functionnamespace = foundtoken.getnamespace()
            functionname = foundtoken.getname()
            if functionnamespace == "_INTERNAL":
                if functionname == "adr" or functionname == "peek" or functionname == "poke":
                    self.code.intfunc_adr(foundtoken, arglist, line=self.t_linenumber)
                elif functionname == "_getstack6502":
                    self.code.intfunc_adr(foundtoken, arglist, line=self.t_linenumber)
                elif functionname == "gettimer" or functionname == "settimer":
                    self.code.intfunc_adr(foundtoken, arglist, line=self.t_linenumber)
                elif functionname == "strlen":
                    self.code.intfunc_strlen(foundtoken, arglist, line=self.t_linenumber)
                elif functionname == "strcpy" or functionname == "strcat":
                    self.code.intfunc_strcpy(foundtoken, arglist, line=self.t_linenumber)
                elif functionname == "sizeof" or functionname == "getch" or functionname == "avail":
                    self.code.intfunc_sizeof(foundtoken, arglist, line=self.t_linenumber)
                elif functionname == "print" or functionname == "println" \
                     or functionname == "printhex" or functionname == "printlnhex":
                    self.code.intfunc_print(foundtoken, arglist, line=self.t_linenumber)
                elif functionname == "and" or functionname == "or" or functionname == "shiftleft" or functionname == "shiftright":
                    self.code.intfunc_logical(foundtoken, arglist, line=self.t_linenumber)
                elif functionname == "rotateleft" or functionname == "rotateright":
                    self.code.intfunc_logical(foundtoken, arglist, line=self.t_linenumber)
                elif functionname == "real" or functionname == "integer" or functionname == "log" \
                            or functionname == "log10" or functionname == "exp":
                    self.code.intfunc_tofloat(foundtoken, arglist, line=self.t_linenumber)
                elif functionname == "lcdcommand" or functionname == "lcddata" or functionname == "lcdstring":
                    self.code.intfunc_lcd(foundtoken, arglist, line=self.t_linenumber)
                elif functionname == "kim_clrx" or functionname == "kim_clry" or functionname == "kim_clrz" \
                        or functionname == "kim_iprec" or functionname == "kim_ploadx" or functionname == "kim_ploady" \
                        or functionname == "kim_uploadx" or functionname == "kim_uploady" or functionname == "kim_dechex" \
                        or functionname == "kim_savxy" or functionname == "kim_rclxy" or functionname == "kim_ustres":
                    self.code.intfunc_kima(foundtoken, arglist, line=self.t_linenumber)
                else:
                    self.code.internalfunctioncall(foundtoken, arglist, line=self.t_linenumber)
            else:
                self.code.createfunctioncall(foundtoken, arglist, line=self.t_linenumber)
            return True
        else: # this is not a simple functioncall, we need the expression routine
            self.index = indexatbeginning - 1  # reset pointer to tokens
            self.nexttoken()
            return False

    def do_alphastatement(self, attributes):
        idname = self.t_value
        namespace = self.blocks.getactivefunctionname()
        if self.t_linenumber == 12:
            x=0
        # foundtoken = self.stokens.get(self.t_value)
        foundtoken = self.stokens.getwithnamespace(self.t_value, namespace)
        if foundtoken == None:
            foundtoken = self.stokens.getwithnamespace(self.t_value, "global")
            if foundtoken == None:
                foundtoken = self.stokens.getwithnamespace(self.t_value, "_INTERNAL")
                if foundtoken == None:
                    print("Line:%d Token %s in namespace '%s' and '%s' and 'internal' not found!" % (self.t_linenumber, idname, namespace, "global"))
                    sys.exit(1)
        self.log.writelog("dotoken/do_alphastatement", "t_type:%s, t_value:%s" % (self.t_type, self.t_value))
        if foundtoken == None:
            self.nexttoken()
            if self.t_type == "colon":
                called_name = idname
                called_type = "label"
                attributes = [ "label_definition" ]
                labeltoken = self.stokens.addwithattributes(called_name, called_type, attributes)
                self.code.startlabel(labeltoken, called_type, called_name)
                return
            else:
                if self.t_value == "equals":
                    self.log.writelog("dotoken/do_alphastatement", "t_type:%s, t_value:%s" % (idname, idname))
                    self.log.writelog("dotoken/do_alphastatement", "Identifier %s not found!" % idname)
                    print("identifier: %s not found, terminating in line number %d" % (idname, self.t_linenumber))
                print("Identifier '%s' not found: Terminating program" % idname)
                sys.exit(1)
        foundtoken.addattributes(attributes)
        tokinfo = foundtoken.getinfo()
        attribs = foundtoken.getattributes()
        self.log.writelog("dotoken/do_alphastatement", "tokinfo:%s" % tokinfo)
        if self.isinlist("vardefinition", attribs):
            self.log.writelog("dotoken/do_alphastatement/varassignment", tokinfo)
            self.nexttoken()
            if self.t_type == "equals":
                self.log.writelog("dotoken/do_alpha", "variable assignment / calculate expression")
                self.do_expression(foundtoken)
        elif self.isinlist("funcdefinition", attribs) or self.isinlist("internalfunc", attribs):
            self.log.writelog("dotoken/do_functioncall", "tokinfo:%s" % tokinfo)
            self.nexttoken()
            if self.t_type == "openbracket":
                self.log.writelog("dotoken/do_alpha", "function call")
                retval = self.do_functioncall(foundtoken, True)
        elif self.isinlist("mnemonic", attribs):
            self.log.writelog("dotoken/do_alpha/mnemonic", "t_type:%s, t_value:%s" % (self.t_type, self.t_value))
            self.nexttoken()

    def do_mnemonic(self):
        lastargument = ""
        mnemonic = self.t_value
        opcode = mnemonic[1:]
        arguments = ""
        self.nexttoken()
        if self.t_value == "number":
            xxxx = 0
        while self.t_type != "semicolon":
            if self.t_value == "comma":
                arguments += ','
            elif self.t_value == "hash":
                arguments += '#'
            elif self.t_value == "openbracket":
                arguments += '('
            elif self.t_value == "closebracket":
                arguments += ')'
            elif self.t_value == "dollarsign":
                arguments += '$'
            elif self.t_value == "percent":
                arguments += '%'
            elif self.t_type == "plussign":
                arguments += '+'
            elif self.t_type == "minussign":
                arguments += '-'
            elif self.t_type == "alpha":
                # bad coding, this will filter out special case were we want a character constant to the assembler
                if lastargument == "hash" and len(self.t_value) == 1:
                    arguments += "'%s'" % self.t_value
                else:
                    arguments += self.t_value
            else:
                arguments += self.t_value
            lastargument = self.t_value;
            self.nexttoken()
        self.log.writelog("do_mnemonic", "opcode: %s args:%s" % (opcode, arguments))
        self.code.insertinline(opcode, arguments, self.t_linenumber)

    def do_goto(self, t_type, t_value):
        if t_type == "statement_goto":
            self.nexttoken()
            labelname = self.t_value
            self.code.jumptolabel(t_type, labelname)
            self.nexttoken()
        return

    def do_if(self, t_type, t_value):
        if t_type == "statement_if":
            returntoken = self.stokens.get("_unireg0")
            self.do_expression(returntoken)
            returnvalue = returntoken.getvalue()
            if self.t_type == "startblock":
                startifblock = self.blocks.beginblock("if", None)
                self.code.do_afterif(startifblock)
        else:
            print("no if statement in line: %d" % self.t_linenumber)
            sys.exit(1)

    def do_endif(self, t_type, blockended, elsefollow=False, line=""):
        if t_type == "endblock":
            if elsefollow:
                self.code.do_afterelse(blockended)
            else:
                self.code.end_afterif(blockended)
            leavednamespace = self.blocks.popfunctionstack()

    def do_else(self, t_type, t_value, blockended):
        if t_type == "statement_else":
            self.nexttoken()
            t = self.t_type
            v = self.t_value
            if self.t_type == "startblock":
                funcdata1 = blockended.getfuncdata()
                funcdata2 = blockended.getfuncdata2()
                leavednamespace = self.blocks.popfunctionstack()
                startelseblock =self.blocks.beginblock("else", None)
                startelseblock.setfuncdata(funcdata1)
                startelseblock.setfuncdata2(funcdata2)
                self.code.do_afterelse(startelseblock)
            else:
                print("startblock in else missing, at line %d" % self.t_linenumber)
                sys.exit(1)
            
        else:
            print("else without if, terminating in line %d" % self.t_linenumber)
            sys.exit(1)

    def do_endelse(self, t_type, blockended, line=""):
        if t_type == "endblock":
            self.code.end_afterelse(blockended)
            leavednamespace = self.blocks.popfunctionstack()

    def do_while(self, t_type, t_value):
        if t_type == "statement_while":
            whilelabel = self.code.do_whileexpression()
            returntoken = self.stokens.get("_unireg0")
            self.do_expression(returntoken)
            returnvalue = returntoken.getvalue()
            if self.t_type == "startblock":
                startwhileblock = self.blocks.beginblock("while", None)
                startwhileblock.setfuncdata(whilelabel)
                self.code.do_afterwhile(startwhileblock)

    def do_for(self, t_type, t_value):
        if t_type == "statement_for____":

            pass
        else:
            print("error in for loop, in line:%d", self.t_linenumber)
            sys.exit(1)
        pass

    def do_endwhile(self, t_type, blockended, line=""):
        if t_type == "endblock":
            self.code.end_afterwhile(blockended)
            leavednamespace = self.blocks.popfunctionstack()

    def emit(self, varstart, programstart, stackstart, outfilepath):
        attributes = []
        self.code.openoutfilepath(outfilepath)
        # add global namespace
        called_type = "void"
        called_name = "global"
        self.log.writelog ("dotoken/emit", "add global namespace: %s, oldvalue: %s" % (called_type, called_name))
        attributes.append("funcdefinition")
        stoken = self.stokens.addwithattributes(called_name, called_type, attributes)
        stoken.setnamespace(self.blocks.getactivefunctionname())
        funcobj = funcdef(called_name, called_type, stoken)
        blockobject = self.blocks.beginblock("global", funcobj)
        # end add global namespace
        self.initasm = initasm(self.log, self.code, self.stokens, varstart, programstart, stackstart)
        # self.code.setvarstart(varstart) # already done at initasm  above
        self.index = 0
        self.nexttoken()
        while not self.eof:
            attributes = self.do_modifier()
            if self.t_type == "pointer" and self.t_value == "star":
                self.nexttoken()
                attributes.append("access_pointer")
            if self.t_type == "ampersand":
                self.nexttoken()
                attributes.append("return_the_address")
            if self.t_type == "constant":
                self.do_constant()
            elif self.isinlist(self.t_type, self.type_buildins):
                self.do_varfuncs(attributes, False)
            elif self.t_type == "alpha" or self.t_type == "starpreid":
                self.do_alphastatement(attributes)
            elif self.t_type == "startblock":
                al = self.code.startblock(self.t_type, self.t_value, [], line=self.t_linenumber)
            elif self.t_type == "endblock":
                blockended = self.blocks.getblockonstack()
                if blockended.getvalue() == "function":
                    al = self.code.endblock(self.t_type, self.t_value, [], line=self.t_linenumber)
                    leavednamespace = self.blocks.popfunctionstack()
                    print("leaved block:%s" % leavednamespace)
                elif blockended.getvalue() == "if":
                    # check for following else
                    if True:
                        checktype = self.gettokentypeatnext()
                        if checktype == "statement_else":
                            self.nexttoken()
                            self.do_endif(self.t_type, blockended, elsefollow=True, line=self.t_linenumber)
                            self.do_else(self.t_type, self.t_value, blockended)
                        else:
                            self.do_endif(self.t_type, blockended, line=self.t_linenumber)
                    else:
                        self.do_endif(self.t_type, blockended, line=self.t_linenumber)
                elif blockended.getvalue() == "else":
                    self.do_endelse(self.t_type, blockended, line=self.t_linenumber)
                    print("do_endelse called, else block is finished")
                elif blockended.getvalue() == "while":
                    self.do_endwhile(self.t_type, blockended, line=self.t_linenumber)
                else:
                    print("unmatched } found, terminating program")
                    sys.exit(1)
            elif self.t_type == "mnemonic":
                self.do_mnemonic()
            elif self.t_type == "statement_goto":
                self.do_goto(self.t_type, self.t_value)
            elif self.t_type == "statement_if":
                self.do_if(self.t_type, self.t_value)
            elif self.t_type == "statement_while":
                self.do_while(self.t_type, self.t_value)
#            elif self.t_type == "statement_for":
#                self.do_for(self.t_type, self.t_value)
            elif self.t_type == "statement_return":
                self.do_returnstatement(self.t_type, self.t_value)
            elif self.t_type == "semicolon":
                self.log.writelog("dotoken/emit", "unused semicolon")
            self.blocks.debugblockstack()
            self.nexttoken()
        self.code.handlesubroutines()
        self.code.createsubroutinetable()
        self.initasm.endasm()

    def close(self):
        print("dotoken close")