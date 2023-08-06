#!/usr/bin/python

import sys
import re

class storelabels:

    def __init__(self):
        self.count = 0
        self.labels = dict()

    def get(self, l):
        try:
            fl = self.labels[l]
            return fl
        except KeyError:
            # print("not found: get(%s):" % l)
            return "" 

    def set(self, l, n):
        self.labels[l] = n

    def printall(self):
        print("start print all labels:")
        for l in self.labels:
            print("%20s, %20s" % (l, self.labels[l]))
        print("end print all labels:")

class parseline:

    def __init__(self, theline, cutchars):
        self.alphaset = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','_']
        self.alphaset += ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        self.numberset = ['0','1','2','3','4','5','6','7','8','9','.']
        self.operandspecials = ['(',')','$','#',',','+','-','=','/','*','.']
        self.labelchars = self.alphaset + self.numberset
        self.opcodechars = self.alphaset
        self.opcodechars = self.alphaset + self.numberset
        self.operandchars = self.alphaset + self.numberset + self.operandspecials
        self.idx = 0
        self.lastpos = 1000
        self.labeldone = False
        self.label = ""
        self.opcodedone = False
        self.opcode = ""
        self.operanddone = False
        self.operand = ""
        self.commentdone = False
        self.comment = ""
        self.original = ""
        self.line = ""
        idx = 0
        for c in theline:
            if c != "\n":
                if idx > cutchars:
                    self.line += c
                idx += 1
        if len(self.line) < cutchars:
            self.line += "          "
        self.line = self.line.lower()

    def getch(self):
        ch = self.line[self.idx]
        self.idx += 1
        if self.idx >= len(self.line):
            ch = -1 # end of line
        else:
            self.original += ch
        return ch


    def do(self, store):
        c = self.getch()
        while c != -1:
            if c == ";":
                c = self.getch()
                while c != -1:
                    c = self.getch()
                    if c == -1:
                        pass
                        # return
                    self.comment += str(c)
            elif self.idx < 2 and c in self.labelchars:
                while c in self.labelchars:
                    self.label += c
                    c = self.getch()
                    self.lastpos = self.idx
                self.labeldone = True
                # print("label found:%s" % self.label)
            elif not self.opcodedone and c in self.opcodechars:
                while c in self.opcodechars:
                    self.opcode += c
                    c = self.getch()
                self.opcodedone = True
            elif not self.operanddone and c in self.operandchars:
                while c in self.operandchars:
                    self.operand += c
                    c = self.getch()
                self.operanddone = True
                # print("operand found:%s" % self.operand )
                if self.operand == "pack2":
                    xxxxx = 0
            if self.idx < len(self.line):
                c = self.getch()
                while c == " " and self.idx < len(self.line):
                    c = self.getch()
        if len(self.label) > 0:
            newlabel = "kimpack_%s" % self.label
            store.set(self.label, newlabel)
            if self.label == "pack2":
                xxxx = 0
            # print("label:'%s' newlabel:'%s'" % (self.label, newlabel))
        if len(self.operand) > 0:
            idx = 0
            prestring = ""
            poststring = ""
            while len(self.operand) > idx and self.operand[idx] not in self.labelchars:
                prestring += self.operand[idx]
                idx += 1
            newoperand = ""
            while len(self.operand) > idx and self.operand[idx] in self.labelchars:
                newoperand += self.operand[idx]
                idx += 1
            while len(self.operand) > idx:
                poststring += self.operand[idx]
                idx += 1
            oop = store.get(newoperand)
            # print("search for: '%s' found: '%s'" % (newoperand, oop))
            if len(oop) > 0:
                if len(prestring) > 0: #  or len(poststring) > 0:
                    debug = 1
                self.operand = "%s%s%s" % (prestring, oop, poststring)
        return

    def show(self, store):    
        print("label:%-15s, opcode:%-4s, operand:%-20s, comment:%s" % (store.get(self.label), self.opcode, self.operand, self.original))

    def codeline(self, store):
        label = store.get(self.label)
        if len(label) > 0:
            print("        self.emit.createcode(\"%s\", \"%s\", \"%s\", name=\"%s\")" % (self.opcode, self.operand, self.original, label))
        else:
            print("        self.emit.createcode(\"%s\", \"%s\", \"%s\")" % (self.opcode, self.operand, self.original))
        


ifile = open("x.txt", "r")
ilines = ifile.readlines()
ifile.close()
s = storelabels()
# do it twice, the first time to collect all labels
for l in ilines:
    p = parseline(l, 15) # cut the first 16 chars, because in mathpack, this is the produced binary code
    p.do(s)
# convert all lines to python code, change labels to unique pattern (kima_ will be preprinted)
s.printall()
for l in ilines:
    p = parseline(l, 15)
    p.do(s)
    p.codeline(s)

