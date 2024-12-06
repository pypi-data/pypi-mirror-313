
import sys
import os
import hashlib
import inspect
#from .base import Base, WBase
class With:
    def __init__(self, fc_in, fc_out, args = False):
        self.fc_in = fc_in
        self.fc_out = fc_out
        self.args = args
    def __enter__(self):
        if self.fc_in is not None:
            self.fc_in()
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        rst = False
        if self.fc_out is not None:
            if self.args:
                rst = self.fc_out(exc_type, exc_val, exc_tb)
            else:
                rst = self.fc_out()
        return rst

pass
def with_out(fc, args = False):
    return With(None, fc, args)

pass
def hashcode(s):
    if type(s)==str:
        s = s.encode("utf-8")
    return hashlib.md5(s).hexdigest()

pass
def test_current(fp, up = 1, adds = []):
    """
        将当前目录的上{up}层目录加入sys.path，这样可以在同层写测试代码，但是写import的时候还是要当作是在上{up}层做import
    """
    if type(adds) not in [list, tuple]:
        adds = [adds]
    dp = os.path.dirname(os.path.abspath(fp))
    for i in range(up):
        dp = os.path.dirname(dp)
    dp = os.path.join(dp, *adds)
    sys.path.insert(0, dp)

pass
add_path = test_current
add_current = test_current
add = test_current
def load(md, fc = None):
    """
        import object(whether module or others) from md(or md.fc)
        exp:
            load("buildz.xf") = package xf
            load("buildz.xf", "loads") = function loads from package buildz.xf
            load("buildz.xf.loads") = function loads from package buildz.xf
    """
    mds = md.split(".")
    arr = mds[1:]
    while len(mds)>0:
        try:
            md = __import__(".".join(mds))
            break
        except ModuleNotFoundError as exp:
            mds = mds[:-1]
    if len(mds)==0:
        raise Exception("can't import package from "+md)
    for k in arr:
        md = getattr(md, k)
    if fc is not None:
        fc = getattr(md, fc)
    else:
        fc = md
    return fc

pass
def pyexe():
    return sys.executable

pass
exe=pyexe
is_windows = sys.platform.lower()=='win32'
def pypkg():
    """
        return python package path, test on linux and windows
    """
    import site
    sites = site.getsitepackages()
    if is_windows:
        fpath = sites[-1]
    else:
        fpath = sites[0]
    return fpath

pass
pkg = pypkg
pth = pypkg

class Pth:
    def __init__(self, fp = "build.pth"):
        self.fp = os.path.join(pth(), fp)
    def read(self):
        fp = self.fp
        if not os.path.isfile(fp):
            return []
        with open(fp, 'rb') as f:
            s = f.read().decode()
        return s.split("\n")
    def add(self, path):
        arr = self.read()
        if path in arr:
            print("alread add")
            return
        arr.append(path)
        self.write(arr)
    def write(self, paths = []):
        if type(paths) not in [list, tuple]:
            paths = [paths]
        s = "\n".join(paths)
        with open(self.fp, 'wb') as f:
            f.write(s.encode())
    def remove(self):
        os.remove(self.fp)

pass

_pth = Pth()
def main(name, fc, *args, **maps):
    if name=="__main__":
        fc(*args, **maps)

pass

def bylocals(mlocals, fc, *args, **maps):
    if mlocals['__name__']=="__main__":
        fc(*args, **maps)

pass
#lcmain=bylocals
lc_main=bylocals
lc = bylocals
local = bylocals
def mainerr(fc, *args, **maps):
    st = inspect.stack()[1]
    if st.filename == '<stdin>':
        fc(*args, **maps)
    else:
        print("not main:", st.filename)

pass
