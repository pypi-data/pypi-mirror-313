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
from collections import deque
from bstack_utils.constants import *
class bstack1ll1l11111_opy_:
    def __init__(self):
        self._1l1l11l1l11_opy_ = deque()
        self._1l1l11lll1l_opy_ = {}
        self._1l1l11ll1l1_opy_ = False
    def bstack1l1l11llll1_opy_(self, test_name, bstack1l1l11l1ll1_opy_):
        bstack1l1l11ll11l_opy_ = self._1l1l11lll1l_opy_.get(test_name, {})
        return bstack1l1l11ll11l_opy_.get(bstack1l1l11l1ll1_opy_, 0)
    def bstack1l1l1l11111_opy_(self, test_name, bstack1l1l11l1ll1_opy_):
        bstack1l1l11lll11_opy_ = self.bstack1l1l11llll1_opy_(test_name, bstack1l1l11l1ll1_opy_)
        self.bstack1l1l11l1l1l_opy_(test_name, bstack1l1l11l1ll1_opy_)
        return bstack1l1l11lll11_opy_
    def bstack1l1l11l1l1l_opy_(self, test_name, bstack1l1l11l1ll1_opy_):
        if test_name not in self._1l1l11lll1l_opy_:
            self._1l1l11lll1l_opy_[test_name] = {}
        bstack1l1l11ll11l_opy_ = self._1l1l11lll1l_opy_[test_name]
        bstack1l1l11lll11_opy_ = bstack1l1l11ll11l_opy_.get(bstack1l1l11l1ll1_opy_, 0)
        bstack1l1l11ll11l_opy_[bstack1l1l11l1ll1_opy_] = bstack1l1l11lll11_opy_ + 1
    def bstack1llll1l1l_opy_(self, bstack1l1l11lllll_opy_, bstack1l1l11l1lll_opy_):
        bstack1l1l1l1111l_opy_ = self.bstack1l1l1l11111_opy_(bstack1l1l11lllll_opy_, bstack1l1l11l1lll_opy_)
        event_name = bstack1l1ll11ll11_opy_[bstack1l1l11l1lll_opy_]
        bstack1l1l11ll111_opy_ = bstack11llll_opy_ (u"ࠦࢀࢃ࠭ࡼࡿ࠰ࡿࢂࠨᘕ").format(bstack1l1l11lllll_opy_, event_name, bstack1l1l1l1111l_opy_)
        self._1l1l11l1l11_opy_.append(bstack1l1l11ll111_opy_)
    def bstack1l111l11l1_opy_(self):
        return len(self._1l1l11l1l11_opy_) == 0
    def bstack11l111111_opy_(self):
        bstack1l1l11ll1ll_opy_ = self._1l1l11l1l11_opy_.popleft()
        return bstack1l1l11ll1ll_opy_
    def capturing(self):
        return self._1l1l11ll1l1_opy_
    def bstack11l11ll1l_opy_(self):
        self._1l1l11ll1l1_opy_ = True
    def bstack1111llll1_opy_(self):
        self._1l1l11ll1l1_opy_ = False