#


from .. import xf
from .. import ioc
from ..base import Base
from ..ioc import wrap
from ..tools import *
import time, sys
from ..tz.log import FpLog
@wrap.obj(id="log")
@wrap.obj_sets(cache="ref,cache")
class AutoLog(FpLog):
    def call(self, maps, fp):
        fp = xf.g(maps, log = None)
        fp = self.cache.rfp(fp)
        self.fp = fp
        shows = xf.get(maps, "log.shows")
        if shows is None:
            shows = ["info", "warn", "error"]
        self.shows = shows
        format = xf.get(maps, "log.format")
        if format is not None:
            self.format = format
        #print(f"[TETSZ] format: {format}")
        return True

pass
