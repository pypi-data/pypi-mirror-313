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
from browserstack_sdk.bstack1111l1ll_opy_ import bstack11l11l11_opy_
from browserstack_sdk.bstack1l11ll11_opy_ import RobotHandler
def bstack11l1ll1l1_opy_(framework):
    if framework.lower() == bstack11llll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫᬤ"):
        return bstack11l11l11_opy_.version()
    elif framework.lower() == bstack11llll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫᬥ"):
        return RobotHandler.version()
    elif framework.lower() == bstack11llll_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ᬦ"):
        import behave
        return behave.__version__
    else:
        return bstack11llll_opy_ (u"ࠧࡶࡰ࡮ࡲࡴࡽ࡮ࠨᬧ")