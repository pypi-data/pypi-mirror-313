
from .readz import loads, load, loadf, loads_args, loadx, is_args
from .write import dumps, dump, dumpf
from .file import *
from .mapz import *
from .xargs import fetch as args
try:
    # C加速代码
    from cxf import loads
except:
    pass
pass
__author__ = "Zzz, emails: 1174534295@qq.com, 1309458652@qq.com"
