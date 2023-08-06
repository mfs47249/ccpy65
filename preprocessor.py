from os.path import join, exists
import sys

class preprocessor:
    debug = False

    def __init__(self, searchpath, debugflag=False):
        self.debug = debugflag
        print("%30s, preprocessor search path:'%s'" % (self.func_name(), searchpath))

    def func_name(self):
        classname = __class__.__name__
        funcname = sys._getframe(1).f_code.co_name
        return classname + '.' + funcname

    def processline(self, preproline):
        if self.debug:
            print("%30s, preproline:'%s'" % (self.func_name(), preproline))

if __name__ == "__main__":
    print("preprocessor Unit")