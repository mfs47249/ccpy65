from storetokens import objects


class handleblocks:
    blockstack = []
    blockindex = 0
    thisblockname = ""
    functionstack = []
    activefunctionname =  ""
    blockdepth = 0

    def __init__(self, stokens):
        self.blockindex = 0
        self.thisblockname = "global"
        self.stokens = stokens

    def getactivefunctionname(self):
        return self.activefunctionname

    def setactivefunctionname(self, activename):
        self.activefunctionname = activename

    def beginblock(self, blockname, obj):
        if obj:
            self.activefunctionname = obj.getfuncname()
            self.functionstack.append(obj)
            bn = self.activefunctionname
        else:
            bn = "%s_%s_%02d" % (self.activefunctionname, blockname[0:3], self.blockdepth)
            self.stokens.addblock(bn, self.activefunctionname)
        bobject = objects(bn, "blockobject")
        bobject.setnamespace(self.activefunctionname)
        bobject.setsize(self.blockdepth)
        bobject.setvalue(blockname)
        self.blockdepth += 1
        self.blockstack.append(bobject)
        print("enter namespace:---------------------------- %s ------------------------------------" % bn)
        return bobject
    
    def popfunctionstack(self):
        lastonblockstack = self.blockstack[-1]
        lastonfuncstack = self.functionstack[-1]
        if lastonblockstack.getname() == lastonfuncstack.getfuncname():
            lastonstack = self.functionstack.pop() # remove function from stack
            lastonstack = self.functionstack[-1]   # get new top of stack
            self.activefunctionname = lastonstack.getfuncname()
        bobject = self.blockstack.pop()
        bactive = self.blockstack[-1]
        self.blockdepth -= 1
        print("leaved namespace:---------------------------- %s --- %s -----------------------------" % (bobject.getname(), bactive.getname()))
        print("active namespace is now: -------------------- %s ------------------------------------" % self.activefunctionname)
        return bobject.getname()

    def getblockonstack(self):
        lastblockonstack = self.blockstack[-1]
        # blockname = lastblockonstack.getname()
        return lastblockonstack

    def getlastfunkstack(self):
        return self.functionstack[-1]

    def lastfunction(self):
        lastobj = self.functionstack[-1]
        return lastobj

    def debugblockstack(self):
        print("debug funcstack:", end="")
        for b in self.functionstack:
            print("%s " % b.getfuncname(), end="")
        print()
        print("debug blockstack:", end="")
        for b in self.blockstack:
            print("%s " % b.getname(), end="")
        print()