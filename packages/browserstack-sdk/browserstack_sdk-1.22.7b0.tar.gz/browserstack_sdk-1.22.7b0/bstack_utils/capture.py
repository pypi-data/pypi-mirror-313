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
import builtins
import logging
class bstack1ll11l1l_opy_:
    def __init__(self, handler):
        self._1l1l1l111l1_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._1l1l1l11ll1_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack11llll_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧᘌ"), bstack11llll_opy_ (u"ࠪࡨࡪࡨࡵࡨࠩᘍ"), bstack11llll_opy_ (u"ࠫࡼࡧࡲ࡯࡫ࡱ࡫ࠬᘎ"), bstack11llll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᘏ")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._1l1l1l11l11_opy_
        self._1l1l1l11l1l_opy_()
    def _1l1l1l11l11_opy_(self, *args, **kwargs):
        self._1l1l1l111l1_opy_(*args, **kwargs)
        message = bstack11llll_opy_ (u"࠭ࠠࠨᘐ").join(map(str, args)) + bstack11llll_opy_ (u"ࠧ࡝ࡰࠪᘑ")
        self._log_message(bstack11llll_opy_ (u"ࠨࡋࡑࡊࡔ࠭ᘒ"), message)
    def _log_message(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack11llll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᘓ"): level, bstack11llll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᘔ"): msg})
    def _1l1l1l11l1l_opy_(self):
        for level, bstack1l1l1l11lll_opy_ in self._1l1l1l11ll1_opy_.items():
            setattr(logging, level, self._1l1l1l111ll_opy_(level, bstack1l1l1l11lll_opy_))
    def _1l1l1l111ll_opy_(self, level, bstack1l1l1l11lll_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack1l1l1l11lll_opy_(msg, *args, **kwargs)
            self._log_message(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._1l1l1l111l1_opy_
        for level, bstack1l1l1l11lll_opy_ in self._1l1l1l11ll1_opy_.items():
            setattr(logging, level, bstack1l1l1l11lll_opy_)