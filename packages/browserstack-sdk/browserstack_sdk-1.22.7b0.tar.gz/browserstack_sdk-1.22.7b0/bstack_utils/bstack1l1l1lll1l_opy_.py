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
import datetime
import threading
from bstack_utils.helper import bstack1l11ll1ll1l_opy_, bstack1l1111ll1l_opy_, get_host_info, bstack1l111l1l11l_opy_, \
 bstack11ll11111_opy_, bstack1ll111l1_opy_, bstack1l11llll_opy_, bstack1l11ll11ll1_opy_, bstack1l111ll1_opy_
import bstack_utils.accessibility as bstack11111l11_opy_
from bstack_utils.bstack11llll1l_opy_ import bstack1lll1l11_opy_
from bstack_utils.percy import bstack1ll1lll1ll_opy_
from bstack_utils.config import Config
bstack1111l1l1_opy_ = Config.bstack111ll1ll_opy_()
logger = logging.getLogger(__name__)
percy = bstack1ll1lll1ll_opy_()
@bstack1l11llll_opy_(class_method=False)
def bstack11ll1l1111l_opy_(bs_config, bstack1l11ll111_opy_):
  try:
    data = {
        bstack11llll_opy_ (u"ࠬ࡬࡯ࡳ࡯ࡤࡸࠬ᫦"): bstack11llll_opy_ (u"࠭ࡪࡴࡱࡱࠫ᫧"),
        bstack11llll_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡠࡰࡤࡱࡪ࠭᫨"): bs_config.get(bstack11llll_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭᫩"), bstack11llll_opy_ (u"ࠩࠪ᫪")),
        bstack11llll_opy_ (u"ࠪࡲࡦࡳࡥࠨ᫫"): bs_config.get(bstack11llll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ᫬"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack11llll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ᫭"): bs_config.get(bstack11llll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ᫮")),
        bstack11llll_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬ᫯"): bs_config.get(bstack11llll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡄࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫ᫰"), bstack11llll_opy_ (u"ࠩࠪ᫱")),
        bstack11llll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ᫲"): bstack1l111ll1_opy_(),
        bstack11llll_opy_ (u"ࠫࡹࡧࡧࡴࠩ᫳"): bstack1l111l1l11l_opy_(bs_config),
        bstack11llll_opy_ (u"ࠬ࡮࡯ࡴࡶࡢ࡭ࡳ࡬࡯ࠨ᫴"): get_host_info(),
        bstack11llll_opy_ (u"࠭ࡣࡪࡡ࡬ࡲ࡫ࡵࠧ᫵"): bstack1l1111ll1l_opy_(),
        bstack11llll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡲࡶࡰࡢ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ᫶"): os.environ.get(bstack11llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧ᫷")),
        bstack11llll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࡡࡷࡩࡸࡺࡳࡠࡴࡨࡶࡺࡴࠧ᫸"): os.environ.get(bstack11llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࠨ᫹"), False),
        bstack11llll_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࡤࡩ࡯࡯ࡶࡵࡳࡱ࠭᫺"): bstack1l11ll1ll1l_opy_(),
        bstack11llll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ᫻"): bstack11ll111l11l_opy_(),
        bstack11llll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡧࡩࡹࡧࡩ࡭ࡵࠪ᫼"): bstack11ll111l1ll_opy_(bstack1l11ll111_opy_),
        bstack11llll_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࡠ࡯ࡤࡴࠬ᫽"): bstack11ll1111ll_opy_(bs_config, bstack1l11ll111_opy_.get(bstack11llll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡺࡹࡥࡥࠩ᫾"), bstack11llll_opy_ (u"ࠩࠪ᫿"))),
        bstack11llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᬀ"): bstack11ll11111_opy_(bs_config),
    }
    return data
  except Exception as error:
    logger.error(bstack11llll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡲࡤࡽࡱࡵࡡࡥࠢࡩࡳࡷࠦࡔࡦࡵࡷࡌࡺࡨ࠺ࠡࠢࡾࢁࠧᬁ").format(str(error)))
    return None
def bstack11ll111l1ll_opy_(framework):
  return {
    bstack11llll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡏࡣࡰࡩࠬᬂ"): framework.get(bstack11llll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࠧᬃ"), bstack11llll_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺࠧᬄ")),
    bstack11llll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࡚ࡪࡸࡳࡪࡱࡱࠫᬅ"): framework.get(bstack11llll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᬆ")),
    bstack11llll_opy_ (u"ࠪࡷࡩࡱࡖࡦࡴࡶ࡭ࡴࡴࠧᬇ"): framework.get(bstack11llll_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᬈ")),
    bstack11llll_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫ࠧᬉ"): bstack11llll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ᬊ"),
    bstack11llll_opy_ (u"ࠧࡵࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠧᬋ"): framework.get(bstack11llll_opy_ (u"ࠨࡶࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨᬌ"))
  }
