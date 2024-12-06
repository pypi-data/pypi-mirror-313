from .. import base
from .. import item
from .. import exp
from ... import file
import json
from . import lr
from ... import code as codez
def init():
    cs = "abfnrtv\\'\"?0123456789xcde"
    maps = {k:k.encode()[0] for k in cs}
    global c2b
    c2b = maps
    global symbal_a
    global a_map
    a_map = [0]*256
    s  = "abfnrtv\\'\"?"
    ts = b"\a\b\f\n\r\t\v\\\'\"\?"
    for c,t in zip(s, ts):
        a_map[c2b[c]] = t
    symbal_a = [False]*256
    for c in s:
        symbal_a[c2b[c]] = True
    global id_0,id_a,id_x
    id_0 = b'0'[0]
    id_a = b'a'[0]
    id_x = b'x'[0]

pass

init()
def translate_bts(bts):
    i = 0
    rs = []
    while i<len(bts):
        c = bts[i]
        i+=1
        if c!=c2b['\\']:
            rs.append(c)
            continue
        x0 = bts[i]
        i+=1
        if symbal_a[x0]:
            rs.append(a_map[x0])
            continue
        v = x0-id_0
        if v>=0 and v<=7:
            tmp = v
            for j in range(2):
                if i+j+1>=len(bts):
                    break
                xi = bts[i+j+1]
                vi = xi-id_0
                if vi>=0 and vi<=7:
                    i+=1
                    tmp = (rs<<3)+vi
                else:
                    break
            rs.append(tmp)
            continue
        if x0 == id_x:
            tmp = 0
            for j in range(2):
                if i+j+1>=len(bts):
                    raise Exception("\\xXX error")
                xi = bts[i+j+1]
                vi = xi-id_0
                if vi<0 or vi>7:
                    vi = xi-id_a
                    if vi<0 or vi > 5:
                        raise Exception("\\xXX error")
                    vi +=10
                tmp=(tmp<<4)+vi
            rs.append(tmp)
            continue
        rs.append(c)
        rs.append(x0)
        #i-=1
    return bytes(rs)

pass

class PrevStrDeal(lr.LRDeal):
    def types(self):
        if not self.deal_build:
            return []
        return ['str']
    def build(self, obj):
        if type(obj.val)==list:
            return None
        if obj.is_val:
            print("error str build")
            return obj
        obj.is_val = 1
        if self.translate:
            print("error str build tr")
            val = obj.val
            val = self.do_translate(val)
            obj.val = val
        return obj
    def prepare(self, mg):
        super().prepare(mg)
        self.label_l2 = mg.like("\\")
        self.label_qt = mg.like('"')
        self.label_et = mg.like("\n")
        self.label_lr = mg.like("\r")
        self.label_nl = mg.like("")
        self.et_in_right = self.right.count(self.label_et)
    def init(self, left = '"', right= '"', single_line = False, note = False, translate = False, deal_build = False):
        super().init(left, right, 'str')
        self.single_line = single_line
        self.note = note
        self.translate = translate
        self.deal_build = deal_build
    def json_loads(self, s):
        x = s
        cd = None
        if type(x)==bytes:
            x, cd = file.decode_c(x)
        rs = json.loads(x)
        if type(s)==bytes:
            rs = rs.encode(cd)
        return rs
    def do_translate(self, s):
        is_bytes = type(s)==bytes
        if not is_bytes:
            s = s.encode("utf-8")
        #s = translate_bts(s)
        s = codez.ubytes(s, "utf-8")
        if not is_bytes:
            s = s.decode("utf-8")
        return s
        """
            取巧直接调用json
        """
        qt = self.label_qt
        ql = self.label_l2
        et = self.label_et
        tr = self.label_lr
        nt = self.label_nl
        pt = ql+qt
        arr = s.split(pt)
        arr = [k.replace(qt, pt) for k in arr]
        s = pt.join(arr)
        #s = s.replace(qt, ql+qt)
        s = s.replace(tr, nt)
        arr = s.split(et)
        outs = [self.json_loads(qt+k+qt) for k in arr]
        outs = et.join(outs)
        return outs
    def deal(self, buffer, rst, mg):
        cl = buffer.read(self.ll)
        if cl != self.left:
            return False
        rm = buffer.full().strip()
        buffer.clean2read(self.ll)
        if len(rm)>0:
            if not self.note:
                raise Exception(f"unexcept char before string: {rm}")
            else:
                rst.append(item.Item(rm, type = "str", is_val = 0))
        tmp = cl[:0]
        ctmp = tmp[:0]
        do_judge = 1
        mark_et = 0
        mark_l2 = 0
        while True:
            if do_judge and self.right == buffer.rget(self.lr):
                break
            c = buffer.read_cache(1)
            if do_judge and c == self.label_et:
                mark_et += 1
            if len(c)==0:
                if self.single_line and self.note:
                    break
                raise Exception(f"unexcept string end while reading str")
            do_judge = 1
            if c == self.label_l2:
                mark_l2 = 1
                do_judge = 0
                c = buffer.read_cache(1)
                if len(c)==0:
                    raise Exception(f"unexcept string end while reading str")
        data = buffer.full()
        data = data[:-self.lr]
        buffer.clean()
        mark_et -= self.et_in_right
        if self.single_line and mark_et>0:
            print("left:",self.left, "right:", self.right)
            raise Exception(f"contain enter in single line string")
        if self.translate and mark_l2:
            data = self.do_translate(data)
        if self.note:
            return True
        rst.append(item.Item(data, type='str', is_val = 1))
        return True

pass
