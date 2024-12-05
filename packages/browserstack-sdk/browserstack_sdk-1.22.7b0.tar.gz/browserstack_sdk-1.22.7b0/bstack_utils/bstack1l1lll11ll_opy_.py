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
import logging
import bstack_utils.accessibility as bstack11111l11_opy_
from bstack_utils.helper import bstack1ll111l1_opy_
logger = logging.getLogger(__name__)
def bstack1lll1l1111_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False
def bstack1llll11l1_opy_(context, *args):
    tags = getattr(args[0], bstack11llll_opy_ (u"ࠧࡵࡣࡪࡷࠬᘃ"), [])
    bstack1lllll1lll_opy_ = bstack11111l11_opy_.bstack11l1ll1ll1_opy_(tags)
    threading.current_thread().isA11yTest = bstack1lllll1lll_opy_
    try:
      bstack1l1ll1lll1_opy_ = threading.current_thread().bstackSessionDriver if bstack1lll1l1111_opy_(bstack11llll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧᘄ")) else context.browser
      if bstack1l1ll1lll1_opy_ and bstack1l1ll1lll1_opy_.session_id and bstack1lllll1lll_opy_ and bstack1ll111l1_opy_(
              threading.current_thread(), bstack11llll_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨᘅ"), None):
          threading.current_thread().isA11yTest = bstack11111l11_opy_.bstack1lllll11ll_opy_(bstack1l1ll1lll1_opy_, bstack1lllll1lll_opy_)
    except Exception as e:
       logger.debug(bstack11llll_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡧ࠱࠲ࡻࠣ࡭ࡳࠦࡢࡦࡪࡤࡺࡪࡀࠠࡼࡿࠪᘆ").format(str(e)))
def bstack1l1ll1l1ll_opy_(bstack1l1ll1lll1_opy_):
    if bstack1ll111l1_opy_(threading.current_thread(), bstack11llll_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨᘇ"), None) and bstack1ll111l1_opy_(
      threading.current_thread(), bstack11llll_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫᘈ"), None) and not bstack1ll111l1_opy_(threading.current_thread(), bstack11llll_opy_ (u"࠭ࡡ࠲࠳ࡼࡣࡸࡺ࡯ࡱࠩᘉ"), False):
      threading.current_thread().a11y_stop = True
      bstack11111l11_opy_.bstack11111l1l_opy_(bstack1l1ll1lll1_opy_, name=bstack11llll_opy_ (u"ࠢࠣᘊ"), path=bstack11llll_opy_ (u"ࠣࠤᘋ"))