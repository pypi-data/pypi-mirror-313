try:
    import pymysql
except ModuleNotFoundError:
    raise Exception("module not found, try: pip install pymysql")
import sys
from .basez import SimpleDv, fetch
from .structz import CMD
class Db(SimpleDv):
    # func to impl:
    def to_list(self, rst):
        result = []
        if rst is None or len(rst)==0:
            return result
        a = rst[0]
        keys = list(a.keys())
        result.append(keys)
        for obj in rst:
            v = [obj[k] for k in keys]
            result.append(v)
        return result
    def new_con(self):
        return pymysql.connect(host=self.host, 
            port = self.port, user =self.user, 
            password =self.pwd, database = self.db,
            charset='utf8',init_command="SET SESSION time_zone='+08:00'")
    def new_cursor(self):
        return self.con.cursor(pymysql.cursors.DictCursor)
    def init(self, *argv, **maps):
        if self.port is None:
            self.port = 3306
        pass

pass
def build(argv, conf):
    dv = Db(*fetch(argv))
    return dv
def buildbk(argv, conf):
    return CMD(make(argv, conf))

pass
