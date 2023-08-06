from helpers import CompilerFault
from storetokens import storetokens, objects
from codeemitter import codeemitter
from cclogger import cclogger
from compilerexceptions import CompilerFault
from dataclasses import dataclass  # if python < 3.7
from typing import Optional, List
from operator import add, sub, mul, truediv
import sys



@dataclass
class Node:
    symbol: str
    left: Optional['Node']
    right: Optional['Node']

    def is_leaf(self) -> bool:
        result = self.left is None and self.right is None
        return result

@dataclass
class Tree:
    root: Node

    @classmethod
    def _tokenize(cls, text: str) -> List[str]:
        prev = ''
        tokenized = []
        for char in text:
            if prev.isdigit() and char.isdigit():
                tokenized.append(tokenized.pop() + char)
            elif prev.isalpha() and char.isalpha():
                tokenized.append(tokenized.pop() + char)
            else:
                tokenized.append(char)
            prev = char
        return tokenized

    @classmethod
    def build(cls, text: str) -> 'Tree':
        raise NotImplementedError

    def evaluate(self, node: Optional[Node] = None):
        OPS = {
            '+': add,
            '-': sub,
            '*': mul,
            '/': truediv
        }
        node = node or self.root
        if node.is_leaf():
            return int(node.symbol)
        else:
            op = OPS[node.symbol]
            le = self.evaluate(node.left)
            ri = self.evaluate(node.right)
            print("evaluate:%s:(%s,%s)" % (node.symbol, le, ri))
            return op(le, ri)

    def evaluatetostring(self, node: Optional[Node] = None):
        node = node or self.root
        if node.is_leaf():
            return (node.symbol)
        else:
            return "(%s,%s)" % (self.evaluatetostring(node.left), self.evaluatetostring(node.right))



    # Parsing with parentheses
    @classmethod
    def build_with_parentheses(cls, text: str) -> 'Tree':
        stack: List[Node] = []
        for char in cls._tokenize(text):
            if char.isdigit():
                    stack.append(Node(symbol=char, left=None, right=None))
            elif char == ')':
                right = stack.pop()
                op = stack.pop()
                left = stack.pop()
                stack.append(Node(symbol=op, left=left, right=right))
            elif char in '+-*/':
                stack.append(char)
        return cls(root=stack.pop())

    # Parsing with operator precedence
    @classmethod
    def build_operator_precedence(cls, text: str) -> 'Tree':
        operator_stack: List[str] = []
        operand_stack: List[Node] = []
        for char in cls._tokenize(text):
            print(operator_stack, operand_stack)
            if char.isdigit():
                operand_stack.append(Node(symbol=char, left=None, right=None))
            elif char in '+-' and len(operator_stack) > 0 and operator_stack[-1] in '*/':
                right = operand_stack.pop()
                op = operator_stack.pop()
                left = operand_stack.pop()
                operand_stack.append(Node(symbol=op, left=left, right=right))
                operator_stack.append(char)
            else:
                operator_stack.append(char)
        while len(operator_stack) > 0:
            right = operand_stack.pop()
            op = operator_stack.pop()
            left = operand_stack.pop()
            operand_stack.append(Node(symbol=op, left=left, right=right))
        return cls(root=operand_stack.pop())

    # Parsing with both operator precedence and parentheses
    @classmethod
    # def build_operator_precedence_and_parantheses(cls, text: str) -> 'Tree':
    def build(cls, text: str) -> 'Tree':
        operator_stack: List[str] = []
        operand_stack: List[Node] = []
        for char in cls._tokenize(text):
            print(operator_stack, operand_stack)
            if char.isdigit() or char.isalpha():
                operand_stack.append(Node(symbol=char, left=None, right=None))
            elif char in '+-' and len(operator_stack) > 0 and operator_stack[-1] in '*/':
                right = operand_stack.pop()
                op = operator_stack.pop()
                left = operand_stack.pop()
                operand_stack.append(Node(symbol=op, left=left, right=right))
                operator_stack.append(char)
            elif char == ')':
                while len(operator_stack) > 0 and operator_stack[-1] != '(':
                    right = operand_stack.pop()
                    op = operator_stack.pop()
                    left = operand_stack.pop()
                    operand_stack.append(Node(symbol=op, left=left, right=right))
                operator_stack.pop()
            else:
                operator_stack.append(char)
        while len(operator_stack) > 0:
            right = operand_stack.pop()
            op = operator_stack.pop()
            left = operand_stack.pop()
            operand_stack.append(Node(symbol=op, left=left, right=right))
        return cls(root=operand_stack.pop())

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
                        print("Object:%s not found for namespace:%s and global and _INTERNAL" % (tvalue, namespace))
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
        if len(self.tokenlist) == 1:
            x = self.tokenlist[0]
            self.code.copyvar(foundtoken, x, lineno=self.linenumber)
            self.tokenlist.clear()
        else:
            for t in self.tokenlist:
                print("namespace:%s, ttype:%s, Value:%s" % (t.getnamespace(), t.gettype(), t.getname()))
            expression = ""
            if True:
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
            print("Expression is:%s" % expression)
            if False:
                tree = Tree.build(expression)
                print(tree.evaluate())
            operator_stack = list()
            operand_stack = list()
            oldversion = False
            createtree = True
            if oldversion:  # works for expressions without functions
                for token in self.tokenlist:
                    t_type = token.gettype()
                    t_value = token.getname()
                    t_namewithnamespace = token.getnamewithnamespace()
                    t_objtype = token.getattributehash()
                    if False:
                        print("Type:%s, Value:%s" % (t_type, t_value)) 
                        self.printstacks(operator_stack, operand_stack)
                    if t_type == "number":
                        newnode = anode(token)
                        operand_stack.append(newnode)
                    elif self.isvar(token) or self.isargument(token):
                        newnode = anode(token)
                        operand_stack.append(newnode)
                    elif self.isfunc(token):
                        newnode = anode(token)
                        operator_stack.append(newnode)
                    elif anode.precedence[t_type] > 0:    # precedence > 0 then the token is an operator
                        newnode = anode(token)
                        operator_stack.append(newnode)
                    elif self.isaddsub(t_type) and len(operator_stack) > 0 and self.ismuldiv(operator_stack[-1].gettoken().gettype()):
                        right = operand_stack.pop()
                        op = operator_stack.pop()
                        left = operand_stack.pop()
                        newnode = anode(op.gettoken())
                        newnode.addleft(left)
                        newnode.addright(right)
                        operand_stack.append(newnode)
                        newnode = anode(token)
                        operator_stack.append(newnode)
                    elif t_type == "openbracket":
                        newnode = anode(token)
                        operator_stack.append(newnode)
                    elif t_type == "closebracket":
                        while len(operator_stack) > 0 and operator_stack[-1].gettoken().gettype() != "openbracket":
                            if len(operand_stack) > 0:
                                right = operand_stack.pop()
                            else:
                                print("operand stack ist empty for filling right branch")
                                sys.exit(1)
                            if len(operator_stack) > 0:
                                op = operator_stack.pop()
                            else:
                                print("operator stack is empty")
                                sys.exit(1)
                            if len(operand_stack) > 0:
                                left = operand_stack.pop()
                            else:
                                print("operand stack ist empty for filling left branch")
                                sys.exit(1)
                            newnode = anode(op.gettoken())
                            newnode.addleft(left)
                            newnode.addright(right)
                            operand_stack.append(newnode)
                            topofoperatorstack = operator_stack[-1].gettoken().gettype()   # not openbracket test
                        operator_stack.pop()
                        if len(operator_stack) > 0 and self.isfunc(operator_stack[-1].gettoken()):
                            func_op = operator_stack.pop()
                    else:
                        print("token does not fit: (%s,%s)" % (t_type, t_value))
                        sys.exit(1)
                        newnode = anode(token)
                        operator_stack.append(newnode)
                # put all stack entrys to the output-queue
                while len(operator_stack) > 0:
                    if operator_stack[-1].gettoken().gettype() == "openbracket":
                        print("error, there are more open brackets then closed brackets")
                        sys.exit(1)
                    right = operand_stack.pop()
                    op = operator_stack.pop()
                    left = operand_stack.pop()
                    newnode = anode(op.gettoken())
                    newnode.addleft(left)
                    newnode.addright(right)
                    operand_stack.append(newnode)
            else:
                # new version with functions
                tokenlistlen = len(self.tokenlist)
                for token in self.tokenlist:
                    node = anode(token)
                    print("%s," % node.getname(), end="")
                    if node.isnumber():
                        self.log.writelog("expressions/generate", "nodename:%s node is number" % node.getname())
                        operand_stack.append(node)
                    elif node.isvar():
                        self.log.writelog("expressions/generate", "nodename:%s node is variable" % node.getname())
                        operand_stack.append(node)
                    elif node.isargument():
                        self.log.writelog("expressions/generate", "nodename:%s node is isargument" % node.getname())
                        operand_stack.append(node)
                    elif node.isfunction():
                        self.log.writelog("expressions/generate", "nodename:%s node is function" % node.getname())
                        operator_stack.append(node)
                    elif node.checktype("openbracket"):
                        self.log.writelog("expressions/generate", "nodename:%s node is openbracket" % node.getname())
                        operator_stack.append(node)
                    elif node.checktype("comma"):
                        self.log.writelog("expressions/generate", "nodename:%s node is comma" % node.getname())
                        while len(operator_stack) > 0 and not operator_stack[-1].checktype("openbracket"):
                            operand_stack.append(operator_stack.pop())
                    elif node.isoperator():
                        self.log.writelog("expressions/generate", "nodename:%s node is operator" % node.getname())
                        if not createtree: # create a simple list
                            while len(operator_stack) > 0 and not operator_stack[-1].checktype("openbracket") and operator_stack[-1].getprecedence() >= node.getprecedence():
                                operand_stack.append(operator_stack.pop())
                            operator_stack.append(node)
                        else:     # create a tree
                            while len(operator_stack) > 0 and not \
                                                operator_stack[-1].checktype("openbracket") and \
                                                operator_stack[-1].getprecedence() >= node.getprecedence():
                                op = operator_stack.pop()
                                right = operand_stack.pop()
                                left = operand_stack.pop()
                                newnode = anode(op.gettoken())
                                newnode.addleft(left)
                                newnode.addright(right)
                                operand_stack.append(newnode)
                                self.log.writelog("expressions/generate", "push operand nodename:%s node is operator" % newnode.getname())
                            operator_stack.append(node)
                    elif node.checktype("closebracket"):
                        self.log.writelog("expressions/generate", "nodename:%s node is closebracket" % node.getname())
                        if not createtree:
                            while len(operator_stack) > 0 and not operator_stack[-1].checktype("openbracket"):
                                operand_stack.append(operator_stack.pop())
                                self.log.writelog("expressions/generate", "push operand nodename:%s node is operator" % newnode.getname())
                            operator_stack.pop()
                        else:
                            while len(operator_stack) > 0 and not \
                                     operator_stack[-1].checktype("openbracket"):
                                right = operand_stack.pop()
                                op = operator_stack.pop()
                                left = operand_stack.pop()
                                newnode = anode(op.gettoken())
                                newnode.addleft(left)
                                newnode.addright(right)
                                operand_stack.append(newnode)
                                self.log.writelog("expressions/generate", "push operand nodename:%s node is operator" % newnode.getname())
                            operator_stack.pop() # pops out openbracket
                            if len(operator_stack) > 0 and operator_stack[-1].isfunction():
                                # ----------------- do function call with variable count of argument
                                op = operator_stack.pop()
                                fcttoken = op.gettoken()
                                fctname = fcttoken.getname()
                                fctdata = fcttoken.getfuncdata()
                                fctargs = fctdata.arg_objects
                                fctarglen = len(fctargs)
                                self.log.writelog("expressions/generate", "function:%s node is functioncall with %d args" % (fctname, fctarglen))
                                if fctarglen == 0:
                                    operand_stack.append(op)
                                    self.log.writelog("expressions/generate", "push operand nodename:%s node is operator" % op.getname())
                                elif fctarglen == 1:
                                    right = operand_stack.pop()
                                    newnode = anode(fcttoken)
                                    newnode.addright(right)
                                    operand_stack.append(newnode)
                                    self.log.writelog("expressions/generate", "push operand nodename:%s node is operator" % newnode.getname())
                                elif fctarglen == 2:
                                    left = operand_stack.pop()
                                    right = operand_stack.pop()
                                    newnode = anode(fcttoken)
                                    newnode.addright(right)
                                    newnode.addleft(left)
                                    operand_stack.append(newnode)
                                    self.log.writelog("expressions/generate", "push operand nodename:%s node is operator" % newnode.getname())
                                elif fctarglen == 3:
                                    node1 = operand_stack.pop()
                                    node2 = operand_stack.pop()
                                    node3 = operand_stack.pop()
                                    # create new leave 
                                    newnode1 = anode(node1.gettoken())
                                    newnode2 = anode(node2.gettoken())
                                    newnode2.addright(newnode1)
                                    newnode3 = anode(node3.gettoken())
                                    newnode3.addright(newnode2)
                                    
                                    # create functionnode
                                    fctnode = anode(fcttoken)
                                    fctnode.addright(newnode3)
                                    operand_stack.append(fctnode)
                                    self.log.writelog("expressions/generate", "push operand nodename:%s node is operator" % fctnode.getname())
                                else:
                                    print()
                                    print("expressions/generate: argument count exceeded (not more then 3 arguments allowed at the moment)")
                                    sys.exit(1)
                    else:
                        print("token not recognized: %s" % node.getname())
                        sys.exit(1)
                while len(operator_stack) > 0:
                    if not createtree:
                        op = operator_stack.pop()
                        if op.checktype("closebracket") and op.checktype("openbracket"):
                            print("bracket mismatch in expression, to manny %s" % op.gettype())
                            sys.exit(1)
                        operand_stack.append(op)
                        self.log.writelog("expressions/generate", "push operand nodename:%s node is operator" % op.getname())
                    else:
                        op = operator_stack.pop()
                        if op.checktype("closebracket") and op.checktype("openbracket"):
                            print("bracket mismatch in expression, to manny %s" % op.gettype())
                            sys.exit(1)
                        right = operand_stack.pop()
                        left = operand_stack.pop()
                        newnode = anode(op.gettoken())
                        newnode.addleft(left)
                        newnode.addright(right)
                        operand_stack.append(newnode)
                        self.log.writelog("expressions/generate", "push operand nodename:%s node is operator" % newnode.getname())
                #self.printstack("output:", operand_stack, printtype=False)
            #self.printstacks(operator_stack, operand_stack)
            root = operand_stack.pop()
            print()
            print("Begin Tree")
            print("Tree:%s" % self.printtree(root))
            print("End Tree")
            keyidx = 0
            firsttype = None

            for k in self.optionkeys:
                print("Item:%s has Type:%s" % (k, self.optionkeys[k].gettype()))
                if keyidx == 0:
                    firsttype = self.optionkeys[k].gettype()
                else:
                    indextype = self.optionkeys[k].gettype()
                    if indextype != firsttype:
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
            self.evaluatedeepthcount = 0
            self.evaluatedepth = 0
            result = self.prepareevaluate(root)
            print("found preavluate evalsize: %d" % self.evalopsize)
            self.code.begindoevaluate(self.evalopsize, expression, self.evaluatedepth)
            result = self.evaluate(root)
            print("found real avluate evalsize: %d" % self.evalopsize)
            self.code.popvarfromstack(foundtoken, lineno=self.linenumber)
            self.optionkeys = dict()
        self.tokenlist.clear()
        self.optionkeys.clear()



