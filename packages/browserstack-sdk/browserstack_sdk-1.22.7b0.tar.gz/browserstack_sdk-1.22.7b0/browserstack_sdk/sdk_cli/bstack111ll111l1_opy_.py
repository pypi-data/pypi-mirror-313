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
import logging
import abc
from browserstack_sdk.sdk_cli.bstack1111llllll_opy_ import bstack1111lllll1_opy_
class bstack111l1lllll_opy_(abc.ABC):
    bin_session_id: str
    bstack1111llllll_opy_: bstack1111lllll1_opy_
    def __init__(self):
        self.bstack111l11l1ll_opy_ = None
        self.bin_session_id = None
        self.bstack1111llllll_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack111l111111_opy_(self):
        return (self.bstack111l11l1ll_opy_ != None and self.bin_session_id != None and self.bstack1111llllll_opy_ != None)
    def configure(self, bstack111l11l1ll_opy_, bin_session_id: str, bstack1111llllll_opy_: bstack1111lllll1_opy_):
        self.bstack111l11l1ll_opy_ = bstack111l11l1ll_opy_
        self.bin_session_id = bin_session_id
        self.bstack1111llllll_opy_ = bstack1111llllll_opy_
        if self.bin_session_id:
            self.logger.info(bstack11llll_opy_ (u"ࠦࡠࢁࡩࡥࠪࡶࡩࡱ࡬ࠩࡾ࡟ࠣࡧࡴࡴࡦࡪࡩࡸࡶࡪࡪࠠ࡮ࡱࡧࡹࡱ࡫ࠠࡼࡵࡨࡰ࡫࠴࡟ࡠࡥ࡯ࡥࡸࡹ࡟ࡠ࠰ࡢࡣࡳࡧ࡭ࡦࡡࡢࢁ࠿ࠦࡢࡪࡰࡢࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪ࠽ࠣ࿄") + str(self.bin_session_id) + bstack11llll_opy_ (u"ࠧࠨ࿅"))
    def bstack111l1l1lll_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstack11llll_opy_ (u"ࠨࡢࡪࡰࡢࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠠࡤࡣࡱࡲࡴࡺࠠࡣࡧࠣࡒࡴࡴࡥ࿆ࠣ"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False