# coding: UTF-8
import sys
bstack1l11lll_opy_ = sys.version_info [0] == 2
bstack1ll11ll_opy_ = 2048
bstack1l1_opy_ = 7
def bstack11llll_opy_ (bstack11lllll_opy_):
    global bstack1111111_opy_
    bstack111l11l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack11lllll_opy_ [:-1]
    bstack11l11ll_opy_ = bstack111l11l_opy_ % len (bstack1l11l1l_opy_)
    bstack11l1111_opy_ = bstack1l11l1l_opy_ [:bstack11l11ll_opy_] + bstack1l11l1l_opy_ [bstack11l11ll_opy_:]
    if bstack1l11lll_opy_:
        bstack11lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11ll_opy_ - (bstack1111lll_opy_ + bstack111l11l_opy_) % bstack1l1_opy_) for bstack1111lll_opy_, char in enumerate (bstack11l1111_opy_)])
    else:
        bstack11lll_opy_ = str () .join ([chr (ord (char) - bstack1ll11ll_opy_ - (bstack1111lll_opy_ + bstack111l11l_opy_) % bstack1l1_opy_) for bstack1111lll_opy_, char in enumerate (bstack11l1111_opy_)])
    return eval (bstack11lll_opy_)
import threading
bstack1l1l111ll1l_opy_ = 1000
bstack1l1l111l1l1_opy_ = 5
bstack1l1l111l1ll_opy_ = 30
bstack1l1l111ll11_opy_ = 2
class bstack1l1l111l11l_opy_:
    def __init__(self, handler, bstack1l1l111llll_opy_=bstack1l1l111ll1l_opy_, bstack1l1l11l11ll_opy_=bstack1l1l111l1l1_opy_):
        self.queue = []
        self.handler = handler
        self.bstack1l1l111llll_opy_ = bstack1l1l111llll_opy_
        self.bstack1l1l11l11ll_opy_ = bstack1l1l11l11ll_opy_
        self.lock = threading.Lock()
        self.timer = None
    def start(self):
        if not self.timer:
            self.bstack1l1l111lll1_opy_()
    def bstack1l1l111lll1_opy_(self):
        self.timer = threading.Timer(self.bstack1l1l11l11ll_opy_, self.bstack1l1l11l111l_opy_)
        self.timer.start()
    def bstack1l1l11l11l1_opy_(self):
        self.timer.cancel()
    def bstack1l1l11l1111_opy_(self):
        self.bstack1l1l11l11l1_opy_()
        self.bstack1l1l111lll1_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack1l1l111llll_opy_:
                t = threading.Thread(target=self.bstack1l1l11l111l_opy_)
                t.start()
                self.bstack1l1l11l1111_opy_()
    def bstack1l1l11l111l_opy_(self):
        if len(self.queue) <= 0:
            return
        data = self.queue[:self.bstack1l1l111llll_opy_]
        del self.queue[:self.bstack1l1l111llll_opy_]
        self.handler(data)
    def shutdown(self):
        self.bstack1l1l11l11l1_opy_()
        while len(self.queue) > 0:
            self.bstack1l1l11l111l_opy_()