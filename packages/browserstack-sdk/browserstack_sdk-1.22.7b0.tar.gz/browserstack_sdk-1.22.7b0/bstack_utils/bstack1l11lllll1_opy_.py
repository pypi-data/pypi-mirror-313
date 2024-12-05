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
class bstack1l1llll11l_opy_:
    def __init__(self, handler):
        self._1l1ll11111l_opy_ = None
        self.handler = handler
        self._1l1l1llllll_opy_ = self.bstack1l1ll111111_opy_()
        self.patch()
    def patch(self):
        self._1l1ll11111l_opy_ = self._1l1l1llllll_opy_.execute
        self._1l1l1llllll_opy_.execute = self.bstack1l1l1lllll1_opy_()
    def bstack1l1l1lllll1_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack11llll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࠦᖬ"), driver_command, None, this, args)
            response = self._1l1ll11111l_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack11llll_opy_ (u"ࠧࡧࡦࡵࡧࡵࠦᖭ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1l1l1llllll_opy_.execute = self._1l1ll11111l_opy_
    @staticmethod
    def bstack1l1ll111111_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver