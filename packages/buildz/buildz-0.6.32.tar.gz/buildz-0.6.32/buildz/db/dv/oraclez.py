
import os
import sys
dp = os.path.dirname(__file__)
gdp = os.path.join(dp, "lib")

def init_path(dp):
    path = os.environ["PATH"] 
    if sys.platform.lower().find("win")>=0:
        cb = ";"
    else:
        cb = ":"
    path = path +cb+dp
    os.environ["PATH"] = path

pass

#init_path(dp)
import sys
from .basez import SimpleDv, fetch
from .structz import CMD
class Db(SimpleDv):
    # func to impl:
    def to_list(self, rst):
        rows = self.cursor.description
        keys = [k[0].lower() for k in rows]
        result = []
        result.append(keys)
        if rst is None or len(rst)==0:
            return result
        result += rst
        return result
    def new_con(self):
        if self.port is not None:
            add = ":"+str(self.port)
        else:
            add = ""
        try:
            import cx_Oracle as pymysql
        except ModuleNotFoundError:
            raise Exception("module not found, try: pip install cx-Oracle")
        return pymysql.connect(self.user, self.pwd, self.host+add+"/"+self.db)
    def new_cursor(self):
        return self.con.cursor()
    def init(self, *argv, **maps):
        pass

pass
def build(argv, conf):
    k = 'oracle_lib'
    dp = gdp
    if k in conf:
        dp = conf[k]
    init_path(dp)
    #print(f"oracle lib: {dp}")
    dv = Db(*fetch(argv))
    return dv
def buildbk(argv, conf):
    return CMD(make(argv, conf))

pass
