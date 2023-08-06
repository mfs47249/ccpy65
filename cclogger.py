import sys

class cclogger:

    def __init__(self, logfilepath):
        self.logfilepath = logfilepath
        self.lf = open(self.logfilepath, "w")

    def writelog(self, tag, logitem):
        self.logitem = logitem
        self.lf.write("%20s: %s\n" % (tag, self.logitem))

    def close(self):
        self.lf.close()
