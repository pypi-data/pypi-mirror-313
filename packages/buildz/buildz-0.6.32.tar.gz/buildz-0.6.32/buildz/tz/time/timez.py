import time
from ... import Base
from ..log import FpLog
class Clock(Base):
    def default(self, cost, fc, rst, *a, **b):
        print(f"cost {cost} sec on {fc}")
    def init(self, fc=None):
        if fc is None:
            fc = self.default
        self.fc = fc
    def call(self, fc):
        curr = time.time()
        def tfc(*a,**b):
            curr = time.time()
            rst = fc(*a,**b)
            cost = time.time()-curr
            self.fc(cost, fc, rst, *a, **b)
            return rst
        return tfc

pass
clock = Clock
timecost = Clock
showcost = Clock()