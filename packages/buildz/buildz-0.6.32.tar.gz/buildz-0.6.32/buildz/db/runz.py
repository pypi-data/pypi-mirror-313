
import sys
import os
import time
from buildz import xf
FP = "run.conf"
def find(arr, k, base = 0):
    for i in range(base, len(arr)):
        if arr[i]==k:
            return i
    return -1

pass
if __name__ == "__main__":
    from dv import build
    from dv.structz import CMD
else:
    from .dv import build
    from .dv.structz import CMD

pass
def cmd(conf):
    obj = conf
    dv = obj['dv']
    db_url = obj['db']
    db_url = obj[db_url]
    user = xf.g(obj,user=None)
    pwd = xf.g(obj,pwd=None)
    src = obj['src']
    out = obj['out']
    cmd = CMD(build(dv, [db_url, user, pwd], obj))
    return cmd

pass
def test(fp):
    obj = xf.loads(xf.fread(fp))
    dv = obj['dv']
    db_url = obj['db']
    db_url = obj[db_url]
    user = xf.g(obj,user=None)
    pwd = xf.g(obj,pwd=None)
    src = obj['src']
    out = obj['out']
    sqls = xf.fread(src)
    sqls = sqls.replace("\r\n", "\n").rstrip().split("\n")
    sqls_strip = [k.strip() for k in sqls]
    i = find(sqls_strip, "!!begin")
    bi = i
    if i < 0:
        bi=0
    j = find(sqls_strip, "!!end", bi)
    sqls = sqls[i+1:j]
    sqls = [k for k in sqls if k.lstrip()[:2]!="--"]
    sqls = "\n".join(sqls)
    sqls = sqls.split(";")
    print(f"[TESTZ] sqls:{sqls}")
    cmd = CMD(build(dv, [db_url, user, pwd], obj))
    cmd.dv.begin()
    print("[TESTZ] A")
    with open(out, 'wb') as f:
        f.write(b"[START SQL]\n\n")
    for sql in sqls:
        if sql.strip()=="":
            continue
        if sql.strip() == "exit":
            break
        print("[TESTZ] B")
        curr=time.time()
        rst = cmd.single(sql)
        cost = time.time()-curr
        print(f"[TESTZ] Cost: {cost} sec")
        rst += f"time cost: {cost} sec\n"
        with open(out, 'ab') as f:
            f.write(rst.encode("utf-8"))
    with open(out, 'ab') as f:
        f.write(b"\n[DONE SQL]")
    cmd.close()

pass
class Runner:
    def __init__(self, fp):
        self.fp = fp
    def init(self):
        self.obj = xf.loads(xf.fread(self.fp))
        self.fps = [self.fp, self.obj['src']]
        self.fps = [os.path.abspath(fp) for fp in self.fps]
        self.curr = [0,0]
    def run(self):
        while True:
            secs = [os.path.getmtime(fp) for fp in self.fps]
            if self.curr != secs:
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "done update")
                self.init()
                self.curr = secs
                test(self.fp)
            time.sleep(float(self.obj['sec']))

pass

def run(fp):
    r = Runner(fp)
    r.init()
    r.run()

pass
def main():
    fp = FP
    if len(sys.argv)>1:
        fp = sys.argv[1]
    return run(fp)

pass

if __name__=="__main__":
    main()

pass
