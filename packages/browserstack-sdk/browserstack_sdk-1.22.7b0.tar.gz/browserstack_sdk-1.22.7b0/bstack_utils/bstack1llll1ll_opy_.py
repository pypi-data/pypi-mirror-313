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
import json
import logging
import os
import datetime
import threading
from bstack_utils.helper import bstack1l11lll111l_opy_, bstack1l11llll1l1_opy_, bstack1l1111l1l_opy_, bstack1l11llll_opy_, bstack1l1l1111111_opy_, bstack1l11l11l111_opy_, bstack1l11ll11ll1_opy_, bstack1l111ll1_opy_
from bstack_utils.bstack1l1l1ll1l1l_opy_ import bstack1l1l111l11l_opy_
import bstack_utils.bstack1l1l1lll1l_opy_ as bstack1lllll111l_opy_
from bstack_utils.bstack11llll1l_opy_ import bstack1lll1l11_opy_
import bstack_utils.accessibility as bstack11111l11_opy_
from bstack_utils.bstack11ll11l1l1_opy_ import bstack11ll11l1l1_opy_
from bstack_utils.bstack1l1l1lll_opy_ import bstack11lll1ll_opy_
bstack11ll11lll1l_opy_ = bstack11llll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡣࡰ࡮࡯ࡩࡨࡺ࡯ࡳ࠯ࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬ᧿")
logger = logging.getLogger(__name__)
class bstack1lll11ll_opy_:
    bstack1l1l1ll1l1l_opy_ = None
    bs_config = None
    bstack1l11ll111_opy_ = None
    @classmethod
    @bstack1l11llll_opy_(class_method=True)
    def launch(cls, bs_config, bstack1l11ll111_opy_):
        cls.bs_config = bs_config
        cls.bstack1l11ll111_opy_ = bstack1l11ll111_opy_
        try:
            cls.bstack11ll1l11lll_opy_()
            bstack11ll1l1llll_opy_ = bstack1l11lll111l_opy_(bs_config)
            bstack11ll1llll1l_opy_ = bstack1l11llll1l1_opy_(bs_config)
            data = bstack1lllll111l_opy_.bstack11ll1l1111l_opy_(bs_config, bstack1l11ll111_opy_)
            config = {
                bstack11llll_opy_ (u"࠭ࡡࡶࡶ࡫ࠫᨀ"): (bstack11ll1l1llll_opy_, bstack11ll1llll1l_opy_),
                bstack11llll_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨᨁ"): cls.default_headers()
            }
            response = bstack1l1111l1l_opy_(bstack11llll_opy_ (u"ࠨࡒࡒࡗ࡙࠭ᨂ"), cls.request_url(bstack11llll_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠳࠱ࡥࡹ࡮ࡲࡤࡴࠩᨃ")), data, config)
            if response.status_code != 200:
                bstack1lll1llllll_opy_ = response.json()
                if bstack1lll1llllll_opy_[bstack11llll_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫᨄ")] == False:
                    cls.bstack11ll11lll11_opy_(bstack1lll1llllll_opy_)
                    return
                cls.bstack11ll1l111l1_opy_(bstack1lll1llllll_opy_[bstack11llll_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫᨅ")])
                cls.bstack11ll11llll1_opy_(bstack1lll1llllll_opy_[bstack11llll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᨆ")])
                return None
            bstack11ll1l1ll1l_opy_ = cls.bstack11ll1l111ll_opy_(response)
            return bstack11ll1l1ll1l_opy_
        except Exception as error:
            logger.error(bstack11llll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡦࡺ࡯࡬ࡥࠢࡩࡳࡷࠦࡔࡦࡵࡷࡌࡺࡨ࠺ࠡࡽࢀࠦᨇ").format(str(error)))
            return None
    @classmethod
    @bstack1l11llll_opy_(class_method=True)
    def stop(cls, bstack11ll1l11l11_opy_=None):
        if not bstack1lll1l11_opy_.on() and not bstack11111l11_opy_.on():
            return
        if os.environ.get(bstack11llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫᨈ")) == bstack11llll_opy_ (u"ࠣࡰࡸࡰࡱࠨᨉ") or os.environ.get(bstack11llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧᨊ")) == bstack11llll_opy_ (u"ࠥࡲࡺࡲ࡬ࠣᨋ"):
            logger.error(bstack11llll_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡹࡵࡰࠡࡤࡸ࡭ࡱࡪࠠࡳࡧࡴࡹࡪࡹࡴࠡࡶࡲࠤ࡙࡫ࡳࡵࡊࡸࡦ࠿ࠦࡍࡪࡵࡶ࡭ࡳ࡭ࠠࡢࡷࡷ࡬ࡪࡴࡴࡪࡥࡤࡸ࡮ࡵ࡮ࠡࡶࡲ࡯ࡪࡴࠧᨌ"))
            return {
                bstack11llll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᨍ"): bstack11llll_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬᨎ"),
                bstack11llll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᨏ"): bstack11llll_opy_ (u"ࠨࡖࡲ࡯ࡪࡴ࠯ࡣࡷ࡬ࡰࡩࡏࡄࠡ࡫ࡶࠤࡺࡴࡤࡦࡨ࡬ࡲࡪࡪࠬࠡࡤࡸ࡭ࡱࡪࠠࡤࡴࡨࡥࡹ࡯࡯࡯ࠢࡰ࡭࡬࡮ࡴࠡࡪࡤࡺࡪࠦࡦࡢ࡫࡯ࡩࡩ࠭ᨐ")
            }
        try:
            cls.bstack1l1l1ll1l1l_opy_.shutdown()
            data = {
                bstack11llll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᨑ"): bstack1l111ll1_opy_()
            }
            if not bstack11ll1l11l11_opy_ is None:
                data[bstack11llll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡳࡥࡵࡣࡧࡥࡹࡧࠧᨒ")] = [{
                    bstack11llll_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫᨓ"): bstack11llll_opy_ (u"ࠬࡻࡳࡦࡴࡢ࡯࡮ࡲ࡬ࡦࡦࠪᨔ"),
                    bstack11llll_opy_ (u"࠭ࡳࡪࡩࡱࡥࡱ࠭ᨕ"): bstack11ll1l11l11_opy_
                }]
            config = {
                bstack11llll_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨᨖ"): cls.default_headers()
            }
            bstack1l11l1lll1l_opy_ = bstack11llll_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀ࠳ࡸࡺ࡯ࡱࠩᨗ").format(os.environ[bstack11llll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊᨘࠢ")])
            bstack11ll1l1ll11_opy_ = cls.request_url(bstack1l11l1lll1l_opy_)
            response = bstack1l1111l1l_opy_(bstack11llll_opy_ (u"ࠪࡔ࡚࡚ࠧᨙ"), bstack11ll1l1ll11_opy_, data, config)
            if not response.ok:
                raise Exception(bstack11llll_opy_ (u"ࠦࡘࡺ࡯ࡱࠢࡵࡩࡶࡻࡥࡴࡶࠣࡲࡴࡺࠠࡰ࡭ࠥᨚ"))
        except Exception as error:
            logger.error(bstack11llll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸࡺ࡯ࡱࠢࡥࡹ࡮ࡲࡤࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡷࡳ࡚ࠥࡥࡴࡶࡋࡹࡧࡀ࠺ࠡࠤᨛ") + str(error))
            return {
                bstack11llll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭᨜"): bstack11llll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭᨝"),
                bstack11llll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ᨞"): str(error)
            }
    @classmethod
    @bstack1l11llll_opy_(class_method=True)
    def bstack11ll1l111ll_opy_(cls, response):
        bstack1lll1llllll_opy_ = response.json() if not isinstance(response, dict) else response
        bstack11ll1l1ll1l_opy_ = {}
        if bstack1lll1llllll_opy_.get(bstack11llll_opy_ (u"ࠩ࡭ࡻࡹ࠭᨟")) is None:
            os.environ[bstack11llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧᨠ")] = bstack11llll_opy_ (u"ࠫࡳࡻ࡬࡭ࠩᨡ")
        else:
            os.environ[bstack11llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩᨢ")] = bstack1lll1llllll_opy_.get(bstack11llll_opy_ (u"࠭ࡪࡸࡶࠪᨣ"), bstack11llll_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬᨤ"))
        os.environ[bstack11llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ᨥ")] = bstack1lll1llllll_opy_.get(bstack11llll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫᨦ"), bstack11llll_opy_ (u"ࠪࡲࡺࡲ࡬ࠨᨧ"))
        if bstack1lll1l11_opy_.bstack1l1l1lll1ll_opy_(cls.bs_config, cls.bstack1l11ll111_opy_.get(bstack11llll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡶࡵࡨࡨࠬᨨ"), bstack11llll_opy_ (u"ࠬ࠭ᨩ"))) is True:
            bstack11ll11l1l1l_opy_, bstack11llll1111_opy_, bstack11ll1l1l111_opy_ = cls.bstack11ll11ll11l_opy_(bstack1lll1llllll_opy_)
            if bstack11ll11l1l1l_opy_ != None and bstack11llll1111_opy_ != None:
                bstack11ll1l1ll1l_opy_[bstack11llll_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ᨪ")] = {
                    bstack11llll_opy_ (u"ࠧ࡫ࡹࡷࡣࡹࡵ࡫ࡦࡰࠪᨫ"): bstack11ll11l1l1l_opy_,
                    bstack11llll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪᨬ"): bstack11llll1111_opy_,
                    bstack11llll_opy_ (u"ࠩࡤࡰࡱࡵࡷࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭ᨭ"): bstack11ll1l1l111_opy_
                }
            else:
                bstack11ll1l1ll1l_opy_[bstack11llll_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪᨮ")] = {}
        else:
            bstack11ll1l1ll1l_opy_[bstack11llll_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫᨯ")] = {}
        if bstack11111l11_opy_.bstack11ll1ll1111_opy_(cls.bs_config) is True:
            bstack11ll11l11ll_opy_, bstack11llll1111_opy_ = cls.bstack11ll11ll111_opy_(bstack1lll1llllll_opy_)
            if bstack11ll11l11ll_opy_ != None and bstack11llll1111_opy_ != None:
                bstack11ll1l1ll1l_opy_[bstack11llll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᨰ")] = {
                    bstack11llll_opy_ (u"࠭ࡡࡶࡶ࡫ࡣࡹࡵ࡫ࡦࡰࠪᨱ"): bstack11ll11l11ll_opy_,
                    bstack11llll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩᨲ"): bstack11llll1111_opy_,
                }
            else:
                bstack11ll1l1ll1l_opy_[bstack11llll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᨳ")] = {}
        else:
            bstack11ll1l1ll1l_opy_[bstack11llll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᨴ")] = {}
        if bstack11ll1l1ll1l_opy_[bstack11llll_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪᨵ")].get(bstack11llll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ᨶ")) != None or bstack11ll1l1ll1l_opy_[bstack11llll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᨷ")].get(bstack11llll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨᨸ")) != None:
            cls.bstack11ll11lllll_opy_(bstack1lll1llllll_opy_.get(bstack11llll_opy_ (u"ࠧ࡫ࡹࡷࠫᨹ")), bstack1lll1llllll_opy_.get(bstack11llll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪᨺ")))
        return bstack11ll1l1ll1l_opy_
    @classmethod
    def bstack11ll11ll11l_opy_(cls, bstack1lll1llllll_opy_):
        if bstack1lll1llllll_opy_.get(bstack11llll_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩᨻ")) == None:
            cls.bstack11ll1l111l1_opy_()
            return [None, None, None]
        if bstack1lll1llllll_opy_[bstack11llll_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪᨼ")][bstack11llll_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬᨽ")] != True:
            cls.bstack11ll1l111l1_opy_(bstack1lll1llllll_opy_[bstack11llll_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬᨾ")])
            return [None, None, None]
        logger.debug(bstack11llll_opy_ (u"࠭ࡔࡦࡵࡷࠤࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠤࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲ࡙ࠥࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭ࠣࠪᨿ"))
        os.environ[bstack11llll_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡇࡔࡓࡐࡍࡇࡗࡉࡉ࠭ᩀ")] = bstack11llll_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᩁ")
        if bstack1lll1llllll_opy_.get(bstack11llll_opy_ (u"ࠩ࡭ࡻࡹ࠭ᩂ")):
            os.environ[bstack11llll_opy_ (u"ࠪࡇࡗࡋࡄࡆࡐࡗࡍࡆࡒࡓࡠࡈࡒࡖࡤࡉࡒࡂࡕࡋࡣࡗࡋࡐࡐࡔࡗࡍࡓࡍࠧᩃ")] = json.dumps({
                bstack11llll_opy_ (u"ࠫࡺࡹࡥࡳࡰࡤࡱࡪ࠭ᩄ"): bstack1l11lll111l_opy_(cls.bs_config),
                bstack11llll_opy_ (u"ࠬࡶࡡࡴࡵࡺࡳࡷࡪࠧᩅ"): bstack1l11llll1l1_opy_(cls.bs_config)
            })
        if bstack1lll1llllll_opy_.get(bstack11llll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨᩆ")):
            os.environ[bstack11llll_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭ᩇ")] = bstack1lll1llllll_opy_[bstack11llll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪᩈ")]
        if bstack1lll1llllll_opy_[bstack11llll_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩᩉ")].get(bstack11llll_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫᩊ"), {}).get(bstack11llll_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨᩋ")):
            os.environ[bstack11llll_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡄࡐࡑࡕࡗࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࡘ࠭ᩌ")] = str(bstack1lll1llllll_opy_[bstack11llll_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ᩍ")][bstack11llll_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨᩎ")][bstack11llll_opy_ (u"ࠨࡣ࡯ࡰࡴࡽ࡟ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬᩏ")])
        else:
            os.environ[bstack11llll_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡁࡍࡎࡒ࡛ࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࡕࠪᩐ")] = bstack11llll_opy_ (u"ࠥࡲࡺࡲ࡬ࠣᩑ")
        return [bstack1lll1llllll_opy_[bstack11llll_opy_ (u"ࠫ࡯ࡽࡴࠨᩒ")], bstack1lll1llllll_opy_[bstack11llll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧᩓ")], os.environ[bstack11llll_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡅࡑࡒࡏࡘࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙࡙ࠧᩔ")]]
    @classmethod
    def bstack11ll11ll111_opy_(cls, bstack1lll1llllll_opy_):
        if bstack1lll1llllll_opy_.get(bstack11llll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᩕ")) == None:
            cls.bstack11ll11llll1_opy_()
            return [None, None]
        if bstack1lll1llllll_opy_[bstack11llll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᩖ")][bstack11llll_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪᩗ")] != True:
            cls.bstack11ll11llll1_opy_(bstack1lll1llllll_opy_[bstack11llll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᩘ")])
            return [None, None]
        if bstack1lll1llllll_opy_[bstack11llll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᩙ")].get(bstack11llll_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭ᩚ")):
            logger.debug(bstack11llll_opy_ (u"࠭ࡔࡦࡵࡷࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲ࡙ࠥࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭ࠣࠪᩛ"))
            parsed = json.loads(os.getenv(bstack11llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨᩜ"), bstack11llll_opy_ (u"ࠨࡽࢀࠫᩝ")))
            capabilities = bstack1lllll111l_opy_.bstack11ll11l1lll_opy_(bstack1lll1llllll_opy_[bstack11llll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᩞ")][bstack11llll_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫ᩟")][bstack11llll_opy_ (u"ࠫࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵ᩠ࠪ")], bstack11llll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᩡ"), bstack11llll_opy_ (u"࠭ࡶࡢ࡮ࡸࡩࠬᩢ"))
            bstack11ll11l11ll_opy_ = capabilities[bstack11llll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡔࡰ࡭ࡨࡲࠬᩣ")]
            os.environ[bstack11llll_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᩤ")] = bstack11ll11l11ll_opy_
            parsed[bstack11llll_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᩥ")] = capabilities[bstack11llll_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᩦ")]
            os.environ[bstack11llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬᩧ")] = json.dumps(parsed)
            scripts = bstack1lllll111l_opy_.bstack11ll11l1lll_opy_(bstack1lll1llllll_opy_[bstack11llll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᩨ")][bstack11llll_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧᩩ")][bstack11llll_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨᩪ")], bstack11llll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᩫ"), bstack11llll_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࠪᩬ"))
            bstack11ll11l1l1_opy_.bstack11lll11l111_opy_(scripts)
            commands = bstack1lll1llllll_opy_[bstack11llll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᩭ")][bstack11llll_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬᩮ")][bstack11llll_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࡔࡰ࡙ࡵࡥࡵ࠭ᩯ")].get(bstack11llll_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳࠨᩰ"))
            bstack11ll11l1l1_opy_.bstack11lll11l1l1_opy_(commands)
            bstack11ll11l1l1_opy_.store()
        return [bstack11ll11l11ll_opy_, bstack1lll1llllll_opy_[bstack11llll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩᩱ")]]
    @classmethod
    def bstack11ll1l111l1_opy_(cls, response=None):
        os.environ[bstack11llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ᩲ")] = bstack11llll_opy_ (u"ࠩࡱࡹࡱࡲࠧᩳ")
        os.environ[bstack11llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧᩴ")] = bstack11llll_opy_ (u"ࠫࡳࡻ࡬࡭ࠩ᩵")
        os.environ[bstack11llll_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡅࡒࡑࡕࡒࡅࡕࡇࡇࠫ᩶")] = bstack11llll_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬ᩷")
        os.environ[bstack11llll_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭᩸")] = bstack11llll_opy_ (u"ࠣࡰࡸࡰࡱࠨ᩹")
        os.environ[bstack11llll_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡁࡍࡎࡒ࡛ࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࡕࠪ᩺")] = bstack11llll_opy_ (u"ࠥࡲࡺࡲ࡬ࠣ᩻")
        cls.bstack11ll11lll11_opy_(response, bstack11llll_opy_ (u"ࠦࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠦ᩼"))
        return [None, None, None]
    @classmethod
    def bstack11ll11llll1_opy_(cls, response=None):
        os.environ[bstack11llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ᩽")] = bstack11llll_opy_ (u"࠭࡮ࡶ࡮࡯ࠫ᩾")
        os.environ[bstack11llll_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘ᩿ࠬ")] = bstack11llll_opy_ (u"ࠨࡰࡸࡰࡱ࠭᪀")
        os.environ[bstack11llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭᪁")] = bstack11llll_opy_ (u"ࠪࡲࡺࡲ࡬ࠨ᪂")
        cls.bstack11ll11lll11_opy_(response, bstack11llll_opy_ (u"ࠦࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠦ᪃"))
        return [None, None, None]
    @classmethod
    def bstack11ll11lllll_opy_(cls, bstack11ll1l1l1l1_opy_, bstack11llll1111_opy_):
        os.environ[bstack11llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ᪄")] = bstack11ll1l1l1l1_opy_
        os.environ[bstack11llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ᪅")] = bstack11llll1111_opy_
    @classmethod
    def bstack11ll11lll11_opy_(cls, response=None, product=bstack11llll_opy_ (u"ࠢࠣ᪆")):
        if response == None:
            logger.error(product + bstack11llll_opy_ (u"ࠣࠢࡅࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣࡪࡦ࡯࡬ࡦࡦࠥ᪇"))
        for error in response[bstack11llll_opy_ (u"ࠩࡨࡶࡷࡵࡲࡴࠩ᪈")]:
            bstack1l11ll1llll_opy_ = error[bstack11llll_opy_ (u"ࠪ࡯ࡪࡿࠧ᪉")]
            error_message = error[bstack11llll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ᪊")]
            if error_message:
                if bstack1l11ll1llll_opy_ == bstack11llll_opy_ (u"ࠧࡋࡒࡓࡑࡕࡣࡆࡉࡃࡆࡕࡖࡣࡉࡋࡎࡊࡇࡇࠦ᪋"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack11llll_opy_ (u"ࠨࡄࡢࡶࡤࠤࡺࡶ࡬ࡰࡣࡧࠤࡹࡵࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࠢ᪌") + product + bstack11llll_opy_ (u"ࠢࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡦࡸࡩࠥࡺ࡯ࠡࡵࡲࡱࡪࠦࡥࡳࡴࡲࡶࠧ᪍"))
    @classmethod
    def bstack11ll1l11lll_opy_(cls):
        if cls.bstack1l1l1ll1l1l_opy_ is not None:
            return
        cls.bstack1l1l1ll1l1l_opy_ = bstack1l1l111l11l_opy_(cls.post_data)
        cls.bstack1l1l1ll1l1l_opy_.start()
    @classmethod
    def bstack1l11lll1_opy_(cls):
        if cls.bstack1l1l1ll1l1l_opy_ is None:
            return
        cls.bstack1l1l1ll1l1l_opy_.shutdown()
    @classmethod
    @bstack1l11llll_opy_(class_method=True)
    def post_data(cls, bstack1l11l1ll_opy_, event_url=bstack11llll_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡤࡸࡨ࡮ࠧ᪎")):
        config = {
            bstack11llll_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪ᪏"): cls.default_headers()
        }
        response = bstack1l1111l1l_opy_(bstack11llll_opy_ (u"ࠪࡔࡔ࡙ࡔࠨ᪐"), cls.request_url(event_url), bstack1l11l1ll_opy_, config)
        bstack11ll1llll11_opy_ = response.json()
    @classmethod
    def bstack11ll1ll1_opy_(cls, bstack1l11l1ll_opy_, event_url=bstack11llll_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡧࡴࡤࡪࠪ᪑")):
        if not bstack1lllll111l_opy_.bstack11ll11l1l11_opy_(bstack1l11l1ll_opy_[bstack11llll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ᪒")]):
            return
        bstack111111111_opy_ = bstack1lllll111l_opy_.bstack11ll1l1l1ll_opy_(bstack1l11l1ll_opy_[bstack11llll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ᪓")], bstack1l11l1ll_opy_.get(bstack11llll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩ᪔")))
        if bstack111111111_opy_ != None:
            if bstack1l11l1ll_opy_.get(bstack11llll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪ᪕")) != None:
                bstack1l11l1ll_opy_[bstack11llll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫ᪖")][bstack11llll_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࡣࡲࡧࡰࠨ᪗")] = bstack111111111_opy_
            else:
                bstack1l11l1ll_opy_[bstack11llll_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࡤࡳࡡࡱࠩ᪘")] = bstack111111111_opy_
        if event_url == bstack11llll_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡡࡵࡥ࡫ࠫ᪙"):
            cls.bstack11ll1l11lll_opy_()
            cls.bstack1l1l1ll1l1l_opy_.add(bstack1l11l1ll_opy_)
        elif event_url == bstack11llll_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫ᪚"):
            cls.post_data([bstack1l11l1ll_opy_], event_url)
    @classmethod
    @bstack1l11llll_opy_(class_method=True)
    def bstack1ll1ll11_opy_(cls, bstack1ll11l11_opy_):
        bstack11ll1l11l1l_opy_ = []
        for log in bstack1ll11l11_opy_:
            bstack11ll1l1l11l_opy_ = {
                bstack11llll_opy_ (u"ࠧ࡬࡫ࡱࡨࠬ᪛"): bstack11llll_opy_ (u"ࠨࡖࡈࡗ࡙ࡥࡌࡐࡉࠪ᪜"),
                bstack11llll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ᪝"): log[bstack11llll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ᪞")],
                bstack11llll_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ᪟"): log[bstack11llll_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ᪠")],
                bstack11llll_opy_ (u"࠭ࡨࡵࡶࡳࡣࡷ࡫ࡳࡱࡱࡱࡷࡪ࠭᪡"): {},
                bstack11llll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ᪢"): log[bstack11llll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ᪣")],
            }
            if bstack11llll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ᪤") in log:
                bstack11ll1l1l11l_opy_[bstack11llll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ᪥")] = log[bstack11llll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ᪦")]
            elif bstack11llll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᪧ") in log:
                bstack11ll1l1l11l_opy_[bstack11llll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭᪨")] = log[bstack11llll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ᪩")]
            bstack11ll1l11l1l_opy_.append(bstack11ll1l1l11l_opy_)
        cls.bstack11ll1ll1_opy_({
            bstack11llll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ᪪"): bstack11llll_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭᪫"),
            bstack11llll_opy_ (u"ࠪࡰࡴ࡭ࡳࠨ᪬"): bstack11ll1l11l1l_opy_
        })
    @classmethod
    @bstack1l11llll_opy_(class_method=True)
    def bstack11ll1l11ll1_opy_(cls, steps):
        bstack11ll1l11111_opy_ = []
        for step in steps:
            bstack11ll11l1ll1_opy_ = {
                bstack11llll_opy_ (u"ࠫࡰ࡯࡮ࡥࠩ᪭"): bstack11llll_opy_ (u"࡚ࠬࡅࡔࡖࡢࡗ࡙ࡋࡐࠨ᪮"),
                bstack11llll_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ᪯"): step[bstack11llll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭᪰")],
                bstack11llll_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ᪱"): step[bstack11llll_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ᪲")],
                bstack11llll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ᪳"): step[bstack11llll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ᪴")],
                bstack11llll_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ᪵ࠧ"): step[bstack11llll_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨ᪶")]
            }
            if bstack11llll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪ᪷ࠧ") in step:
                bstack11ll11l1ll1_opy_[bstack11llll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ᪸")] = step[bstack11llll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥ᪹ࠩ")]
            elif bstack11llll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦ᪺ࠪ") in step:
                bstack11ll11l1ll1_opy_[bstack11llll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ᪻")] = step[bstack11llll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ᪼")]
            bstack11ll1l11111_opy_.append(bstack11ll11l1ll1_opy_)
        cls.bstack11ll1ll1_opy_({
            bstack11llll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧ᪽ࠪ"): bstack11llll_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫ᪾"),
            bstack11llll_opy_ (u"ࠨ࡮ࡲ࡫ࡸᪿ࠭"): bstack11ll1l11111_opy_
        })
    @classmethod
    @bstack1l11llll_opy_(class_method=True)
    def bstack1ll1lll11_opy_(cls, screenshot):
        cls.bstack11ll1ll1_opy_({
            bstack11llll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪᫀ࠭"): bstack11llll_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧ᫁"),
            bstack11llll_opy_ (u"ࠫࡱࡵࡧࡴࠩ᫂"): [{
                bstack11llll_opy_ (u"ࠬࡱࡩ࡯ࡦ᫃ࠪ"): bstack11llll_opy_ (u"࠭ࡔࡆࡕࡗࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࠨ᫄"),
                bstack11llll_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ᫅"): datetime.datetime.utcnow().isoformat() + bstack11llll_opy_ (u"ࠨ࡜ࠪ᫆"),
                bstack11llll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ᫇"): screenshot[bstack11llll_opy_ (u"ࠪ࡭ࡲࡧࡧࡦࠩ᫈")],
                bstack11llll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ᫉"): screenshot[bstack11llll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨ᫊ࠬ")]
            }]
        }, event_url=bstack11llll_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫ᫋"))
    @classmethod
    @bstack1l11llll_opy_(class_method=True)
    def bstack1ll1ll1l1_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack11ll1ll1_opy_({
            bstack11llll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫᫌ"): bstack11llll_opy_ (u"ࠨࡅࡅࡘࡘ࡫ࡳࡴ࡫ࡲࡲࡈࡸࡥࡢࡶࡨࡨࠬᫍ"),
            bstack11llll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫᫎ"): {
                bstack11llll_opy_ (u"ࠥࡹࡺ࡯ࡤࠣ᫏"): cls.current_test_uuid(),
                bstack11llll_opy_ (u"ࠦ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠥ᫐"): cls.bstack1l1ll111_opy_(driver)
            }
        })
    @classmethod
    def bstack1l1l11ll_opy_(cls, event: str, bstack1l11l1ll_opy_: bstack11lll1ll_opy_):
        bstack1lllll11_opy_ = {
            bstack11llll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ᫑"): event,
            bstack1l11l1ll_opy_.bstack1l1lll1l_opy_(): bstack1l11l1ll_opy_.bstack1lll1l1l_opy_(event)
        }
        cls.bstack11ll1ll1_opy_(bstack1lllll11_opy_)
    @classmethod
    def on(cls):
        if (os.environ.get(bstack11llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ᫒"), None) is None or os.environ[bstack11llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ᫓")] == bstack11llll_opy_ (u"ࠣࡰࡸࡰࡱࠨ᫔")) and (os.environ.get(bstack11llll_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ᫕"), None) is None or os.environ[bstack11llll_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ᫖")] == bstack11llll_opy_ (u"ࠦࡳࡻ࡬࡭ࠤ᫗")):
            return False
        return True
    @staticmethod
    def bstack11ll11ll1l1_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1lll11ll_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack11llll_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫ᫘"): bstack11llll_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩ᫙"),
            bstack11llll_opy_ (u"࡙ࠧ࠯ࡅࡗ࡙ࡇࡃࡌ࠯ࡗࡉࡘ࡚ࡏࡑࡕࠪ᫚"): bstack11llll_opy_ (u"ࠨࡶࡵࡹࡪ࠭᫛")
        }
        if os.environ.get(bstack11llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭᫜"), None):
            headers[bstack11llll_opy_ (u"ࠪࡅࡺࡺࡨࡰࡴ࡬ࡾࡦࡺࡩࡰࡰࠪ᫝")] = bstack11llll_opy_ (u"ࠫࡇ࡫ࡡࡳࡧࡵࠤࢀࢃࠧ᫞").format(os.environ[bstack11llll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠤ᫟")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack11llll_opy_ (u"࠭ࡻࡾ࠱ࡾࢁࠬ᫠").format(bstack11ll11lll1l_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack11llll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ᫡"), None)
    @staticmethod
    def bstack1l1ll111_opy_(driver):
        return {
            bstack1l1l1111111_opy_(): bstack1l11l11l111_opy_(driver)
        }
    @staticmethod
    def bstack11ll11ll1ll_opy_(exception_info, report):
        return [{bstack11llll_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫ᫢"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack111llll11l_opy_(typename):
        if bstack11llll_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࠧ᫣") in typename:
            return bstack11llll_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦ᫤")
        return bstack11llll_opy_ (u"࡚ࠦࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠧ᫥")