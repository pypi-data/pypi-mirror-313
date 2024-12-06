#coding=utf-8
from . import pyz
class Base:
    def str(self):
        return str(self.__class__)
    def __str__(self):
        return self.str()
    def __repr__(self):
        return self.__str__()
    def __init__(self, *args, **maps):
        self.init(*args, **maps)
    def __call__(self, *args, **maps):
        return self.call(*args, **maps)
    def init(self, *args, **maps):
        pass
    def call(self, *args, **maps):
        return self.deal(*args, **maps)
    def deal(self, *args, **maps):
        return None

pass

class WBase(Base):
    def _open(self):
        pass
    def open(self):
        self._open()
        return pyz.with_out(self.close, True)
    def _close(self):
        pass
    def close(self, exc_type, exc_val, exc_tb):
        self._close()

pass

class With(Base):
    def init(self, args=False):
        self.args = args
    def call(self, cls):
        def _open(obj):
            pass
        def open(obj):
            obj._open()
            return pyz.with_out(obj.close, self.args)
        def _close(obj):
            pass
        def close(obj):
            obj._close()
        cls._open = _open
        cls._close = _close
        cls.open = open
        cls.close = close
        return cls

pass
