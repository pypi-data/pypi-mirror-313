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
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack1llllllll_opy_ = {}
        bstack1111111l_opy_ = os.environ.get(bstack11llll_opy_ (u"ࠨࡅࡘࡖࡗࡋࡎࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡉࡇࡔࡂࠩয"), bstack11llll_opy_ (u"ࠩࠪর"))
        if not bstack1111111l_opy_:
            return bstack1llllllll_opy_
        try:
            bstack11111111_opy_ = json.loads(bstack1111111l_opy_)
            if bstack11llll_opy_ (u"ࠥࡳࡸࠨ঱") in bstack11111111_opy_:
                bstack1llllllll_opy_[bstack11llll_opy_ (u"ࠦࡴࡹࠢল")] = bstack11111111_opy_[bstack11llll_opy_ (u"ࠧࡵࡳࠣ঳")]
            if bstack11llll_opy_ (u"ࠨ࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠥ঴") in bstack11111111_opy_ or bstack11llll_opy_ (u"ࠢࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠥ঵") in bstack11111111_opy_:
                bstack1llllllll_opy_[bstack11llll_opy_ (u"ࠣࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠦশ")] = bstack11111111_opy_.get(bstack11llll_opy_ (u"ࠤࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳࠨষ"), bstack11111111_opy_.get(bstack11llll_opy_ (u"ࠥࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳࠨস")))
            if bstack11llll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࠧহ") in bstack11111111_opy_ or bstack11llll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠥ঺") in bstack11111111_opy_:
                bstack1llllllll_opy_[bstack11llll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠦ঻")] = bstack11111111_opy_.get(bstack11llll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲ়ࠣ"), bstack11111111_opy_.get(bstack11llll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࠨঽ")))
            if bstack11llll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠦা") in bstack11111111_opy_ or bstack11llll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠦি") in bstack11111111_opy_:
                bstack1llllllll_opy_[bstack11llll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠧী")] = bstack11111111_opy_.get(bstack11llll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠢু"), bstack11111111_opy_.get(bstack11llll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠢূ")))
            if bstack11llll_opy_ (u"ࠢࡥࡧࡹ࡭ࡨ࡫ࠢৃ") in bstack11111111_opy_ or bstack11llll_opy_ (u"ࠣࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠧৄ") in bstack11111111_opy_:
                bstack1llllllll_opy_[bstack11llll_opy_ (u"ࠤࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪࠨ৅")] = bstack11111111_opy_.get(bstack11llll_opy_ (u"ࠥࡨࡪࡼࡩࡤࡧࠥ৆"), bstack11111111_opy_.get(bstack11llll_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠣে")))
            if bstack11llll_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࠢৈ") in bstack11111111_opy_ or bstack11llll_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠧ৉") in bstack11111111_opy_:
                bstack1llllllll_opy_[bstack11llll_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨ৊")] = bstack11111111_opy_.get(bstack11llll_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠥো"), bstack11111111_opy_.get(bstack11llll_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣৌ")))
            if bstack11llll_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡤࡼࡥࡳࡵ࡬ࡳࡳࠨ্") in bstack11111111_opy_ or bstack11llll_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨৎ") in bstack11111111_opy_:
                bstack1llllllll_opy_[bstack11llll_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢ৏")] = bstack11111111_opy_.get(bstack11llll_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠤ৐"), bstack11111111_opy_.get(bstack11llll_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤ৑")))
            if bstack11llll_opy_ (u"ࠣࡥࡸࡷࡹࡵ࡭ࡗࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠥ৒") in bstack11111111_opy_:
                bstack1llllllll_opy_[bstack11llll_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡘࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠦ৓")] = bstack11111111_opy_[bstack11llll_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠧ৔")]
        except Exception as error:
            logger.error(bstack11llll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡤࡷࡵࡶࡪࡴࡴࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡨࡦࡺࡡ࠻ࠢࠥ৕") +  str(error))
        return bstack1llllllll_opy_