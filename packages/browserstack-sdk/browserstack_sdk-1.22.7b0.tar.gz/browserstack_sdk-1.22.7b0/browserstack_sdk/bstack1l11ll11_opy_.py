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
import os
class RobotHandler():
    def __init__(self, args, logger, bstack111lll1l_opy_, bstack1111l111_opy_):
        self.args = args
        self.logger = logger
        self.bstack111lll1l_opy_ = bstack111lll1l_opy_
        self.bstack1111l111_opy_ = bstack1111l111_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack1ll111ll_opy_(bstack111llll1l1_opy_):
        bstack111lll1lll_opy_ = []
        if bstack111llll1l1_opy_:
            tokens = str(os.path.basename(bstack111llll1l1_opy_)).split(bstack11llll_opy_ (u"ࠧࡥཱࠢ"))
            camelcase_name = bstack11llll_opy_ (u"ࠨིࠠࠣ").join(t.title() for t in tokens)
            suite_name, bstack111llll111_opy_ = os.path.splitext(camelcase_name)
            bstack111lll1lll_opy_.append(suite_name)
        return bstack111lll1lll_opy_
    @staticmethod
    def bstack111llll11l_opy_(typename):
        if bstack11llll_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰཱིࠥ") in typename:
            return bstack11llll_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࡉࡷࡸ࡯ࡳࠤུ")
        return bstack11llll_opy_ (u"ࠤࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴཱུࠥ")