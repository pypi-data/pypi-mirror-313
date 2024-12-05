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
import requests
import logging
import threading
from urllib.parse import urlparse
from bstack_utils.constants import bstack1l1ll11l1ll_opy_ as bstack11ll1l1lll1_opy_
from bstack_utils.bstack11ll11l1l1_opy_ import bstack11ll11l1l1_opy_
from bstack_utils.helper import bstack1l111ll1_opy_, bstack1l111l1l_opy_, bstack11ll11111_opy_, bstack1l11lll111l_opy_, bstack1l11llll1l1_opy_, bstack1l1111ll1l_opy_, get_host_info, bstack1l11ll1ll1l_opy_, bstack1l1111l1l_opy_, bstack1l11llll_opy_
from browserstack_sdk._version import __version__
logger = logging.getLogger(__name__)
@bstack1l11llll_opy_(class_method=False)
def _11ll1lll111_opy_(driver, bstack1111ll11_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack11llll_opy_ (u"ࠨࡱࡶࡣࡳࡧ࡭ࡦࠩᥓ"): caps.get(bstack11llll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠨᥔ"), None),
        bstack11llll_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᥕ"): bstack1111ll11_opy_.get(bstack11llll_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧᥖ"), None),
        bstack11llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥ࡮ࡢ࡯ࡨࠫᥗ"): caps.get(bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫᥘ"), None),
        bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᥙ"): caps.get(bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᥚ"), None)
    }
  except Exception as error:
    logger.debug(bstack11llll_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡨࡨࡸࡨ࡮ࡩ࡯ࡩࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡪࡥࡵࡣ࡬ࡰࡸࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴࠣ࠾ࠥ࠭ᥛ") + str(error))
  return response
def on():
    if os.environ.get(bstack11llll_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᥜ"), None) is None or os.environ[bstack11llll_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᥝ")] == bstack11llll_opy_ (u"ࠧࡴࡵ࡭࡮ࠥᥞ"):
        return False
    return True
def bstack11ll1ll1111_opy_(config):
  return config.get(bstack11llll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᥟ"), False) or any([p.get(bstack11llll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᥠ"), False) == True for p in config.get(bstack11llll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᥡ"), [])])
def bstack1l1llll11_opy_(config, bstack1ll111l11_opy_):
  try:
    if not bstack11ll11111_opy_(config):
      return False
    bstack11lll1111ll_opy_ = config.get(bstack11llll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᥢ"), False)
    if int(bstack1ll111l11_opy_) < len(config.get(bstack11llll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᥣ"), [])) and config[bstack11llll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᥤ")][bstack1ll111l11_opy_]:
      bstack11ll1lll1l1_opy_ = config[bstack11llll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᥥ")][bstack1ll111l11_opy_].get(bstack11llll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᥦ"), None)
    else:
      bstack11ll1lll1l1_opy_ = config.get(bstack11llll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᥧ"), None)
    if bstack11ll1lll1l1_opy_ != None:
      bstack11lll1111ll_opy_ = bstack11ll1lll1l1_opy_
    bstack11ll1ll11l1_opy_ = os.getenv(bstack11llll_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᥨ")) is not None and len(os.getenv(bstack11llll_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᥩ"))) > 0 and os.getenv(bstack11llll_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᥪ")) != bstack11llll_opy_ (u"ࠫࡳࡻ࡬࡭ࠩᥫ")
    return bstack11lll1111ll_opy_ and bstack11ll1ll11l1_opy_
  except Exception as error:
    logger.debug(bstack11llll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡻ࡫ࡲࡪࡨࡼ࡭ࡳ࡭ࠠࡵࡪࡨࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳࠢ࠽ࠤࠬᥬ") + str(error))
  return False
def bstack11l1ll1ll1_opy_(test_tags):
  bstack1ll1lll1111_opy_ = os.getenv(bstack11llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧᥭ"))
  if bstack1ll1lll1111_opy_ is None:
    return True
  bstack1ll1lll1111_opy_ = json.loads(bstack1ll1lll1111_opy_)
  try:
    include_tags = bstack1ll1lll1111_opy_[bstack11llll_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬ᥮")] if bstack11llll_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭᥯") in bstack1ll1lll1111_opy_ and isinstance(bstack1ll1lll1111_opy_[bstack11llll_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᥰ")], list) else []
    exclude_tags = bstack1ll1lll1111_opy_[bstack11llll_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᥱ")] if bstack11llll_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᥲ") in bstack1ll1lll1111_opy_ and isinstance(bstack1ll1lll1111_opy_[bstack11llll_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᥳ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack11llll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡻࡧ࡬ࡪࡦࡤࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤ࡫ࡵࡲࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡤࡨࡪࡴࡸࡥࠡࡵࡦࡥࡳࡴࡩ࡯ࡩ࠱ࠤࡊࡸࡲࡰࡴࠣ࠾ࠥࠨᥴ") + str(error))
  return False
def bstack11ll1llllll_opy_(config, frameworkName, bstack11ll1lll1ll_opy_, bstack11ll1ll1l1l_opy_):
  bstack11ll1l1llll_opy_ = bstack1l11lll111l_opy_(config)
  bstack11ll1llll1l_opy_ = bstack1l11llll1l1_opy_(config)
  if bstack11ll1l1llll_opy_ is None or bstack11ll1llll1l_opy_ is None:
    logger.error(bstack11llll_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡵࡹࡳࠦࡦࡰࡴࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡀࠠࡎ࡫ࡶࡷ࡮ࡴࡧࠡࡣࡸࡸ࡭࡫࡮ࡵ࡫ࡦࡥࡹ࡯࡯࡯ࠢࡷࡳࡰ࡫࡮ࠨ᥵"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack11llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩ᥶"), bstack11llll_opy_ (u"ࠩࡾࢁࠬ᥷")))
    data = {
        bstack11llll_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨ᥸"): config[bstack11llll_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩ᥹")],
        bstack11llll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ᥺"): config.get(bstack11llll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ᥻"), os.path.basename(os.getcwd())),
        bstack11llll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡚ࡩ࡮ࡧࠪ᥼"): bstack1l111ll1_opy_(),
        bstack11llll_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭᥽"): config.get(bstack11llll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡅࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬ᥾"), bstack11llll_opy_ (u"ࠪࠫ᥿")),
        bstack11llll_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫᦀ"): {
            bstack11llll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡏࡣࡰࡩࠬᦁ"): frameworkName,
            bstack11llll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩᦂ"): bstack11ll1lll1ll_opy_,
            bstack11llll_opy_ (u"ࠧࡴࡦ࡮࡚ࡪࡸࡳࡪࡱࡱࠫᦃ"): __version__,
            bstack11llll_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠪᦄ"): bstack11llll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩᦅ"),
            bstack11llll_opy_ (u"ࠪࡸࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪᦆ"): bstack11llll_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠭ᦇ"),
            bstack11llll_opy_ (u"ࠬࡺࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬᦈ"): bstack11ll1ll1l1l_opy_
        },
        bstack11llll_opy_ (u"࠭ࡳࡦࡶࡷ࡭ࡳ࡭ࡳࠨᦉ"): settings,
        bstack11llll_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࡄࡱࡱࡸࡷࡵ࡬ࠨᦊ"): bstack1l11ll1ll1l_opy_(),
        bstack11llll_opy_ (u"ࠨࡥ࡬ࡍࡳ࡬࡯ࠨᦋ"): bstack1l1111ll1l_opy_(),
        bstack11llll_opy_ (u"ࠩ࡫ࡳࡸࡺࡉ࡯ࡨࡲࠫᦌ"): get_host_info(),
        bstack11llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᦍ"): bstack11ll11111_opy_(config)
    }
    headers = {
        bstack11llll_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪᦎ"): bstack11llll_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨᦏ"),
    }
    config = {
        bstack11llll_opy_ (u"࠭ࡡࡶࡶ࡫ࠫᦐ"): (bstack11ll1l1llll_opy_, bstack11ll1llll1l_opy_),
        bstack11llll_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨᦑ"): headers
    }
    response = bstack1l1111l1l_opy_(bstack11llll_opy_ (u"ࠨࡒࡒࡗ࡙࠭ᦒ"), bstack11ll1l1lll1_opy_ + bstack11llll_opy_ (u"ࠩ࠲ࡺ࠷࠵ࡴࡦࡵࡷࡣࡷࡻ࡮ࡴࠩᦓ"), data, config)
    bstack11ll1llll11_opy_ = response.json()
    if bstack11ll1llll11_opy_[bstack11llll_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫᦔ")]:
      parsed = json.loads(os.getenv(bstack11llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬᦕ"), bstack11llll_opy_ (u"ࠬࢁࡽࠨᦖ")))
      parsed[bstack11llll_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᦗ")] = bstack11ll1llll11_opy_[bstack11llll_opy_ (u"ࠧࡥࡣࡷࡥࠬᦘ")][bstack11llll_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᦙ")]
      os.environ[bstack11llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪᦚ")] = json.dumps(parsed)
      bstack11ll11l1l1_opy_.bstack11lll11l111_opy_(bstack11ll1llll11_opy_[bstack11llll_opy_ (u"ࠪࡨࡦࡺࡡࠨᦛ")][bstack11llll_opy_ (u"ࠫࡸࡩࡲࡪࡲࡷࡷࠬᦜ")])
      bstack11ll11l1l1_opy_.bstack11lll11l1l1_opy_(bstack11ll1llll11_opy_[bstack11llll_opy_ (u"ࠬࡪࡡࡵࡣࠪᦝ")][bstack11llll_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳࠨᦞ")])
      bstack11ll11l1l1_opy_.store()
      return bstack11ll1llll11_opy_[bstack11llll_opy_ (u"ࠧࡥࡣࡷࡥࠬᦟ")][bstack11llll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡕࡱ࡮ࡩࡳ࠭ᦠ")], bstack11ll1llll11_opy_[bstack11llll_opy_ (u"ࠩࡧࡥࡹࡧࠧᦡ")][bstack11llll_opy_ (u"ࠪ࡭ࡩ࠭ᦢ")]
    else:
      logger.error(bstack11llll_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠽ࠤࠬᦣ") + bstack11ll1llll11_opy_[bstack11llll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᦤ")])
      if bstack11ll1llll11_opy_[bstack11llll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᦥ")] == bstack11llll_opy_ (u"ࠧࡊࡰࡹࡥࡱ࡯ࡤࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡲࡤࡷࡸ࡫ࡤ࠯ࠩᦦ"):
        for bstack11ll1ll11ll_opy_ in bstack11ll1llll11_opy_[bstack11llll_opy_ (u"ࠨࡧࡵࡶࡴࡸࡳࠨᦧ")]:
          logger.error(bstack11ll1ll11ll_opy_[bstack11llll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᦨ")])
      return None, None
  except Exception as error:
    logger.error(bstack11llll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡸࡵ࡯ࠢࡩࡳࡷࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠼ࠣࠦᦩ") +  str(error))
    return None, None
def bstack11lll1111l1_opy_():
  if os.getenv(bstack11llll_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᦪ")) is None:
    return {
        bstack11llll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᦫ"): bstack11llll_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ᦬"),
        bstack11llll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ᦭"): bstack11llll_opy_ (u"ࠨࡄࡸ࡭ࡱࡪࠠࡤࡴࡨࡥࡹ࡯࡯࡯ࠢ࡫ࡥࡩࠦࡦࡢ࡫࡯ࡩࡩ࠴ࠧ᦮")
    }
  data = {bstack11llll_opy_ (u"ࠩࡨࡲࡩ࡚ࡩ࡮ࡧࠪ᦯"): bstack1l111ll1_opy_()}
  headers = {
      bstack11llll_opy_ (u"ࠪࡅࡺࡺࡨࡰࡴ࡬ࡾࡦࡺࡩࡰࡰࠪᦰ"): bstack11llll_opy_ (u"ࠫࡇ࡫ࡡࡳࡧࡵࠤࠬᦱ") + os.getenv(bstack11llll_opy_ (u"ࠧࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠥᦲ")),
      bstack11llll_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬᦳ"): bstack11llll_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪᦴ")
  }
  response = bstack1l1111l1l_opy_(bstack11llll_opy_ (u"ࠨࡒࡘࡘࠬᦵ"), bstack11ll1l1lll1_opy_ + bstack11llll_opy_ (u"ࠩ࠲ࡸࡪࡹࡴࡠࡴࡸࡲࡸ࠵ࡳࡵࡱࡳࠫᦶ"), data, { bstack11llll_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫᦷ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack11llll_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡕࡧࡶࡸࠥࡘࡵ࡯ࠢࡰࡥࡷࡱࡥࡥࠢࡤࡷࠥࡩ࡯࡮ࡲ࡯ࡩࡹ࡫ࡤࠡࡣࡷࠤࠧᦸ") + bstack1l111l1l_opy_().isoformat() + bstack11llll_opy_ (u"ࠬࡠࠧᦹ"))
      return {bstack11llll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ᦺ"): bstack11llll_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨᦻ"), bstack11llll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᦼ"): bstack11llll_opy_ (u"ࠩࠪᦽ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack11llll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡳࡡࡳ࡭࡬ࡲ࡬ࠦࡣࡰ࡯ࡳࡰࡪࡺࡩࡰࡰࠣࡳ࡫ࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡗࡩࡸࡺࠠࡓࡷࡱ࠾ࠥࠨᦾ") + str(error))
    return {
        bstack11llll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᦿ"): bstack11llll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᧀ"),
        bstack11llll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᧁ"): str(error)
    }
def bstack11ll11ll11_opy_(caps, options, desired_capabilities={}):
  try:
    bstack11ll1ll1lll_opy_ = caps.get(bstack11llll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᧂ"), {}).get(bstack11llll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬᧃ"), caps.get(bstack11llll_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩᧄ"), bstack11llll_opy_ (u"ࠪࠫᧅ")))
    if bstack11ll1ll1lll_opy_:
      logger.warn(bstack11llll_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡉ࡫ࡳ࡬ࡶࡲࡴࠥࡨࡲࡰࡹࡶࡩࡷࡹ࠮ࠣᧆ"))
      return False
    if options:
      bstack11lll111111_opy_ = options.to_capabilities()
    elif desired_capabilities:
      bstack11lll111111_opy_ = desired_capabilities
    else:
      bstack11lll111111_opy_ = {}
    browser = caps.get(bstack11llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪᧇ"), bstack11llll_opy_ (u"࠭ࠧᧈ")).lower() or bstack11lll111111_opy_.get(bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬᧉ"), bstack11llll_opy_ (u"ࠨࠩ᧊")).lower()
    if browser != bstack11llll_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩ᧋"):
      logger.warning(bstack11llll_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨ᧌"))
      return False
    browser_version = caps.get(bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ᧍")) or caps.get(bstack11llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ᧎")) or bstack11lll111111_opy_.get(bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ᧏")) or bstack11lll111111_opy_.get(bstack11llll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ᧐"), {}).get(bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ᧑")) or bstack11lll111111_opy_.get(bstack11llll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ᧒"), {}).get(bstack11llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ᧓"))
    if browser_version and browser_version != bstack11llll_opy_ (u"ࠫࡱࡧࡴࡦࡵࡷࠫ᧔") and int(browser_version.split(bstack11llll_opy_ (u"ࠬ࠴ࠧ᧕"))[0]) <= 98:
      logger.warning(bstack11llll_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡃࡩࡴࡲࡱࡪࠦࡢࡳࡱࡺࡷࡪࡸࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡩࡵࡩࡦࡺࡥࡳࠢࡷ࡬ࡦࡴࠠ࠺࠺࠱ࠦ᧖"))
      return False
    if not options:
      bstack11ll1lll11l_opy_ = caps.get(bstack11llll_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ᧗")) or bstack11lll111111_opy_.get(bstack11llll_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭᧘"), {})
      if bstack11llll_opy_ (u"ࠩ࠰࠱࡭࡫ࡡࡥ࡮ࡨࡷࡸ࠭᧙") in bstack11ll1lll11l_opy_.get(bstack11llll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨ᧚"), []):
        logger.warn(bstack11llll_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦ࡮ࡰࡶࠣࡶࡺࡴࠠࡰࡰࠣࡰࡪ࡭ࡡࡤࡻࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧ࠱ࠤࡘࡽࡩࡵࡥ࡫ࠤࡹࡵࠠ࡯ࡧࡺࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨࠤࡴࡸࠠࡢࡸࡲ࡭ࡩࠦࡵࡴ࡫ࡱ࡫ࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠨ᧛"))
        return False
    return True
  except Exception as error:
    logger.debug(bstack11llll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡻࡧ࡬ࡪࡦࡤࡸࡪࠦࡡ࠲࠳ࡼࠤࡸࡻࡰࡱࡱࡵࡸࠥࡀࠢ᧜") + str(error))
    return False
def set_capabilities(caps, config):
  try:
    bstack1llll11111l_opy_ = config.get(bstack11llll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭᧝"), {})
    bstack1llll11111l_opy_[bstack11llll_opy_ (u"ࠧࡢࡷࡷ࡬࡙ࡵ࡫ࡦࡰࠪ᧞")] = os.getenv(bstack11llll_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭᧟"))
    bstack11ll1lllll1_opy_ = json.loads(os.getenv(bstack11llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪ᧠"), bstack11llll_opy_ (u"ࠪࡿࢂ࠭᧡"))).get(bstack11llll_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ᧢"))
    caps[bstack11llll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ᧣")] = True
    if bstack11llll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ᧤") in caps:
      caps[bstack11llll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ᧥")][bstack11llll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ᧦")] = bstack1llll11111l_opy_
      caps[bstack11llll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ᧧")][bstack11llll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ᧨")][bstack11llll_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ᧩")] = bstack11ll1lllll1_opy_
    else:
      caps[bstack11llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ᧪")] = bstack1llll11111l_opy_
      caps[bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ᧫")][bstack11llll_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ᧬")] = bstack11ll1lllll1_opy_
  except Exception as error:
    logger.debug(bstack11llll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡷࡪࡺࡴࡪࡰࡪࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹ࠮ࠡࡇࡵࡶࡴࡸ࠺ࠡࠤ᧭") +  str(error))
def bstack1lllll11ll_opy_(driver, bstack11ll1ll1ll1_opy_):
  try:
    setattr(driver, bstack11llll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩ᧮"), True)
    session = driver.session_id
    if session:
      bstack11lll11111l_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11lll11111l_opy_ = False
      bstack11lll11111l_opy_ = url.scheme in [bstack11llll_opy_ (u"ࠥ࡬ࡹࡺࡰࠣ᧯"), bstack11llll_opy_ (u"ࠦ࡭ࡺࡴࡱࡵࠥ᧰")]
      if bstack11lll11111l_opy_:
        if bstack11ll1ll1ll1_opy_:
          logger.info(bstack11llll_opy_ (u"࡙ࠧࡥࡵࡷࡳࠤ࡫ࡵࡲࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢ࡫ࡥࡸࠦࡳࡵࡣࡵࡸࡪࡪ࠮ࠡࡃࡸࡸࡴࡳࡡࡵࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡥࡹࡧࡦࡹࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡣࡧࡪ࡭ࡳࠦ࡭ࡰ࡯ࡨࡲࡹࡧࡲࡪ࡮ࡼ࠲ࠧ᧱"))
      return bstack11ll1ll1ll1_opy_
  except Exception as e:
    logger.error(bstack11llll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡴࡢࡴࡷ࡭ࡳ࡭ࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸࡩࡡ࡯ࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫࠺ࠡࠤ᧲") + str(e))
    return False
def bstack11111l1l_opy_(driver, name, path):
  try:
    bstack11ll1ll111l_opy_ = {
        bstack11llll_opy_ (u"ࠧࡵࡪࡗࡩࡸࡺࡒࡶࡰࡘࡹ࡮ࡪࠧ᧳"): threading.current_thread().current_test_uuid,
        bstack11llll_opy_ (u"ࠨࡶ࡫ࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭᧴"): os.environ.get(bstack11llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ᧵"), bstack11llll_opy_ (u"ࠪࠫ᧶")),
        bstack11llll_opy_ (u"ࠫࡹ࡮ࡊࡸࡶࡗࡳࡰ࡫࡮ࠨ᧷"): os.environ.get(bstack11llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ᧸"), bstack11llll_opy_ (u"࠭ࠧ᧹"))
    }
    logger.debug(bstack11llll_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡥࡻ࡯࡮ࡨࠢࡵࡩࡸࡻ࡬ࡵࡵࠪ᧺"))
    logger.debug(driver.execute_async_script(bstack11ll11l1l1_opy_.perform_scan, {bstack11llll_opy_ (u"ࠣ࡯ࡨࡸ࡭ࡵࡤࠣ᧻"): name}))
    logger.debug(driver.execute_async_script(bstack11ll11l1l1_opy_.bstack11lll111lll_opy_, bstack11ll1ll111l_opy_))
    logger.info(bstack11llll_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣࡪࡴࡸࠠࡵࡪ࡬ࡷࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡪࡤࡷࠥ࡫࡮ࡥࡧࡧ࠲ࠧ᧼"))
  except Exception as bstack11ll1ll1l11_opy_:
    logger.error(bstack11llll_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡨࡵࡵ࡭ࡦࠣࡲࡴࡺࠠࡣࡧࠣࡴࡷࡵࡣࡦࡵࡶࡩࡩࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧ࠽ࠤࠧ᧽") + str(path) + bstack11llll_opy_ (u"ࠦࠥࡋࡲࡳࡱࡵࠤ࠿ࠨ᧾") + str(bstack11ll1ll1l11_opy_))