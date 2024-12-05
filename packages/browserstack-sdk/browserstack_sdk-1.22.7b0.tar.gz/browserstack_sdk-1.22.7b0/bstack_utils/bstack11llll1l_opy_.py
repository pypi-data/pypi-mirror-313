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
import os
import threading
from bstack_utils.helper import bstack1lll1lll11_opy_
from bstack_utils.constants import bstack1l1ll11l111_opy_
logger = logging.getLogger(__name__)
class bstack1lll1l11_opy_:
    bstack1l1l1ll1l1l_opy_ = None
    @classmethod
    def bstack1l111lllll_opy_(cls):
        if cls.on():
            logger.info(
                bstack11llll_opy_ (u"࠭ࡖࡪࡵ࡬ࡸࠥ࡮ࡴࡵࡲࡶ࠾࠴࠵࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁࠥࡺ࡯ࠡࡸ࡬ࡩࡼࠦࡢࡶ࡫࡯ࡨࠥࡸࡥࡱࡱࡵࡸ࠱ࠦࡩ࡯ࡵ࡬࡫࡭ࡺࡳ࠭ࠢࡤࡲࡩࠦ࡭ࡢࡰࡼࠤࡲࡵࡲࡦࠢࡧࡩࡧࡻࡧࡨ࡫ࡱ࡫ࠥ࡯࡮ࡧࡱࡵࡱࡦࡺࡩࡰࡰࠣࡥࡱࡲࠠࡢࡶࠣࡳࡳ࡫ࠠࡱ࡮ࡤࡧࡪࠧ࡜࡯ࠩᖮ").format(os.environ[bstack11llll_opy_ (u"ࠢࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉࠨᖯ")]))
    @classmethod
    def on(cls):
        if os.environ.get(bstack11llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬᖰ"), None) is None or os.environ[bstack11llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭ᖱ")] == bstack11llll_opy_ (u"ࠥࡲࡺࡲ࡬ࠣᖲ"):
            return False
        return True
    @classmethod
    def bstack1l1l1lll11l_opy_(cls, bs_config, framework=bstack11llll_opy_ (u"ࠦࠧᖳ")):
        if framework == bstack11llll_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬᖴ"):
            return bstack1lll1lll11_opy_(bs_config.get(bstack11llll_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪᖵ")))
        bstack1l1l1llll11_opy_ = framework in bstack1l1ll11l111_opy_
        return bstack1lll1lll11_opy_(bs_config.get(bstack11llll_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫᖶ"), bstack1l1l1llll11_opy_))
    @classmethod
    def bstack1l1l1lll111_opy_(cls, framework):
        return framework in bstack1l1ll11l111_opy_
    @classmethod
    def bstack1l1l1lll1ll_opy_(cls, bs_config, framework):
        return cls.bstack1l1l1lll11l_opy_(bs_config, framework) is True and cls.bstack1l1l1lll111_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack11llll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬᖷ"), None)
    @staticmethod
    def bstack11lll11l_opy_():
        if getattr(threading.current_thread(), bstack11llll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ᖸ"), None):
            return {
                bstack11llll_opy_ (u"ࠪࡸࡾࡶࡥࠨᖹ"): bstack11llll_opy_ (u"ࠫࡹ࡫ࡳࡵࠩᖺ"),
                bstack11llll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᖻ"): getattr(threading.current_thread(), bstack11llll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪᖼ"), None)
            }
        if getattr(threading.current_thread(), bstack11llll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᖽ"), None):
            return {
                bstack11llll_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᖾ"): bstack11llll_opy_ (u"ࠩ࡫ࡳࡴࡱࠧᖿ"),
                bstack11llll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᗀ"): getattr(threading.current_thread(), bstack11llll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᗁ"), None)
            }
        return None
    @staticmethod
    def bstack1l1l1ll1lll_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1lll1l11_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack1ll111ll_opy_(test, hook_name=None):
        bstack1l1l1llll1l_opy_ = test.parent
        if hook_name in [bstack11llll_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡨࡲࡡࡴࡵࠪᗂ"), bstack11llll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠧᗃ"), bstack11llll_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭ᗄ"), bstack11llll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪᗅ")]:
            bstack1l1l1llll1l_opy_ = test
        scope = []
        while bstack1l1l1llll1l_opy_ is not None:
            scope.append(bstack1l1l1llll1l_opy_.name)
            bstack1l1l1llll1l_opy_ = bstack1l1l1llll1l_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1l1l1lll1l1_opy_(hook_type):
        if hook_type == bstack11llll_opy_ (u"ࠤࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠢᗆ"):
            return bstack11llll_opy_ (u"ࠥࡗࡪࡺࡵࡱࠢ࡫ࡳࡴࡱࠢᗇ")
        elif hook_type == bstack11llll_opy_ (u"ࠦࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠣᗈ"):
            return bstack11llll_opy_ (u"࡚ࠧࡥࡢࡴࡧࡳࡼࡴࠠࡩࡱࡲ࡯ࠧᗉ")
    @staticmethod
    def bstack1l1l1ll1ll1_opy_(bstack111l1111_opy_):
        try:
            if not bstack1lll1l11_opy_.on():
                return bstack111l1111_opy_
            if os.environ.get(bstack11llll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࠦᗊ"), None) == bstack11llll_opy_ (u"ࠢࡵࡴࡸࡩࠧᗋ"):
                tests = os.environ.get(bstack11llll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓࡥࡔࡆࡕࡗࡗࠧᗌ"), None)
                if tests is None or tests == bstack11llll_opy_ (u"ࠤࡱࡹࡱࡲࠢᗍ"):
                    return bstack111l1111_opy_
                bstack111l1111_opy_ = tests.split(bstack11llll_opy_ (u"ࠪ࠰ࠬᗎ"))
                return bstack111l1111_opy_
        except Exception as exc:
            print(bstack11llll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡶࡪࡸࡵ࡯ࠢ࡫ࡥࡳࡪ࡬ࡦࡴ࠽ࠤࠧᗏ"), str(exc))
        return bstack111l1111_opy_