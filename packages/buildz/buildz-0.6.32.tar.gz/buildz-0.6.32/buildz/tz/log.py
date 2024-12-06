#


from .. import xf
from .. import ioc
from ..base import Base
from ..ioc import wrap
from ..tools import *
import time, sys
class Log(Base):
    def tag(self, _tag):
        log = Log(self.shows, _tag, self)
        return log
    def get_tag(self):
        return self._tag
    def init(self, shows = None, tag= None, base = None):
        if shows is None:
            shows = ["info", "debug", "warn", "error"]
        self.shows=shows
        self._tag = tag
        self.base = base
    def xlog(self, level, *args):
        if level not in self.shows:
            return
        self.log(level, self.tag, *args)
    def log(self, level, tag, *args):
        if self.base is not None:
            return self.base.log(level, tag, *args)
        raise Exception("unimpl")
    def info(self, *args):
        if "info" not in self.shows:
            return
        self.log("info", self._tag, *args)
    def warn(self, *args):
        if "warn" not in self.shows:
            return
        self.log("warn", self._tag, *args)
    def debug(self, *args):
        if "debug" not in self.shows:
            return
        self.log("debug", self._tag, *args)
    def error(self, *args):
        if "error" not in self.shows:
            return
        self.log("error", self._tag, *args)

pass
def replaces(s, *args):
    for i in range(0,len(args),2):
        k,v = args[i],args[i+1]
        s = s.replace(k,v)
    return s

pass
def mstr(s):
    if s is None or len(s)==0:
        return s
    return s[:1].upper()+s[1:].lower()
class FpLog(Log):
    def init(self, fp = None,shows =None, tag=None, format=None):
        if format is None:
            format = "[{LEVEL}] %Y-%m-%d %H:%M:%S {tag} {msg}\n"
        self.format=format
        super().init(shows, tag)
        self.fp = fp
    def log(self, level, tag, *args):
        m_level = level.lower()
        u_level = level.upper()
        x_level = mstr(level)
        args = [str(k) for k in args]
        msg = " ".join(args)
        if tag is None:
            tag = "base"
        rst = time.strftime(self.format, time.localtime(time.time()))
        msg = replaces(rst, "{Level}", x_level, "{level}", m_level, "{LEVEL}", u_level, "{tag}", tag, "{msg}", msg)
        # rst = rst.replace("{level}",level).replace("{tag}", tag).replace
        # msg = f"[{level}] {date} {tag} {msg}\n"
        sys.stdout.write(msg)
        if self.fp is not None:
            fp = time.strftime(self.fp)
            fz.makefdir(fp)
            fz.write(msg.encode("utf-8"), fp, 'ab')

pass
