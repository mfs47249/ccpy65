from helpers import CompilerFault
from storetokens import storetokens, objects
from codeemitter import codeemitter
from cclogger import cclogger
from compilerexceptions import CompilerFault
from dataclasses import dataclass  # if python < 3.7
from typing import Optional, List
from operator import add, sub, mul, truediv
import sys


class anode:
    precedence = {
            "number" : 0,
            "openbracket" : 0,
            "closebracket" : 0,
            "comma" : 0,
            "plussign" : 5,
            "minussign" : 5,
            "star" : 6,
            "pointer" : 6,
            "slash" : 6,
            "percent" : 6,
            "shiftleft" : 4,
            "shiftright" : 4,
            "smaller" : 3,
            "smallerequal" : 3,
            "equalsmaller" : 3,
            "greaterequal" : 3,
            "equalgreater" : 3,
            "greater" : 3,
            "equalequal" : 2,
            "notequal" : 2,
            "equal" : 1,
            "float" : 0,
            "double" : 0,
            "wozfloat" : 0,
            "longlong" : 0,
            "long" : 0,
            "byte" :0,
            "int" : 0,
            "type_integer" : 0,
            "type_float" : 0,
            "type_pointer" : 0,
            "type_varpointer" : 0,
            "ADDRESSPTR" : 0,
            "char" : 0
        }

    def __init__(self, tok):
        self.token = tok
        self.left = None
        self.right = None
        self.name = ""
        if tok.gettype() == "number":
            self.name = str(tok.getname())
        self.prec = self.precedence[tok.gettype()]

    def isleaf(self):
        result = ((self.left is None) and (self.right is None))
        return result

    def addleft(self, tok):
        self.left = tok
    
    def addright(self, tok):
        self.right = tok

    def getleft(self):
        return self.left

    def getright(self):
        return self.right

    def addtoken(self, tok):
        self.token = tok

    def gettoken(self):
        return self.token
    
    def getcontentstr(self):
        if False:
            resultstring = "("
            if self.left != None:
                resultstring = self.left.gettoken().getname()
            resultstring += ")("
            if self.right != None:
                resultstring = self.right.gettoken().getname()
            resultstring += ")"
        else:
            resultstring = self.right.gettoken().getname()
            return resultstring

    def getprecedence(self):
        return self.prec

    def isnumber(self):
        return self.token.gettype() == "number"

    def isvar(self):
        attributes = self.token.getattributehash()
        try:
            if attributes['vardefinition']:
                return True
        except KeyError as e:
            return False
        return False

    def isargument(self):
        attributes = self.token.getattributehash()
        try:
            if attributes['isargument']:
                return True
        except KeyError as e:
            return False
        return False

    def checktype(self, tocheck):
        return self.token.gettype() == tocheck

    def getname(self):
        return self.token.getname()

    def isoperator(self):
        return (self.prec > 0)

    def isfunction(self):
        attributes = self.token.getattributehash()
        try:
            if attributes['funcdefinition']:
                return True
        except KeyError as e:
            return False
        return False

    def isfunction(self):
        attributes = self.token.getattributehash()
        try:
            if attributes['funcdefinition']:
                return True
        except KeyError as e:
            return False
        return False

    def isinternalfunc(self):
        attributes = self.token.getattributehash()
        try:
            if attributes['internalfunc']:
                return True
        except KeyError as e:
            return False
        return False



