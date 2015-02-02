# This file was automatically generated by SWIG (http://www.swig.org).
# Version 2.0.11
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.





from sys import version_info
if version_info >= (2,6,0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_bigNumber', [dirname(__file__)])
        except ImportError:
            import _bigNumber
            return _bigNumber
        if fp is not None:
            try:
                _mod = imp.load_module('_bigNumber', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _bigNumber = swig_import_helper()
    del swig_import_helper
else:
    import _bigNumber
del version_info
try:
    _swig_property = property
except NameError:
    pass # Python < 2.2 doesn't have 'property'.
def _swig_setattr_nondynamic(self,class_type,name,value,static=1):
    if (name == "thisown"): return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name,None)
    if method: return method(self,value)
    if (not static):
        self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)

def _swig_setattr(self,class_type,name,value):
    return _swig_setattr_nondynamic(self,class_type,name,value,0)

def _swig_getattr(self,class_type,name):
    if (name == "thisown"): return self.this.own()
    method = class_type.__swig_getmethods__.get(name,None)
    if method: return method(self)
    raise AttributeError(name)

def _swig_repr(self):
    try: strthis = "proxy of " + self.this.__repr__()
    except: strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

try:
    _object = object
    _newclass = 1
except AttributeError:
    class _object : pass
    _newclass = 0


BASE = _bigNumber.BASE
DIV_ON_ZERO = _bigNumber.DIV_ON_ZERO
class bigNumber(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, bigNumber, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, bigNumber, name)
    def __init__(self, *args): 
        this = _bigNumber.new_bigNumber(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _bigNumber.delete_bigNumber
    __del__ = lambda self : None;
    def GetString(self): return _bigNumber.bigNumber_GetString(self)
    def __str__(self): return _bigNumber.bigNumber___str__(self)
    def __repr__(self): return _bigNumber.bigNumber___repr__(self)
    def GetNumberFromFile(self, *args): return _bigNumber.bigNumber_GetNumberFromFile(self, *args)
    def SaveNumberToFile(self, *args): return _bigNumber.bigNumber_SaveNumberToFile(self, *args)
    def GetNumberFromBinFile(self, *args): return _bigNumber.bigNumber_GetNumberFromBinFile(self, *args)
    def SaveNumberInBinFile(self, *args): return _bigNumber.bigNumber_SaveNumberInBinFile(self, *args)
    def Odd(self): return _bigNumber.bigNumber_Odd(self)
    def __neg__(self): return _bigNumber.bigNumber___neg__(self)
    def __xor__(self, *args): return _bigNumber.bigNumber___xor__(self, *args)
    def __add__(self, *args): return _bigNumber.bigNumber___add__(self, *args)
    def __sub__(self, *args): return _bigNumber.bigNumber___sub__(self, *args)
    def __mul__(self, *args): return _bigNumber.bigNumber___mul__(self, *args)
    def __div__(self, *args): return _bigNumber.bigNumber___div__(self, *args)
    def __mod__(self, *args): return _bigNumber.bigNumber___mod__(self, *args)
    def __gt__(self, *args): return _bigNumber.bigNumber___gt__(self, *args)
    def __ge__(self, *args): return _bigNumber.bigNumber___ge__(self, *args)
    def __lt__(self, *args): return _bigNumber.bigNumber___lt__(self, *args)
    def __le__(self, *args): return _bigNumber.bigNumber___le__(self, *args)
    def __eq__(self, *args): return _bigNumber.bigNumber___eq__(self, *args)
    def __ne__(self, *args): return _bigNumber.bigNumber___ne__(self, *args)
bigNumber_swigregister = _bigNumber.bigNumber_swigregister
bigNumber_swigregister(bigNumber)

def GenerateRandomLen(*args):
  return _bigNumber.GenerateRandomLen(*args)
GenerateRandomLen = _bigNumber.GenerateRandomLen

def GenerateRandomMax(*args):
  return _bigNumber.GenerateRandomMax(*args)
GenerateRandomMax = _bigNumber.GenerateRandomMax


def Pow(*args):
  return _bigNumber.Pow(*args)
Pow = _bigNumber.Pow

def initRandom():
  return _bigNumber.initRandom()
initRandom = _bigNumber.initRandom
# This file is compatible with both classic and new-style classes.