def bstack11ll1111ll_opy_(bs_config, framework):
  bstack1l1lll1l1_opy_ = False
  bstack1l1ll1ll1l_opy_ = False
  bstack11ll111llll_opy_ = False
  if bstack11llll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ᬍ") in bs_config:
    bstack11ll111llll_opy_ = True
  elif bstack11llll_opy_ (u"ࠪࡥࡵࡶࠧᬎ") in bs_config:
    bstack1l1lll1l1_opy_ = True
  else:
    bstack1l1ll1ll1l_opy_ = True
  bstack111111111_opy_ = {
    bstack11llll_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫᬏ"): bstack1lll1l11_opy_.bstack1l1l1lll11l_opy_(bs_config, framework),
    bstack11llll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᬐ"): bstack11111l11_opy_.bstack11ll1ll1111_opy_(bs_config),
    bstack11llll_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬᬑ"): bs_config.get(bstack11llll_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ᬒ"), False),
    bstack11llll_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪᬓ"): bstack1l1ll1ll1l_opy_,
    bstack11llll_opy_ (u"ࠩࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠨᬔ"): bstack1l1lll1l1_opy_,
    bstack11llll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧᬕ"): bstack11ll111llll_opy_
  }
  return bstack111111111_opy_
@bstack1l11llll_opy_(class_method=False)
def bstack11ll111l11l_opy_():
  try:
    bstack11ll111lll1_opy_ = json.loads(os.getenv(bstack11llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬᬖ"), bstack11llll_opy_ (u"ࠬࢁࡽࠨᬗ")))
    return {
        bstack11llll_opy_ (u"࠭ࡳࡦࡶࡷ࡭ࡳ࡭ࡳࠨᬘ"): bstack11ll111lll1_opy_
    }
  except Exception as error:
    logger.error(bstack11llll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤ࡬࡫ࡴࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡵࡨࡸࡹ࡯࡮ࡨࡵࠣࡪࡴࡸࠠࡕࡧࡶࡸࡍࡻࡢ࠻ࠢࠣࡿࢂࠨᬙ").format(str(error)))
    return {}
def bstack11ll11l1lll_opy_(array, bstack11ll11l1111_opy_, bstack11ll11l111l_opy_):
  result = {}
  for o in array:
    key = o[bstack11ll11l1111_opy_]
    result[key] = o[bstack11ll11l111l_opy_]
  return result
def bstack11ll11l1l11_opy_(bstack1lll111l1l_opy_=bstack11llll_opy_ (u"ࠨࠩᬚ")):
  bstack11ll111l1l1_opy_ = bstack11111l11_opy_.on()
  bstack11ll111ll11_opy_ = bstack1lll1l11_opy_.on()
  bstack11ll11l11l1_opy_ = percy.bstack11ll11llll_opy_()
  if bstack11ll11l11l1_opy_ and not bstack11ll111ll11_opy_ and not bstack11ll111l1l1_opy_:
    return bstack1lll111l1l_opy_ not in [bstack11llll_opy_ (u"ࠩࡆࡆ࡙࡙ࡥࡴࡵ࡬ࡳࡳࡉࡲࡦࡣࡷࡩࡩ࠭ᬛ"), bstack11llll_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧᬜ")]
  elif bstack11ll111l1l1_opy_ and not bstack11ll111ll11_opy_:
    return bstack1lll111l1l_opy_ not in [bstack11llll_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᬝ"), bstack11llll_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᬞ"), bstack11llll_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪᬟ")]
  return bstack11ll111l1l1_opy_ or bstack11ll111ll11_opy_ or bstack11ll11l11l1_opy_
@bstack1l11llll_opy_(class_method=False)
def bstack11ll1l1l1ll_opy_(bstack1lll111l1l_opy_, test=None):
  bstack11ll111ll1l_opy_ = bstack11111l11_opy_.on()
  if not bstack11ll111ll1l_opy_ or bstack1lll111l1l_opy_ not in [bstack11llll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᬠ")] or test == None:
    return None
  return {
    bstack11llll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᬡ"): bstack11ll111ll1l_opy_ and bstack1ll111l1_opy_(threading.current_thread(), bstack11llll_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨᬢ"), None) == True and bstack11111l11_opy_.bstack11l1ll1ll1_opy_(test[bstack11llll_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᬣ")])
  }