class expressions:
    def __init__(self, logger, stokens, code):
        self.log = logger
        self.stokens = stokens
        self.code = code
        self.orderdtoken = []
        self.tokenlist = []
        self.tokenstack = []
        self.evaluatedepth = 0
        self.evaluatedeepthcount = 0
        self.evalstacksize = 8 # for long value
        self.options = None
        self.optionkeys = dict()

    def add(self, pointeraccess, namespace, ttype, tvalue):
        print("expressions/add: Namespace:%s, TType:%s, Value:%s" % (namespace, ttype, tvalue))
        if tvalue == "toreal":
            xxxx = 0
        if ttype == "alpha":
            stok = self.stokens.getwithnamespace(tvalue, namespace)
            if stok == None:
                stok = self.stokens.getwithnamespace(tvalue, "global")
                if stok == None:
                    stok = self.stokens.getwithnamespace(tvalue, "_INTERNAL")
                    if stok != None:
                        if pointeraccess:
                            stok.settemppointer()
                        namewithnamespace = stok.getnamewithnamespace()
                        self.optionkeys[namewithnamespace] = stok
                        self.tokenlist.append(stok)
                    else:
                        print("Object:%s not found for namespace:%s and global and _INTERNAL, line:%d" % (tvalue, namespace, self.linenumber))
                        sys.exit(1)
                else:
                    if pointeraccess:
                        stok.settemppointer()
                    namewithnamespace = stok.getnamewithnamespace()
                    self.optionkeys[namewithnamespace] = stok
                    self.tokenlist.append(stok)
            else:
                if pointeraccess:
                    stok.settemppointer()
                namewithnamespace = stok.getnamewithnamespace()
                self.optionkeys[namewithnamespace] = stok
                self.tokenlist.append(stok)
        else:
            stok = objects(tvalue, ttype)
            stok.setprecedence(anode.precedence[ttype])
            stok.setvalue(tvalue)
            self.tokenlist.append(stok)
        return

    def listall(self):
        self.log.writelog("expressions/listall", "values:%s" % self.orderdtoken)

    def printtokenlist(self):
        index = 0
        for x in self.tokenlist:
            print("Ptraccess:%s, Info:%s" % (self.tokenptracc[index], x.getinfo()))
            index += 1

    def printnode(self, node, printtype=True):
        result = ""
        if node.isleaf():
            if printtype:
                result = "{%s|%s}" % (node.gettoken().gettype(), node.gettoken().getname())
            else:
                result = "%s " % node.gettoken().getname()
            return result
        if node.getleft() != None:
            result += self.printnode(node.getleft())
        if node.getright() != None:
            result += self.printnode(node.getright())
        return result

    def printstack(self, name, stackobj, printtype=True):
        stack_string = ""
        for s in stackobj:
            stack_string += self.printnode(s, printtype) + ','
        print(name, "%s" % stack_string)

    def printstacks(self, operators, operands, printtype=True):
        operands_string = ""
        operators_string = ""
        for o in operands:
            operands_string += self.printnode(o,printtype) + ','
        for o in operators:
            operators_string += self.printnode(o,printtype) + ','
        print("%s @ %s" % (operators_string, operands_string))

    def gettreenode(self, node):
        result = ""
        s = node.gettoken()
        if s == None:
            result += "nil"
        else:
            result += "%s " % s.getname()
        return result

    def printtree(self, tree):
        lt = tree.getleft()
        if lt != None:
            left = self.gettreenode(lt)
            self.printtree(lt)
        else:
            left = "nil"
        rt = tree.getright()
        if rt != None:
            right = self.gettreenode(rt)
            self.printtree(rt)
        else:
            right = "nil"
        node = self.gettreenode(tree)
        print("Node:%10s, Left:%20s, Right:%20s" % (node, left, right))

    def pushstack(self, token):
        self.tokenstack.append(token)

    def popstack(self):
        return self.tokenstack.pop()

    def stackempty(self):
        return (len(self.tokenstack) == 0)

    def isaddsub(self, operator):
        return (operator == "plussign" or operator == "minussign" or operator == "equalequal")
        # return (operator == "plussign" or operator == "minussign")

    def ismuldiv(self, operator):
        return (operator == "pointer" or operator == "star" or operator == "slash")
    
    def isvar(self, operator):
        attributes = operator.getattributehash()
        try:
            if attributes['vardefinition']:
                return True
        except KeyError as e:
            return False
        return False

    def isargument(self, operator):
        attributes = operator.getattributehash()
        try:
            if attributes['isargument']:
                return True
        except KeyError as e:
            return False
        return False

    def isfunc(self, operator):
        attributes = operator.getattributehash()
        try:
            if attributes['funcdefinition']:
                return True
        except KeyError as e:
            return False
        return False

    def evaluate_test(self, anode):
        node = anode
        result = "Token(%s)" % node.gettoken().getname()
        if node.getleft() != None:
            result += "Left(%s)" % self.evaluate_test(node.getleft())
        if node.getright() != None:
            result += "Right(%s)" % self.evaluate_test(node.getright())
        return result

    def evaluate_orig(self, anode):
        node = anode
        if node.isleaf():
            result = "Single(%s)" % node.gettoken().getname()
            return result
        else:
            result = "Double(%s|%s)" % (self.evaluate_orig(node.getleft()),self.evaluate_orig(node.getright()))
            return result
    
    def calculatesizeofconstant(self, value):
        size = 1
        value = int(value)
        if value > 0xFF:
            size = 2
            if value > 0xFFFF:
                size = 4
                if value > 0xFFFFFFFF:
                    size = 8
        return size

    def prepareevaluate(self, anode):
        node = anode
        self.evalopsize = 1
        if node.isleaf():
            leafnode = node.gettoken()
            return leafnode
        else:
            nodetoken = node.gettoken()
            nodetokenname = nodetoken.getname()
            if node.getleft() != None:
                leftnodename = node.getleft().gettoken().getname()
                lefttoken = self.prepareevaluate(node.getleft())
                if lefttoken != None and self.isfunc(lefttoken):
                    print("lefttoken:%s is function" % lefttoken.getname())
            else:
                lefttoken = None
            if node.getright() != None:
                rightnodename = node.getright().gettoken().getname()
                righttoken = self.prepareevaluate(node.getright())
                if righttoken != None and self.isfunc(righttoken):
                    print("righttoken:%s is function" % righttoken.getname())
            else:
                righttoken = None
            if lefttoken != None:
                leftnodename = lefttoken.getname()
                if self.evalopsize < lefttoken.getsize():
                    self.evalopsize = lefttoken.getsize() 
                action_l = "push %s" % leftnodename
            else:
                action_l = ""
                leftnodename = "(none)"
            if righttoken != None:
                rightnodename = righttoken.getname()
                if self.evalopsize < righttoken.getsize():
                    self.evalopsize = righttoken.getsize() 
                action_r = "push %s" % rightnodename
            else:
                action_r = ""
                rightnodename = "(none)"
            print("prepareevaluate: %s Left:%s, Right:%s" % (nodetokenname, leftnodename, rightnodename))
            if action_l != "":
                print("prepare  left: %s" % action_l)
                t_type_left = lefttoken.gettype()
                t_value_left = lefttoken.getvalue()
                if t_type_left == "number":
                    self.evaluatedeepthcount += 1
                    if self.evaluatedeepthcount > self.evaluatedepth:
                        self.evaluatedepth = self.evaluatedeepthcount
                    constsize = self.calculatesizeofconstant(lefttoken.getvalue())
                    if self.evalopsize < constsize:
                        self.evalopsize = constsize
                elif self.isvar(lefttoken) or self.isargument(lefttoken):
                    self.evaluatedeepthcount += 1
                    if self.evaluatedeepthcount > self.evaluatedepth:
                        self.evaluatedepth = self.evaluatedeepthcount
                elif self.isfunc(lefttoken):
                    print("calling function in left branch is wrong")
                    sys.exit(1)
                    self.evaluatedeepthcount += 1
                    if self.evaluatedeepthcount > self.evaluatedepth:
                        self.evaluatedepth = self.evaluatedeepthcount
                else:
                    print("Line: %d prepareevaluate:  t_type_left not found, t_type is: %s, Value: %s" % (self.linenumber, t_type_left, t_value_left))
                    sys.exit(1)
            if action_r != "":
                print("prepare right: %s" % action_r)
                t_type_right = righttoken.gettype()
                t_value_right = righttoken.getvalue()
                if t_type_right == "number":
                    self.evaluatedeepthcount += 1
                    if self.evaluatedeepthcount > self.evaluatedepth:
                        self.evaluatedepth = self.evaluatedeepthcount
                    constsize = self.calculatesizeofconstant(righttoken.getvalue())
                    if self.evalopsize < constsize:
                        self.evalopsize = constsize
                elif self.isvar(righttoken) or self.isargument(righttoken):
                    self.evaluatedeepthcount += 1
                    if self.evaluatedeepthcount > self.evaluatedepth:
                        self.evaluatedepth = self.evaluatedeepthcount
                elif self.isfunc(righttoken):
                    print("calling function in right branch is wrong")
                    sys.exit(1)
                    self.evaluatedeepthcount += 1
                    if self.evaluatedeepthcount > self.evaluatedepth:
                        self.evaluatedepth = self.evaluatedeepthcount
                else:
                    print("Line: %d prepareevaluate: t_type_right not found, t_type is: %s, Value: %s" % (self.linenumber, t_type_right, t_value_right))
                    sys.exit(1)
                # print("prepareevaluate: Count=%d Stackdepth:%d" % (self.evaluatedeepthcount, self.evaluatedepth))
            operation = nodetokenname
            print("---prepare: operation:%s" % operation)
            if operation == "plussign":
                self.evaluatedeepthcount -= 1
            elif operation == "minussign":
                self.evaluatedeepthcount -= 1
            elif operation == "star" or operation == "pointer":
                self.evaluatedeepthcount -= 1
            elif operation == "slash":
                self.evaluatedeepthcount -= 1
            elif operation == "equalequal":
                self.evaluatedeepthcount -= 1
            elif operation == "notequal":
                self.evaluatedeepthcount -= 1
            elif operation == "equalsmaller" or operation == "smallerequal":
                self.evaluatedeepthcount -= 1
            elif operation == "equalgreater" or operation == "greaterequal":
                self.evaluatedeepthcount -= 1
            elif operation == "smaller":
                self.evaluatedeepthcount -= 1
            elif operation == "greater":
                self.evaluatedeepthcount -= 1
            else:
                tokenfullname = nodetoken.getnamewithnamespace()
                if tokenfullname == None:
                    print("operation >%s< unknown in prepareevaluate" % operation)
                    sys.exit(1)

    def evaluate(self, anode):
        self.evalopsize = 1
        node = anode
        if node.isleaf():
            leafnode = node.gettoken()
            return leafnode
        else:
            nodetoken = node.gettoken()
            nodetokenname = nodetoken.getname()
            if nodetokenname == "256":
                xxx = 0
            if node.getleft() != None:
                leftnodename = node.getleft().gettoken().getname()
                lefttoken = self.evaluate(node.getleft())
            else:
                lefttoken = None
            if node.getright() != None:
                rightnodename = node.getright().gettoken().getname()
                righttoken = self.evaluate(node.getright())
            else:
                righttoken = None

            if lefttoken != None:
                leftnodename = lefttoken.getname()
                action_l = "push %s" % leftnodename
            else:
                action_l = ""
                leftnodename = "(none)"
            if righttoken != None:
                rightnodename = righttoken.getname()
                action_r = "push %s" % rightnodename
            else:
                action_r = ""
                rightnodename = "(none)"
            self.log.writelog("expressions/evaluate:", "%s Left:%s, Right:%s" % (nodetokenname, leftnodename, rightnodename))
            if action_l != "":
                print("evaluate: %s" % action_l)
                t_type_left = lefttoken.gettype()
                if t_type_left == "number":
                    constsize = self.calculatesizeofconstant(lefttoken.getvalue())
                    if self.evalopsize < constsize:
                        self.evalopsize = constsize
                    self.code.pushvaluetostack(lefttoken)
                    self.log.writelog("expressions/evaluate:", "leftnode,pushvaluetostack: %s" % leftnodename)
                    self.code.createdumpevalstack("PSH-VAL", "after action_l operation in evaluation stack")
                elif self.isvar(lefttoken) or self.isargument(lefttoken):
                    self.code.pushvartostack(lefttoken)
                    self.log.writelog("expressions/evaluate:", "leftnode,pushvartostack: %s" % leftnodename)
                    self.code.createdumpevalstack("PSH-VAR", "after action_l operation in evaluation stack")
                elif self.isfunc(lefttoken):
                    print("lefttoken is func")
                    sys.exit(1)
                    print("call function '%s' in action_l from expressions" % lefttoken.getname())
                    if self.evalopsize < lefttoken.getsize():
                        self.evalopsize = lefttoken.getsize()
                    self.code.funcfromexpression(lefttoken)
                    self.log.writelog("expressions/evaluate:", "leftnode,callfuncfromexpr.: %s" % leftnodename)
                else:
                    print("t_type_left not found, t_type is: %s" % t_type_left)
                    sys.exit(0)
            if action_r != "":
                print("evaluate: %s" % action_r)
                t_type_right = righttoken.gettype()
                if t_type_right == "number":
                    constsize = self.calculatesizeofconstant(righttoken.getvalue())
                    if self.evalopsize < constsize:
                        self.evalopsize = constsize
                    self.code.pushvaluetostack(righttoken)
                    self.log.writelog("expressions/evaluate:", "rightnode,pushvaluetostack: %s" % rightnodename)
                    self.code.createdumpevalstack("PSH-VAL", "after action_r operation in evaluation stack")
                elif self.isvar(righttoken) or self.isargument(righttoken):
                    self.code.pushvartostack(righttoken)
                    self.log.writelog("expressions/evaluate:", "rightnode,pushvartostack: %s" % rightnodename)
                    if self.evalopsize < righttoken.getsize():
                        self.evalopsize = righttoken.getsize()
                    self.code.createdumpevalstack("PSH-VAR", "after action_r operation in evaluation stack")
                elif self.isfunc(righttoken):
                    print("righttoken is func")
                    sys.exit(1)
                    self.log.writelog("expressions/evaluate", "call function:%s" % righttoken.getname())
                    print("Line: %d call function '%s' in action_r from expressions" % (self.linenumber, righttoken.getname()))
                    if self.evalopsize < righttoken.getsize():
                        self.evalopsize = righttoken.getsize()
                    self.code.funcfromexpression(righttoken)
                    self.log.writelog("expressions/evaluate:", "rightnode,callfuncfromexpr.: %s" % rightnodename)
                else:
                    print("t_type_right not found, t_type is: %s" % t_type_right)
                    sys.exit(0)
            operation = nodetokenname
            print("evaluate: operation:%s" % operation)
            if operation == "plussign":
                self.code.addonstack(self.options)
            elif operation == "minussign":
                self.code.subonstack(self.options)
            elif operation == "star" or operation == "pointer":
                self.code.mulonstack(self.options)
            elif operation == "slash":
                self.code.divonstack(self.options)
            elif operation == "equalequal":
                self.code.equalstack(self.options)
            elif operation == "notequal":
                self.code.notequalstack(self.options)
            elif operation == "equalsmaller" or operation == "smallerequal":
                self.code.equalsmallerstack(self.options)
            elif operation == "equalgreater" or operation == "greaterequal":
                self.code.equalgreaterstack(self.options)
            elif operation == "smaller":
                self.code.smallerstack(self.options)
            elif operation == "greater":
                self.code.greaterstack(self.options)
            else:
                tokenfullname = nodetoken.getnamewithnamespace()
                if tokenfullname == None:
                    print("operation >%s< unknown in evaluate" % operation)
                    sys.exit(1)
                if self.isfunc(nodetoken):
                    self.code.funcfromexpression(nodetoken, self.options)
                    self.log.writelog("expressions/evaluate:", "midnode,callfuncfromexpr.: %s" % tokenfullname)
                else:
                    print("nodetoken: %s is not a function" % tokenfullname)
                    t_type = nodetoken.gettype()
                    if t_type == "number":
                        constsize = self.calculatesizeofconstant(nodetoken.getvalue())
                        if self.evalopsize < constsize:
                            self.evalopsize = constsize
                        self.code.pushvaluetostack(nodetoken)
                        self.log.writelog("expressions/evaluate:", "midnode,pushvaluetostack.: %s" % tokenfullname)
                    elif self.isvar(nodetoken) or self.isargument(nodetoken):
                        self.code.pushvartostack(nodetoken)
                        self.log.writelog("expressions/evaluate:", "midnode,pushvartostack.: %s" % tokenfullname)
                    else:
                        print("t_type not found, t_type is: %s" % t_type)
                        sys.exit(0)
            self.code.createdumpevalstack(operation, "after %s operation on stack" % operation)

    def generate(self, foundtoken, lineno):
        self.linenumber = lineno
        destvarname = foundtoken.getname()
        if destvarname == "testvalue":
            x = 0
        namespace = foundtoken.getnamespace()
        useopsize = foundtoken.getsize()
        if False and len(self.tokenlist) == 1:
            x = self.tokenlist[0]
            self.code.copyvar(foundtoken, x, lineno=self.linenumber)
            self.tokenlist.clear()
        else:
            for t in self.tokenlist:
                print("namespace:%s, ttype:%s, Value:%s" % (t.getnamespace(), t.gettype(), t.getname()))
            expression = ""
            for token in self.tokenlist:
                t_value = token.getname()
                t_type = token.gettype()
                t_function = self.isfunc(token)
                if t_type == "plussign":
                    t_value = '+'
                elif t_type == "minussign":
                    t_value = '-'
                elif t_type == "pointer" or t_type == "star":
                    t_value = '*'
                elif t_type == "openbracket":
                    t_value = '('
                elif t_type == "closebracket":
                    t_value = ')'
                elif t_type == "slash":
                    t_value = '/'
                elif t_type == "equalequal":
                    t_value = '=='
                elif t_type == "notequal":
                    t_value = '!='
                elif t_type == "greaterequal":
                    t_value = '>='
                elif t_type == "equalgreater":
                    t_value = '=>'
                elif t_type == "smallerequal":
                    t_value = '<='
                elif t_type == "equalsmaller":
                    t_value = '=<'
                elif t_type == "greater":
                    t_value = '>'
                elif t_type == "smaller":
                    t_value = '<'
                elif t_type == "comma":
                    t_value = ','
                elif t_function:
                    pass
                else:
                    pass
                expression += " %s " % t_value
            print("Expression is:%s = %s" % (destvarname, expression))
            operator_stack = list()
            operand_stack = list()
            oldversion = False
            createtree = True
            self.evalopsize = 1
            print("-------------------------- WORKING ON THE FOLLOWING TOKENS ---------------------------")
            for token in self.tokenlist:
                node = anode(token)
                print("%s," % node.getname(), end="")
            print()
            print("--------------------------------------------------------------------------------------")
            stackdepth = 0
            for token in self.tokenlist:
                node = anode(token)
                node_name = node.getname()
                if node_name == "log10":
                    xxx = 0
                # print("%s," % node.getname(), end="")
                if node.isnumber():
                    self.log.writelog("expressions/generate", "nodename:%s node is number" % node.getname())
                    print("Node is Number:%s, Linenumber:%d" % (node.getname(), self.linenumber))
                    constsize = self.calculatesizeofconstant(token.getsize())
                    if self.evalopsize < constsize:
                        self.evalopsize = constsize
                    operand_stack.append(node)
                    stackdepth += 1
                elif node.isvar():
                    self.log.writelog("expressions/generate", "nodename:%s node is variable" % node.getname())
                    print("Node is Variable:%s, Linenumber:%d" % (node.getname(), self.linenumber))
                    varsize = node.gettoken().getsize()
                    if self.evalopsize < varsize:
                        self.evalopsize = varsize
                    operand_stack.append(node)
                    stackdepth += 1
                elif node.isargument():
                    self.log.writelog("expressions/generate", "nodename:%s node is isargument" % node.getname())
                    print("Node is Argument:%s, Linenumber:%d" % (node.getname(), self.linenumber))
                    varsize = node.gettoken().getsize()
                    if self.evalopsize < varsize:
                        self.evalopsize = varsize
                    operand_stack.append(node)
                    stackdepth += 1
                elif node.isfunction():
                    self.log.writelog("expressions/generate", "nodename:%s node is function" % node.getname())
                    print("Node is Function:%s, Linenumber:%d" % (node.getname(), self.linenumber))
                    varsize = node.gettoken().getsize()
                    if self.evalopsize < varsize:
                        self.evalopsize = varsize
                    operator_stack.append(node)
                elif node.isinternalfunc():
                    self.log.writelog("expressions/generate", "nodename:%s node is function" % node.getname())
                    print("Node is internal Function:%s, Linenumber:%d" % (node.getname(), self.linenumber))
                    varsize = node.gettoken().getsize()
                    if self.evalopsize < varsize:
                        self.evalopsize = varsize
                    operator_stack.append(node)
                elif node.checktype("openbracket"):
                    self.log.writelog("expressions/generate", "nodename:%s node is openbracket" % node.getname())
                    print("Node is %s, Linenumber:%d" % (node.getname(), self.linenumber))
                    operator_stack.append(node)
                elif node.checktype("comma"):
                    self.log.writelog("expressions/generate", "nodename:%s node is comma" % node.getname())
                    print("Node is %s, Linenumber:%d" % (node.getname(), self.linenumber))
                    while len(operator_stack) > 0 and not operator_stack[-1].checktype("openbracket"):
                        operand_stack.append(operator_stack.pop())
                        stackdepth += 1
                elif node.isoperator():
                    self.log.writelog("expressions/generate", "nodename:%s node is operator" % node.getname())
                    print("Node is Operator:%s, Linenumber:%d" % (node.getname(), self.linenumber))
                    while len(operator_stack) > 0 and not \
                                        operator_stack[-1].checktype("openbracket") and \
                                        operator_stack[-1].getprecedence() >= node.getprecedence():
                        operand_stack.append(operator_stack.pop())
                        stackdepth += 1
                    operator_stack.append(node)
                elif node.checktype("closebracket"):
                    self.log.writelog("expressions/generate", "nodename:%s node is closebracket" % node.getname())
                    print("Node is %s, Linenumber:%d" % (node.getname(), self.linenumber))
                    while len(operator_stack) > 0 and not operator_stack[-1].checktype("openbracket"):
                        op = operator_stack.pop()
                        operand_stack.append(op)
                        stackdepth += 1
                        self.log.writelog("expressions/generate", "push operand nodename:%s node is operator" % operand_stack[-1].getname())
                        print("Append to Operand-Stack:%s"%operand_stack[-1].getname())
                    operator_stack.pop() # pops out openbracket
                    if len(operator_stack) > 0 and \
                                (operator_stack[-1].isfunction() or operator_stack[-1].isinternalfunc()):
                        # ----------------- do function call with variable count of argument
                        print("Append Function call to Operator Stack:%s" % operator_stack[-1].getname())
                        op = operator_stack.pop()
                        fcttoken = op.gettoken()
                        fctname = fcttoken.getname()
                        fctdata = fcttoken.getfuncdata()
                        fctargs = fctdata.arg_objects
                        fctarglen = len(fctargs)
                        self.log.writelog("expressions/generate", "function:%s node is functioncall with %d args" % (fctname, fctarglen))
                        # create functionnode
                        fctnode = anode(fcttoken)
                        operand_stack.append(fctnode)
                        self.log.writelog("expressions/generate", "push operand nodename:%s node is operator" % fctname)
                else:
                    print("token not recognized: %s" % node.getname())
                    sys.exit(1)
            print("complete operand_stack with rest of Operator Stack")
            while len(operator_stack) > 0:
                op = operator_stack.pop()
                print("Add to Operand Stack:%s" % op.getname())
                if op.checktype("closebracket") and op.checktype("openbracket"):
                    print("bracket mismatch in expression, to manny %s" % op.gettype())
                    sys.exit(1)
                operand_stack.append(op)
                self.log.writelog("expressions/generate", "push operand nodename:%s node is operator" % op.getname())
            self.printstacks(operator_stack, operand_stack)
            keyidx = 0
            firsttype = None
            for k in self.optionkeys:
                print("Item:%s has Type:%s" % (k, self.optionkeys[k].gettype()))
                if keyidx == 0:
                    firsttype = self.optionkeys[k].gettype()
                    if firsttype == "wozfloat":
                        firsttype = "type_float"
                else:
                    indextype = self.optionkeys[k].gettype()
                    if indextype == "wozfloat":
                        indextype = "type_float"
                    if False and indextype != firsttype:
                        print("different tokentype found in expression, actual not implemented")
                        print("error is in line: %d" % self.linenumber)
                        print("Warning, Not all Tokens are from the same Type!")
                        for k in self.optionkeys:
                            print("Tokeninfo:%s, Type:%s" % (k, indextype))
                        print("Warning, Not all Tokens are from the same Type!")
                        sys.exit(1)
                keyidx += 1
            if firsttype == None:
                self.options = "byte"
            else:
                self.options = firsttype
            if firsttype == "type_float":
                firsttype = self.options = "wozfloat"
            print("found preavluate evalsize: %d" % self.evalopsize)
            print("Found preevaluated stackdepth: %d" % stackdepth)
            self.evaluatedepth = stackdepth + 1;
            self.code.begindoevaluate(self.evalopsize, expression, self.evaluatedepth)
            print("------------------------ Generate Code ---------------------------")
            stackdepth = 0
            for op in operand_stack:
                token = op.gettoken()
                print("Name:%s" % token.getname())
                operation = token.getname()
                print("evaluate: operation:%s" % operation)
                if operation == "plussign":
                    self.code.addonstack(self.options)
                    stackdepth -= 1
                elif operation == "minussign":
                    self.code.subonstack(self.options)
                    stackdepth -= 1
                elif operation == "star" or operation == "pointer":
                    self.code.mulonstack(self.options)
                    stackdepth -= 1
                elif operation == "slash":
                    self.code.divonstack(self.options)
                    stackdepth -= 1
                elif operation == "equalequal":
                    self.code.equalstack(self.options)
                    stackdepth -= 1
                elif operation == "notequal":
                    self.code.notequalstack(self.options)
                    stackdepth -= 1
                elif operation == "equalsmaller" or operation == "smallerequal":
                    self.code.equalsmallerstack(self.options)
                    stackdepth -= 1
                elif operation == "equalgreater" or operation == "greaterequal":
                    self.code.equalgreaterstack(self.options)
                    stackdepth -= 1
                elif operation == "smaller":
                    self.code.smallerstack(self.options)
                    stackdepth -= 1
                elif operation == "greater":
                    self.code.greaterstack(self.options)
                    stackdepth -= 1
                elif op.isnumber():
                    tokenfullname = token.getnamewithnamespace()
                    if tokenfullname == None:
                        print("operation >%s< unknown in evaluate" % operation)
                        sys.exit(1)
                    self.code.pushvaluetostack(token)
                    stackdepth += 1
                elif op.isfunction():
                    tokenfullname = token.getnamewithnamespace()
                    if tokenfullname == None:
                        print("operation >%s< unknown in evaluate" % operation)
                        sys.exit(1)
                    if self.evalopsize < token.getsize():
                        self.evalopsize = token.getsize()
                    self.code.funcfromexpression(token, self.options)
                    stackdepth -= 1
                    self.log.writelog("expressions/generate:", "isfunction: %s" % tokenfullname)
                elif op.isinternalfunc():
                    tokenfullname = token.getnamewithnamespace()
                    if tokenfullname == None:
                        print("operation >%s< unknown in evaluate" % operation)
                        sys.exit(1)
                    if self.evalopsize < token.getsize():
                        self.evalopsize = token.getsize()
                    self.options = token.gettype()
                    self.code.internalfuncfromexpression(token, self.options)
                    stackdepth -= 1
                    self.log.writelog("expressions/generate:", "isinternalfunc: %s" % tokenfullname)
                elif op.isvar():
                    tokenfullname = token.getnamewithnamespace()
                    if tokenfullname == None:
                        print("operation >%s< unknown in evaluate" % operation)
                        sys.exit(1)
                    if self.evalopsize < token.getsize():
                        self.evalopsize = token.getsize()
                    stackdepth += 1
                    self.options = token.gettype()
                    self.code.pushvartostack(token)
                elif op.isargument():
                    tokenfullname = token.getnamewithnamespace()
                    if tokenfullname == None:
                        print("operation >%s< unknown in evaluate" % operation)
                        sys.exit(1)
                    if self.evalopsize < token.getsize():
                        self.evalopsize = token.getsize()
                    stackdepth += 1
                    self.options = token.gettype()
                    self.code.pushvartostack(token)
                else:
                    print("something is going wrong in expressions/generate code gerenration >%s< unknown in evaluate" % operation)
                    sys.exit(1)
            # root = operand_stack.pop()
            print("Found preevaluated stackdepth: %d" % stackdepth)
            self.evaluatedeepthcount = 0
            self.evaluatedepth = 0
            # result = self.prepareevaluate(root)
            # result = self.evaluate(root)
            # print("found real avluate evalsize: %d" % self.evalopsize)
            self.code.popvarfromstack(foundtoken, lineno=self.linenumber)
            self.optionkeys = dict()
        self.tokenlist.clear()
        self.optionkeys.clear()



