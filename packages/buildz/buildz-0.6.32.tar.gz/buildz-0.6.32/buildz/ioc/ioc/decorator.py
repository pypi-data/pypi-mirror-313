#coding=utf-8
from buildz.base import Base
from buildz import xf
from threading import Lock
class Decorator(Base):
    def init(self):
        self.conf = {}
        self.confs = {}
        self.confs[None] = self.conf
        self.namespace = None
        self.fcs = {}
        self._ns = {}
        self.regist("add_datas", self.add_datas)
    def fcns(self, namespace, fc):
        self._ns[fc] = namespace
    def ns(self, namespace):
        self.namespace = namespace
    def curr_ns(self):
        return self.namespace
    def regist(self, key, fc):
        self.fcs[key] = fc
    def get_conf(self, src):
        ns = self.namespace
        if src in self._ns:
            ns = self._ns[src]
        if ns not in self.confs:
            conf = {}
            conf['namespace'] = ns
            self.confs[ns] = conf
        return self.confs[ns]
    def get(self, tag, index, src=None):
        conf = self.get_conf(src)
        if tag not in conf:
            conf[tag]=[]
        return conf[tag][index]
    def add(self, tag, data, src = None):
        conf = self.get_conf(src)
        if tag not in conf:
            conf[tag]=[]
        id = len(conf[tag])
        conf[tag].append(data)
        return id
    def set(self, tag, key, val, src=None):
        conf = self.get_conf(src)
        if tag not in conf:
            conf[tag]={}
        conf[tag][key]=val
    def add_datas(self, item, key):
        if type(item)==str:
            item = xf.loads(item)
        return self.add("datas", item, key)
    def get_datas(self, id):
        return self.get("datas", id)
    def set_datas(self, id, val):
        return self.set("datas", id, val)
    def set_envs(self, key, val):
        return self.set("env", key, val)
    def add_inits(self, val):
        return self.add("inits", val)
    def add_locals(self, item):
        return self.add("locals", item)
    def all(self):
        arr = [val for k,val in self.confs.items()]
        return arr
    def call(self):
        return self.conf

pass

decorator = Decorator()
class Fcs:
    pass

pass
class NameSpace(Base):
    def init(self, decorator):
        self.decorator = decorator
        self.lock = Lock()
    def fc(self, namespace, rfc):
        def wfc(*a, **b):
            with self.lock:
                ns = self.decorator.curr_ns()
                self.decorator.ns(namespace)
                rst = rfc(*a,**b)
                self.decorator.fcns(namespace, rst)
                self.decorator.ns(ns)
                return rst
        return wfc
    def call(self, namespace):
        fcs = self.decorator.fcs
        obj = Fcs()
        for k,f in fcs.items():
            setattr(obj, k, self.fc(namespace, f))
        return obj

pass
ns = NameSpace(decorator)