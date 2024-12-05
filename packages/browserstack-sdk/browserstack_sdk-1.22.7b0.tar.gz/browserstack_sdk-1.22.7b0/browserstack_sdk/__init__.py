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
import atexit
import os
import signal
import sys
import yaml
import requests
import logging
import threading
import socket
import datetime
import string
import random
import json
import collections.abc
import re
import multiprocessing
import traceback
import copy
import tempfile
from packaging import version
from uuid import uuid4
from browserstack.local import Local
from urllib.parse import urlparse
from dotenv import load_dotenv
from bstack_utils.constants import *
from bstack_utils.percy import *
from browserstack_sdk.bstack1lllllll1_opy_ import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack1ll1lllll_opy_ import bstack1ll1l11111_opy_
import time
import requests
def bstack1ll1l1l1l_opy_():
  global CONFIG
  headers = {
        bstack11llll_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡴࡺࡲࡨࠫ৖"): bstack11llll_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩৗ"),
      }
  proxies = bstack1ll111111_opy_(CONFIG, bstack1l1111l1ll_opy_)
  try:
    response = requests.get(bstack1l1111l1ll_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack1l111l1ll1_opy_ = response.json()[bstack11llll_opy_ (u"ࠧࡩࡷࡥࡷࠬ৘")]
      logger.debug(bstack1l111llll_opy_.format(response.json()))
      return bstack1l111l1ll1_opy_
    else:
      logger.debug(bstack11llll1ll1_opy_.format(bstack11llll_opy_ (u"ࠣࡔࡨࡷࡵࡵ࡮ࡴࡧࠣࡎࡘࡕࡎࠡࡲࡤࡶࡸ࡫ࠠࡦࡴࡵࡳࡷࠦࠢ৙")))
  except Exception as e:
    logger.debug(bstack11llll1ll1_opy_.format(e))
def bstack11l11l1111_opy_(hub_url):
  global CONFIG
  url = bstack11llll_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦ৚")+  hub_url + bstack11llll_opy_ (u"ࠥ࠳ࡨ࡮ࡥࡤ࡭ࠥ৛")
  headers = {
        bstack11llll_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲ࡺࡹࡱࡧࠪড়"): bstack11llll_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨঢ়"),
      }
  proxies = bstack1ll111111_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack111llll1ll_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack11l1l11ll_opy_.format(hub_url, e))
def bstack1lll1111ll_opy_():
  try:
    global bstack111l11l11_opy_
    bstack1l111l1ll1_opy_ = bstack1ll1l1l1l_opy_()
    bstack1ll11ll1ll_opy_ = []
    results = []
    for bstack11ll1lll11_opy_ in bstack1l111l1ll1_opy_:
      bstack1ll11ll1ll_opy_.append(bstack1ll11lll1l_opy_(target=bstack11l11l1111_opy_,args=(bstack11ll1lll11_opy_,)))
    for t in bstack1ll11ll1ll_opy_:
      t.start()
    for t in bstack1ll11ll1ll_opy_:
      results.append(t.join())
    bstack11l11lllll_opy_ = {}
    for item in results:
      hub_url = item[bstack11llll_opy_ (u"࠭ࡨࡶࡤࡢࡹࡷࡲࠧ৞")]
      latency = item[bstack11llll_opy_ (u"ࠧ࡭ࡣࡷࡩࡳࡩࡹࠨয়")]
      bstack11l11lllll_opy_[hub_url] = latency
    bstack1llll1lll_opy_ = min(bstack11l11lllll_opy_, key= lambda x: bstack11l11lllll_opy_[x])
    bstack111l11l11_opy_ = bstack1llll1lll_opy_
    logger.debug(bstack111111lll_opy_.format(bstack1llll1lll_opy_))
  except Exception as e:
    logger.debug(bstack1lll1111l_opy_.format(e))
from bstack_utils.messages import *
from bstack_utils import bstack1ll1l1l1l1_opy_
from bstack_utils.config import Config
from bstack_utils.constants import bstack11l1111ll1_opy_
from bstack_utils.helper import bstack1l1lllll1l_opy_, bstack1l1111l1l_opy_, bstack11l1ll11l_opy_, bstack1ll111l1_opy_, bstack11ll11111_opy_, \
  Notset, bstack1ll11l1111_opy_, \
  bstack1ll111111l_opy_, bstack1llll1l1l1_opy_, bstack1ll1ll11ll_opy_, bstack1l1111ll1l_opy_, bstack1l1lll1l1l_opy_, bstack1l1ll11ll_opy_, \
  bstack1l111llll1_opy_, \
  bstack1l11l1ll11_opy_, bstack1ll1lll11l_opy_, bstack1l1l1l11l1_opy_, bstack1l11111lll_opy_, \
  bstack1ll1l111l1_opy_, bstack1l1111ll1_opy_, bstack1lll1lll11_opy_, bstack11l111l11l_opy_
from bstack_utils.bstack11ll11l11_opy_ import bstack11l1ll1l1_opy_
from bstack_utils.bstack1l11lllll1_opy_ import bstack1l1llll11l_opy_
from bstack_utils.bstack1l1ll1ll11_opy_ import bstack11l11l11ll_opy_, bstack11ll111lll_opy_
from bstack_utils.bstack1llll1ll_opy_ import bstack1lll11ll_opy_
from bstack_utils.bstack11llll1l_opy_ import bstack1lll1l11_opy_
from bstack_utils.bstack11ll11l1l1_opy_ import bstack11ll11l1l1_opy_
from bstack_utils.proxy import bstack11l1ll1l11_opy_, bstack1ll111111_opy_, bstack11l1lll1l_opy_, bstack11lll1l1ll_opy_
import bstack_utils.accessibility as bstack11111l11_opy_
from browserstack_sdk.bstack1111l1ll_opy_ import *
from browserstack_sdk.bstack111llll1_opy_ import *
from bstack_utils.bstack1lll11ll1_opy_ import bstack1ll11llll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1ll11l_opy_ import bstack1lll1ll11l_opy_, Events, bstack11lll1111l_opy_, bstack11lllll11_opy_
from browserstack_sdk.bstack11l11lll_opy_ import *
import requests
from bstack_utils.constants import *
def bstack1ll1ll11l_opy_():
    global bstack111l11l11_opy_
    try:
        bstack1l11ll1l1l_opy_ = bstack1l1ll1ll1_opy_()
        bstack11ll1lll1l_opy_(bstack1l11ll1l1l_opy_)
        hub_url = bstack1l11ll1l1l_opy_.get(bstack11llll_opy_ (u"ࠣࡷࡵࡰࠧৠ"), bstack11llll_opy_ (u"ࠤࠥৡ"))
        if hub_url.endswith(bstack11llll_opy_ (u"ࠪ࠳ࡼࡪ࠯ࡩࡷࡥࠫৢ")):
            hub_url = hub_url.rsplit(bstack11llll_opy_ (u"ࠫ࠴ࡽࡤ࠰ࡪࡸࡦࠬৣ"), 1)[0]
        if hub_url.startswith(bstack11llll_opy_ (u"ࠬ࡮ࡴࡵࡲ࠽࠳࠴࠭৤")):
            hub_url = hub_url[7:]
        elif hub_url.startswith(bstack11llll_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࠨ৥")):
            hub_url = hub_url[8:]
        bstack111l11l11_opy_ = hub_url
    except Exception as e:
        raise RuntimeError(e)
def bstack1l1ll1ll1_opy_():
    global CONFIG
    bstack1l1l1lll1_opy_ = CONFIG.get(bstack11llll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࡓࡵࡺࡩࡰࡰࡶࠫ০"), {}).get(bstack11llll_opy_ (u"ࠨࡩࡵ࡭ࡩࡔࡡ࡮ࡧࠪ১"), bstack11llll_opy_ (u"ࠩࡑࡓࡤࡍࡒࡊࡆࡢࡒࡆࡓࡅࡠࡒࡄࡗࡘࡋࡄࠨ২"))
    if not isinstance(bstack1l1l1lll1_opy_, str):
        raise ValueError(bstack11llll_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡊࡶ࡮ࡪࠠ࡯ࡣࡰࡩࠥࡳࡵࡴࡶࠣࡦࡪࠦࡡࠡࡸࡤࡰ࡮ࡪࠠࡴࡶࡵ࡭ࡳ࡭ࠢ৩"))
    try:
        bstack1l11ll1l1l_opy_ = bstack1l111ll11l_opy_(bstack1l1l1lll1_opy_)
        return bstack1l11ll1l1l_opy_
    except Exception as e:
        logger.error(bstack11llll_opy_ (u"ࠦࡆ࡚ࡓࠡ࠼ࠣࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡧࡳ࡫ࡧࠤࡩ࡫ࡴࡢ࡫࡯ࡷࠥࡀࠠࡼࡿࠥ৪").format(str(e)))
        return {}
def bstack1l111ll11l_opy_(bstack1l1l1lll1_opy_):
    global CONFIG
    try:
        if not CONFIG[bstack11llll_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ৫")] or not CONFIG[bstack11llll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ৬")]:
            raise ValueError(bstack11llll_opy_ (u"ࠢࡎ࡫ࡶࡷ࡮ࡴࡧࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡶࡵࡨࡶࡳࡧ࡭ࡦࠢࡲࡶࠥࡧࡣࡤࡧࡶࡷࠥࡱࡥࡺࠤ৭"))
        url = bstack11l1l1111l_opy_ + bstack1l1l1lll1_opy_
        auth = (CONFIG[bstack11llll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ৮")], CONFIG[bstack11llll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ৯")])
        response = requests.get(url, auth=auth)
        if response.status_code == 200 and response.text:
            bstack11ll1lllll_opy_ = json.loads(response.text)
            return bstack11ll1lllll_opy_
    except ValueError as ve:
        logger.error(bstack11llll_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡈࡶࡷࡵࡲࠡ࡫ࡱࠤ࡫࡫ࡴࡤࡪ࡬ࡲ࡬ࠦࡧࡳ࡫ࡧࠤࡩ࡫ࡴࡢ࡫࡯ࡷࠥࡀࠠࡼࡿࠥৰ").format(str(ve)))
        raise ValueError(ve)
    except Exception as e:
        logger.error(bstack11llll_opy_ (u"ࠦࡆ࡚ࡓࠡ࠼ࠣࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥ࡬ࡥࡵࡥ࡫࡭ࡳ࡭ࠠࡨࡴ࡬ࡨࠥࡪࡥࡵࡣ࡬ࡰࡸࠦ࠺ࠡࡽࢀࠦৱ").format(str(e)))
        raise RuntimeError(e)
    return {}
def bstack11ll1lll1l_opy_(bstack1l11ll1ll1_opy_):
    global CONFIG
    if bstack11llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ৲") not in CONFIG or str(CONFIG[bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ৳")]).lower() == bstack11llll_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭৴"):
        CONFIG[bstack11llll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࠧ৵")] = False
    elif bstack11llll_opy_ (u"ࠩ࡬ࡷ࡙ࡸࡩࡢ࡮ࡊࡶ࡮ࡪࠧ৶") in bstack1l11ll1ll1_opy_:
        bstack11l11lll11_opy_ = CONFIG.get(bstack11llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ৷"), {})
        logger.debug(bstack11llll_opy_ (u"ࠦࡆ࡚ࡓࠡ࠼ࠣࡉࡽ࡯ࡳࡵ࡫ࡱ࡫ࠥࡲ࡯ࡤࡣ࡯ࠤࡴࡶࡴࡪࡱࡱࡷ࠿ࠦࠥࡴࠤ৸"), bstack11l11lll11_opy_)
        bstack111l1l1ll_opy_ = bstack1l11ll1ll1_opy_.get(bstack11llll_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱࡗ࡫ࡰࡦࡣࡷࡩࡷࡹࠢ৹"), [])
        bstack1l1llll1l_opy_ = bstack11llll_opy_ (u"ࠨࠬࠣ৺").join(bstack111l1l1ll_opy_)
        logger.debug(bstack11llll_opy_ (u"ࠢࡂࡖࡖࠤ࠿ࠦࡃࡶࡵࡷࡳࡲࠦࡲࡦࡲࡨࡥࡹ࡫ࡲࠡࡵࡷࡶ࡮ࡴࡧ࠻ࠢࠨࡷࠧ৻"), bstack1l1llll1l_opy_)
        bstack1llll1ll11_opy_ = {
            bstack11llll_opy_ (u"ࠣ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠥৼ"): bstack11llll_opy_ (u"ࠤࡤࡸࡸ࠳ࡲࡦࡲࡨࡥࡹ࡫ࡲࠣ৽"),
            bstack11llll_opy_ (u"ࠥࡪࡴࡸࡣࡦࡎࡲࡧࡦࡲࠢ৾"): bstack11llll_opy_ (u"ࠦࡹࡸࡵࡦࠤ৿"),
            bstack11llll_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱ࠲ࡸࡥࡱࡧࡤࡸࡪࡸࠢ਀"): bstack1l1llll1l_opy_
        }
        bstack11l11lll11_opy_.update(bstack1llll1ll11_opy_)
        logger.debug(bstack11llll_opy_ (u"ࠨࡁࡕࡕࠣ࠾࡛ࠥࡰࡥࡣࡷࡩࡩࠦ࡬ࡰࡥࡤࡰࠥࡵࡰࡵ࡫ࡲࡲࡸࡀࠠࠦࡵࠥਁ"), bstack11l11lll11_opy_)
        CONFIG[bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫਂ")] = bstack11l11lll11_opy_
        logger.debug(bstack11llll_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡇ࡫ࡱࡥࡱࠦࡃࡐࡐࡉࡍࡌࡀࠠࠦࡵࠥਃ"), CONFIG)
def bstack1l1ll1l11_opy_():
    bstack1l11ll1l1l_opy_ = bstack1l1ll1ll1_opy_()
    if not bstack1l11ll1l1l_opy_[bstack11llll_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࡛ࡲ࡭ࠩ਄")]:
      raise ValueError(bstack11llll_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࡕࡳ࡮ࠣ࡭ࡸࠦ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࡧࡴࡲࡱࠥ࡭ࡲࡪࡦࠣࡨࡪࡺࡡࡪ࡮ࡶ࠲ࠧਅ"))
    return bstack1l11ll1l1l_opy_[bstack11llll_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡖࡴ࡯ࠫਆ")] + bstack11llll_opy_ (u"ࠬࡅࡣࡢࡲࡶࡁࠬਇ")
def bstack11l1ll1ll_opy_() -> list:
    global CONFIG
    result = []
    if CONFIG:
        auth = (CONFIG[bstack11llll_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨਈ")], CONFIG[bstack11llll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪਉ")])
        url = bstack11ll1l11l_opy_
        logger.debug(bstack11llll_opy_ (u"ࠣࡃࡷࡸࡪࡳࡰࡵ࡫ࡱ࡫ࠥࡺ࡯ࠡࡨࡨࡸࡨ࡮ࠠࡣࡷ࡬ࡰࡩࡹࠠࡧࡴࡲࡱࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤ࡙ࡻࡲࡣࡱࡖࡧࡦࡲࡥࠡࡃࡓࡍࠧਊ"))
        try:
            response = requests.get(url, auth=auth, headers={bstack11llll_opy_ (u"ࠤࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠣ਋"): bstack11llll_opy_ (u"ࠥࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳࠨ਌")})
            if response.status_code == 200:
                bstack1l1l11l11l_opy_ = json.loads(response.text)
                bstack11ll1lll1_opy_ = bstack1l1l11l11l_opy_.get(bstack11llll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡶࠫ਍"), [])
                if bstack11ll1lll1_opy_:
                    bstack1111l11ll_opy_ = bstack11ll1lll1_opy_[0]
                    bstack11llll1111_opy_ = bstack1111l11ll_opy_.get(bstack11llll_opy_ (u"ࠬ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ਎"))
                    bstack1l1l1ll1ll_opy_ = bstack11111ll1l_opy_ + bstack11llll1111_opy_
                    result.extend([bstack11llll1111_opy_, bstack1l1l1ll1ll_opy_])
                    logger.info(bstack11l1l11l1l_opy_.format(bstack1l1l1ll1ll_opy_))
                    bstack1l1111llll_opy_ = CONFIG[bstack11llll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩਏ")]
                    if bstack11llll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩਐ") in CONFIG:
                      bstack1l1111llll_opy_ += bstack11llll_opy_ (u"ࠨࠢࠪ਑") + CONFIG[bstack11llll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ਒")]
                    if bstack1l1111llll_opy_ != bstack1111l11ll_opy_.get(bstack11llll_opy_ (u"ࠪࡲࡦࡳࡥࠨਓ")):
                      logger.debug(bstack111lllll1l_opy_.format(bstack1111l11ll_opy_.get(bstack11llll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩਔ")), bstack1l1111llll_opy_))
                    return result
                else:
                    logger.debug(bstack11llll_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡓࡵࠠࡣࡷ࡬ࡰࡩࡹࠠࡧࡱࡸࡲࡩࠦࡩ࡯ࠢࡷ࡬ࡪࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠯ࠤਕ"))
            else:
                logger.debug(bstack11llll_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡨࡨࡸࡨ࡮ࠠࡣࡷ࡬ࡰࡩࡹ࠮ࠣਖ"))
        except Exception as e:
            logger.error(bstack11llll_opy_ (u"ࠢࡂࡖࡖࠤ࠿ࠦࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡥࡹ࡮ࡲࡤࡴࠢ࠽ࠤࢀࢃࠢਗ").format(str(e)))
    else:
        logger.debug(bstack11llll_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡄࡑࡑࡊࡎࡍࠠࡪࡵࠣࡲࡴࡺࠠࡴࡧࡷ࠲࡛ࠥ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡨࡨࡸࡨ࡮ࠠࡣࡷ࡬ࡰࡩࡹ࠮ࠣਘ"))
    return [None, None]
import bstack_utils.bstack1l1l1lll1l_opy_ as bstack1lllll111l_opy_
import bstack_utils.bstack1l1lll11ll_opy_ as bstack11llll1l11_opy_
from browserstack_sdk.sdk_cli.cli import cli
cli.bstack11l11ll111_opy_()
bstack1l1l11l1l_opy_ = bstack11llll_opy_ (u"ࠩࠣࠤ࠴࠰ࠠ࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࠤ࠯࠵࡜࡯ࠢࠣ࡭࡫࠮ࡰࡢࡩࡨࠤࡂࡃ࠽ࠡࡸࡲ࡭ࡩࠦ࠰ࠪࠢࡾࡠࡳࠦࠠࠡࡶࡵࡽࢀࡢ࡮ࠡࡥࡲࡲࡸࡺࠠࡧࡵࠣࡁࠥࡸࡥࡲࡷ࡬ࡶࡪ࠮࡜ࠨࡨࡶࡠࠬ࠯࠻࡝ࡰࠣࠤࠥࠦࠠࡧࡵ࠱ࡥࡵࡶࡥ࡯ࡦࡉ࡭ࡱ࡫ࡓࡺࡰࡦࠬࡧࡹࡴࡢࡥ࡮ࡣࡵࡧࡴࡩ࠮ࠣࡎࡘࡕࡎ࠯ࡵࡷࡶ࡮ࡴࡧࡪࡨࡼࠬࡵࡥࡩ࡯ࡦࡨࡼ࠮ࠦࠫࠡࠤ࠽ࠦࠥ࠱ࠠࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡌࡖࡓࡓ࠴ࡰࡢࡴࡶࡩ࠭࠮ࡡࡸࡣ࡬ࡸࠥࡴࡥࡸࡒࡤ࡫ࡪ࠸࠮ࡦࡸࡤࡰࡺࡧࡴࡦࠪࠥࠬ࠮ࠦ࠽࠿ࠢࡾࢁࠧ࠲ࠠ࡝ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡪࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡥࡵࡣ࡬ࡰࡸࠨࡽ࡝ࠩࠬ࠭࠮ࡡࠢࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠥࡡ࠮ࠦࠫࠡࠤ࠯ࡠࡡࡴࠢࠪ࡞ࡱࠤࠥࠦࠠࡾࡥࡤࡸࡨ࡮ࠨࡦࡺࠬࡿࡡࡴࠠࠡࠢࠣࢁࡡࡴࠠࠡࡿ࡟ࡲࠥࠦ࠯ࠫࠢࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࠦࠪ࠰ࠩਙ")
bstack11lll11111_opy_ = bstack11llll_opy_ (u"ࠪࡠࡳ࠵ࠪࠡ࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࠥ࠰࠯࡝ࡰࡦࡳࡳࡹࡴࠡࡤࡶࡸࡦࡩ࡫ࡠࡲࡤࡸ࡭ࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠵ࡠࡠࡳࡩ࡯࡯ࡵࡷࠤࡧࡹࡴࡢࡥ࡮ࡣࡨࡧࡰࡴࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࡞ࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠶ࡣ࡜࡯ࡥࡲࡲࡸࡺࠠࡱࡡ࡬ࡲࡩ࡫ࡸࠡ࠿ࠣࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࡝ࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࠯࡮ࡨࡲ࡬ࡺࡨࠡ࠯ࠣ࠶ࡢࡢ࡮ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮ࡴ࡮࡬ࡧࡪ࠮࠰࠭ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࠯࡮ࡨࡲ࡬ࡺࡨࠡ࠯ࠣ࠷࠮ࡢ࡮ࡤࡱࡱࡷࡹࠦࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮ࠤࡂࠦࡲࡦࡳࡸ࡭ࡷ࡫ࠨࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧ࠯࠻࡝ࡰ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱ࠮ࡤࡪࡵࡳࡲ࡯ࡵ࡮࠰࡯ࡥࡺࡴࡣࡩࠢࡀࠤࡦࡹࡹ࡯ࡥࠣࠬࡱࡧࡵ࡯ࡥ࡫ࡓࡵࡺࡩࡰࡰࡶ࠭ࠥࡃ࠾ࠡࡽ࡟ࡲࡱ࡫ࡴࠡࡥࡤࡴࡸࡁ࡜࡯ࡶࡵࡽࠥࢁ࡜࡯ࡥࡤࡴࡸࠦ࠽ࠡࡌࡖࡓࡓ࠴ࡰࡢࡴࡶࡩ࠭ࡨࡳࡵࡣࡦ࡯ࡤࡩࡡࡱࡵࠬࡠࡳࠦࠠࡾࠢࡦࡥࡹࡩࡨࠩࡧࡻ࠭ࠥࢁ࡜࡯ࠢࠣࠤࠥࢃ࡜࡯ࠢࠣࡶࡪࡺࡵࡳࡰࠣࡥࡼࡧࡩࡵࠢ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱ࠮ࡤࡪࡵࡳࡲ࡯ࡵ࡮࠰ࡦࡳࡳࡴࡥࡤࡶࠫࡿࡡࡴࠠࠡࠢࠣࡻࡸࡋ࡮ࡥࡲࡲ࡭ࡳࡺ࠺ࠡࡢࡺࡷࡸࡀ࠯࠰ࡥࡧࡴ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡄࡩࡡࡱࡵࡀࠨࢀ࡫࡮ࡤࡱࡧࡩ࡚ࡘࡉࡄࡱࡰࡴࡴࡴࡥ࡯ࡶࠫࡎࡘࡕࡎ࠯ࡵࡷࡶ࡮ࡴࡧࡪࡨࡼࠬࡨࡧࡰࡴࠫࠬࢁࡥ࠲࡜࡯ࠢࠣࠤࠥ࠴࠮࠯࡮ࡤࡹࡳࡩࡨࡐࡲࡷ࡭ࡴࡴࡳ࡝ࡰࠣࠤࢂ࠯࡜࡯ࡿ࡟ࡲ࠴࠰ࠠ࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࠤ࠯࠵࡜࡯ࠩਚ")
from ._version import __version__
bstack11ll111l1_opy_ = None
CONFIG = {}
bstack1ll111l111_opy_ = {}
bstack1l11lll11l_opy_ = {}
bstack1l1l11111_opy_ = None
bstack11l1l1ll1_opy_ = None
bstack1ll11ll11l_opy_ = None
bstack11l111ll1l_opy_ = -1
bstack1lll111lll_opy_ = 0
bstack1ll1l1ll1l_opy_ = bstack1ll111lll_opy_
bstack11lll11ll1_opy_ = 1
bstack1l111l1l11_opy_ = False
bstack1l1l11lll1_opy_ = False
bstack1l1l11llll_opy_ = bstack11llll_opy_ (u"ࠫࠬਛ")
bstack11ll1111l1_opy_ = bstack11llll_opy_ (u"ࠬ࠭ਜ")
bstack11l111lll_opy_ = False
bstack1l1l1l111_opy_ = True
bstack1l1l11lll_opy_ = bstack11llll_opy_ (u"࠭ࠧਝ")
bstack1ll1111111_opy_ = []
bstack111l11l11_opy_ = bstack11llll_opy_ (u"ࠧࠨਞ")
bstack11111l11l_opy_ = False
bstack1ll1111l11_opy_ = None
bstack1l111l111l_opy_ = None
bstack1l1l1l11ll_opy_ = None
bstack11ll1llll1_opy_ = -1
bstack111l1l111_opy_ = os.path.join(os.path.expanduser(bstack11llll_opy_ (u"ࠨࢀࠪਟ")), bstack11llll_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩਠ"), bstack11llll_opy_ (u"ࠪ࠲ࡷࡵࡢࡰࡶ࠰ࡶࡪࡶ࡯ࡳࡶ࠰࡬ࡪࡲࡰࡦࡴ࠱࡮ࡸࡵ࡮ࠨਡ"))
bstack11llll1lll_opy_ = 0
bstack1l111ll1ll_opy_ = 0
bstack1llll1ll1l_opy_ = []
bstack1ll1ll111_opy_ = []
bstack1l1l1lllll_opy_ = []
bstack1111lllll_opy_ = []
bstack111llll1l_opy_ = bstack11llll_opy_ (u"ࠫࠬਢ")
bstack11ll111ll1_opy_ = bstack11llll_opy_ (u"ࠬ࠭ਣ")
bstack1lll1ll11_opy_ = False
bstack1llll1l111_opy_ = False
bstack1l1lll1ll1_opy_ = {}
bstack11l1l1lll1_opy_ = None
bstack1lll11ll11_opy_ = None
bstack1ll11l111_opy_ = None
bstack1lll1lll1_opy_ = None
bstack11ll1l11l1_opy_ = None
bstack11ll1ll1l1_opy_ = None
bstack111l11lll_opy_ = None
bstack1ll1llll11_opy_ = None
bstack11l1lll1ll_opy_ = None
bstack1l1111lll_opy_ = None
bstack11ll1l1l11_opy_ = None
bstack11l1ll111_opy_ = None
bstack1ll1111l1l_opy_ = None
bstack1l11llll1l_opy_ = None
bstack11ll1llll_opy_ = None
bstack11lll1111_opy_ = None
bstack1l1l1l1l1l_opy_ = None
bstack1l1111l1l1_opy_ = None
bstack11lll1l11_opy_ = None
bstack1llll1llll_opy_ = None
bstack1ll1l111ll_opy_ = None
bstack1lll11l1l1_opy_ = None
bstack1l1lll1ll_opy_ = False
bstack111lllllll_opy_ = bstack11llll_opy_ (u"ࠨࠢਤ")
logger = bstack1ll1l1l1l1_opy_.get_logger(__name__, bstack1ll1l1ll1l_opy_)
bstack1111l1l1_opy_ = Config.bstack111ll1ll_opy_()
percy = bstack1ll1lll1ll_opy_()
bstack11l1l1l11l_opy_ = bstack1ll1l11111_opy_()
bstack1l1l111ll_opy_ = bstack11l11lll_opy_()
def bstack1lllllllll_opy_():
  global CONFIG
  global bstack1lll1ll11_opy_
  global bstack1111l1l1_opy_
  bstack1ll111ll1l_opy_ = bstack1l11l11lll_opy_(CONFIG)
  if bstack11ll11111_opy_(CONFIG):
    if (bstack11llll_opy_ (u"ࠧࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩਥ") in bstack1ll111ll1l_opy_ and str(bstack1ll111ll1l_opy_[bstack11llll_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪਦ")]).lower() == bstack11llll_opy_ (u"ࠩࡷࡶࡺ࡫ࠧਧ")):
      bstack1lll1ll11_opy_ = True
    bstack1111l1l1_opy_.bstack1l1lll1lll_opy_(bstack1ll111ll1l_opy_.get(bstack11llll_opy_ (u"ࠪࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧਨ"), False))
  else:
    bstack1lll1ll11_opy_ = True
    bstack1111l1l1_opy_.bstack1l1lll1lll_opy_(True)
def bstack1llll1l1ll_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack111l1111l_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack111lll1l1_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack11llll_opy_ (u"ࠦ࠲࠳ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡨࡵ࡮ࡧ࡫ࡪࡪ࡮ࡲࡥࠣ਩") == args[i].lower() or bstack11llll_opy_ (u"ࠧ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰࡰࡩ࡭࡬ࠨਪ") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1l1l11lll_opy_
      bstack1l1l11lll_opy_ += bstack11llll_opy_ (u"࠭࠭࠮ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡃࡰࡰࡩ࡭࡬ࡌࡩ࡭ࡧࠣࠫਫ") + path
      return path
  return None
bstack1l1l1111l_opy_ = re.compile(bstack11llll_opy_ (u"ࡲࠣ࠰࠭ࡃࡡࠪࡻࠩ࠰࠭ࡃ࠮ࢃ࠮ࠫࡁࠥਬ"))
def bstack11ll11lll1_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack1l1l1111l_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack11llll_opy_ (u"ࠣࠦࡾࠦਭ") + group + bstack11llll_opy_ (u"ࠤࢀࠦਮ"), os.environ.get(group))
  return value
def bstack11llll1l1l_opy_():
  bstack11l1l11lll_opy_ = bstack111lll1l1_opy_()
  if bstack11l1l11lll_opy_ and os.path.exists(os.path.abspath(bstack11l1l11lll_opy_)):
    fileName = bstack11l1l11lll_opy_
  if bstack11llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࡡࡉࡍࡑࡋࠧਯ") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack11llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨਰ")])) and not bstack11llll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡑࡥࡲ࡫ࠧ਱") in locals():
    fileName = os.environ[bstack11llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࡤࡌࡉࡍࡇࠪਲ")]
  if bstack11llll_opy_ (u"ࠧࡧ࡫࡯ࡩࡓࡧ࡭ࡦࠩਲ਼") in locals():
    bstack1l111l_opy_ = os.path.abspath(fileName)
  else:
    bstack1l111l_opy_ = bstack11llll_opy_ (u"ࠨࠩ਴")
  bstack1ll1llll1_opy_ = os.getcwd()
  bstack11llllll11_opy_ = bstack11llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠬਵ")
  bstack1l11l1l1ll_opy_ = bstack11llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡥࡲࡲࠧਸ਼")
  while (not os.path.exists(bstack1l111l_opy_)) and bstack1ll1llll1_opy_ != bstack11llll_opy_ (u"ࠦࠧ਷"):
    bstack1l111l_opy_ = os.path.join(bstack1ll1llll1_opy_, bstack11llllll11_opy_)
    if not os.path.exists(bstack1l111l_opy_):
      bstack1l111l_opy_ = os.path.join(bstack1ll1llll1_opy_, bstack1l11l1l1ll_opy_)
    if bstack1ll1llll1_opy_ != os.path.dirname(bstack1ll1llll1_opy_):
      bstack1ll1llll1_opy_ = os.path.dirname(bstack1ll1llll1_opy_)
    else:
      bstack1ll1llll1_opy_ = bstack11llll_opy_ (u"ࠧࠨਸ")
  return bstack1l111l_opy_ if os.path.exists(bstack1l111l_opy_) else None
def bstack1ll1111ll1_opy_():
  bstack1l111l_opy_ = bstack11llll1l1l_opy_()
  if not os.path.exists(bstack1l111l_opy_):
    bstack1ll1l1lll_opy_(
      bstack111lllll11_opy_.format(os.getcwd()))
  try:
    with open(bstack1l111l_opy_, bstack11llll_opy_ (u"࠭ࡲࠨਹ")) as stream:
      yaml.add_implicit_resolver(bstack11llll_opy_ (u"ࠢࠢࡲࡤࡸ࡭࡫ࡸࠣ਺"), bstack1l1l1111l_opy_)
      yaml.add_constructor(bstack11llll_opy_ (u"ࠣࠣࡳࡥࡹ࡮ࡥࡹࠤ਻"), bstack11ll11lll1_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      return config
  except:
    with open(bstack1l111l_opy_, bstack11llll_opy_ (u"ࠩࡵ਼ࠫ")) as stream:
      try:
        config = yaml.safe_load(stream)
        return config
      except yaml.YAMLError as exc:
        bstack1ll1l1lll_opy_(bstack1111ll11l_opy_.format(str(exc)))
def bstack11111l1ll_opy_(config):
  bstack1ll1l11l1_opy_ = bstack1l111l1lll_opy_(config)
  for option in list(bstack1ll1l11l1_opy_):
    if option.lower() in bstack1111lll11_opy_ and option != bstack1111lll11_opy_[option.lower()]:
      bstack1ll1l11l1_opy_[bstack1111lll11_opy_[option.lower()]] = bstack1ll1l11l1_opy_[option]
      del bstack1ll1l11l1_opy_[option]
  return config
def bstack1ll111l11l_opy_():
  global bstack1l11lll11l_opy_
  for key, bstack1ll1l1ll11_opy_ in bstack1l11lll111_opy_.items():
    if isinstance(bstack1ll1l1ll11_opy_, list):
      for var in bstack1ll1l1ll11_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack1l11lll11l_opy_[key] = os.environ[var]
          break
    elif bstack1ll1l1ll11_opy_ in os.environ and os.environ[bstack1ll1l1ll11_opy_] and str(os.environ[bstack1ll1l1ll11_opy_]).strip():
      bstack1l11lll11l_opy_[key] = os.environ[bstack1ll1l1ll11_opy_]
  if bstack11llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬ਽") in os.environ:
    bstack1l11lll11l_opy_[bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨਾ")] = {}
    bstack1l11lll11l_opy_[bstack11llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩਿ")][bstack11llll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨੀ")] = os.environ[bstack11llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩੁ")]
def bstack11l11l1lll_opy_():
  global bstack1ll111l111_opy_
  global bstack1l1l11lll_opy_
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) and bstack11llll_opy_ (u"ࠨ࠯࠰ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫੂ").lower() == val.lower():
      bstack1ll111l111_opy_[bstack11llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭੃")] = {}
      bstack1ll111l111_opy_[bstack11llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ੄")][bstack11llll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭੅")] = sys.argv[idx + 1]
      del sys.argv[idx:idx + 2]
      break
  for key, bstack11l1l1l1l1_opy_ in bstack11lll11l1l_opy_.items():
    if isinstance(bstack11l1l1l1l1_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack11l1l1l1l1_opy_:
          if idx < len(sys.argv) and bstack11llll_opy_ (u"ࠬ࠳࠭ࠨ੆") + var.lower() == val.lower() and not key in bstack1ll111l111_opy_:
            bstack1ll111l111_opy_[key] = sys.argv[idx + 1]
            bstack1l1l11lll_opy_ += bstack11llll_opy_ (u"࠭ࠠ࠮࠯ࠪੇ") + var + bstack11llll_opy_ (u"ࠧࠡࠩੈ") + sys.argv[idx + 1]
            del sys.argv[idx:idx + 2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx < len(sys.argv) and bstack11llll_opy_ (u"ࠨ࠯࠰ࠫ੉") + bstack11l1l1l1l1_opy_.lower() == val.lower() and not key in bstack1ll111l111_opy_:
          bstack1ll111l111_opy_[key] = sys.argv[idx + 1]
          bstack1l1l11lll_opy_ += bstack11llll_opy_ (u"ࠩࠣ࠱࠲࠭੊") + bstack11l1l1l1l1_opy_ + bstack11llll_opy_ (u"ࠪࠤࠬੋ") + sys.argv[idx + 1]
          del sys.argv[idx:idx + 2]
def bstack11111llll_opy_(config):
  bstack1ll1llllll_opy_ = config.keys()
  for bstack111lll111_opy_, bstack1l11l1l1l1_opy_ in bstack1ll1ll1l11_opy_.items():
    if bstack1l11l1l1l1_opy_ in bstack1ll1llllll_opy_:
      config[bstack111lll111_opy_] = config[bstack1l11l1l1l1_opy_]
      del config[bstack1l11l1l1l1_opy_]
  for bstack111lll111_opy_, bstack1l11l1l1l1_opy_ in bstack11ll111l11_opy_.items():
    if isinstance(bstack1l11l1l1l1_opy_, list):
      for bstack11l11lll1l_opy_ in bstack1l11l1l1l1_opy_:
        if bstack11l11lll1l_opy_ in bstack1ll1llllll_opy_:
          config[bstack111lll111_opy_] = config[bstack11l11lll1l_opy_]
          del config[bstack11l11lll1l_opy_]
          break
    elif bstack1l11l1l1l1_opy_ in bstack1ll1llllll_opy_:
      config[bstack111lll111_opy_] = config[bstack1l11l1l1l1_opy_]
      del config[bstack1l11l1l1l1_opy_]
  for bstack11l11lll1l_opy_ in list(config):
    for bstack1ll1l11ll_opy_ in bstack111l1llll_opy_:
      if bstack11l11lll1l_opy_.lower() == bstack1ll1l11ll_opy_.lower() and bstack11l11lll1l_opy_ != bstack1ll1l11ll_opy_:
        config[bstack1ll1l11ll_opy_] = config[bstack11l11lll1l_opy_]
        del config[bstack11l11lll1l_opy_]
  bstack11l11lll1_opy_ = [{}]
  if not config.get(bstack11llll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧੌ")):
    config[bstack11llll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ੍")] = [{}]
  bstack11l11lll1_opy_ = config[bstack11llll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ੎")]
  for platform in bstack11l11lll1_opy_:
    for bstack11l11lll1l_opy_ in list(platform):
      for bstack1ll1l11ll_opy_ in bstack111l1llll_opy_:
        if bstack11l11lll1l_opy_.lower() == bstack1ll1l11ll_opy_.lower() and bstack11l11lll1l_opy_ != bstack1ll1l11ll_opy_:
          platform[bstack1ll1l11ll_opy_] = platform[bstack11l11lll1l_opy_]
          del platform[bstack11l11lll1l_opy_]
  for bstack111lll111_opy_, bstack1l11l1l1l1_opy_ in bstack11ll111l11_opy_.items():
    for platform in bstack11l11lll1_opy_:
      if isinstance(bstack1l11l1l1l1_opy_, list):
        for bstack11l11lll1l_opy_ in bstack1l11l1l1l1_opy_:
          if bstack11l11lll1l_opy_ in platform:
            platform[bstack111lll111_opy_] = platform[bstack11l11lll1l_opy_]
            del platform[bstack11l11lll1l_opy_]
            break
      elif bstack1l11l1l1l1_opy_ in platform:
        platform[bstack111lll111_opy_] = platform[bstack1l11l1l1l1_opy_]
        del platform[bstack1l11l1l1l1_opy_]
  for bstack11llll111_opy_ in bstack11ll1111l_opy_:
    if bstack11llll111_opy_ in config:
      if not bstack11ll1111l_opy_[bstack11llll111_opy_] in config:
        config[bstack11ll1111l_opy_[bstack11llll111_opy_]] = {}
      config[bstack11ll1111l_opy_[bstack11llll111_opy_]].update(config[bstack11llll111_opy_])
      del config[bstack11llll111_opy_]
  for platform in bstack11l11lll1_opy_:
    for bstack11llll111_opy_ in bstack11ll1111l_opy_:
      if bstack11llll111_opy_ in list(platform):
        if not bstack11ll1111l_opy_[bstack11llll111_opy_] in platform:
          platform[bstack11ll1111l_opy_[bstack11llll111_opy_]] = {}
        platform[bstack11ll1111l_opy_[bstack11llll111_opy_]].update(platform[bstack11llll111_opy_])
        del platform[bstack11llll111_opy_]
  config = bstack11111l1ll_opy_(config)
  return config
def bstack1llllll1l1_opy_(config):
  global bstack11ll1111l1_opy_
  bstack11lll11l11_opy_ = False
  if bstack11llll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ੏") in config and str(config[bstack11llll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ੐")]).lower() != bstack11llll_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨੑ"):
    if bstack11llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ੒") not in config or str(config[bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ੓")]).lower() == bstack11llll_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ੔"):
      config[bstack11llll_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬ੕")] = False
    else:
      bstack1l11ll1l1l_opy_ = bstack1l1ll1ll1_opy_()
      if bstack11llll_opy_ (u"ࠧࡪࡵࡗࡶ࡮ࡧ࡬ࡈࡴ࡬ࡨࠬ੖") in bstack1l11ll1l1l_opy_:
        if not bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ੗") in config:
          config[bstack11llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭੘")] = {}
        config[bstack11llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧਖ਼")][bstack11llll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ਗ਼")] = bstack11llll_opy_ (u"ࠬࡧࡴࡴ࠯ࡵࡩࡵ࡫ࡡࡵࡧࡵࠫਜ਼")
        bstack11lll11l11_opy_ = True
        bstack11ll1111l1_opy_ = config[bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪੜ")].get(bstack11llll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ੝"))
  if bstack11ll11111_opy_(config) and bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬਫ਼") in config and str(config[bstack11llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭੟")]).lower() != bstack11llll_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩ੠") and not bstack11lll11l11_opy_:
    if not bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ੡") in config:
      config[bstack11llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ੢")] = {}
    if not config[bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ੣")].get(bstack11llll_opy_ (u"ࠧࡴ࡭࡬ࡴࡇ࡯࡮ࡢࡴࡼࡍࡳ࡯ࡴࡪࡣ࡯࡭ࡸࡧࡴࡪࡱࡱࠫ੤")) and not bstack11llll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ੥") in config[bstack11llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭੦")]:
      bstack1l111ll1_opy_ = datetime.datetime.now()
      bstack1l1l1l1111_opy_ = bstack1l111ll1_opy_.strftime(bstack11llll_opy_ (u"ࠪࠩࡩࡥࠥࡣࡡࠨࡌࠪࡓࠧ੧"))
      hostname = socket.gethostname()
      bstack11l1lll11_opy_ = bstack11llll_opy_ (u"ࠫࠬ੨").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack11llll_opy_ (u"ࠬࢁࡽࡠࡽࢀࡣࢀࢃࠧ੩").format(bstack1l1l1l1111_opy_, hostname, bstack11l1lll11_opy_)
      config[bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ੪")][bstack11llll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ੫")] = identifier
    bstack11ll1111l1_opy_ = config[bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ੬")].get(bstack11llll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ੭"))
  return config
def bstack1l1l1ll11_opy_():
  bstack1llll11lll_opy_ =  bstack1l1111ll1l_opy_()[bstack11llll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠩ੮")]
  return bstack1llll11lll_opy_ if bstack1llll11lll_opy_ else -1
def bstack1l1l11ll1_opy_(bstack1llll11lll_opy_):
  global CONFIG
  if not bstack11llll_opy_ (u"ࠫࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭੯") in CONFIG[bstack11llll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧੰ")]:
    return
  CONFIG[bstack11llll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨੱ")] = CONFIG[bstack11llll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩੲ")].replace(
    bstack11llll_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪੳ"),
    str(bstack1llll11lll_opy_)
  )
def bstack11l1llll1_opy_():
  global CONFIG
  if not bstack11llll_opy_ (u"ࠩࠧࡿࡉࡇࡔࡆࡡࡗࡍࡒࡋࡽࠨੴ") in CONFIG[bstack11llll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬੵ")]:
    return
  bstack1l111ll1_opy_ = datetime.datetime.now()
  bstack1l1l1l1111_opy_ = bstack1l111ll1_opy_.strftime(bstack11llll_opy_ (u"ࠫࠪࡪ࠭ࠦࡤ࠰ࠩࡍࡀࠥࡎࠩ੶"))
  CONFIG[bstack11llll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ੷")] = CONFIG[bstack11llll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ੸")].replace(
    bstack11llll_opy_ (u"ࠧࠥࡽࡇࡅ࡙ࡋ࡟ࡕࡋࡐࡉࢂ࠭੹"),
    bstack1l1l1l1111_opy_
  )
def bstack1ll1111ll_opy_():
  global CONFIG
  if bstack11llll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ੺") in CONFIG and not bool(CONFIG[bstack11llll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ੻")]):
    del CONFIG[bstack11llll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ੼")]
    return
  if not bstack11llll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭੽") in CONFIG:
    CONFIG[bstack11llll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ੾")] = bstack11llll_opy_ (u"࠭ࠣࠥࡽࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࡾࠩ੿")
  if bstack11llll_opy_ (u"ࠧࠥࡽࡇࡅ࡙ࡋ࡟ࡕࡋࡐࡉࢂ࠭઀") in CONFIG[bstack11llll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪઁ")]:
    bstack11l1llll1_opy_()
    os.environ[bstack11llll_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡡࡆࡓࡒࡈࡉࡏࡇࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉ࠭ં")] = CONFIG[bstack11llll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬઃ")]
  if not bstack11llll_opy_ (u"ࠫࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭઄") in CONFIG[bstack11llll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧઅ")]:
    return
  bstack1llll11lll_opy_ = bstack11llll_opy_ (u"࠭ࠧઆ")
  bstack1l1ll1111_opy_ = bstack1l1l1ll11_opy_()
  if bstack1l1ll1111_opy_ != -1:
    bstack1llll11lll_opy_ = bstack11llll_opy_ (u"ࠧࡄࡋࠣࠫઇ") + str(bstack1l1ll1111_opy_)
  if bstack1llll11lll_opy_ == bstack11llll_opy_ (u"ࠨࠩઈ"):
    bstack1lll11l11_opy_ = bstack1l1l1l1ll_opy_(CONFIG[bstack11llll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬઉ")])
    if bstack1lll11l11_opy_ != -1:
      bstack1llll11lll_opy_ = str(bstack1lll11l11_opy_)
  if bstack1llll11lll_opy_:
    bstack1l1l11ll1_opy_(bstack1llll11lll_opy_)
    os.environ[bstack11llll_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧઊ")] = CONFIG[bstack11llll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ઋ")]
def bstack11l1lll1l1_opy_(bstack111llll11_opy_, bstack11ll1ll111_opy_, path):
  json_data = {
    bstack11llll_opy_ (u"ࠬ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩઌ"): bstack11ll1ll111_opy_
  }
  if os.path.exists(path):
    bstack1l1lll1111_opy_ = json.load(open(path, bstack11llll_opy_ (u"࠭ࡲࡣࠩઍ")))
  else:
    bstack1l1lll1111_opy_ = {}
  bstack1l1lll1111_opy_[bstack111llll11_opy_] = json_data
  with open(path, bstack11llll_opy_ (u"ࠢࡸ࠭ࠥ઎")) as outfile:
    json.dump(bstack1l1lll1111_opy_, outfile)
def bstack1l1l1l1ll_opy_(bstack111llll11_opy_):
  bstack111llll11_opy_ = str(bstack111llll11_opy_)
  bstack11ll1ll11l_opy_ = os.path.join(os.path.expanduser(bstack11llll_opy_ (u"ࠨࢀࠪએ")), bstack11llll_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩઐ"))
  try:
    if not os.path.exists(bstack11ll1ll11l_opy_):
      os.makedirs(bstack11ll1ll11l_opy_)
    file_path = os.path.join(os.path.expanduser(bstack11llll_opy_ (u"ࠪࢂࠬઑ")), bstack11llll_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ઒"), bstack11llll_opy_ (u"ࠬ࠴ࡢࡶ࡫࡯ࡨ࠲ࡴࡡ࡮ࡧ࠰ࡧࡦࡩࡨࡦ࠰࡭ࡷࡴࡴࠧઓ"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack11llll_opy_ (u"࠭ࡷࠨઔ")):
        pass
      with open(file_path, bstack11llll_opy_ (u"ࠢࡸ࠭ࠥક")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack11llll_opy_ (u"ࠨࡴࠪખ")) as bstack11ll111l1l_opy_:
      bstack1l1l111l1l_opy_ = json.load(bstack11ll111l1l_opy_)
    if bstack111llll11_opy_ in bstack1l1l111l1l_opy_:
      bstack11llll1l1_opy_ = bstack1l1l111l1l_opy_[bstack111llll11_opy_][bstack11llll_opy_ (u"ࠩ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ગ")]
      bstack1llll11ll1_opy_ = int(bstack11llll1l1_opy_) + 1
      bstack11l1lll1l1_opy_(bstack111llll11_opy_, bstack1llll11ll1_opy_, file_path)
      return bstack1llll11ll1_opy_
    else:
      bstack11l1lll1l1_opy_(bstack111llll11_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack1lll1ll111_opy_.format(str(e)))
    return -1
def bstack1lll1llll1_opy_(config):
  if not config[bstack11llll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬઘ")] or not config[bstack11llll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧઙ")]:
    return True
  else:
    return False
def bstack1l111l1111_opy_(config, index=0):
  global bstack11l111lll_opy_
  bstack1ll1l11ll1_opy_ = {}
  caps = bstack11l111l11_opy_ + bstack1l11l11l11_opy_
  if config.get(bstack11llll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩચ"), False):
    bstack1ll1l11ll1_opy_[bstack11llll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪછ")] = True
    bstack1ll1l11ll1_opy_[bstack11llll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࡓࡵࡺࡩࡰࡰࡶࠫજ")] = config.get(bstack11llll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࡔࡶࡴࡪࡱࡱࡷࠬઝ"), {})
  if bstack11l111lll_opy_:
    caps += bstack11lll1l1l_opy_
  for key in config:
    if key in caps + [bstack11llll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬઞ")]:
      continue
    bstack1ll1l11ll1_opy_[key] = config[key]
  if bstack11llll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ટ") in config:
    for bstack1l1lll111_opy_ in config[bstack11llll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧઠ")][index]:
      if bstack1l1lll111_opy_ in caps:
        continue
      bstack1ll1l11ll1_opy_[bstack1l1lll111_opy_] = config[bstack11llll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨડ")][index][bstack1l1lll111_opy_]
  bstack1ll1l11ll1_opy_[bstack11llll_opy_ (u"࠭ࡨࡰࡵࡷࡒࡦࡳࡥࠨઢ")] = socket.gethostname()
  if bstack11llll_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨણ") in bstack1ll1l11ll1_opy_:
    del (bstack1ll1l11ll1_opy_[bstack11llll_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩત")])
  return bstack1ll1l11ll1_opy_
def bstack11l1l1ll1l_opy_(config):
  global bstack11l111lll_opy_
  bstack11ll11l111_opy_ = {}
  caps = bstack1l11l11l11_opy_
  if bstack11l111lll_opy_:
    caps += bstack11lll1l1l_opy_
  for key in caps:
    if key in config:
      bstack11ll11l111_opy_[key] = config[key]
  return bstack11ll11l111_opy_
def bstack1llll1l11_opy_(bstack1ll1l11ll1_opy_, bstack11ll11l111_opy_):
  bstack11ll11l1ll_opy_ = {}
  for key in bstack1ll1l11ll1_opy_.keys():
    if key in bstack1ll1ll1l11_opy_:
      bstack11ll11l1ll_opy_[bstack1ll1ll1l11_opy_[key]] = bstack1ll1l11ll1_opy_[key]
    else:
      bstack11ll11l1ll_opy_[key] = bstack1ll1l11ll1_opy_[key]
  for key in bstack11ll11l111_opy_:
    if key in bstack1ll1ll1l11_opy_:
      bstack11ll11l1ll_opy_[bstack1ll1ll1l11_opy_[key]] = bstack11ll11l111_opy_[key]
    else:
      bstack11ll11l1ll_opy_[key] = bstack11ll11l111_opy_[key]
  return bstack11ll11l1ll_opy_
def bstack11lll1ll1_opy_(config, index=0):
  global bstack11l111lll_opy_
  caps = {}
  config = copy.deepcopy(config)
  bstack11l1l1l1ll_opy_ = bstack1l1lllll1l_opy_(bstack1111l1l1l_opy_, config, logger)
  bstack11ll11l111_opy_ = bstack11l1l1ll1l_opy_(config)
  bstack11l1llll1l_opy_ = bstack1l11l11l11_opy_
  bstack11l1llll1l_opy_ += bstack1lll11lll1_opy_
  bstack11ll11l111_opy_ = update(bstack11ll11l111_opy_, bstack11l1l1l1ll_opy_)
  if bstack11l111lll_opy_:
    bstack11l1llll1l_opy_ += bstack11lll1l1l_opy_
  if bstack11llll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬથ") in config:
    if bstack11llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨદ") in config[bstack11llll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧધ")][index]:
      caps[bstack11llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪન")] = config[bstack11llll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ઩")][index][bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬપ")]
    if bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩફ") in config[bstack11llll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬબ")][index]:
      caps[bstack11llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫભ")] = str(config[bstack11llll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧમ")][index][bstack11llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ય")])
    bstack1ll111ll11_opy_ = bstack1l1lllll1l_opy_(bstack1111l1l1l_opy_, config[bstack11llll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩર")][index], logger)
    bstack11l1llll1l_opy_ += list(bstack1ll111ll11_opy_.keys())
    for bstack1l1111lll1_opy_ in bstack11l1llll1l_opy_:
      if bstack1l1111lll1_opy_ in config[bstack11llll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ઱")][index]:
        if bstack1l1111lll1_opy_ == bstack11llll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪલ"):
          try:
            bstack1ll111ll11_opy_[bstack1l1111lll1_opy_] = str(config[bstack11llll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬળ")][index][bstack1l1111lll1_opy_] * 1.0)
          except:
            bstack1ll111ll11_opy_[bstack1l1111lll1_opy_] = str(config[bstack11llll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭઴")][index][bstack1l1111lll1_opy_])
        else:
          bstack1ll111ll11_opy_[bstack1l1111lll1_opy_] = config[bstack11llll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧવ")][index][bstack1l1111lll1_opy_]
        del (config[bstack11llll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨશ")][index][bstack1l1111lll1_opy_])
    bstack11ll11l111_opy_ = update(bstack11ll11l111_opy_, bstack1ll111ll11_opy_)
  bstack1ll1l11ll1_opy_ = bstack1l111l1111_opy_(config, index)
  for bstack11l11lll1l_opy_ in bstack1l11l11l11_opy_ + list(bstack11l1l1l1ll_opy_.keys()):
    if bstack11l11lll1l_opy_ in bstack1ll1l11ll1_opy_:
      bstack11ll11l111_opy_[bstack11l11lll1l_opy_] = bstack1ll1l11ll1_opy_[bstack11l11lll1l_opy_]
      del (bstack1ll1l11ll1_opy_[bstack11l11lll1l_opy_])
  if bstack1ll11l1111_opy_(config):
    bstack1ll1l11ll1_opy_[bstack11llll_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ષ")] = True
    caps.update(bstack11ll11l111_opy_)
    caps[bstack11llll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨસ")] = bstack1ll1l11ll1_opy_
  else:
    bstack1ll1l11ll1_opy_[bstack11llll_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨહ")] = False
    caps.update(bstack1llll1l11_opy_(bstack1ll1l11ll1_opy_, bstack11ll11l111_opy_))
    if bstack11llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ઺") in caps:
      caps[bstack11llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫ઻")] = caps[bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦ઼ࠩ")]
      del (caps[bstack11llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪઽ")])
    if bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧા") in caps:
      caps[bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩિ")] = caps[bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩી")]
      del (caps[bstack11llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪુ")])
  return caps
def bstack1lll1l1l1l_opy_():
  global bstack111l11l11_opy_
  global CONFIG
  if bstack111l1111l_opy_() <= version.parse(bstack11llll_opy_ (u"ࠪ࠷࠳࠷࠳࠯࠲ࠪૂ")):
    if bstack111l11l11_opy_ != bstack11llll_opy_ (u"ࠫࠬૃ"):
      return bstack11llll_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨૄ") + bstack111l11l11_opy_ + bstack11llll_opy_ (u"ࠨ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠥૅ")
    return bstack11ll11lll_opy_
  if bstack111l11l11_opy_ != bstack11llll_opy_ (u"ࠧࠨ૆"):
    return bstack11llll_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥે") + bstack111l11l11_opy_ + bstack11llll_opy_ (u"ࠤ࠲ࡻࡩ࠵ࡨࡶࡤࠥૈ")
  return bstack1llll111ll_opy_
def bstack111111l1l_opy_(options):
  return hasattr(options, bstack11llll_opy_ (u"ࠪࡷࡪࡺ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶࡼࠫૉ"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack111ll1ll1_opy_(options, bstack1ll111l1ll_opy_):
  for bstack11l1lll11l_opy_ in bstack1ll111l1ll_opy_:
    if bstack11l1lll11l_opy_ in [bstack11llll_opy_ (u"ࠫࡦࡸࡧࡴࠩ૊"), bstack11llll_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩો")]:
      continue
    if bstack11l1lll11l_opy_ in options._experimental_options:
      options._experimental_options[bstack11l1lll11l_opy_] = update(options._experimental_options[bstack11l1lll11l_opy_],
                                                         bstack1ll111l1ll_opy_[bstack11l1lll11l_opy_])
    else:
      options.add_experimental_option(bstack11l1lll11l_opy_, bstack1ll111l1ll_opy_[bstack11l1lll11l_opy_])
  if bstack11llll_opy_ (u"࠭ࡡࡳࡩࡶࠫૌ") in bstack1ll111l1ll_opy_:
    for arg in bstack1ll111l1ll_opy_[bstack11llll_opy_ (u"ࠧࡢࡴࡪࡷ્ࠬ")]:
      options.add_argument(arg)
    del (bstack1ll111l1ll_opy_[bstack11llll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭૎")])
  if bstack11llll_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭૏") in bstack1ll111l1ll_opy_:
    for ext in bstack1ll111l1ll_opy_[bstack11llll_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧૐ")]:
      options.add_extension(ext)
    del (bstack1ll111l1ll_opy_[bstack11llll_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨ૑")])
def bstack1l11lll1l1_opy_(options, bstack11ll11ll1l_opy_):
  if bstack11llll_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫ૒") in bstack11ll11ll1l_opy_:
    for bstack111111ll1_opy_ in bstack11ll11ll1l_opy_[bstack11llll_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬ૓")]:
      if bstack111111ll1_opy_ in options._preferences:
        options._preferences[bstack111111ll1_opy_] = update(options._preferences[bstack111111ll1_opy_], bstack11ll11ll1l_opy_[bstack11llll_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭૔")][bstack111111ll1_opy_])
      else:
        options.set_preference(bstack111111ll1_opy_, bstack11ll11ll1l_opy_[bstack11llll_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧ૕")][bstack111111ll1_opy_])
  if bstack11llll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ૖") in bstack11ll11ll1l_opy_:
    for arg in bstack11ll11ll1l_opy_[bstack11llll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨ૗")]:
      options.add_argument(arg)
def bstack11l1111l1l_opy_(options, bstack1llll11l11_opy_):
  if bstack11llll_opy_ (u"ࠫࡼ࡫ࡢࡷ࡫ࡨࡻࠬ૘") in bstack1llll11l11_opy_:
    options.use_webview(bool(bstack1llll11l11_opy_[bstack11llll_opy_ (u"ࠬࡽࡥࡣࡸ࡬ࡩࡼ࠭૙")]))
  bstack111ll1ll1_opy_(options, bstack1llll11l11_opy_)
def bstack11l1ll1l1l_opy_(options, bstack1l1ll111l1_opy_):
  for bstack1l1ll1l1l1_opy_ in bstack1l1ll111l1_opy_:
    if bstack1l1ll1l1l1_opy_ in [bstack11llll_opy_ (u"࠭ࡴࡦࡥ࡫ࡲࡴࡲ࡯ࡨࡻࡓࡶࡪࡼࡩࡦࡹࠪ૚"), bstack11llll_opy_ (u"ࠧࡢࡴࡪࡷࠬ૛")]:
      continue
    options.set_capability(bstack1l1ll1l1l1_opy_, bstack1l1ll111l1_opy_[bstack1l1ll1l1l1_opy_])
  if bstack11llll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭૜") in bstack1l1ll111l1_opy_:
    for arg in bstack1l1ll111l1_opy_[bstack11llll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ૝")]:
      options.add_argument(arg)
  if bstack11llll_opy_ (u"ࠪࡸࡪࡩࡨ࡯ࡱ࡯ࡳ࡬ࡿࡐࡳࡧࡹ࡭ࡪࡽࠧ૞") in bstack1l1ll111l1_opy_:
    options.bstack1lll1l11l_opy_(bool(bstack1l1ll111l1_opy_[bstack11llll_opy_ (u"ࠫࡹ࡫ࡣࡩࡰࡲࡰࡴ࡭ࡹࡑࡴࡨࡺ࡮࡫ࡷࠨ૟")]))
def bstack1111l1lll_opy_(options, bstack1l111l111_opy_):
  for bstack1l11ll1111_opy_ in bstack1l111l111_opy_:
    if bstack1l11ll1111_opy_ in [bstack11llll_opy_ (u"ࠬࡧࡤࡥ࡫ࡷ࡭ࡴࡴࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩૠ"), bstack11llll_opy_ (u"࠭ࡡࡳࡩࡶࠫૡ")]:
      continue
    options._options[bstack1l11ll1111_opy_] = bstack1l111l111_opy_[bstack1l11ll1111_opy_]
  if bstack11llll_opy_ (u"ࠧࡢࡦࡧ࡭ࡹ࡯࡯࡯ࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫૢ") in bstack1l111l111_opy_:
    for bstack1l1l1l1l1_opy_ in bstack1l111l111_opy_[bstack11llll_opy_ (u"ࠨࡣࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬૣ")]:
      options.bstack1l1lll111l_opy_(
        bstack1l1l1l1l1_opy_, bstack1l111l111_opy_[bstack11llll_opy_ (u"ࠩࡤࡨࡩ࡯ࡴࡪࡱࡱࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭૤")][bstack1l1l1l1l1_opy_])
  if bstack11llll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨ૥") in bstack1l111l111_opy_:
    for arg in bstack1l111l111_opy_[bstack11llll_opy_ (u"ࠫࡦࡸࡧࡴࠩ૦")]:
      options.add_argument(arg)
def bstack1l11l1ll1_opy_(options, caps):
  if not hasattr(options, bstack11llll_opy_ (u"ࠬࡑࡅ࡚ࠩ૧")):
    return
  if options.KEY == bstack11llll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ૨") and options.KEY in caps:
    bstack111ll1ll1_opy_(options, caps[bstack11llll_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ૩")])
  elif options.KEY == bstack11llll_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭૪") and options.KEY in caps:
    bstack1l11lll1l1_opy_(options, caps[bstack11llll_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧ૫")])
  elif options.KEY == bstack11llll_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫ૬") and options.KEY in caps:
    bstack11l1ll1l1l_opy_(options, caps[bstack11llll_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬ૭")])
  elif options.KEY == bstack11llll_opy_ (u"ࠬࡳࡳ࠻ࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭૮") and options.KEY in caps:
    bstack11l1111l1l_opy_(options, caps[bstack11llll_opy_ (u"࠭࡭ࡴ࠼ࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ૯")])
  elif options.KEY == bstack11llll_opy_ (u"ࠧࡴࡧ࠽࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭૰") and options.KEY in caps:
    bstack1111l1lll_opy_(options, caps[bstack11llll_opy_ (u"ࠨࡵࡨ࠾࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ૱")])
def bstack1llll1ll1_opy_(caps):
  global bstack11l111lll_opy_
  if isinstance(os.environ.get(bstack11llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪ૲")), str):
    bstack11l111lll_opy_ = eval(os.getenv(bstack11llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫ૳")))
  if bstack11l111lll_opy_:
    if bstack1llll1l1ll_opy_() < version.parse(bstack11llll_opy_ (u"ࠫ࠷࠴࠳࠯࠲ࠪ૴")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack11llll_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬ૵")
    if bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ૶") in caps:
      browser = caps[bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ૷")]
    elif bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩ૸") in caps:
      browser = caps[bstack11llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪૹ")]
    browser = str(browser).lower()
    if browser == bstack11llll_opy_ (u"ࠪ࡭ࡵ࡮࡯࡯ࡧࠪૺ") or browser == bstack11llll_opy_ (u"ࠫ࡮ࡶࡡࡥࠩૻ"):
      browser = bstack11llll_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࠬૼ")
    if browser == bstack11llll_opy_ (u"࠭ࡳࡢ࡯ࡶࡹࡳ࡭ࠧ૽"):
      browser = bstack11llll_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧ૾")
    if browser not in [bstack11llll_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨ૿"), bstack11llll_opy_ (u"ࠩࡨࡨ࡬࡫ࠧ଀"), bstack11llll_opy_ (u"ࠪ࡭ࡪ࠭ଁ"), bstack11llll_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࠫଂ"), bstack11llll_opy_ (u"ࠬ࡬ࡩࡳࡧࡩࡳࡽ࠭ଃ")]:
      return None
    try:
      package = bstack11llll_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࠯ࡹࡨࡦࡩࡸࡩࡷࡧࡵ࠲ࢀࢃ࠮ࡰࡲࡷ࡭ࡴࡴࡳࠨ଄").format(browser)
      name = bstack11llll_opy_ (u"ࠧࡐࡲࡷ࡭ࡴࡴࡳࠨଅ")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack111111l1l_opy_(options):
        return None
      for bstack11l11lll1l_opy_ in caps.keys():
        options.set_capability(bstack11l11lll1l_opy_, caps[bstack11l11lll1l_opy_])
      bstack1l11l1ll1_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1ll1l1l1ll_opy_(options, bstack11lll11lll_opy_):
  if not bstack111111l1l_opy_(options):
    return
  for bstack11l11lll1l_opy_ in bstack11lll11lll_opy_.keys():
    if bstack11l11lll1l_opy_ in bstack1lll11lll1_opy_:
      continue
    if bstack11l11lll1l_opy_ in options._caps and type(options._caps[bstack11l11lll1l_opy_]) in [dict, list]:
      options._caps[bstack11l11lll1l_opy_] = update(options._caps[bstack11l11lll1l_opy_], bstack11lll11lll_opy_[bstack11l11lll1l_opy_])
    else:
      options.set_capability(bstack11l11lll1l_opy_, bstack11lll11lll_opy_[bstack11l11lll1l_opy_])
  bstack1l11l1ll1_opy_(options, bstack11lll11lll_opy_)
  if bstack11llll_opy_ (u"ࠨ࡯ࡲࡾ࠿ࡪࡥࡣࡷࡪ࡫ࡪࡸࡁࡥࡦࡵࡩࡸࡹࠧଆ") in options._caps:
    if options._caps[bstack11llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧଇ")] and options._caps[bstack11llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨଈ")].lower() != bstack11llll_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬଉ"):
      del options._caps[bstack11llll_opy_ (u"ࠬࡳ࡯ࡻ࠼ࡧࡩࡧࡻࡧࡨࡧࡵࡅࡩࡪࡲࡦࡵࡶࠫଊ")]
def bstack1l11l111ll_opy_(proxy_config):
  if bstack11llll_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪଋ") in proxy_config:
    proxy_config[bstack11llll_opy_ (u"ࠧࡴࡵ࡯ࡔࡷࡵࡸࡺࠩଌ")] = proxy_config[bstack11llll_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬ଍")]
    del (proxy_config[bstack11llll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭଎")])
  if bstack11llll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡖࡼࡴࡪ࠭ଏ") in proxy_config and proxy_config[bstack11llll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡗࡽࡵ࡫ࠧଐ")].lower() != bstack11llll_opy_ (u"ࠬࡪࡩࡳࡧࡦࡸࠬ଑"):
    proxy_config[bstack11llll_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡙ࡿࡰࡦࠩ଒")] = bstack11llll_opy_ (u"ࠧ࡮ࡣࡱࡹࡦࡲࠧଓ")
  if bstack11llll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡁࡶࡶࡲࡧࡴࡴࡦࡪࡩࡘࡶࡱ࠭ଔ") in proxy_config:
    proxy_config[bstack11llll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬକ")] = bstack11llll_opy_ (u"ࠪࡴࡦࡩࠧଖ")
  return proxy_config
def bstack11l1111ll_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack11llll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪଗ") in config:
    return proxy
  config[bstack11llll_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫଘ")] = bstack1l11l111ll_opy_(config[bstack11llll_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬଙ")])
  if proxy == None:
    proxy = Proxy(config[bstack11llll_opy_ (u"ࠧࡱࡴࡲࡼࡾ࠭ଚ")])
  return proxy
def bstack1l11lllll_opy_(self):
  global CONFIG
  global bstack11l1ll111_opy_
  try:
    proxy = bstack11l1lll1l_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack11llll_opy_ (u"ࠨ࠰ࡳࡥࡨ࠭ଛ")):
        proxies = bstack11l1ll1l11_opy_(proxy, bstack1lll1l1l1l_opy_())
        if len(proxies) > 0:
          protocol, bstack111ll1l1l_opy_ = proxies.popitem()
          if bstack11llll_opy_ (u"ࠤ࠽࠳࠴ࠨଜ") in bstack111ll1l1l_opy_:
            return bstack111ll1l1l_opy_
          else:
            return bstack11llll_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦଝ") + bstack111ll1l1l_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack11llll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡱࡴࡲࡼࡾࠦࡵࡳ࡮ࠣ࠾ࠥࢁࡽࠣଞ").format(str(e)))
  return bstack11l1ll111_opy_(self)
def bstack1l1l1ll11l_opy_():
  global CONFIG
  return bstack11lll1l1ll_opy_(CONFIG) and bstack1l1ll11ll_opy_() and bstack111l1111l_opy_() >= version.parse(bstack1ll11llll1_opy_)
def bstack11l1lllll_opy_():
  global CONFIG
  return (bstack11llll_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨଟ") in CONFIG or bstack11llll_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪଠ") in CONFIG) and bstack1l111llll1_opy_()
def bstack1l111l1lll_opy_(config):
  bstack1ll1l11l1_opy_ = {}
  if bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫଡ") in config:
    bstack1ll1l11l1_opy_ = config[bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬଢ")]
  if bstack11llll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨଣ") in config:
    bstack1ll1l11l1_opy_ = config[bstack11llll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩତ")]
  proxy = bstack11l1lll1l_opy_(config)
  if proxy:
    if proxy.endswith(bstack11llll_opy_ (u"ࠫ࠳ࡶࡡࡤࠩଥ")) and os.path.isfile(proxy):
      bstack1ll1l11l1_opy_[bstack11llll_opy_ (u"ࠬ࠳ࡰࡢࡥ࠰ࡪ࡮ࡲࡥࠨଦ")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack11llll_opy_ (u"࠭࠮ࡱࡣࡦࠫଧ")):
        proxies = bstack1ll111111_opy_(config, bstack1lll1l1l1l_opy_())
        if len(proxies) > 0:
          protocol, bstack111ll1l1l_opy_ = proxies.popitem()
          if bstack11llll_opy_ (u"ࠢ࠻࠱࠲ࠦନ") in bstack111ll1l1l_opy_:
            parsed_url = urlparse(bstack111ll1l1l_opy_)
          else:
            parsed_url = urlparse(protocol + bstack11llll_opy_ (u"ࠣ࠼࠲࠳ࠧ଩") + bstack111ll1l1l_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack1ll1l11l1_opy_[bstack11llll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡉࡱࡶࡸࠬପ")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack1ll1l11l1_opy_[bstack11llll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡲࡶࡹ࠭ଫ")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack1ll1l11l1_opy_[bstack11llll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡘࡷࡪࡸࠧବ")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack1ll1l11l1_opy_[bstack11llll_opy_ (u"ࠬࡶࡲࡰࡺࡼࡔࡦࡹࡳࠨଭ")] = str(parsed_url.password)
  return bstack1ll1l11l1_opy_
def bstack1l11l11lll_opy_(config):
  if bstack11llll_opy_ (u"࠭ࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠫମ") in config:
    return config[bstack11llll_opy_ (u"ࠧࡵࡧࡶࡸࡈࡵ࡮ࡵࡧࡻࡸࡔࡶࡴࡪࡱࡱࡷࠬଯ")]
  return {}
def bstack111ll1lll_opy_(caps):
  global bstack11ll1111l1_opy_
  if bstack11llll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩର") in caps:
    caps[bstack11llll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ଱")][bstack11llll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࠩଲ")] = True
    if bstack11ll1111l1_opy_:
      caps[bstack11llll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬଳ")][bstack11llll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ଴")] = bstack11ll1111l1_opy_
  else:
    caps[bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࠫଵ")] = True
    if bstack11ll1111l1_opy_:
      caps[bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨଶ")] = bstack11ll1111l1_opy_
def bstack1l111111l1_opy_():
  global CONFIG
  if not bstack11ll11111_opy_(CONFIG) or cli.is_enabled(CONFIG):
    return
  if bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬଷ") in CONFIG and bstack1lll1lll11_opy_(CONFIG[bstack11llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ସ")]):
    if (
      bstack11llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧହ") in CONFIG
      and bstack1lll1lll11_opy_(CONFIG[bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ଺")].get(bstack11llll_opy_ (u"ࠬࡹ࡫ࡪࡲࡅ࡭ࡳࡧࡲࡺࡋࡱ࡭ࡹ࡯ࡡ࡭࡫ࡶࡥࡹ࡯࡯࡯ࠩ଻")))
    ):
      logger.debug(bstack11llll_opy_ (u"ࠨࡌࡰࡥࡤࡰࠥࡨࡩ࡯ࡣࡵࡽࠥࡴ࡯ࡵࠢࡶࡸࡦࡸࡴࡦࡦࠣࡥࡸࠦࡳ࡬࡫ࡳࡆ࡮ࡴࡡࡳࡻࡌࡲ࡮ࡺࡩࡢ࡮࡬ࡷࡦࡺࡩࡰࡰࠣ࡭ࡸࠦࡥ࡯ࡣࡥࡰࡪࡪ଼ࠢ"))
      return
    bstack1ll1l11l1_opy_ = bstack1l111l1lll_opy_(CONFIG)
    bstack1llll111l1_opy_(CONFIG[bstack11llll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪଽ")], bstack1ll1l11l1_opy_)
def bstack1llll111l1_opy_(key, bstack1ll1l11l1_opy_):
  global bstack11ll111l1_opy_
  logger.info(bstack1l1ll11ll1_opy_)
  try:
    bstack11ll111l1_opy_ = Local()
    bstack1ll11ll111_opy_ = {bstack11llll_opy_ (u"ࠨ࡭ࡨࡽࠬା"): key}
    bstack1ll11ll111_opy_.update(bstack1ll1l11l1_opy_)
    logger.debug(bstack11ll1l1111_opy_.format(str(bstack1ll11ll111_opy_)))
    bstack11ll111l1_opy_.start(**bstack1ll11ll111_opy_)
    if bstack11ll111l1_opy_.isRunning():
      logger.info(bstack1l1ll111ll_opy_)
  except Exception as e:
    bstack1ll1l1lll_opy_(bstack111lll11l_opy_.format(str(e)))
def bstack1l1l11ll1l_opy_():
  global bstack11ll111l1_opy_
  if bstack11ll111l1_opy_.isRunning():
    logger.info(bstack11l11ll11_opy_)
    bstack11ll111l1_opy_.stop()
  bstack11ll111l1_opy_ = None
def bstack1lllllll11_opy_(bstack1ll11l1ll1_opy_=[]):
  global CONFIG
  bstack1llll11l1l_opy_ = []
  bstack1ll11l1ll_opy_ = [bstack11llll_opy_ (u"ࠩࡲࡷࠬି"), bstack11llll_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ୀ"), bstack11llll_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨୁ"), bstack11llll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧୂ"), bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫୃ"), bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨୄ")]
  try:
    for err in bstack1ll11l1ll1_opy_:
      bstack1lll1l1lll_opy_ = {}
      for k in bstack1ll11l1ll_opy_:
        val = CONFIG[bstack11llll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ୅")][int(err[bstack11llll_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨ୆")])].get(k)
        if val:
          bstack1lll1l1lll_opy_[k] = val
      if(err[bstack11llll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩେ")] != bstack11llll_opy_ (u"ࠫࠬୈ")):
        bstack1lll1l1lll_opy_[bstack11llll_opy_ (u"ࠬࡺࡥࡴࡶࡶࠫ୉")] = {
          err[bstack11llll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ୊")]: err[bstack11llll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ୋ")]
        }
        bstack1llll11l1l_opy_.append(bstack1lll1l1lll_opy_)
  except Exception as e:
    logger.debug(bstack11llll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪࡴࡸ࡭ࡢࡶࡷ࡭ࡳ࡭ࠠࡥࡣࡷࡥࠥ࡬࡯ࡳࠢࡨࡺࡪࡴࡴ࠻ࠢࠪୌ") + str(e))
  finally:
    return bstack1llll11l1l_opy_
def bstack11lll111ll_opy_(file_name):
  bstack1ll1l11l1l_opy_ = []
  try:
    bstack11l11111ll_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack11l11111ll_opy_):
      with open(bstack11l11111ll_opy_) as f:
        bstack1l111ll1l_opy_ = json.load(f)
        bstack1ll1l11l1l_opy_ = bstack1l111ll1l_opy_
      os.remove(bstack11l11111ll_opy_)
    return bstack1ll1l11l1l_opy_
  except Exception as e:
    logger.debug(bstack11llll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤ࡫࡯࡮ࡥ࡫ࡱ࡫ࠥ࡫ࡲࡳࡱࡵࠤࡱ࡯ࡳࡵ࠼୍ࠣࠫ") + str(e))
    return bstack1ll1l11l1l_opy_
def bstack11l11l1l1l_opy_():
  global bstack111lllllll_opy_
  global bstack1ll1111111_opy_
  global bstack1llll1ll1l_opy_
  global bstack1ll1ll111_opy_
  global bstack1l1l1lllll_opy_
  global bstack11ll111ll1_opy_
  global CONFIG
  bstack1lll1l11l1_opy_ = os.environ.get(bstack11llll_opy_ (u"ࠪࡊࡗࡇࡍࡆ࡙ࡒࡖࡐࡥࡕࡔࡇࡇࠫ୎"))
  if bstack1lll1l11l1_opy_ in [bstack11llll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ୏"), bstack11llll_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ୐")]:
    bstack11l1llllll_opy_()
  percy.shutdown()
  if bstack111lllllll_opy_:
    logger.warning(bstack1l1l1llll1_opy_.format(str(bstack111lllllll_opy_)))
  else:
    try:
      bstack1l1lll1111_opy_ = bstack1ll111111l_opy_(bstack11llll_opy_ (u"࠭࠮ࡣࡵࡷࡥࡨࡱ࠭ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬ୑"), logger)
      if bstack1l1lll1111_opy_.get(bstack11llll_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬ୒")) and bstack1l1lll1111_opy_.get(bstack11llll_opy_ (u"ࠨࡰࡸࡨ࡬࡫࡟࡭ࡱࡦࡥࡱ࠭୓")).get(bstack11llll_opy_ (u"ࠩ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠫ୔")):
        logger.warning(bstack1l1l1llll1_opy_.format(str(bstack1l1lll1111_opy_[bstack11llll_opy_ (u"ࠪࡲࡺࡪࡧࡦࡡ࡯ࡳࡨࡧ࡬ࠨ୕")][bstack11llll_opy_ (u"ࠫ࡭ࡵࡳࡵࡰࡤࡱࡪ࠭ୖ")])))
    except Exception as e:
      logger.error(e)
  bstack1lll1ll11l_opy_.invoke(Events.bstack1ll1ll1l1l_opy_)
  logger.info(bstack1l11111l1l_opy_)
  global bstack11ll111l1_opy_
  if bstack11ll111l1_opy_:
    bstack1l1l11ll1l_opy_()
  try:
    for driver in bstack1ll1111111_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack1l1ll111l_opy_)
  if bstack11ll111ll1_opy_ == bstack11llll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫୗ"):
    bstack1l1l1lllll_opy_ = bstack11lll111ll_opy_(bstack11llll_opy_ (u"࠭ࡲࡰࡤࡲࡸࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧ୘"))
  if bstack11ll111ll1_opy_ == bstack11llll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ୙") and len(bstack1ll1ll111_opy_) == 0:
    bstack1ll1ll111_opy_ = bstack11lll111ll_opy_(bstack11llll_opy_ (u"ࠨࡲࡺࡣࡵࡿࡴࡦࡵࡷࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭୚"))
    if len(bstack1ll1ll111_opy_) == 0:
      bstack1ll1ll111_opy_ = bstack11lll111ll_opy_(bstack11llll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡳࡴࡵࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨ୛"))
  bstack1l11l1111l_opy_ = bstack11llll_opy_ (u"ࠪࠫଡ଼")
  if len(bstack1llll1ll1l_opy_) > 0:
    bstack1l11l1111l_opy_ = bstack1lllllll11_opy_(bstack1llll1ll1l_opy_)
  elif len(bstack1ll1ll111_opy_) > 0:
    bstack1l11l1111l_opy_ = bstack1lllllll11_opy_(bstack1ll1ll111_opy_)
  elif len(bstack1l1l1lllll_opy_) > 0:
    bstack1l11l1111l_opy_ = bstack1lllllll11_opy_(bstack1l1l1lllll_opy_)
  elif len(bstack1111lllll_opy_) > 0:
    bstack1l11l1111l_opy_ = bstack1lllllll11_opy_(bstack1111lllll_opy_)
  if bool(bstack1l11l1111l_opy_):
    bstack11ll1l1ll1_opy_(bstack1l11l1111l_opy_)
  else:
    bstack11ll1l1ll1_opy_()
  bstack1llll1l1l1_opy_(bstack1111111ll_opy_, logger)
  bstack1ll1l1l1l1_opy_.bstack1ll1ll11_opy_(CONFIG)
  if len(bstack1l1l1lllll_opy_) > 0:
    sys.exit(len(bstack1l1l1lllll_opy_))
def bstack1l111lll1l_opy_(bstack11lllllll1_opy_, frame):
  global bstack1111l1l1_opy_
  logger.error(bstack1l11111111_opy_)
  bstack1111l1l1_opy_.set_property(bstack11llll_opy_ (u"ࠫࡸࡪ࡫ࡌ࡫࡯ࡰࡓࡵࠧଢ଼"), bstack11lllllll1_opy_)
  if hasattr(signal, bstack11llll_opy_ (u"࡙ࠬࡩࡨࡰࡤࡰࡸ࠭୞")):
    bstack1111l1l1_opy_.set_property(bstack11llll_opy_ (u"࠭ࡳࡥ࡭ࡎ࡭ࡱࡲࡓࡪࡩࡱࡥࡱ࠭ୟ"), signal.Signals(bstack11lllllll1_opy_).name)
  else:
    bstack1111l1l1_opy_.set_property(bstack11llll_opy_ (u"ࠧࡴࡦ࡮ࡏ࡮ࡲ࡬ࡔ࡫ࡪࡲࡦࡲࠧୠ"), bstack11llll_opy_ (u"ࠨࡕࡌࡋ࡚ࡔࡋࡏࡑ࡚ࡒࠬୡ"))
  if cli.is_running():
    bstack1lll1ll11l_opy_.invoke(Events.bstack1ll1ll1l1l_opy_)
  bstack1lll1l11l1_opy_ = os.environ.get(bstack11llll_opy_ (u"ࠩࡉࡖࡆࡓࡅࡘࡑࡕࡏࡤ࡛ࡓࡆࡆࠪୢ"))
  if bstack1lll1l11l1_opy_ == bstack11llll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪୣ"):
    bstack1lll11ll_opy_.stop(bstack1111l1l1_opy_.get_property(bstack11llll_opy_ (u"ࠫࡸࡪ࡫ࡌ࡫࡯ࡰࡘ࡯ࡧ࡯ࡣ࡯ࠫ୤")))
  bstack11l11l1l1l_opy_()
  sys.exit(1)
def bstack1ll1l1lll_opy_(err):
  logger.critical(bstack11l1l1l111_opy_.format(str(err)))
  bstack11ll1l1ll1_opy_(bstack11l1l1l111_opy_.format(str(err)), True)
  atexit.unregister(bstack11l11l1l1l_opy_)
  bstack11l1llllll_opy_()
  sys.exit(1)
def bstack1ll1l1llll_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack11ll1l1ll1_opy_(message, True)
  atexit.unregister(bstack11l11l1l1l_opy_)
  bstack11l1llllll_opy_()
  sys.exit(1)
def bstack1ll1ll1lll_opy_():
  global CONFIG
  global bstack1ll111l111_opy_
  global bstack1l11lll11l_opy_
  global bstack1l1l1l111_opy_
  CONFIG = bstack1ll1111ll1_opy_()
  load_dotenv(CONFIG.get(bstack11llll_opy_ (u"ࠬ࡫࡮ࡷࡈ࡬ࡰࡪ࠭୥")))
  bstack1ll111l11l_opy_()
  bstack11l11l1lll_opy_()
  CONFIG = bstack11111llll_opy_(CONFIG)
  update(CONFIG, bstack1l11lll11l_opy_)
  update(CONFIG, bstack1ll111l111_opy_)
  if not cli.is_enabled(CONFIG):
    CONFIG = bstack1llllll1l1_opy_(CONFIG)
  bstack1l1l1l111_opy_ = bstack11ll11111_opy_(CONFIG)
  os.environ[bstack11llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩ୦")] = bstack1l1l1l111_opy_.__str__()
  bstack1111l1l1_opy_.set_property(bstack11llll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨ୧"), bstack1l1l1l111_opy_)
  if (bstack11llll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ୨") in CONFIG and bstack11llll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ୩") in bstack1ll111l111_opy_) or (
          bstack11llll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭୪") in CONFIG and bstack11llll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ୫") not in bstack1l11lll11l_opy_):
    if os.getenv(bstack11llll_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡤࡉࡏࡎࡄࡌࡒࡊࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠩ୬")):
      CONFIG[bstack11llll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ୭")] = os.getenv(bstack11llll_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡄࡑࡐࡆࡎࡔࡅࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫ୮"))
    else:
      if not CONFIG.get(bstack11llll_opy_ (u"ࠣࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠦ୯"), bstack11llll_opy_ (u"ࠤࠥ୰")) in bstack11l1111ll1_opy_:
        bstack1ll1111ll_opy_()
  elif (bstack11llll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ୱ") not in CONFIG and bstack11llll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭୲") in CONFIG) or (
          bstack11llll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ୳") in bstack1l11lll11l_opy_ and bstack11llll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ୴") not in bstack1ll111l111_opy_):
    del (CONFIG[bstack11llll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ୵")])
  if bstack1lll1llll1_opy_(CONFIG):
    bstack1ll1l1lll_opy_(bstack1l11llll1_opy_)
  bstack1lll1l1l11_opy_()
  bstack11ll11ll1_opy_()
  if bstack11l111lll_opy_ and not CONFIG.get(bstack11llll_opy_ (u"ࠣࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠦ୶"), bstack11llll_opy_ (u"ࠤࠥ୷")) in bstack11l1111ll1_opy_:
    CONFIG[bstack11llll_opy_ (u"ࠪࡥࡵࡶࠧ୸")] = bstack1111ll1ll_opy_(CONFIG)
    logger.info(bstack1ll111ll1_opy_.format(CONFIG[bstack11llll_opy_ (u"ࠫࡦࡶࡰࠨ୹")]))
  if not bstack1l1l1l111_opy_:
    CONFIG[bstack11llll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ୺")] = [{}]
def bstack1lll11l11l_opy_(config, bstack11lllllll_opy_):
  global CONFIG
  global bstack11l111lll_opy_
  CONFIG = config
  bstack11l111lll_opy_ = bstack11lllllll_opy_
def bstack11ll11ll1_opy_():
  global CONFIG
  global bstack11l111lll_opy_
  if bstack11llll_opy_ (u"࠭ࡡࡱࡲࠪ୻") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1ll1l1llll_opy_(e, bstack1l11111l11_opy_)
    bstack11l111lll_opy_ = True
    bstack1111l1l1_opy_.set_property(bstack11llll_opy_ (u"ࠧࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭୼"), True)
def bstack1111ll1ll_opy_(config):
  bstack11ll1l1l1_opy_ = bstack11llll_opy_ (u"ࠨࠩ୽")
  app = config[bstack11llll_opy_ (u"ࠩࡤࡴࡵ࠭୾")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack11l1ll111l_opy_:
      if os.path.exists(app):
        bstack11ll1l1l1_opy_ = bstack1l1l11l11_opy_(config, app)
      elif bstack11l1ll11ll_opy_(app):
        bstack11ll1l1l1_opy_ = app
      else:
        bstack1ll1l1lll_opy_(bstack1lllllll1l_opy_.format(app))
    else:
      if bstack11l1ll11ll_opy_(app):
        bstack11ll1l1l1_opy_ = app
      elif os.path.exists(app):
        bstack11ll1l1l1_opy_ = bstack1l1l11l11_opy_(app)
      else:
        bstack1ll1l1lll_opy_(bstack1111l1111_opy_)
  else:
    if len(app) > 2:
      bstack1ll1l1lll_opy_(bstack1lll11llll_opy_)
    elif len(app) == 2:
      if bstack11llll_opy_ (u"ࠪࡴࡦࡺࡨࠨ୿") in app and bstack11llll_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡣ࡮ࡪࠧ஀") in app:
        if os.path.exists(app[bstack11llll_opy_ (u"ࠬࡶࡡࡵࡪࠪ஁")]):
          bstack11ll1l1l1_opy_ = bstack1l1l11l11_opy_(config, app[bstack11llll_opy_ (u"࠭ࡰࡢࡶ࡫ࠫஂ")], app[bstack11llll_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࡟ࡪࡦࠪஃ")])
        else:
          bstack1ll1l1lll_opy_(bstack1lllllll1l_opy_.format(app))
      else:
        bstack1ll1l1lll_opy_(bstack1lll11llll_opy_)
    else:
      for key in app:
        if key in bstack1llllll1ll_opy_:
          if key == bstack11llll_opy_ (u"ࠨࡲࡤࡸ࡭࠭஄"):
            if os.path.exists(app[key]):
              bstack11ll1l1l1_opy_ = bstack1l1l11l11_opy_(config, app[key])
            else:
              bstack1ll1l1lll_opy_(bstack1lllllll1l_opy_.format(app))
          else:
            bstack11ll1l1l1_opy_ = app[key]
        else:
          bstack1ll1l1lll_opy_(bstack1l1ll11l1_opy_)
  return bstack11ll1l1l1_opy_
def bstack11l1ll11ll_opy_(bstack11ll1l1l1_opy_):
  import re
  bstack11l11llll1_opy_ = re.compile(bstack11llll_opy_ (u"ࡴࠥࡢࡠࡧ࠭ࡻࡃ࠰࡞࠵࠳࠹࡝ࡡ࠱ࡠ࠲ࡣࠪࠥࠤஅ"))
  bstack1l11ll1l11_opy_ = re.compile(bstack11llll_opy_ (u"ࡵࠦࡣࡡࡡ࠮ࡼࡄ࠱࡟࠶࠭࠺࡞ࡢ࠲ࡡ࠳࡝ࠫ࠱࡞ࡥ࠲ࢀࡁ࠮࡜࠳࠱࠾ࡢ࡟࠯࡞࠰ࡡ࠯ࠪࠢஆ"))
  if bstack11llll_opy_ (u"ࠫࡧࡹ࠺࠰࠱ࠪஇ") in bstack11ll1l1l1_opy_ or re.fullmatch(bstack11l11llll1_opy_, bstack11ll1l1l1_opy_) or re.fullmatch(bstack1l11ll1l11_opy_, bstack11ll1l1l1_opy_):
    return True
  else:
    return False
def bstack1l1l11l11_opy_(config, path, bstack11l1l111ll_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack11llll_opy_ (u"ࠬࡸࡢࠨஈ")).read()).hexdigest()
  bstack1l1l11l1ll_opy_ = bstack1ll11l1l1_opy_(md5_hash)
  bstack11ll1l1l1_opy_ = None
  if bstack1l1l11l1ll_opy_:
    logger.info(bstack1ll11ll1l_opy_.format(bstack1l1l11l1ll_opy_, md5_hash))
    return bstack1l1l11l1ll_opy_
  bstack111l1l1l1_opy_ = datetime.datetime.now()
  multipart_data = MultipartEncoder(
    fields={
      bstack11llll_opy_ (u"࠭ࡦࡪ࡮ࡨࠫஉ"): (os.path.basename(path), open(os.path.abspath(path), bstack11llll_opy_ (u"ࠧࡳࡤࠪஊ")), bstack11llll_opy_ (u"ࠨࡶࡨࡼࡹ࠵ࡰ࡭ࡣ࡬ࡲࠬ஋")),
      bstack11llll_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬ஌"): bstack11l1l111ll_opy_
    }
  )
  response = requests.post(bstack1l11l11l1_opy_, data=multipart_data,
                           headers={bstack11llll_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩ஍"): multipart_data.content_type},
                           auth=(config[bstack11llll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭எ")], config[bstack11llll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨஏ")]))
  try:
    res = json.loads(response.text)
    bstack11ll1l1l1_opy_ = res[bstack11llll_opy_ (u"࠭ࡡࡱࡲࡢࡹࡷࡲࠧஐ")]
    logger.info(bstack1ll1l1l111_opy_.format(bstack11ll1l1l1_opy_))
    bstack11lll1lll1_opy_(md5_hash, bstack11ll1l1l1_opy_)
    cli.bstack1ll1l1l11l_opy_(bstack11llll_opy_ (u"ࠢࡩࡶࡷࡴ࠿ࡻࡰ࡭ࡱࡤࡨࡤࡧࡰࡱࠤ஑"), datetime.datetime.now() - bstack111l1l1l1_opy_)
  except ValueError as err:
    bstack1ll1l1lll_opy_(bstack1l1lllllll_opy_.format(str(err)))
  return bstack11ll1l1l1_opy_
def bstack1lll1l1l11_opy_(framework_name=None, args=None):
  global CONFIG
  global bstack11lll11ll1_opy_
  bstack1llllllll_opy_ = 1
  bstack11l111ll1_opy_ = 1
  if bstack11llll_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨஒ") in CONFIG:
    bstack11l111ll1_opy_ = CONFIG[bstack11llll_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩஓ")]
  else:
    bstack11l111ll1_opy_ = bstack1ll11l11l1_opy_(framework_name, args) or 1
  if bstack11llll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ஔ") in CONFIG:
    bstack1llllllll_opy_ = len(CONFIG[bstack11llll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧக")])
  bstack11lll11ll1_opy_ = int(bstack11l111ll1_opy_) * int(bstack1llllllll_opy_)
def bstack1ll11l11l1_opy_(framework_name, args):
  if framework_name == bstack1lllll1111_opy_ and args and bstack11llll_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪ஖") in args:
      bstack1lllll1ll1_opy_ = args.index(bstack11llll_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫ஗"))
      return int(args[bstack1lllll1ll1_opy_ + 1]) or 1
  return 1
def bstack1ll11l1l1_opy_(md5_hash):
  bstack11lllll1l_opy_ = os.path.join(os.path.expanduser(bstack11llll_opy_ (u"ࠧࡿࠩ஘")), bstack11llll_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨங"), bstack11llll_opy_ (u"ࠩࡤࡴࡵ࡛ࡰ࡭ࡱࡤࡨࡒࡊ࠵ࡉࡣࡶ࡬࠳ࡰࡳࡰࡰࠪச"))
  if os.path.exists(bstack11lllll1l_opy_):
    bstack1lll11l111_opy_ = json.load(open(bstack11lllll1l_opy_, bstack11llll_opy_ (u"ࠪࡶࡧ࠭஛")))
    if md5_hash in bstack1lll11l111_opy_:
      bstack1l1l111111_opy_ = bstack1lll11l111_opy_[md5_hash]
      bstack111111l11_opy_ = datetime.datetime.now()
      bstack1l11l11ll1_opy_ = datetime.datetime.strptime(bstack1l1l111111_opy_[bstack11llll_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧஜ")], bstack11llll_opy_ (u"ࠬࠫࡤ࠰ࠧࡰ࠳ࠪ࡟ࠠࠦࡊ࠽ࠩࡒࡀࠥࡔࠩ஝"))
      if (bstack111111l11_opy_ - bstack1l11l11ll1_opy_).days > 30:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack1l1l111111_opy_[bstack11llll_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫஞ")]):
        return None
      return bstack1l1l111111_opy_[bstack11llll_opy_ (u"ࠧࡪࡦࠪட")]
  else:
    return None
def bstack11lll1lll1_opy_(md5_hash, bstack11ll1l1l1_opy_):
  bstack11ll1ll11l_opy_ = os.path.join(os.path.expanduser(bstack11llll_opy_ (u"ࠨࢀࠪ஠")), bstack11llll_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ஡"))
  if not os.path.exists(bstack11ll1ll11l_opy_):
    os.makedirs(bstack11ll1ll11l_opy_)
  bstack11lllll1l_opy_ = os.path.join(os.path.expanduser(bstack11llll_opy_ (u"ࠪࢂࠬ஢")), bstack11llll_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫண"), bstack11llll_opy_ (u"ࠬࡧࡰࡱࡗࡳࡰࡴࡧࡤࡎࡆ࠸ࡌࡦࡹࡨ࠯࡬ࡶࡳࡳ࠭த"))
  bstack1l1l1lll11_opy_ = {
    bstack11llll_opy_ (u"࠭ࡩࡥࠩ஥"): bstack11ll1l1l1_opy_,
    bstack11llll_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ஦"): datetime.datetime.strftime(datetime.datetime.now(), bstack11llll_opy_ (u"ࠨࠧࡧ࠳ࠪࡳ࠯࡛ࠦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗࠬ஧")),
    bstack11llll_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧந"): str(__version__)
  }
  if os.path.exists(bstack11lllll1l_opy_):
    bstack1lll11l111_opy_ = json.load(open(bstack11lllll1l_opy_, bstack11llll_opy_ (u"ࠪࡶࡧ࠭ன")))
  else:
    bstack1lll11l111_opy_ = {}
  bstack1lll11l111_opy_[md5_hash] = bstack1l1l1lll11_opy_
  with open(bstack11lllll1l_opy_, bstack11llll_opy_ (u"ࠦࡼ࠱ࠢப")) as outfile:
    json.dump(bstack1lll11l111_opy_, outfile)
def bstack1ll1lllll1_opy_(self):
  return
def bstack11llllllll_opy_(self):
  return
def bstack11l1ll11l1_opy_(self):
  global bstack1ll1111l1l_opy_
  bstack1ll1111l1l_opy_(self)
def bstack11l1ll1111_opy_():
  global bstack1l1l1l11ll_opy_
  bstack1l1l1l11ll_opy_ = True
def bstack11lllll11l_opy_(self):
  global bstack1l1l11llll_opy_
  global bstack1l1l11111_opy_
  global bstack1lll11ll11_opy_
  try:
    if bstack11llll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ஫") in bstack1l1l11llll_opy_ and self.session_id != None and bstack1ll111l1_opy_(threading.current_thread(), bstack11llll_opy_ (u"࠭ࡴࡦࡵࡷࡗࡹࡧࡴࡶࡵࠪ஬"), bstack11llll_opy_ (u"ࠧࠨ஭")) != bstack11llll_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩம"):
      bstack1l1ll1l1l_opy_ = bstack11llll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩய") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack11llll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪர")
      if bstack1l1ll1l1l_opy_ == bstack11llll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫற"):
        bstack1ll1l111l1_opy_(logger)
      if self != None:
        bstack11l11l11ll_opy_(self, bstack1l1ll1l1l_opy_, bstack11llll_opy_ (u"ࠬ࠲ࠠࠨல").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack11llll_opy_ (u"࠭ࠧள")
    if bstack11llll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧழ") in bstack1l1l11llll_opy_ and getattr(threading.current_thread(), bstack11llll_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧவ"), None):
      bstack11l11l11_opy_.bstack111l1ll1_opy_(self, bstack1l1lll1ll1_opy_, logger, wait=True)
    if bstack11llll_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩஶ") in bstack1l1l11llll_opy_:
      if not threading.currentThread().behave_test_status:
        bstack11l11l11ll_opy_(self, bstack11llll_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥஷ"))
      bstack11llll1l11_opy_.bstack1l1ll1l1ll_opy_(self)
  except Exception as e:
    logger.debug(bstack11llll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡰࡥࡷࡱࡩ࡯ࡩࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࠧஸ") + str(e))
  bstack1lll11ll11_opy_(self)
  self.session_id = None
def bstack1l1ll11lll_opy_(self, *args, **kwargs):
  try:
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    from bstack_utils.helper import bstack1l111ll11_opy_
    global bstack1l1l11llll_opy_
    command_executor = kwargs.get(bstack11llll_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠨஹ"), bstack11llll_opy_ (u"࠭ࠧ஺"))
    bstack11l1111lll_opy_ = False
    if type(command_executor) == str and bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪ஻") in command_executor:
      bstack11l1111lll_opy_ = True
    elif isinstance(command_executor, RemoteConnection) and bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫ஼") in str(getattr(command_executor, bstack11llll_opy_ (u"ࠩࡢࡹࡷࡲࠧ஽"), bstack11llll_opy_ (u"ࠪࠫா"))):
      bstack11l1111lll_opy_ = True
    else:
      return bstack11l1l1lll1_opy_(self, *args, **kwargs)
    if bstack11l1111lll_opy_:
      if kwargs.get(bstack11llll_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬி")):
        kwargs[bstack11llll_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭ீ")] = bstack1l111ll11_opy_(kwargs[bstack11llll_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧு")], bstack1l1l11llll_opy_)
      elif kwargs.get(bstack11llll_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧூ")):
        kwargs[bstack11llll_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨ௃")] = bstack1l111ll11_opy_(kwargs[bstack11llll_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩ௄")], bstack1l1l11llll_opy_)
  except Exception as e:
    logger.error(bstack11llll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬ࡪࡴࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡘࡊࡋࠡࡥࡤࡴࡸࡀࠠࡼࡿࠥ௅").format(str(e)))
  return bstack11l1l1lll1_opy_(self, *args, **kwargs)
def bstack1l11l1l11_opy_(self, command_executor=bstack11llll_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳࠶࠸࠷࠯࠲࠱࠴࠳࠷࠺࠵࠶࠷࠸ࠧெ"), *args, **kwargs):
  bstack1l11l1l1l_opy_ = bstack1l1ll11lll_opy_(self, command_executor=command_executor, *args, **kwargs)
  if not bstack1lll1l11_opy_.on():
    return bstack1l11l1l1l_opy_
  try:
    logger.debug(bstack11llll_opy_ (u"ࠬࡉ࡯࡮࡯ࡤࡲࡩࠦࡅࡹࡧࡦࡹࡹࡵࡲࠡࡹ࡫ࡩࡳࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢ࡬ࡷࠥ࡬ࡡ࡭ࡵࡨࠤ࠲ࠦࡻࡾࠩே").format(str(command_executor)))
    logger.debug(bstack11llll_opy_ (u"࠭ࡈࡶࡤ࡙ࠣࡗࡒࠠࡪࡵࠣ࠱ࠥࢁࡽࠨை").format(str(command_executor._url)))
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪ௉") in command_executor._url:
      bstack1111l1l1_opy_.set_property(bstack11llll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩொ"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack11llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬோ") in command_executor):
    bstack1111l1l1_opy_.set_property(bstack11llll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫௌ"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack1lll11ll_opy_.bstack1ll1ll1l1_opy_(self)
  return bstack1l11l1l1l_opy_
def bstack1l11l11111_opy_(args):
  return bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ்ࠬ") in str(args)
def bstack1ll111l1l1_opy_(self, driver_command, *args, **kwargs):
  global bstack1llll1llll_opy_
  global bstack1l1lll1ll_opy_
  bstack1llll1l11l_opy_ = bstack1ll111l1_opy_(threading.current_thread(), bstack11llll_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩ௎"), None) and bstack1ll111l1_opy_(
          threading.current_thread(), bstack11llll_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ௏"), None)
  bstack1llllllll1_opy_ = getattr(self, bstack11llll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧௐ"), None) != None and getattr(self, bstack11llll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨ௑"), None) == True
  if not bstack1l1lll1ll_opy_ and bstack1l1l1l111_opy_ and bstack11llll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ௒") in CONFIG and CONFIG[bstack11llll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ௓")] == True and bstack11ll11l1l1_opy_.bstack1111l1ll1_opy_(driver_command) and (bstack1llllllll1_opy_ or bstack1llll1l11l_opy_) and not bstack1l11l11111_opy_(args):
    try:
      bstack1l1lll1ll_opy_ = True
      logger.debug(bstack11llll_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡦࡰࡴࠣࡿࢂ࠭௔").format(driver_command))
      logger.debug(perform_scan(self, driver_command=driver_command))
    except Exception as err:
      logger.debug(bstack11llll_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡨࡶ࡫ࡵࡲ࡮ࠢࡶࡧࡦࡴࠠࡼࡿࠪ௕").format(str(err)))
    bstack1l1lll1ll_opy_ = False
  response = bstack1llll1llll_opy_(self, driver_command, *args, **kwargs)
  if (bstack11llll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ௖") in str(bstack1l1l11llll_opy_).lower() or bstack11llll_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧௗ") in str(bstack1l1l11llll_opy_).lower()) and bstack1lll1l11_opy_.on():
    try:
      if driver_command == bstack11llll_opy_ (u"ࠨࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠬ௘"):
        bstack1lll11ll_opy_.bstack1ll1lll11_opy_({
            bstack11llll_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨ௙"): response[bstack11llll_opy_ (u"ࠪࡺࡦࡲࡵࡦࠩ௚")],
            bstack11llll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ௛"): bstack1lll11ll_opy_.current_test_uuid() if bstack1lll11ll_opy_.current_test_uuid() else bstack1lll1l11_opy_.current_hook_uuid()
        })
    except:
      pass
  return response
def bstack1l111ll1l1_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack1l1l11111_opy_
  global bstack11l111ll1l_opy_
  global bstack1ll11ll11l_opy_
  global bstack1l111l1l11_opy_
  global bstack1l1l11lll1_opy_
  global bstack1l1l11llll_opy_
  global bstack11l1l1lll1_opy_
  global bstack1ll1111111_opy_
  global bstack11ll1llll1_opy_
  global bstack1l1lll1ll1_opy_
  CONFIG[bstack11llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ௜")] = str(bstack1l1l11llll_opy_) + str(__version__)
  command_executor = bstack1lll1l1l1l_opy_()
  logger.debug(bstack1l111l1l1_opy_.format(command_executor))
  proxy = bstack11l1111ll_opy_(CONFIG, proxy)
  bstack1ll111l11_opy_ = 0 if bstack11l111ll1l_opy_ < 0 else bstack11l111ll1l_opy_
  try:
    if bstack1l111l1l11_opy_ is True:
      bstack1ll111l11_opy_ = int(multiprocessing.current_process().name)
    elif bstack1l1l11lll1_opy_ is True:
      bstack1ll111l11_opy_ = int(threading.current_thread().name)
  except:
    bstack1ll111l11_opy_ = 0
  bstack11lll11lll_opy_ = bstack11lll1ll1_opy_(CONFIG, bstack1ll111l11_opy_)
  logger.debug(bstack1l11lll11_opy_.format(str(bstack11lll11lll_opy_)))
  if bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ௝") in CONFIG and bstack1lll1lll11_opy_(CONFIG[bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ௞")]):
    bstack111ll1lll_opy_(bstack11lll11lll_opy_)
  if bstack11111l11_opy_.bstack1l1llll11_opy_(CONFIG, bstack1ll111l11_opy_) and bstack11111l11_opy_.bstack11ll11ll11_opy_(bstack11lll11lll_opy_, options, desired_capabilities):
    threading.current_thread().a11yPlatform = True
    if not cli.accessibility.is_enabled():
      bstack11111l11_opy_.set_capabilities(bstack11lll11lll_opy_, CONFIG)
  if desired_capabilities:
    bstack11l11l11l_opy_ = bstack11111llll_opy_(desired_capabilities)
    bstack11l11l11l_opy_[bstack11llll_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨ௟")] = bstack1ll11l1111_opy_(CONFIG)
    bstack111llllll_opy_ = bstack11lll1ll1_opy_(bstack11l11l11l_opy_)
    if bstack111llllll_opy_:
      bstack11lll11lll_opy_ = update(bstack111llllll_opy_, bstack11lll11lll_opy_)
    desired_capabilities = None
  if options:
    bstack1ll1l1l1ll_opy_(options, bstack11lll11lll_opy_)
  if not options:
    options = bstack1llll1ll1_opy_(bstack11lll11lll_opy_)
  bstack1l1lll1ll1_opy_ = CONFIG.get(bstack11llll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ௠"))[bstack1ll111l11_opy_]
  if proxy and bstack111l1111l_opy_() >= version.parse(bstack11llll_opy_ (u"ࠪ࠸࠳࠷࠰࠯࠲ࠪ௡")):
    options.proxy(proxy)
  if options and bstack111l1111l_opy_() >= version.parse(bstack11llll_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪ௢")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack111l1111l_opy_() < version.parse(bstack11llll_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫ௣")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack11lll11lll_opy_)
  logger.info(bstack11ll1l1l1l_opy_)
  if bstack111l1111l_opy_() >= version.parse(bstack11llll_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭௤")):
    bstack11l1l1lll1_opy_(self, command_executor=command_executor,
              options=options, keep_alive=keep_alive, file_detector=file_detector)
  elif bstack111l1111l_opy_() >= version.parse(bstack11llll_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭௥")):
    bstack11l1l1lll1_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities, options=options,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  elif bstack111l1111l_opy_() >= version.parse(bstack11llll_opy_ (u"ࠨ࠴࠱࠹࠸࠴࠰ࠨ௦")):
    bstack11l1l1lll1_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack11l1l1lll1_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive)
  try:
    bstack11ll11l1l_opy_ = bstack11llll_opy_ (u"ࠩࠪ௧")
    if bstack111l1111l_opy_() >= version.parse(bstack11llll_opy_ (u"ࠪ࠸࠳࠶࠮࠱ࡤ࠴ࠫ௨")):
      bstack11ll11l1l_opy_ = self.caps.get(bstack11llll_opy_ (u"ࠦࡴࡶࡴࡪ࡯ࡤࡰࡍࡻࡢࡖࡴ࡯ࠦ௩"))
    else:
      bstack11ll11l1l_opy_ = self.capabilities.get(bstack11llll_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧ௪"))
    if bstack11ll11l1l_opy_:
      bstack1l1l1l11l1_opy_(bstack11ll11l1l_opy_)
      if bstack111l1111l_opy_() <= version.parse(bstack11llll_opy_ (u"࠭࠳࠯࠳࠶࠲࠵࠭௫")):
        self.command_executor._url = bstack11llll_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣ௬") + bstack111l11l11_opy_ + bstack11llll_opy_ (u"ࠣ࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠧ௭")
      else:
        self.command_executor._url = bstack11llll_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦ௮") + bstack11ll11l1l_opy_ + bstack11llll_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦ௯")
      logger.debug(bstack1lllll111_opy_.format(bstack11ll11l1l_opy_))
    else:
      logger.debug(bstack1l1llll1ll_opy_.format(bstack11llll_opy_ (u"ࠦࡔࡶࡴࡪ࡯ࡤࡰࠥࡎࡵࡣࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨࠧ௰")))
  except Exception as e:
    logger.debug(bstack1l1llll1ll_opy_.format(e))
  if bstack11llll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ௱") in bstack1l1l11llll_opy_:
    bstack1ll1l1lll1_opy_(bstack11l111ll1l_opy_, bstack11ll1llll1_opy_)
  bstack1l1l11111_opy_ = self.session_id
  if bstack11llll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭௲") in bstack1l1l11llll_opy_ or bstack11llll_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ௳") in bstack1l1l11llll_opy_ or bstack11llll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ௴") in bstack1l1l11llll_opy_:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
    bstack1lll11ll_opy_.bstack1ll1ll1l1_opy_(self)
  bstack1ll1111111_opy_.append(self)
  if bstack11llll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ௵") in CONFIG and bstack11llll_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ௶") in CONFIG[bstack11llll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ௷")][bstack1ll111l11_opy_]:
    bstack1ll11ll11l_opy_ = CONFIG[bstack11llll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ௸")][bstack1ll111l11_opy_][bstack11llll_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ௹")]
  logger.debug(bstack111l1ll1l_opy_.format(bstack1l1l11111_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    from browserstack_sdk.__init__ import bstack1l1ll1l11_opy_
    def bstack11l11l1l11_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack11111l11l_opy_
      if(bstack11llll_opy_ (u"ࠢࡪࡰࡧࡩࡽ࠴ࡪࡴࠤ௺") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack11llll_opy_ (u"ࠨࢀࠪ௻")), bstack11llll_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ௼"), bstack11llll_opy_ (u"ࠪ࠲ࡸ࡫ࡳࡴ࡫ࡲࡲ࡮ࡪࡳ࠯ࡶࡻࡸࠬ௽")), bstack11llll_opy_ (u"ࠫࡼ࠭௾")) as fp:
          fp.write(bstack11llll_opy_ (u"ࠧࠨ௿"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack11llll_opy_ (u"ࠨࡩ࡯ࡦࡨࡼࡤࡨࡳࡵࡣࡦ࡯࠳ࡰࡳࠣఀ")))):
          with open(args[1], bstack11llll_opy_ (u"ࠧࡳࠩఁ")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack11llll_opy_ (u"ࠨࡣࡶࡽࡳࡩࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࡢࡲࡪࡽࡐࡢࡩࡨࠬࡨࡵ࡮ࡵࡧࡻࡸ࠱ࠦࡰࡢࡩࡨࠤࡂࠦࡶࡰ࡫ࡧࠤ࠵࠯ࠧం") in line), None)
            if index is not None:
                lines.insert(index+2, bstack1l1l11l1l_opy_)
            if bstack11llll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ః") in CONFIG and str(CONFIG[bstack11llll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧఄ")]).lower() != bstack11llll_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪఅ"):
                bstack1llll11ll_opy_ = bstack1l1ll1l11_opy_()
                bstack11lll11111_opy_ = bstack11llll_opy_ (u"ࠬ࠭ࠧࠋ࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࠎࡨࡵ࡮ࡴࡶࠣࡦࡸࡺࡡࡤ࡭ࡢࡴࡦࡺࡨࠡ࠿ࠣࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࡝ࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࠯࡮ࡨࡲ࡬ࡺࡨࠡ࠯ࠣ࠷ࡢࡁࠊࡤࡱࡱࡷࡹࠦࡢࡴࡶࡤࡧࡰࡥࡣࡢࡲࡶࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࡠࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠱࡞࠽ࠍࡧࡴࡴࡳࡵࠢࡳࡣ࡮ࡴࡤࡦࡺࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠸࡝࠼ࠌࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶࠡ࠿ࠣࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰ࡶࡰ࡮ࡩࡥࠩ࠲࠯ࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠹ࠩ࠼ࠌࡦࡳࡳࡹࡴࠡ࡫ࡰࡴࡴࡸࡴࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠹ࡥࡢࡴࡶࡤࡧࡰࠦ࠽ࠡࡴࡨࡵࡺ࡯ࡲࡦࠪࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢࠪ࠽ࠍ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡰࡦࡻ࡮ࡤࡪࠣࡁࠥࡧࡳࡺࡰࡦࠤ࠭ࡲࡡࡶࡰࡦ࡬ࡔࡶࡴࡪࡱࡱࡷ࠮ࠦ࠽࠿ࠢࡾࡿࠏࠦࠠ࡭ࡧࡷࠤࡨࡧࡰࡴ࠽ࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠋࠢࠣࡸࡷࡿࠠࡼࡽࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠌࠣࠤࠥࠦࡣࡢࡲࡶࠤࡂࠦࡊࡔࡑࡑ࠲ࡵࡧࡲࡴࡧࠫࡦࡸࡺࡡࡤ࡭ࡢࡧࡦࡶࡳࠪ࠽ࠍࠤࠥࢃࡽࠡࡥࡤࡸࡨ࡮ࠠࠩࡧࡻ࠭ࠥࢁࡻࠋࠢࠣࠤࠥࡩ࡯࡯ࡵࡲࡰࡪ࠴ࡥࡳࡴࡲࡶ࠭ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡥࡷࡹࡥࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹ࠺ࠣ࠮ࠣࡩࡽ࠯࠻ࠋࠢࠣࢁࢂࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠏࠦࠠࡳࡧࡷࡹࡷࡴࠠࡢࡹࡤ࡭ࡹࠦࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴ࡣࡰࡰࡱࡩࡨࡺࠨࡼࡽࠍࠤࠥࠦࠠࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷ࠾ࠥ࠭ࡻࡤࡦࡳ࡙ࡷࡲࡽࠨࠢ࠮ࠤࡪࡴࡣࡰࡦࡨ࡙ࡗࡏࡃࡰ࡯ࡳࡳࡳ࡫࡮ࡵࠪࡍࡗࡔࡔ࠮ࡴࡶࡵ࡭ࡳ࡭ࡩࡧࡻࠫࡧࡦࡶࡳࠪࠫ࠯ࠎࠥࠦࠠࠡ࠰࠱࠲ࡱࡧࡵ࡯ࡥ࡫ࡓࡵࡺࡩࡰࡰࡶࠎࠥࠦࡽࡾࠫ࠾ࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠋࡿࢀ࠿ࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠋ࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࠎࠬ࠭ࠧఆ").format(bstack1llll11ll_opy_=bstack1llll11ll_opy_)
            lines.insert(1, bstack11lll11111_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack11llll_opy_ (u"ࠨࡩ࡯ࡦࡨࡼࡤࡨࡳࡵࡣࡦ࡯࠳ࡰࡳࠣఇ")), bstack11llll_opy_ (u"ࠧࡸࠩఈ")) as bstack11111ll11_opy_:
              bstack11111ll11_opy_.writelines(lines)
        CONFIG[bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪఉ")] = str(bstack1l1l11llll_opy_) + str(__version__)
        bstack1ll111l11_opy_ = 0 if bstack11l111ll1l_opy_ < 0 else bstack11l111ll1l_opy_
        try:
          if bstack1l111l1l11_opy_ is True:
            bstack1ll111l11_opy_ = int(multiprocessing.current_process().name)
          elif bstack1l1l11lll1_opy_ is True:
            bstack1ll111l11_opy_ = int(threading.current_thread().name)
        except:
          bstack1ll111l11_opy_ = 0
        CONFIG[bstack11llll_opy_ (u"ࠤࡸࡷࡪ࡝࠳ࡄࠤఊ")] = False
        CONFIG[bstack11llll_opy_ (u"ࠥ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤఋ")] = True
        bstack11lll11lll_opy_ = bstack11lll1ll1_opy_(CONFIG, bstack1ll111l11_opy_)
        logger.debug(bstack1l11lll11_opy_.format(str(bstack11lll11lll_opy_)))
        if CONFIG.get(bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨఌ")):
          bstack111ll1lll_opy_(bstack11lll11lll_opy_)
        if bstack11llll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ఍") in CONFIG and bstack11llll_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫఎ") in CONFIG[bstack11llll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪఏ")][bstack1ll111l11_opy_]:
          bstack1ll11ll11l_opy_ = CONFIG[bstack11llll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫఐ")][bstack1ll111l11_opy_][bstack11llll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ఑")]
        args.append(os.path.join(os.path.expanduser(bstack11llll_opy_ (u"ࠪࢂࠬఒ")), bstack11llll_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫఓ"), bstack11llll_opy_ (u"ࠬ࠴ࡳࡦࡵࡶ࡭ࡴࡴࡩࡥࡵ࠱ࡸࡽࡺࠧఔ")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack11lll11lll_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack11llll_opy_ (u"ࠨࡩ࡯ࡦࡨࡼࡤࡨࡳࡵࡣࡦ࡯࠳ࡰࡳࠣక"))
      bstack11111l11l_opy_ = True
      return bstack11ll1llll_opy_(self, args, bufsize=bufsize, executable=executable,
                    stdin=stdin, stdout=stdout, stderr=stderr,
                    preexec_fn=preexec_fn, close_fds=close_fds,
                    shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines,
                    startupinfo=startupinfo, creationflags=creationflags,
                    restore_signals=restore_signals, start_new_session=start_new_session,
                    pass_fds=pass_fds, user=user, group=group, extra_groups=extra_groups,
                    encoding=encoding, errors=errors, text=text, umask=umask, pipesize=pipesize)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack1l111l1ll_opy_(self,
        executablePath = None,
        channel = None,
        args = None,
        ignoreDefaultArgs = None,
        handleSIGINT = None,
        handleSIGTERM = None,
        handleSIGHUP = None,
        timeout = None,
        env = None,
        headless = None,
        devtools = None,
        proxy = None,
        downloadsPath = None,
        slowMo = None,
        tracesDir = None,
        chromiumSandbox = None,
        firefoxUserPrefs = None
        ):
    global CONFIG
    global bstack11l111ll1l_opy_
    global bstack1ll11ll11l_opy_
    global bstack1l111l1l11_opy_
    global bstack1l1l11lll1_opy_
    global bstack1l1l11llll_opy_
    CONFIG[bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩఖ")] = str(bstack1l1l11llll_opy_) + str(__version__)
    bstack1ll111l11_opy_ = 0 if bstack11l111ll1l_opy_ < 0 else bstack11l111ll1l_opy_
    try:
      if bstack1l111l1l11_opy_ is True:
        bstack1ll111l11_opy_ = int(multiprocessing.current_process().name)
      elif bstack1l1l11lll1_opy_ is True:
        bstack1ll111l11_opy_ = int(threading.current_thread().name)
    except:
      bstack1ll111l11_opy_ = 0
    CONFIG[bstack11llll_opy_ (u"ࠣ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢగ")] = True
    bstack11lll11lll_opy_ = bstack11lll1ll1_opy_(CONFIG, bstack1ll111l11_opy_)
    logger.debug(bstack1l11lll11_opy_.format(str(bstack11lll11lll_opy_)))
    if CONFIG.get(bstack11llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ఘ")):
      bstack111ll1lll_opy_(bstack11lll11lll_opy_)
    if bstack11llll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ఙ") in CONFIG and bstack11llll_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩచ") in CONFIG[bstack11llll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨఛ")][bstack1ll111l11_opy_]:
      bstack1ll11ll11l_opy_ = CONFIG[bstack11llll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩజ")][bstack1ll111l11_opy_][bstack11llll_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬఝ")]
    import urllib
    import json
    if bstack11llll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬఞ") in CONFIG and str(CONFIG[bstack11llll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ట")]).lower() != bstack11llll_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩఠ"):
        bstack1l11l11ll_opy_ = bstack1l1ll1l11_opy_()
        bstack1llll11ll_opy_ = bstack1l11l11ll_opy_ + urllib.parse.quote(json.dumps(bstack11lll11lll_opy_))
    else:
        bstack1llll11ll_opy_ = bstack11llll_opy_ (u"ࠫࡼࡹࡳ࠻࠱࠲ࡧࡩࡶ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠿ࡤࡣࡳࡷࡂ࠭డ") + urllib.parse.quote(json.dumps(bstack11lll11lll_opy_))
    browser = self.connect(bstack1llll11ll_opy_)
    return browser
except Exception as e:
    pass
def bstack1ll1l11l11_opy_():
    global bstack11111l11l_opy_
    global bstack1l1l11llll_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1l11ll1ll_opy_
        if not bstack1l1l1l111_opy_:
          global bstack1lll11l1l1_opy_
          if not bstack1lll11l1l1_opy_:
            from bstack_utils.helper import bstack1l11l111l_opy_, bstack1l1l1111l1_opy_
            bstack1lll11l1l1_opy_ = bstack1l11l111l_opy_()
            bstack1l1l1111l1_opy_(bstack1l1l11llll_opy_)
          BrowserType.connect = bstack1l11ll1ll_opy_
          return
        BrowserType.launch = bstack1l111l1ll_opy_
        bstack11111l11l_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack11l11l1l11_opy_
      bstack11111l11l_opy_ = True
    except Exception as e:
      pass
def bstack1ll1lll1l1_opy_(context, bstack11l1l1ll11_opy_):
  try:
    context.page.evaluate(bstack11llll_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨఢ"), bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠪణ")+ json.dumps(bstack11l1l1ll11_opy_) + bstack11llll_opy_ (u"ࠢࡾࡿࠥత"))
  except Exception as e:
    logger.debug(bstack11llll_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣࡿࢂࠨథ"), e)
def bstack1l11l1111_opy_(context, message, level):
  try:
    context.page.evaluate(bstack11llll_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥద"), bstack11llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨధ") + json.dumps(message) + bstack11llll_opy_ (u"ࠫ࠱ࠨ࡬ࡦࡸࡨࡰࠧࡀࠧన") + json.dumps(level) + bstack11llll_opy_ (u"ࠬࢃࡽࠨ఩"))
  except Exception as e:
    logger.debug(bstack11llll_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡤࡲࡳࡵࡴࡢࡶ࡬ࡳࡳࠦࡻࡾࠤప"), e)
def bstack11l1111l11_opy_(self, url):
  global bstack1l11llll1l_opy_
  try:
    bstack11llll11l_opy_(url)
  except Exception as err:
    logger.debug(bstack1lll111ll_opy_.format(str(err)))
  try:
    bstack1l11llll1l_opy_(self, url)
  except Exception as e:
    try:
      parsed_error = str(e)
      if any(err_msg in parsed_error for err_msg in bstack1ll11l1lll_opy_):
        bstack11llll11l_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1lll111ll_opy_.format(str(err)))
    raise e
def bstack11l11l111_opy_(self):
  global bstack1l111l111l_opy_
  bstack1l111l111l_opy_ = self
  return
def bstack11lllll111_opy_(self):
  global bstack1ll1111l11_opy_
  bstack1ll1111l11_opy_ = self
  return
def bstack1lll1llll_opy_(test_name, bstack1l1l1ll1l_opy_):
  global CONFIG
  if percy.bstack11ll11llll_opy_() == bstack11llll_opy_ (u"ࠢࡵࡴࡸࡩࠧఫ"):
    bstack1lll1ll1l_opy_ = os.path.relpath(bstack1l1l1ll1l_opy_, start=os.getcwd())
    suite_name, _ = os.path.splitext(bstack1lll1ll1l_opy_)
    bstack1l111l11l_opy_ = suite_name + bstack11llll_opy_ (u"ࠣ࠯ࠥబ") + test_name
    threading.current_thread().percySessionName = bstack1l111l11l_opy_
def bstack1l1l11111l_opy_(self, test, *args, **kwargs):
  global bstack1ll11l111_opy_
  test_name = None
  bstack1l1l1ll1l_opy_ = None
  if test:
    test_name = str(test.name)
    bstack1l1l1ll1l_opy_ = str(test.source)
  bstack1lll1llll_opy_(test_name, bstack1l1l1ll1l_opy_)
  bstack1ll11l111_opy_(self, test, *args, **kwargs)
def bstack1ll111llll_opy_(driver, bstack1l111l11l_opy_):
  if not bstack1lll1ll11_opy_ and bstack1l111l11l_opy_:
      bstack111l11l1l_opy_ = {
          bstack11llll_opy_ (u"ࠩࡤࡧࡹ࡯࡯࡯ࠩభ"): bstack11llll_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫమ"),
          bstack11llll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧయ"): {
              bstack11llll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪర"): bstack1l111l11l_opy_
          }
      }
      bstack1l1ll11l11_opy_ = bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫఱ").format(json.dumps(bstack111l11l1l_opy_))
      driver.execute_script(bstack1l1ll11l11_opy_)
  if bstack11l1l1ll1_opy_:
      bstack1l11111l1_opy_ = {
          bstack11llll_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧల"): bstack11llll_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪళ"),
          bstack11llll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬఴ"): {
              bstack11llll_opy_ (u"ࠪࡨࡦࡺࡡࠨవ"): bstack1l111l11l_opy_ + bstack11llll_opy_ (u"ࠫࠥࡶࡡࡴࡵࡨࡨࠦ࠭శ"),
              bstack11llll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫష"): bstack11llll_opy_ (u"࠭ࡩ࡯ࡨࡲࠫస")
          }
      }
      if bstack11l1l1ll1_opy_.status == bstack11llll_opy_ (u"ࠧࡑࡃࡖࡗࠬహ"):
          bstack1lll11lll_opy_ = bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭఺").format(json.dumps(bstack1l11111l1_opy_))
          driver.execute_script(bstack1lll11lll_opy_)
          bstack11l11l11ll_opy_(driver, bstack11llll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ఻"))
      elif bstack11l1l1ll1_opy_.status == bstack11llll_opy_ (u"ࠪࡊࡆࡏࡌࠨ఼"):
          reason = bstack11llll_opy_ (u"ࠦࠧఽ")
          bstack11ll11111l_opy_ = bstack1l111l11l_opy_ + bstack11llll_opy_ (u"ࠬࠦࡦࡢ࡫࡯ࡩࡩ࠭ా")
          if bstack11l1l1ll1_opy_.message:
              reason = str(bstack11l1l1ll1_opy_.message)
              bstack11ll11111l_opy_ = bstack11ll11111l_opy_ + bstack11llll_opy_ (u"࠭ࠠࡸ࡫ࡷ࡬ࠥ࡫ࡲࡳࡱࡵ࠾ࠥ࠭ి") + reason
          bstack1l11111l1_opy_[bstack11llll_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪీ")] = {
              bstack11llll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧు"): bstack11llll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨూ"),
              bstack11llll_opy_ (u"ࠪࡨࡦࡺࡡࠨృ"): bstack11ll11111l_opy_
          }
          bstack1lll11lll_opy_ = bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩౄ").format(json.dumps(bstack1l11111l1_opy_))
          driver.execute_script(bstack1lll11lll_opy_)
          bstack11l11l11ll_opy_(driver, bstack11llll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ౅"), reason)
          bstack1l1111ll1_opy_(reason, str(bstack11l1l1ll1_opy_), str(bstack11l111ll1l_opy_), logger)
def bstack1ll11lll11_opy_(driver, test):
  if percy.bstack11ll11llll_opy_() == bstack11llll_opy_ (u"ࠨࡴࡳࡷࡨࠦె") and percy.bstack11111l1l1_opy_() == bstack11llll_opy_ (u"ࠢࡵࡧࡶࡸࡨࡧࡳࡦࠤే"):
      bstack1l11lll1l_opy_ = bstack1ll111l1_opy_(threading.current_thread(), bstack11llll_opy_ (u"ࠨࡲࡨࡶࡨࡿࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫై"), None)
      bstack11lll111l1_opy_(driver, bstack1l11lll1l_opy_, test)
  if bstack1ll111l1_opy_(threading.current_thread(), bstack11llll_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭౉"), None) and bstack1ll111l1_opy_(
          threading.current_thread(), bstack11llll_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩొ"), None):
      logger.info(bstack11llll_opy_ (u"ࠦࡆࡻࡴࡰ࡯ࡤࡸࡪࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢࡨࡼࡪࡩࡵࡵ࡫ࡲࡲࠥ࡮ࡡࡴࠢࡨࡲࡩ࡫ࡤ࠯ࠢࡓࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡮ࡹࠠࡶࡰࡧࡩࡷࡽࡡࡺ࠰ࠣࠦో"))
      bstack11111l11_opy_.bstack11111l1l_opy_(driver, name=test.name, path=test.source)
def bstack1l1lll1l11_opy_(test, bstack1l111l11l_opy_):
    try:
      bstack111l1l1l1_opy_ = datetime.datetime.now()
      data = {}
      if test:
        data[bstack11llll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪౌ")] = bstack1l111l11l_opy_
      if bstack11l1l1ll1_opy_:
        if bstack11l1l1ll1_opy_.status == bstack11llll_opy_ (u"࠭ࡐࡂࡕࡖ్ࠫ"):
          data[bstack11llll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ౎")] = bstack11llll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ౏")
        elif bstack11l1l1ll1_opy_.status == bstack11llll_opy_ (u"ࠩࡉࡅࡎࡒࠧ౐"):
          data[bstack11llll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ౑")] = bstack11llll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ౒")
          if bstack11l1l1ll1_opy_.message:
            data[bstack11llll_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬ౓")] = str(bstack11l1l1ll1_opy_.message)
      user = CONFIG[bstack11llll_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ౔")]
      key = CONFIG[bstack11llll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻౕࠪ")]
      url = bstack11llll_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡾࢁ࠿ࢁࡽࡁࡣࡳ࡭࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡷࡪࡹࡳࡪࡱࡱࡷ࠴ࢁࡽ࠯࡬ࡶࡳࡳౖ࠭").format(user, key, bstack1l1l11111_opy_)
      headers = {
        bstack11llll_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨ౗"): bstack11llll_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ౘ"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
        cli.bstack1ll1l1l11l_opy_(bstack11llll_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼ࡸࡴࡩࡧࡴࡦࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡵࡷࡥࡹࡻࡳࠣౙ"), datetime.datetime.now() - bstack111l1l1l1_opy_)
    except Exception as e:
      logger.error(bstack1ll111l1l_opy_.format(str(e)))
def bstack1lll1lll1l_opy_(test, bstack1l111l11l_opy_):
  global CONFIG
  global bstack1ll1111l11_opy_
  global bstack1l111l111l_opy_
  global bstack1l1l11111_opy_
  global bstack11l1l1ll1_opy_
  global bstack1ll11ll11l_opy_
  global bstack1lll1lll1_opy_
  global bstack11ll1l11l1_opy_
  global bstack11ll1ll1l1_opy_
  global bstack1ll1l111ll_opy_
  global bstack1ll1111111_opy_
  global bstack1l1lll1ll1_opy_
  try:
    if not bstack1l1l11111_opy_:
      with open(os.path.join(os.path.expanduser(bstack11llll_opy_ (u"ࠬࢄࠧౚ")), bstack11llll_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭౛"), bstack11llll_opy_ (u"ࠧ࠯ࡵࡨࡷࡸ࡯࡯࡯࡫ࡧࡷ࠳ࡺࡸࡵࠩ౜"))) as f:
        bstack1lllll11l_opy_ = json.loads(bstack11llll_opy_ (u"ࠣࡽࠥౝ") + f.read().strip() + bstack11llll_opy_ (u"ࠩࠥࡼࠧࡀࠠࠣࡻࠥࠫ౞") + bstack11llll_opy_ (u"ࠥࢁࠧ౟"))
        bstack1l1l11111_opy_ = bstack1lllll11l_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack1ll1111111_opy_:
    for driver in bstack1ll1111111_opy_:
      if bstack1l1l11111_opy_ == driver.session_id:
        if test:
          bstack1ll11lll11_opy_(driver, test)
        bstack1ll111llll_opy_(driver, bstack1l111l11l_opy_)
  elif bstack1l1l11111_opy_:
    bstack1l1lll1l11_opy_(test, bstack1l111l11l_opy_)
  if bstack1ll1111l11_opy_:
    bstack11ll1l11l1_opy_(bstack1ll1111l11_opy_)
  if bstack1l111l111l_opy_:
    bstack11ll1ll1l1_opy_(bstack1l111l111l_opy_)
  if bstack1l1l1l11ll_opy_:
    bstack1ll1l111ll_opy_()
def bstack1lllll11l1_opy_(self, test, *args, **kwargs):
  bstack1l111l11l_opy_ = None
  if test:
    bstack1l111l11l_opy_ = str(test.name)
  bstack1lll1lll1l_opy_(test, bstack1l111l11l_opy_)
  bstack1lll1lll1_opy_(self, test, *args, **kwargs)
def bstack11l11l11l1_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack111l11lll_opy_
  global CONFIG
  global bstack1ll1111111_opy_
  global bstack1l1l11111_opy_
  bstack1l1ll1lll1_opy_ = None
  try:
    if bstack1ll111l1_opy_(threading.current_thread(), bstack11llll_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪౠ"), None):
      try:
        if not bstack1l1l11111_opy_:
          with open(os.path.join(os.path.expanduser(bstack11llll_opy_ (u"ࠬࢄࠧౡ")), bstack11llll_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ౢ"), bstack11llll_opy_ (u"ࠧ࠯ࡵࡨࡷࡸ࡯࡯࡯࡫ࡧࡷ࠳ࡺࡸࡵࠩౣ"))) as f:
            bstack1lllll11l_opy_ = json.loads(bstack11llll_opy_ (u"ࠣࡽࠥ౤") + f.read().strip() + bstack11llll_opy_ (u"ࠩࠥࡼࠧࡀࠠࠣࡻࠥࠫ౥") + bstack11llll_opy_ (u"ࠥࢁࠧ౦"))
            bstack1l1l11111_opy_ = bstack1lllll11l_opy_[str(threading.get_ident())]
      except:
        pass
      if bstack1ll1111111_opy_:
        for driver in bstack1ll1111111_opy_:
          if bstack1l1l11111_opy_ == driver.session_id:
            bstack1l1ll1lll1_opy_ = driver
    bstack1lllll1lll_opy_ = bstack11111l11_opy_.bstack11l1ll1ll1_opy_(test.tags)
    if bstack1l1ll1lll1_opy_:
      threading.current_thread().isA11yTest = bstack11111l11_opy_.bstack1lllll11ll_opy_(bstack1l1ll1lll1_opy_, bstack1lllll1lll_opy_)
    else:
      threading.current_thread().isA11yTest = bstack1lllll1lll_opy_
  except:
    pass
  bstack111l11lll_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack11l1l1ll1_opy_
  bstack11l1l1ll1_opy_ = self._test
def bstack1ll1ll111l_opy_():
  global bstack111l1l111_opy_
  try:
    if os.path.exists(bstack111l1l111_opy_):
      os.remove(bstack111l1l111_opy_)
  except Exception as e:
    logger.debug(bstack11llll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡤࡦ࡮ࡨࡸ࡮ࡴࡧࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠠࡧ࡫࡯ࡩ࠿ࠦࠧ౧") + str(e))
def bstack1l1llll111_opy_():
  global bstack111l1l111_opy_
  bstack1l1lll1111_opy_ = {}
  try:
    if not os.path.isfile(bstack111l1l111_opy_):
      with open(bstack111l1l111_opy_, bstack11llll_opy_ (u"ࠬࡽࠧ౨")):
        pass
      with open(bstack111l1l111_opy_, bstack11llll_opy_ (u"ࠨࡷࠬࠤ౩")) as outfile:
        json.dump({}, outfile)
    if os.path.exists(bstack111l1l111_opy_):
      bstack1l1lll1111_opy_ = json.load(open(bstack111l1l111_opy_, bstack11llll_opy_ (u"ࠧࡳࡤࠪ౪")))
  except Exception as e:
    logger.debug(bstack11llll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡶࡪࡧࡤࡪࡰࡪࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠣࡪ࡮ࡲࡥ࠻ࠢࠪ౫") + str(e))
  finally:
    return bstack1l1lll1111_opy_
def bstack1ll1l1lll1_opy_(platform_index, item_index):
  global bstack111l1l111_opy_
  try:
    bstack1l1lll1111_opy_ = bstack1l1llll111_opy_()
    bstack1l1lll1111_opy_[item_index] = platform_index
    with open(bstack111l1l111_opy_, bstack11llll_opy_ (u"ࠤࡺ࠯ࠧ౬")) as outfile:
      json.dump(bstack1l1lll1111_opy_, outfile)
  except Exception as e:
    logger.debug(bstack11llll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡽࡲࡪࡶ࡬ࡲ࡬ࠦࡴࡰࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠡࡨ࡬ࡰࡪࡀࠠࠨ౭") + str(e))
def bstack1ll1l1l11_opy_(bstack111lll1ll_opy_):
  global CONFIG
  bstack11l1l1111_opy_ = bstack11llll_opy_ (u"ࠫࠬ౮")
  if not bstack11llll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ౯") in CONFIG:
    logger.info(bstack11llll_opy_ (u"࠭ࡎࡰࠢࡳࡰࡦࡺࡦࡰࡴࡰࡷࠥࡶࡡࡴࡵࡨࡨࠥࡻ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡩࡨࡲࡪࡸࡡࡵࡧࠣࡶࡪࡶ࡯ࡳࡶࠣࡪࡴࡸࠠࡓࡱࡥࡳࡹࠦࡲࡶࡰࠪ౰"))
  try:
    platform = CONFIG[bstack11llll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ౱")][bstack111lll1ll_opy_]
    if bstack11llll_opy_ (u"ࠨࡱࡶࠫ౲") in platform:
      bstack11l1l1111_opy_ += str(platform[bstack11llll_opy_ (u"ࠩࡲࡷࠬ౳")]) + bstack11llll_opy_ (u"ࠪ࠰ࠥ࠭౴")
    if bstack11llll_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧ౵") in platform:
      bstack11l1l1111_opy_ += str(platform[bstack11llll_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨ౶")]) + bstack11llll_opy_ (u"࠭ࠬࠡࠩ౷")
    if bstack11llll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫ౸") in platform:
      bstack11l1l1111_opy_ += str(platform[bstack11llll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬ౹")]) + bstack11llll_opy_ (u"ࠩ࠯ࠤࠬ౺")
    if bstack11llll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬ౻") in platform:
      bstack11l1l1111_opy_ += str(platform[bstack11llll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭౼")]) + bstack11llll_opy_ (u"ࠬ࠲ࠠࠨ౽")
    if bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ౾") in platform:
      bstack11l1l1111_opy_ += str(platform[bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ౿")]) + bstack11llll_opy_ (u"ࠨ࠮ࠣࠫಀ")
    if bstack11llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪಁ") in platform:
      bstack11l1l1111_opy_ += str(platform[bstack11llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫಂ")]) + bstack11llll_opy_ (u"ࠫ࠱ࠦࠧಃ")
  except Exception as e:
    logger.debug(bstack11llll_opy_ (u"࡙ࠬ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠢ࡬ࡲࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡯࡮ࡨࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡸࡺࡲࡪࡰࡪࠤ࡫ࡵࡲࠡࡴࡨࡴࡴࡸࡴࠡࡩࡨࡲࡪࡸࡡࡵ࡫ࡲࡲࠬ಄") + str(e))
  finally:
    if bstack11l1l1111_opy_[len(bstack11l1l1111_opy_) - 2:] == bstack11llll_opy_ (u"࠭ࠬࠡࠩಅ"):
      bstack11l1l1111_opy_ = bstack11l1l1111_opy_[:-2]
    return bstack11l1l1111_opy_
def bstack11ll1l111_opy_(path, bstack11l1l1111_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack111ll11l1_opy_ = ET.parse(path)
    bstack1l11l1l111_opy_ = bstack111ll11l1_opy_.getroot()
    bstack1111l111l_opy_ = None
    for suite in bstack1l11l1l111_opy_.iter(bstack11llll_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭ಆ")):
      if bstack11llll_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨಇ") in suite.attrib:
        suite.attrib[bstack11llll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧಈ")] += bstack11llll_opy_ (u"ࠪࠤࠬಉ") + bstack11l1l1111_opy_
        bstack1111l111l_opy_ = suite
    bstack111l11111_opy_ = None
    for robot in bstack1l11l1l111_opy_.iter(bstack11llll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪಊ")):
      bstack111l11111_opy_ = robot
    bstack1ll1lll111_opy_ = len(bstack111l11111_opy_.findall(bstack11llll_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫಋ")))
    if bstack1ll1lll111_opy_ == 1:
      bstack111l11111_opy_.remove(bstack111l11111_opy_.findall(bstack11llll_opy_ (u"࠭ࡳࡶ࡫ࡷࡩࠬಌ"))[0])
      bstack11l111llll_opy_ = ET.Element(bstack11llll_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭಍"), attrib={bstack11llll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ಎ"): bstack11llll_opy_ (u"ࠩࡖࡹ࡮ࡺࡥࡴࠩಏ"), bstack11llll_opy_ (u"ࠪ࡭ࡩ࠭ಐ"): bstack11llll_opy_ (u"ࠫࡸ࠶ࠧ಑")})
      bstack111l11111_opy_.insert(1, bstack11l111llll_opy_)
      bstack1111111l1_opy_ = None
      for suite in bstack111l11111_opy_.iter(bstack11llll_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫಒ")):
        bstack1111111l1_opy_ = suite
      bstack1111111l1_opy_.append(bstack1111l111l_opy_)
      bstack11ll111111_opy_ = None
      for status in bstack1111l111l_opy_.iter(bstack11llll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ಓ")):
        bstack11ll111111_opy_ = status
      bstack1111111l1_opy_.append(bstack11ll111111_opy_)
    bstack111ll11l1_opy_.write(path)
  except Exception as e:
    logger.debug(bstack11llll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡳࡥࡷࡹࡩ࡯ࡩࠣࡻ࡭࡯࡬ࡦࠢࡪࡩࡳ࡫ࡲࡢࡶ࡬ࡲ࡬ࠦࡲࡰࡤࡲࡸࠥࡸࡥࡱࡱࡵࡸࠬಔ") + str(e))
def bstack1ll1lll1l_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack1l1111l1l1_opy_
  global CONFIG
  if bstack11llll_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࡱࡣࡷ࡬ࠧಕ") in options:
    del options[bstack11llll_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯ࡲࡤࡸ࡭ࠨಖ")]
  json_data = bstack1l1llll111_opy_()
  for bstack1l11ll111l_opy_ in json_data.keys():
    path = os.path.join(os.getcwd(), bstack11llll_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࡡࡵࡩࡸࡻ࡬ࡵࡵࠪಗ"), str(bstack1l11ll111l_opy_), bstack11llll_opy_ (u"ࠫࡴࡻࡴࡱࡷࡷ࠲ࡽࡳ࡬ࠨಘ"))
    bstack11ll1l111_opy_(path, bstack1ll1l1l11_opy_(json_data[bstack1l11ll111l_opy_]))
  bstack1ll1ll111l_opy_()
  return bstack1l1111l1l1_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1llll1111l_opy_(self, ff_profile_dir):
  global bstack1ll1llll11_opy_
  if not ff_profile_dir:
    return None
  return bstack1ll1llll11_opy_(self, ff_profile_dir)
def bstack1l111111l_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack11ll1111l1_opy_
  bstack11l1l111l1_opy_ = []
  if bstack11llll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨಙ") in CONFIG:
    bstack11l1l111l1_opy_ = CONFIG[bstack11llll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩಚ")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack11llll_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࠣಛ")],
      pabot_args[bstack11llll_opy_ (u"ࠣࡸࡨࡶࡧࡵࡳࡦࠤಜ")],
      argfile,
      pabot_args.get(bstack11llll_opy_ (u"ࠤ࡫࡭ࡻ࡫ࠢಝ")),
      pabot_args[bstack11llll_opy_ (u"ࠥࡴࡷࡵࡣࡦࡵࡶࡩࡸࠨಞ")],
      platform[0],
      bstack11ll1111l1_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack11llll_opy_ (u"ࠦࡦࡸࡧࡶ࡯ࡨࡲࡹ࡬ࡩ࡭ࡧࡶࠦಟ")] or [(bstack11llll_opy_ (u"ࠧࠨಠ"), None)]
    for platform in enumerate(bstack11l1l111l1_opy_)
  ]
def bstack11l111111l_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack1ll1ll1111_opy_=bstack11llll_opy_ (u"࠭ࠧಡ")):
  global bstack1l1111lll_opy_
  self.platform_index = platform_index
  self.bstack1lll111ll1_opy_ = bstack1ll1ll1111_opy_
  bstack1l1111lll_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack1111ll111_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack11ll1l1l11_opy_
  global bstack1l1l11lll_opy_
  bstack11l1l1llll_opy_ = copy.deepcopy(item)
  if not bstack11llll_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩಢ") in item.options:
    bstack11l1l1llll_opy_.options[bstack11llll_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪಣ")] = []
  bstack1ll11111ll_opy_ = bstack11l1l1llll_opy_.options[bstack11llll_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫತ")].copy()
  for v in bstack11l1l1llll_opy_.options[bstack11llll_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬಥ")]:
    if bstack11llll_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡔࡑࡇࡔࡇࡑࡕࡑࡎࡔࡄࡆ࡚ࠪದ") in v:
      bstack1ll11111ll_opy_.remove(v)
    if bstack11llll_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡈࡒࡉࡂࡔࡊࡗࠬಧ") in v:
      bstack1ll11111ll_opy_.remove(v)
    if bstack11llll_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡊࡅࡇࡎࡒࡇࡆࡒࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪನ") in v:
      bstack1ll11111ll_opy_.remove(v)
  bstack1ll11111ll_opy_.insert(0, bstack11llll_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡐࡍࡃࡗࡊࡔࡘࡍࡊࡐࡇࡉ࡝ࡀࡻࡾࠩ಩").format(bstack11l1l1llll_opy_.platform_index))
  bstack1ll11111ll_opy_.insert(0, bstack11llll_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡅࡇࡉࡐࡔࡉࡁࡍࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖ࠿ࢁࡽࠨಪ").format(bstack11l1l1llll_opy_.bstack1lll111ll1_opy_))
  bstack11l1l1llll_opy_.options[bstack11llll_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫಫ")] = bstack1ll11111ll_opy_
  if bstack1l1l11lll_opy_:
    bstack11l1l1llll_opy_.options[bstack11llll_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬಬ")].insert(0, bstack11llll_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡇࡑࡏࡁࡓࡉࡖ࠾ࢀࢃࠧಭ").format(bstack1l1l11lll_opy_))
  return bstack11ll1l1l11_opy_(caller_id, datasources, is_last, bstack11l1l1llll_opy_, outs_dir)
def bstack11ll1l111l_opy_(command, item_index):
  if bstack1111l1l1_opy_.get_property(bstack11llll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭ಮ")):
    os.environ[bstack11llll_opy_ (u"࠭ࡃࡖࡔࡕࡉࡓ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡇࡅ࡙ࡇࠧಯ")] = json.dumps(CONFIG[bstack11llll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪರ")][item_index % bstack1lll111lll_opy_])
  global bstack1l1l11lll_opy_
  if bstack1l1l11lll_opy_:
    command[0] = command[0].replace(bstack11llll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧಱ"), bstack11llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠮ࡵࡧ࡯ࠥࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱࠦ࠭࠮ࡤࡶࡸࡦࡩ࡫ࡠ࡫ࡷࡩࡲࡥࡩ࡯ࡦࡨࡼࠥ࠭ಲ") + str(
      item_index) + bstack11llll_opy_ (u"ࠪࠤࠬಳ") + bstack1l1l11lll_opy_, 1)
  else:
    command[0] = command[0].replace(bstack11llll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ಴"),
                                    bstack11llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠱ࡸࡪ࡫ࠡࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠢ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣ࡮ࡺࡥ࡮ࡡ࡬ࡲࡩ࡫ࡸࠡࠩವ") + str(item_index), 1)
def bstack1l1l11l1l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack11l1lll1ll_opy_
  bstack11ll1l111l_opy_(command, item_index)
  return bstack11l1lll1ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack11llll1ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack11l1lll1ll_opy_
  bstack11ll1l111l_opy_(command, item_index)
  return bstack11l1lll1ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack11lllll1l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack11l1lll1ll_opy_
  bstack11ll1l111l_opy_(command, item_index)
  return bstack11l1lll1ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def is_driver_active(driver):
  return True if driver and driver.session_id else False
def bstack1lll1111l1_opy_(self, runner, quiet=False, capture=True):
  global bstack1lll1l11ll_opy_
  bstack1lll11ll1l_opy_ = bstack1lll1l11ll_opy_(self, runner, quiet=quiet, capture=capture)
  if self.exception:
    if not hasattr(runner, bstack11llll_opy_ (u"࠭ࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࡡࡤࡶࡷ࠭ಶ")):
      runner.exception_arr = []
    if not hasattr(runner, bstack11llll_opy_ (u"ࠧࡦࡺࡦࡣࡹࡸࡡࡤࡧࡥࡥࡨࡱ࡟ࡢࡴࡵࠫಷ")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1lll11ll1l_opy_
def bstack1lllll1l1l_opy_(runner, hook_name, context, element, bstack1l1l1l1ll1_opy_, *args):
  try:
    if runner.hooks.get(hook_name):
      bstack1l1l111ll_opy_.bstack11ll111l_opy_(hook_name, element)
    bstack1l1l1l1ll1_opy_(runner, hook_name, context, *args)
    if runner.hooks.get(hook_name):
      bstack1l1l111ll_opy_.bstack11ll1l1l_opy_(element)
      if hook_name not in [bstack11llll_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠬಸ"), bstack11llll_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡣ࡯ࡰࠬಹ")] and args and hasattr(args[0], bstack11llll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡡࡰࡩࡸࡹࡡࡨࡧࠪ಺")):
        args[0].error_message = bstack11llll_opy_ (u"ࠫࠬ಻")
  except Exception as e:
    logger.debug(bstack11llll_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡪࡤࡲࡩࡲࡥࠡࡪࡲࡳࡰࡹࠠࡪࡰࠣࡦࡪ࡮ࡡࡷࡧ࠽ࠤࢀࢃ಼ࠧ").format(str(e)))
def bstack11lll1llll_opy_(runner, name, context, bstack1l1l1l1ll1_opy_, *args):
    if runner.hooks.get(bstack11llll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠥಽ")).__name__ != bstack11llll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࡣࡩ࡫ࡦࡢࡷ࡯ࡸࡤ࡮࡯ࡰ࡭ࠥಾ"):
      bstack1lllll1l1l_opy_(runner, name, context, runner, bstack1l1l1l1ll1_opy_, *args)
    try:
      threading.current_thread().bstackSessionDriver if bstack1lll1l1111_opy_(bstack11llll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧಿ")) else context.browser
      runner.driver_initialised = bstack11llll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࠨೀ")
    except Exception as e:
      logger.debug(bstack11llll_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡨࡷ࡯ࡶࡦࡴࠣ࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡸ࡫ࠠࡢࡶࡷࡶ࡮ࡨࡵࡵࡧ࠽ࠤࢀࢃࠧು").format(str(e)))
def bstack11ll1ll1l_opy_(runner, name, context, bstack1l1l1l1ll1_opy_, *args):
    bstack1lllll1l1l_opy_(runner, name, context, context.feature, bstack1l1l1l1ll1_opy_, *args)
    try:
      if not bstack1lll1ll11_opy_:
        bstack1l1ll1lll1_opy_ = threading.current_thread().bstackSessionDriver if bstack1lll1l1111_opy_(bstack11llll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪೂ")) else context.browser
        if is_driver_active(bstack1l1ll1lll1_opy_):
          if runner.driver_initialised is None: runner.driver_initialised = bstack11llll_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤ࡬ࡥࡢࡶࡸࡶࡪࠨೃ")
          bstack11l1l1ll11_opy_ = str(runner.feature.name)
          bstack1ll1lll1l1_opy_(context, bstack11l1l1ll11_opy_)
          bstack1l1ll1lll1_opy_.execute_script(bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫೄ") + json.dumps(bstack11l1l1ll11_opy_) + bstack11llll_opy_ (u"ࠧࡾࡿࠪ೅"))
    except Exception as e:
      logger.debug(bstack11llll_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡪࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡪࡪࡧࡴࡶࡴࡨ࠾ࠥࢁࡽࠨೆ").format(str(e)))
def bstack111ll111l_opy_(runner, name, context, bstack1l1l1l1ll1_opy_, *args):
    if hasattr(context, bstack11llll_opy_ (u"ࠩࡶࡧࡪࡴࡡࡳ࡫ࡲࠫೇ")):
        bstack1l1l111ll_opy_.start_test(context)
    target = context.scenario if hasattr(context, bstack11llll_opy_ (u"ࠪࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬೈ")) else context.feature
    bstack1lllll1l1l_opy_(runner, name, context, target, bstack1l1l1l1ll1_opy_, *args)
def bstack111ll1111_opy_(runner, name, context, bstack1l1l1l1ll1_opy_, *args):
    if len(context.scenario.tags) == 0: bstack1l1l111ll_opy_.start_test(context)
    bstack1lllll1l1l_opy_(runner, name, context, context.scenario, bstack1l1l1l1ll1_opy_, *args)
    threading.current_thread().a11y_stop = False
    bstack11llll1l11_opy_.bstack1llll11l1_opy_(context, *args)
    try:
      bstack1l1ll1lll1_opy_ = bstack1ll111l1_opy_(threading.current_thread(), bstack11llll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪ೉"), context.browser)
      if is_driver_active(bstack1l1ll1lll1_opy_):
        bstack1lll11ll_opy_.bstack1ll1ll1l1_opy_(bstack1ll111l1_opy_(threading.current_thread(), bstack11llll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫೊ"), {}))
        if runner.driver_initialised is None: runner.driver_initialised = bstack11llll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠣೋ")
        if (not bstack1lll1ll11_opy_):
          scenario_name = args[0].name
          feature_name = bstack11l1l1ll11_opy_ = str(runner.feature.name)
          bstack11l1l1ll11_opy_ = feature_name + bstack11llll_opy_ (u"ࠧࠡ࠯ࠣࠫೌ") + scenario_name
          if runner.driver_initialised == bstack11llll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱ್ࠥ"):
            bstack1ll1lll1l1_opy_(context, bstack11l1l1ll11_opy_)
            bstack1l1ll1lll1_opy_.execute_script(bstack11llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿ࠦࠧ೎") + json.dumps(bstack11l1l1ll11_opy_) + bstack11llll_opy_ (u"ࠪࢁࢂ࠭೏"))
    except Exception as e:
      logger.debug(bstack11llll_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣ࡭ࡳࠦࡢࡦࡨࡲࡶࡪࠦࡳࡤࡧࡱࡥࡷ࡯࡯࠻ࠢࡾࢁࠬ೐").format(str(e)))
def bstack1l1l1l1lll_opy_(runner, name, context, bstack1l1l1l1ll1_opy_, *args):
    bstack1lllll1l1l_opy_(runner, name, context, args[0], bstack1l1l1l1ll1_opy_, *args)
    try:
      bstack1l1ll1lll1_opy_ = threading.current_thread().bstackSessionDriver if bstack1lll1l1111_opy_(bstack11llll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ೑")) else context.browser
      if is_driver_active(bstack1l1ll1lll1_opy_):
        if runner.driver_initialised is None: runner.driver_initialised = bstack11llll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠦ೒")
        bstack1l1l111ll_opy_.bstack11ll11l1_opy_(args[0])
        if runner.driver_initialised == bstack11llll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠧ೓"):
          feature_name = bstack11l1l1ll11_opy_ = str(runner.feature.name)
          bstack11l1l1ll11_opy_ = feature_name + bstack11llll_opy_ (u"ࠨࠢ࠰ࠤࠬ೔") + context.scenario.name
          bstack1l1ll1lll1_opy_.execute_script(bstack11llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿ࠦࠧೕ") + json.dumps(bstack11l1l1ll11_opy_) + bstack11llll_opy_ (u"ࠪࢁࢂ࠭ೖ"))
    except Exception as e:
      logger.debug(bstack11llll_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣ࡭ࡳࠦࡢࡦࡨࡲࡶࡪࠦࡳࡵࡧࡳ࠾ࠥࢁࡽࠨ೗").format(str(e)))
def bstack1lll11l1l_opy_(runner, name, context, bstack1l1l1l1ll1_opy_, *args):
  bstack1l1l111ll_opy_.bstack11l1ll1l_opy_(args[0])
  try:
    bstack11l11ll11l_opy_ = args[0].status.name
    bstack1l1ll1lll1_opy_ = threading.current_thread().bstackSessionDriver if bstack11llll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ೘") in threading.current_thread().__dict__.keys() else context.browser
    if is_driver_active(bstack1l1ll1lll1_opy_):
      if runner.driver_initialised is None:
        runner.driver_initialised  = bstack11llll_opy_ (u"࠭ࡩ࡯ࡵࡷࡩࡵ࠭೙")
        feature_name = bstack11l1l1ll11_opy_ = str(runner.feature.name)
        bstack11l1l1ll11_opy_ = feature_name + bstack11llll_opy_ (u"ࠧࠡ࠯ࠣࠫ೚") + context.scenario.name
        bstack1l1ll1lll1_opy_.execute_script(bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭೛") + json.dumps(bstack11l1l1ll11_opy_) + bstack11llll_opy_ (u"ࠩࢀࢁࠬ೜"))
    if str(bstack11l11ll11l_opy_).lower() == bstack11llll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪೝ"):
      bstack11l11111l_opy_ = bstack11llll_opy_ (u"ࠫࠬೞ")
      bstack1l11ll11l1_opy_ = bstack11llll_opy_ (u"ࠬ࠭೟")
      bstack11l1l11ll1_opy_ = bstack11llll_opy_ (u"࠭ࠧೠ")
      try:
        import traceback
        bstack11l11111l_opy_ = runner.exception.__class__.__name__
        bstack11l1lll1_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1l11ll11l1_opy_ = bstack11llll_opy_ (u"ࠧࠡࠩೡ").join(bstack11l1lll1_opy_)
        bstack11l1l11ll1_opy_ = bstack11l1lll1_opy_[-1]
      except Exception as e:
        logger.debug(bstack1ll1111lll_opy_.format(str(e)))
      bstack11l11111l_opy_ += bstack11l1l11ll1_opy_
      bstack1l11l1111_opy_(context, json.dumps(str(args[0].name) + bstack11llll_opy_ (u"ࠣࠢ࠰ࠤࡋࡧࡩ࡭ࡧࡧࠥࡡࡴࠢೢ") + str(bstack1l11ll11l1_opy_)),
                          bstack11llll_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣೣ"))
      if runner.driver_initialised == bstack11llll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠣ೤"):
        bstack11ll111lll_opy_(getattr(context, bstack11llll_opy_ (u"ࠫࡵࡧࡧࡦࠩ೥"), None), bstack11llll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ೦"), bstack11l11111l_opy_)
        bstack1l1ll1lll1_opy_.execute_script(bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫ೧") + json.dumps(str(args[0].name) + bstack11llll_opy_ (u"ࠢࠡ࠯ࠣࡊࡦ࡯࡬ࡦࡦࠤࡠࡳࠨ೨") + str(bstack1l11ll11l1_opy_)) + bstack11llll_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧࢃࡽࠨ೩"))
      if runner.driver_initialised == bstack11llll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠢ೪"):
        bstack11l11l11ll_opy_(bstack1l1ll1lll1_opy_, bstack11llll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ೫"), bstack11llll_opy_ (u"ࠦࡘࡩࡥ࡯ࡣࡵ࡭ࡴࠦࡦࡢ࡫࡯ࡩࡩࠦࡷࡪࡶ࡫࠾ࠥࡢ࡮ࠣ೬") + str(bstack11l11111l_opy_))
    else:
      bstack1l11l1111_opy_(context, bstack11llll_opy_ (u"ࠧࡖࡡࡴࡵࡨࡨࠦࠨ೭"), bstack11llll_opy_ (u"ࠨࡩ࡯ࡨࡲࠦ೮"))
      if runner.driver_initialised == bstack11llll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠧ೯"):
        bstack11ll111lll_opy_(getattr(context, bstack11llll_opy_ (u"ࠨࡲࡤ࡫ࡪ࠭೰"), None), bstack11llll_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤೱ"))
      bstack1l1ll1lll1_opy_.execute_script(bstack11llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨೲ") + json.dumps(str(args[0].name) + bstack11llll_opy_ (u"ࠦࠥ࠳ࠠࡑࡣࡶࡷࡪࡪࠡࠣೳ")) + bstack11llll_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣࡿࢀࠫ೴"))
      if runner.driver_initialised == bstack11llll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠦ೵"):
        bstack11l11l11ll_opy_(bstack1l1ll1lll1_opy_, bstack11llll_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢ೶"))
  except Exception as e:
    logger.debug(bstack11llll_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡲࡧࡲ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣ࡭ࡳࠦࡡࡧࡶࡨࡶࠥࡹࡴࡦࡲ࠽ࠤࢀࢃࠧ೷").format(str(e)))
  bstack1lllll1l1l_opy_(runner, name, context, args[0], bstack1l1l1l1ll1_opy_, *args)
def bstack11l11ll1ll_opy_(runner, name, context, bstack1l1l1l1ll1_opy_, *args):
  bstack1l1l111ll_opy_.end_test(args[0])
  try:
    bstack11lll1lll_opy_ = args[0].status.name
    bstack1l1ll1lll1_opy_ = bstack1ll111l1_opy_(threading.current_thread(), bstack11llll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ೸"), context.browser)
    bstack11llll1l11_opy_.bstack1l1ll1l1ll_opy_(bstack1l1ll1lll1_opy_)
    if str(bstack11lll1lll_opy_).lower() == bstack11llll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ೹"):
      bstack11l11111l_opy_ = bstack11llll_opy_ (u"ࠫࠬ೺")
      bstack1l11ll11l1_opy_ = bstack11llll_opy_ (u"ࠬ࠭೻")
      bstack11l1l11ll1_opy_ = bstack11llll_opy_ (u"࠭ࠧ೼")
      try:
        import traceback
        bstack11l11111l_opy_ = runner.exception.__class__.__name__
        bstack11l1lll1_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1l11ll11l1_opy_ = bstack11llll_opy_ (u"ࠧࠡࠩ೽").join(bstack11l1lll1_opy_)
        bstack11l1l11ll1_opy_ = bstack11l1lll1_opy_[-1]
      except Exception as e:
        logger.debug(bstack1ll1111lll_opy_.format(str(e)))
      bstack11l11111l_opy_ += bstack11l1l11ll1_opy_
      bstack1l11l1111_opy_(context, json.dumps(str(args[0].name) + bstack11llll_opy_ (u"ࠣࠢ࠰ࠤࡋࡧࡩ࡭ࡧࡧࠥࡡࡴࠢ೾") + str(bstack1l11ll11l1_opy_)),
                          bstack11llll_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣ೿"))
      if runner.driver_initialised == bstack11llll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧഀ") or runner.driver_initialised == bstack11llll_opy_ (u"ࠫ࡮ࡴࡳࡵࡧࡳࠫഁ"):
        bstack11ll111lll_opy_(getattr(context, bstack11llll_opy_ (u"ࠬࡶࡡࡨࡧࠪം"), None), bstack11llll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨഃ"), bstack11l11111l_opy_)
        bstack1l1ll1lll1_opy_.execute_script(bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬഄ") + json.dumps(str(args[0].name) + bstack11llll_opy_ (u"ࠣࠢ࠰ࠤࡋࡧࡩ࡭ࡧࡧࠥࡡࡴࠢഅ") + str(bstack1l11ll11l1_opy_)) + bstack11llll_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡦࡴࡵࡳࡷࠨࡽࡾࠩആ"))
      if runner.driver_initialised == bstack11llll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧഇ") or runner.driver_initialised == bstack11llll_opy_ (u"ࠫ࡮ࡴࡳࡵࡧࡳࠫഈ"):
        bstack11l11l11ll_opy_(bstack1l1ll1lll1_opy_, bstack11llll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬഉ"), bstack11llll_opy_ (u"ࠨࡓࡤࡧࡱࡥࡷ࡯࡯ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡹ࡬ࡸ࡭ࡀࠠ࡝ࡰࠥഊ") + str(bstack11l11111l_opy_))
    else:
      bstack1l11l1111_opy_(context, bstack11llll_opy_ (u"ࠢࡑࡣࡶࡷࡪࡪࠡࠣഋ"), bstack11llll_opy_ (u"ࠣ࡫ࡱࡪࡴࠨഌ"))
      if runner.driver_initialised == bstack11llll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠦ഍") or runner.driver_initialised == bstack11llll_opy_ (u"ࠪ࡭ࡳࡹࡴࡦࡲࠪഎ"):
        bstack11ll111lll_opy_(getattr(context, bstack11llll_opy_ (u"ࠫࡵࡧࡧࡦࠩഏ"), None), bstack11llll_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧഐ"))
      bstack1l1ll1lll1_opy_.execute_script(bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫ഑") + json.dumps(str(args[0].name) + bstack11llll_opy_ (u"ࠢࠡ࠯ࠣࡔࡦࡹࡳࡦࡦࠤࠦഒ")) + bstack11llll_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡩ࡯ࡨࡲࠦࢂࢃࠧഓ"))
      if runner.driver_initialised == bstack11llll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠦഔ") or runner.driver_initialised == bstack11llll_opy_ (u"ࠪ࡭ࡳࡹࡴࡦࡲࠪക"):
        bstack11l11l11ll_opy_(bstack1l1ll1lll1_opy_, bstack11llll_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦഖ"))
  except Exception as e:
    logger.debug(bstack11llll_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡪࡰࠣࡥ࡫ࡺࡥࡳࠢࡩࡩࡦࡺࡵࡳࡧ࠽ࠤࢀࢃࠧഗ").format(str(e)))
  bstack1lllll1l1l_opy_(runner, name, context, context.scenario, bstack1l1l1l1ll1_opy_, *args)
  if len(context.scenario.tags) == 0: threading.current_thread().current_test_uuid = None
def bstack11ll1l1lll_opy_(runner, name, context, bstack1l1l1l1ll1_opy_, *args):
    target = context.scenario if hasattr(context, bstack11llll_opy_ (u"࠭ࡳࡤࡧࡱࡥࡷ࡯࡯ࠨഘ")) else context.feature
    bstack1lllll1l1l_opy_(runner, name, context, target, bstack1l1l1l1ll1_opy_, *args)
    threading.current_thread().current_test_uuid = None
def bstack11l1l1lll_opy_(runner, name, context, bstack1l1l1l1ll1_opy_, *args):
    try:
      bstack1l1ll1lll1_opy_ = bstack1ll111l1_opy_(threading.current_thread(), bstack11llll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ങ"), context.browser)
      if context.failed is True:
        bstack11ll1l11ll_opy_ = []
        bstack111l1lll1_opy_ = []
        bstack1lll11111_opy_ = []
        bstack111ll1l11_opy_ = bstack11llll_opy_ (u"ࠨࠩച")
        try:
          import traceback
          for exc in runner.exception_arr:
            bstack11ll1l11ll_opy_.append(exc.__class__.__name__)
          for exc_tb in runner.exc_traceback_arr:
            bstack11l1lll1_opy_ = traceback.format_tb(exc_tb)
            bstack1l11llll11_opy_ = bstack11llll_opy_ (u"ࠩࠣࠫഛ").join(bstack11l1lll1_opy_)
            bstack111l1lll1_opy_.append(bstack1l11llll11_opy_)
            bstack1lll11111_opy_.append(bstack11l1lll1_opy_[-1])
        except Exception as e:
          logger.debug(bstack1ll1111lll_opy_.format(str(e)))
        bstack11l11111l_opy_ = bstack11llll_opy_ (u"ࠪࠫജ")
        for i in range(len(bstack11ll1l11ll_opy_)):
          bstack11l11111l_opy_ += bstack11ll1l11ll_opy_[i] + bstack1lll11111_opy_[i] + bstack11llll_opy_ (u"ࠫࡡࡴࠧഝ")
        bstack111ll1l11_opy_ = bstack11llll_opy_ (u"ࠬࠦࠧഞ").join(bstack111l1lll1_opy_)
        if runner.driver_initialised in [bstack11llll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡦࡦࡣࡷࡹࡷ࡫ࠢട"), bstack11llll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠦഠ")]:
          bstack1l11l1111_opy_(context, bstack111ll1l11_opy_, bstack11llll_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢഡ"))
          bstack11ll111lll_opy_(getattr(context, bstack11llll_opy_ (u"ࠩࡳࡥ࡬࡫ࠧഢ"), None), bstack11llll_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥണ"), bstack11l11111l_opy_)
          bstack1l1ll1lll1_opy_.execute_script(bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩത") + json.dumps(bstack111ll1l11_opy_) + bstack11llll_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥࡩࡷࡸ࡯ࡳࠤࢀࢁࠬഥ"))
          bstack11l11l11ll_opy_(bstack1l1ll1lll1_opy_, bstack11llll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨദ"), bstack11llll_opy_ (u"ࠢࡔࡱࡰࡩࠥࡹࡣࡦࡰࡤࡶ࡮ࡵࡳࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢ࡟ࡲࠧധ") + str(bstack11l11111l_opy_))
          bstack1llll1111_opy_ = bstack1l11111lll_opy_(bstack111ll1l11_opy_, runner.feature.name, logger)
          if (bstack1llll1111_opy_ != None):
            bstack1111lllll_opy_.append(bstack1llll1111_opy_)
      else:
        if runner.driver_initialised in [bstack11llll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠤന"), bstack11llll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࠨഩ")]:
          bstack1l11l1111_opy_(context, bstack11llll_opy_ (u"ࠥࡊࡪࡧࡴࡶࡴࡨ࠾ࠥࠨപ") + str(runner.feature.name) + bstack11llll_opy_ (u"ࠦࠥࡶࡡࡴࡵࡨࡨࠦࠨഫ"), bstack11llll_opy_ (u"ࠧ࡯࡮ࡧࡱࠥബ"))
          bstack11ll111lll_opy_(getattr(context, bstack11llll_opy_ (u"࠭ࡰࡢࡩࡨࠫഭ"), None), bstack11llll_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢമ"))
          bstack1l1ll1lll1_opy_.execute_script(bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭യ") + json.dumps(bstack11llll_opy_ (u"ࠤࡉࡩࡦࡺࡵࡳࡧ࠽ࠤࠧര") + str(runner.feature.name) + bstack11llll_opy_ (u"ࠥࠤࡵࡧࡳࡴࡧࡧࠥࠧറ")) + bstack11llll_opy_ (u"ࠫ࠱ࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤ࡬ࡲ࡫ࡵࠢࡾࡿࠪല"))
          bstack11l11l11ll_opy_(bstack1l1ll1lll1_opy_, bstack11llll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬള"))
          bstack1llll1111_opy_ = bstack1l11111lll_opy_(bstack111ll1l11_opy_, runner.feature.name, logger)
          if (bstack1llll1111_opy_ != None):
            bstack1111lllll_opy_.append(bstack1llll1111_opy_)
    except Exception as e:
      logger.debug(bstack11llll_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡰࡥࡷࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡ࡫ࡱࠤࡦ࡬ࡴࡦࡴࠣࡪࡪࡧࡴࡶࡴࡨ࠾ࠥࢁࡽࠨഴ").format(str(e)))
    bstack1lllll1l1l_opy_(runner, name, context, context.feature, bstack1l1l1l1ll1_opy_, *args)
def bstack111llllll1_opy_(runner, name, context, bstack1l1l1l1ll1_opy_, *args):
    bstack1lllll1l1l_opy_(runner, name, context, runner, bstack1l1l1l1ll1_opy_, *args)
def bstack1lll111111_opy_(self, name, context, *args):
  if bstack1l1l1l111_opy_:
    platform_index = int(threading.current_thread()._name) % bstack1lll111lll_opy_
    bstack11lll11ll_opy_ = CONFIG[bstack11llll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪവ")][platform_index]
    os.environ[bstack11llll_opy_ (u"ࠨࡅࡘࡖࡗࡋࡎࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡉࡇࡔࡂࠩശ")] = json.dumps(bstack11lll11ll_opy_)
  global bstack1l1l1l1ll1_opy_
  if not hasattr(self, bstack11llll_opy_ (u"ࠩࡧࡶ࡮ࡼࡥࡳࡡ࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡷࡪࡪࠧഷ")):
    self.driver_initialised = None
  bstack11lll11l1_opy_ = {
      bstack11llll_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠧസ"): bstack11lll1llll_opy_,
      bstack11llll_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩࠬഹ"): bstack11ll1ll1l_opy_,
      bstack11llll_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡺࡡࡨࠩഺ"): bstack111ll111l_opy_,
      bstack11llll_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨ഻"): bstack111ll1111_opy_,
      bstack11llll_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴ഼ࠬ"): bstack1l1l1l1lll_opy_,
      bstack11llll_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡴࡶࡨࡴࠬഽ"): bstack1lll11l1l_opy_,
      bstack11llll_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪാ"): bstack11l11ll1ll_opy_,
      bstack11llll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡷࡥ࡬࠭ി"): bstack11ll1l1lll_opy_,
      bstack11llll_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡪࡪࡧࡴࡶࡴࡨࠫീ"): bstack11l1l1lll_opy_,
      bstack11llll_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡦࡲ࡬ࠨു"): bstack111llllll1_opy_
  }
  handler = bstack11lll11l1_opy_.get(name, bstack1l1l1l1ll1_opy_)
  handler(self, name, context, bstack1l1l1l1ll1_opy_, *args)
  if name in [bstack11llll_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭ൂ"), bstack11llll_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨൃ"), bstack11llll_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡢ࡮࡯ࠫൄ")]:
    try:
      bstack1l1ll1lll1_opy_ = threading.current_thread().bstackSessionDriver if bstack1lll1l1111_opy_(bstack11llll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ൅")) else context.browser
      bstack1111l1l11_opy_ = (
        (name == bstack11llll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡤࡰࡱ࠭െ") and self.driver_initialised == bstack11llll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠣേ")) or
        (name == bstack11llll_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣ࡫࡫ࡡࡵࡷࡵࡩࠬൈ") and self.driver_initialised == bstack11llll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡦࡦࡣࡷࡹࡷ࡫ࠢ൉")) or
        (name == bstack11llll_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨൊ") and self.driver_initialised in [bstack11llll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥോ"), bstack11llll_opy_ (u"ࠤ࡬ࡲࡸࡺࡥࡱࠤൌ")]) or
        (name == bstack11llll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡸࡪࡶ്ࠧ") and self.driver_initialised == bstack11llll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠤൎ"))
      )
      if bstack1111l1l11_opy_:
        self.driver_initialised = None
        bstack1l1ll1lll1_opy_.quit()
    except Exception:
      pass
def bstack11111l111_opy_(config, startdir):
  return bstack11llll_opy_ (u"ࠧࡪࡲࡪࡸࡨࡶ࠿ࠦࡻ࠱ࡿࠥ൏").format(bstack11llll_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠧ൐"))
notset = Notset()
def bstack1l11ll11l_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack11lll1111_opy_
  if str(name).lower() == bstack11llll_opy_ (u"ࠧࡥࡴ࡬ࡺࡪࡸࠧ൑"):
    return bstack11llll_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢ൒")
  else:
    return bstack11lll1111_opy_(self, name, default, skip)
def bstack1llllll11_opy_(item, when):
  global bstack1l1l1l1l1l_opy_
  try:
    bstack1l1l1l1l1l_opy_(item, when)
  except Exception as e:
    pass
def bstack111l111ll_opy_():
  return
def bstack1l111lll11_opy_(type, name, status, reason, bstack1ll11lll1_opy_, bstack1l11l1ll1l_opy_):
  bstack111l11l1l_opy_ = {
    bstack11llll_opy_ (u"ࠩࡤࡧࡹ࡯࡯࡯ࠩ൓"): type,
    bstack11llll_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ൔ"): {}
  }
  if type == bstack11llll_opy_ (u"ࠫࡦࡴ࡮ࡰࡶࡤࡸࡪ࠭ൕ"):
    bstack111l11l1l_opy_[bstack11llll_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨൖ")][bstack11llll_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬൗ")] = bstack1ll11lll1_opy_
    bstack111l11l1l_opy_[bstack11llll_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ൘")][bstack11llll_opy_ (u"ࠨࡦࡤࡸࡦ࠭൙")] = json.dumps(str(bstack1l11l1ll1l_opy_))
  if type == bstack11llll_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ൚"):
    bstack111l11l1l_opy_[bstack11llll_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭൛")][bstack11llll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ൜")] = name
  if type == bstack11llll_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨ൝"):
    bstack111l11l1l_opy_[bstack11llll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ൞")][bstack11llll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧൟ")] = status
    if status == bstack11llll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨൠ"):
      bstack111l11l1l_opy_[bstack11llll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬൡ")][bstack11llll_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪൢ")] = json.dumps(str(reason))
  bstack1l1ll11l11_opy_ = bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩൣ").format(json.dumps(bstack111l11l1l_opy_))
  return bstack1l1ll11l11_opy_
def bstack11l1lll111_opy_(driver_command, response):
    if driver_command == bstack11llll_opy_ (u"ࠬࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠩ൤"):
        bstack1lll11ll_opy_.bstack1ll1lll11_opy_({
            bstack11llll_opy_ (u"࠭ࡩ࡮ࡣࡪࡩࠬ൥"): response[bstack11llll_opy_ (u"ࠧࡷࡣ࡯ࡹࡪ࠭൦")],
            bstack11llll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ൧"): bstack1lll11ll_opy_.current_test_uuid()
        })
def bstack1ll1l11lll_opy_(item, call, rep):
  global bstack11lll1l11_opy_
  global bstack1ll1111111_opy_
  global bstack1lll1ll11_opy_
  name = bstack11llll_opy_ (u"ࠩࠪ൨")
  try:
    if rep.when == bstack11llll_opy_ (u"ࠪࡧࡦࡲ࡬ࠨ൩"):
      bstack1l1l11111_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack1lll1ll11_opy_:
          name = str(rep.nodeid)
          bstack11l1lllll1_opy_ = bstack1l111lll11_opy_(bstack11llll_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ൪"), name, bstack11llll_opy_ (u"ࠬ࠭൫"), bstack11llll_opy_ (u"࠭ࠧ൬"), bstack11llll_opy_ (u"ࠧࠨ൭"), bstack11llll_opy_ (u"ࠨࠩ൮"))
          threading.current_thread().bstack11lll1ll1l_opy_ = name
          for driver in bstack1ll1111111_opy_:
            if bstack1l1l11111_opy_ == driver.session_id:
              driver.execute_script(bstack11l1lllll1_opy_)
      except Exception as e:
        logger.debug(bstack11llll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩ൯").format(str(e)))
      try:
        bstack1ll11llll_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack11llll_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ൰"):
          status = bstack11llll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ൱") if rep.outcome.lower() == bstack11llll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ൲") else bstack11llll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭൳")
          reason = bstack11llll_opy_ (u"ࠧࠨ൴")
          if status == bstack11llll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ൵"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack11llll_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧ൶") if status == bstack11llll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ൷") else bstack11llll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ൸")
          data = name + bstack11llll_opy_ (u"ࠬࠦࡰࡢࡵࡶࡩࡩࠧࠧ൹") if status == bstack11llll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ൺ") else name + bstack11llll_opy_ (u"ࠧࠡࡨࡤ࡭ࡱ࡫ࡤࠢࠢࠪൻ") + reason
          bstack1llll1lll1_opy_ = bstack1l111lll11_opy_(bstack11llll_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪർ"), bstack11llll_opy_ (u"ࠩࠪൽ"), bstack11llll_opy_ (u"ࠪࠫൾ"), bstack11llll_opy_ (u"ࠫࠬൿ"), level, data)
          for driver in bstack1ll1111111_opy_:
            if bstack1l1l11111_opy_ == driver.session_id:
              driver.execute_script(bstack1llll1lll1_opy_)
      except Exception as e:
        logger.debug(bstack11llll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡦࡳࡳࡺࡥࡹࡶࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩ඀").format(str(e)))
  except Exception as e:
    logger.debug(bstack11llll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡶࡸࡦࡺࡥࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࠦࡳࡵࡣࡷࡹࡸࡀࠠࡼࡿࠪඁ").format(str(e)))
  bstack11lll1l11_opy_(item, call, rep)
def bstack11lll111l1_opy_(driver, bstack11llll11ll_opy_, test=None):
  global bstack11l111ll1l_opy_
  if test != None:
    bstack1ll11l11ll_opy_ = getattr(test, bstack11llll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬං"), None)
    bstack1ll1ll1ll_opy_ = getattr(test, bstack11llll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ඃ"), None)
    PercySDK.screenshot(driver, bstack11llll11ll_opy_, bstack1ll11l11ll_opy_=bstack1ll11l11ll_opy_, bstack1ll1ll1ll_opy_=bstack1ll1ll1ll_opy_, bstack1l1ll11l1l_opy_=bstack11l111ll1l_opy_)
  else:
    PercySDK.screenshot(driver, bstack11llll11ll_opy_)
def bstack1111lll1l_opy_(driver):
  if bstack11l1l1l11l_opy_.bstack1l111l11l1_opy_() is True or bstack11l1l1l11l_opy_.capturing() is True:
    return
  bstack11l1l1l11l_opy_.bstack11l11ll1l_opy_()
  while not bstack11l1l1l11l_opy_.bstack1l111l11l1_opy_():
    bstack11l11l1l1_opy_ = bstack11l1l1l11l_opy_.bstack11l111111_opy_()
    bstack11lll111l1_opy_(driver, bstack11l11l1l1_opy_)
  bstack11l1l1l11l_opy_.bstack1111llll1_opy_()
def bstack1l11ll1l1_opy_(sequence, driver_command, response = None, bstack11ll1ll1ll_opy_ = None, args = None):
    try:
      if sequence != bstack11llll_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࠩ඄"):
        return
      if percy.bstack11ll11llll_opy_() == bstack11llll_opy_ (u"ࠥࡪࡦࡲࡳࡦࠤඅ"):
        return
      bstack11l11l1l1_opy_ = bstack1ll111l1_opy_(threading.current_thread(), bstack11llll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧආ"), None)
      for command in bstack111ll11ll_opy_:
        if command == driver_command:
          for driver in bstack1ll1111111_opy_:
            bstack1111lll1l_opy_(driver)
      bstack11l11l111l_opy_ = percy.bstack11111l1l1_opy_()
      if driver_command in bstack1l1llll1l1_opy_[bstack11l11l111l_opy_]:
        bstack11l1l1l11l_opy_.bstack1llll1l1l_opy_(bstack11l11l1l1_opy_, driver_command)
    except Exception as e:
      pass
def bstack1l11lll1ll_opy_(framework_name):
  if bstack1111l1l1_opy_.get_property(bstack11llll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡳ࡯ࡥࡡࡦࡥࡱࡲࡥࡥࠩඇ")):
      return
  bstack1111l1l1_opy_.set_property(bstack11llll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥ࡭ࡰࡦࡢࡧࡦࡲ࡬ࡦࡦࠪඈ"), True)
  global bstack1l1l11llll_opy_
  global bstack11111l11l_opy_
  global bstack1llll1l111_opy_
  bstack1l1l11llll_opy_ = framework_name
  logger.info(bstack11llll111l_opy_.format(bstack1l1l11llll_opy_.split(bstack11llll_opy_ (u"ࠧ࠮ࠩඉ"))[0]))
  bstack1lllllllll_opy_()
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack1l1l1l111_opy_:
      Service.start = bstack1ll1lllll1_opy_
      Service.stop = bstack11llllllll_opy_
      webdriver.Remote.get = bstack11l1111l11_opy_
      WebDriver.close = bstack11l1ll11l1_opy_
      WebDriver.quit = bstack11lllll11l_opy_
      webdriver.Remote.__init__ = bstack1l111ll1l1_opy_
      WebDriver.getAccessibilityResults = getAccessibilityResults
      WebDriver.get_accessibility_results = getAccessibilityResults
      WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
      WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
      WebDriver.performScan = perform_scan
      WebDriver.perform_scan = perform_scan
    if not bstack1l1l1l111_opy_:
        webdriver.Remote.__init__ = bstack1l11l1l11_opy_
    WebDriver.execute = bstack1ll111l1l1_opy_
    bstack11111l11l_opy_ = True
  except Exception as e:
    pass
  try:
    if bstack1l1l1l111_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack11l1ll1111_opy_
  except Exception as e:
    pass
  bstack1ll1l11l11_opy_()
  if not bstack11111l11l_opy_:
    bstack1ll1l1llll_opy_(bstack11llll_opy_ (u"ࠣࡒࡤࡧࡰࡧࡧࡦࡵࠣࡲࡴࡺࠠࡪࡰࡶࡸࡦࡲ࡬ࡦࡦࠥඊ"), bstack11ll111ll_opy_)
  if bstack1l1l1ll11l_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._1lll1l111l_opy_ = bstack1l11lllll_opy_
    except Exception as e:
      logger.error(bstack1lll1l111_opy_.format(str(e)))
  if bstack11l1lllll_opy_():
    bstack1l11l1ll11_opy_(CONFIG, logger)
  if (bstack11llll_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨඋ") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        if percy.bstack11ll11llll_opy_() == bstack11llll_opy_ (u"ࠥࡸࡷࡻࡥࠣඌ"):
          bstack1l1llll11l_opy_(bstack1l11ll1l1_opy_)
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1llll1111l_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack11lllll111_opy_
      except Exception as e:
        logger.warn(bstack1ll1l1111_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import bstack1l1ll1llll_opy_
        bstack1l1ll1llll_opy_.close = bstack11l11l111_opy_
      except Exception as e:
        logger.debug(bstack11l1l11111_opy_ + str(e))
    except Exception as e:
      bstack1ll1l1llll_opy_(e, bstack1ll1l1111_opy_)
    Output.start_test = bstack1l1l11111l_opy_
    Output.end_test = bstack1lllll11l1_opy_
    TestStatus.__init__ = bstack11l11l11l1_opy_
    QueueItem.__init__ = bstack11l111111l_opy_
    pabot._create_items = bstack1l111111l_opy_
    try:
      from pabot import __version__ as bstack111l1l11l_opy_
      if version.parse(bstack111l1l11l_opy_) >= version.parse(bstack11llll_opy_ (u"ࠫ࠷࠴࠱࠶࠰࠳ࠫඍ")):
        pabot._run = bstack11lllll1l1_opy_
      elif version.parse(bstack111l1l11l_opy_) >= version.parse(bstack11llll_opy_ (u"ࠬ࠸࠮࠲࠵࠱࠴ࠬඎ")):
        pabot._run = bstack11llll1ll_opy_
      else:
        pabot._run = bstack1l1l11l1l1_opy_
    except Exception as e:
      pabot._run = bstack1l1l11l1l1_opy_
    pabot._create_command_for_execution = bstack1111ll111_opy_
    pabot._report_results = bstack1ll1lll1l_opy_
  if bstack11llll_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ඏ") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1ll1l1llll_opy_(e, bstack1l1l1111ll_opy_)
    Runner.run_hook = bstack1lll111111_opy_
    Step.run = bstack1lll1111l1_opy_
  if bstack11llll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧඐ") in str(framework_name).lower():
    if not bstack1l1l1l111_opy_:
      return
    try:
      if percy.bstack11ll11llll_opy_() == bstack11llll_opy_ (u"ࠣࡶࡵࡹࡪࠨඑ"):
          bstack1l1llll11l_opy_(bstack1l11ll1l1_opy_)
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack11111l111_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack111l111ll_opy_
      Config.getoption = bstack1l11ll11l_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack1ll1l11lll_opy_
    except Exception as e:
      pass
def bstack1lll1lllll_opy_():
  global CONFIG
  if bstack11llll_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩඒ") in CONFIG and int(CONFIG[bstack11llll_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪඓ")]) > 1:
    logger.warn(bstack11lll1l1l1_opy_)
def bstack1lllll1l11_opy_(arg, bstack11l11111_opy_, bstack1ll1l11l1l_opy_=None):
  global CONFIG
  global bstack111l11l11_opy_
  global bstack11l111lll_opy_
  global bstack1l1l1l111_opy_
  global bstack1111l1l1_opy_
  bstack1lll1l11l1_opy_ = bstack11llll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫඔ")
  if bstack11l11111_opy_ and isinstance(bstack11l11111_opy_, str):
    bstack11l11111_opy_ = eval(bstack11l11111_opy_)
  CONFIG = bstack11l11111_opy_[bstack11llll_opy_ (u"ࠬࡉࡏࡏࡈࡌࡋࠬඕ")]
  bstack111l11l11_opy_ = bstack11l11111_opy_[bstack11llll_opy_ (u"࠭ࡈࡖࡄࡢ࡙ࡗࡒࠧඖ")]
  bstack11l111lll_opy_ = bstack11l11111_opy_[bstack11llll_opy_ (u"ࠧࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩ඗")]
  bstack1l1l1l111_opy_ = bstack11l11111_opy_[bstack11llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫ඘")]
  bstack1111l1l1_opy_.set_property(bstack11llll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪ඙"), bstack1l1l1l111_opy_)
  os.environ[bstack11llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬක")] = bstack1lll1l11l1_opy_
  os.environ[bstack11llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࠪඛ")] = json.dumps(CONFIG)
  os.environ[bstack11llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡍ࡛ࡂࡠࡗࡕࡐࠬග")] = bstack111l11l11_opy_
  os.environ[bstack11llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧඝ")] = str(bstack11l111lll_opy_)
  os.environ[bstack11llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐ࡚ࡖࡈࡗ࡙ࡥࡐࡍࡗࡊࡍࡓ࠭ඞ")] = str(True)
  if bstack1ll1ll11ll_opy_(arg, [bstack11llll_opy_ (u"ࠨ࠯ࡱࠫඟ"), bstack11llll_opy_ (u"ࠩ࠰࠱ࡳࡻ࡭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪච")]) != -1:
    os.environ[bstack11llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓ࡝࡙ࡋࡓࡕࡡࡓࡅࡗࡇࡌࡍࡇࡏࠫඡ")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack11111111l_opy_)
    return
  bstack1l1ll1l111_opy_()
  global bstack11lll11ll1_opy_
  global bstack11l111ll1l_opy_
  global bstack11ll1111l1_opy_
  global bstack1l1l11lll_opy_
  global bstack1ll1ll111_opy_
  global bstack1llll1l111_opy_
  global bstack1l111l1l11_opy_
  arg.append(bstack11llll_opy_ (u"ࠦ࠲࡝ࠢජ"))
  arg.append(bstack11llll_opy_ (u"ࠧ࡯ࡧ࡯ࡱࡵࡩ࠿ࡓ࡯ࡥࡷ࡯ࡩࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡩ࡮ࡲࡲࡶࡹ࡫ࡤ࠻ࡲࡼࡸࡪࡹࡴ࠯ࡒࡼࡸࡪࡹࡴࡘࡣࡵࡲ࡮ࡴࡧࠣඣ"))
  arg.append(bstack11llll_opy_ (u"ࠨ࠭ࡘࠤඤ"))
  arg.append(bstack11llll_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡫࠺ࡕࡪࡨࠤ࡭ࡵ࡯࡬࡫ࡰࡴࡱࠨඥ"))
  global bstack11l1l1lll1_opy_
  global bstack1lll11ll11_opy_
  global bstack1llll1llll_opy_
  global bstack111l11lll_opy_
  global bstack1ll1llll11_opy_
  global bstack1l1111lll_opy_
  global bstack11ll1l1l11_opy_
  global bstack1ll1111l1l_opy_
  global bstack1l11llll1l_opy_
  global bstack11l1ll111_opy_
  global bstack11lll1111_opy_
  global bstack1l1l1l1l1l_opy_
  global bstack11lll1l11_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack11l1l1lll1_opy_ = webdriver.Remote.__init__
    bstack1lll11ll11_opy_ = WebDriver.quit
    bstack1ll1111l1l_opy_ = WebDriver.close
    bstack1l11llll1l_opy_ = WebDriver.get
    bstack1llll1llll_opy_ = WebDriver.execute
  except Exception as e:
    pass
  if bstack11lll1l1ll_opy_(CONFIG) and bstack1l1ll11ll_opy_():
    if bstack111l1111l_opy_() < version.parse(bstack1ll11llll1_opy_):
      logger.error(bstack1ll1l1ll1_opy_.format(bstack111l1111l_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack11l1ll111_opy_ = RemoteConnection._1lll1l111l_opy_
      except Exception as e:
        logger.error(bstack1lll1l111_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack11lll1111_opy_ = Config.getoption
    from _pytest import runner
    bstack1l1l1l1l1l_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warn(e, bstack1111l11l_opy_)
  try:
    from pytest_bdd import reporting
    bstack11lll1l11_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack11llll_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡰࠢࡵࡹࡳࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡪࡹࡴࡴࠩඦ"))
  bstack11ll1111l1_opy_ = CONFIG.get(bstack11llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ට"), {}).get(bstack11llll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬඨ"))
  bstack1l111l1l11_opy_ = True
  if cli.is_enabled(CONFIG):
    if cli.bstack11llllll1_opy_():
      bstack1lll1ll11l_opy_.invoke(Events.CONNECT, bstack11lllll11_opy_())
    platform_index = int(os.environ.get(bstack11llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫඩ"), bstack11llll_opy_ (u"ࠬ࠶ࠧඪ")))
  else:
    bstack1l11lll1ll_opy_(bstack11l1111l1_opy_)
  os.environ[bstack11llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠧණ")] = CONFIG[bstack11llll_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩඬ")]
  os.environ[bstack11llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡌࡇ࡜ࠫත")] = CONFIG[bstack11llll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬථ")]
  os.environ[bstack11llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓ࠭ද")] = bstack1l1l1l111_opy_.__str__()
  from _pytest.config import main as bstack11l1ll1lll_opy_
  bstack11ll1ll11_opy_ = []
  try:
    bstack11ll11l11l_opy_ = bstack11l1ll1lll_opy_(arg)
    if cli.is_enabled(CONFIG):
      cli.bstack1l111l11ll_opy_()
    if bstack11llll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴࠨධ") in multiprocessing.current_process().__dict__.keys():
      for bstack1l11111ll_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack11ll1ll11_opy_.append(bstack1l11111ll_opy_)
    try:
      bstack1lll1l1l1_opy_ = (bstack11ll1ll11_opy_, int(bstack11ll11l11l_opy_))
      bstack1ll1l11l1l_opy_.append(bstack1lll1l1l1_opy_)
    except:
      bstack1ll1l11l1l_opy_.append((bstack11ll1ll11_opy_, bstack11ll11l11l_opy_))
  except Exception as e:
    logger.error(traceback.format_exc())
    bstack11ll1ll11_opy_.append({bstack11llll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪන"): bstack11llll_opy_ (u"࠭ࡐࡳࡱࡦࡩࡸࡹࠠࠨ඲") + os.environ.get(bstack11llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧඳ")), bstack11llll_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧප"): traceback.format_exc(), bstack11llll_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨඵ"): int(os.environ.get(bstack11llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪබ")))})
    bstack1ll1l11l1l_opy_.append((bstack11ll1ll11_opy_, 1))
def bstack1l11l11l1l_opy_(arg):
  global bstack1l111ll1ll_opy_
  bstack1l11lll1ll_opy_(bstack1111ll1l1_opy_)
  os.environ[bstack11llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬභ")] = str(bstack11l111lll_opy_)
  from behave.__main__ import main as bstack1lll1ll1l1_opy_
  status_code = bstack1lll1ll1l1_opy_(arg)
  if status_code != 0:
    bstack1l111ll1ll_opy_ = status_code
def bstack11l1l1l11_opy_():
  logger.info(bstack1ll1l111l_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack11llll_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫම"), help=bstack11llll_opy_ (u"࠭ࡇࡦࡰࡨࡶࡦࡺࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡤࡱࡱࡪ࡮࡭ࠧඹ"))
  parser.add_argument(bstack11llll_opy_ (u"ࠧ࠮ࡷࠪය"), bstack11llll_opy_ (u"ࠨ࠯࠰ࡹࡸ࡫ࡲ࡯ࡣࡰࡩࠬර"), help=bstack11llll_opy_ (u"ࠩ࡜ࡳࡺࡸࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡵࡴࡧࡵࡲࡦࡳࡥࠨ඼"))
  parser.add_argument(bstack11llll_opy_ (u"ࠪ࠱ࡰ࠭ල"), bstack11llll_opy_ (u"ࠫ࠲࠳࡫ࡦࡻࠪ඾"), help=bstack11llll_opy_ (u"ࠬ࡟࡯ࡶࡴࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡤࡧࡨ࡫ࡳࡴࠢ࡮ࡩࡾ࠭඿"))
  parser.add_argument(bstack11llll_opy_ (u"࠭࠭ࡧࠩව"), bstack11llll_opy_ (u"ࠧ࠮࠯ࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬශ"), help=bstack11llll_opy_ (u"ࠨ࡛ࡲࡹࡷࠦࡴࡦࡵࡷࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧෂ"))
  bstack1l11l1llll_opy_ = parser.parse_args()
  try:
    bstack11ll1l1ll_opy_ = bstack11llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡩࡨࡲࡪࡸࡩࡤ࠰ࡼࡱࡱ࠴ࡳࡢ࡯ࡳࡰࡪ࠭ස")
    if bstack1l11l1llll_opy_.framework and bstack1l11l1llll_opy_.framework not in (bstack11llll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪහ"), bstack11llll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠷ࠬළ")):
      bstack11ll1l1ll_opy_ = bstack11llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠮ࡺ࡯࡯࠲ࡸࡧ࡭ࡱ࡮ࡨࠫෆ")
    bstack1ll1llll1l_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11ll1l1ll_opy_)
    bstack11llllll1l_opy_ = open(bstack1ll1llll1l_opy_, bstack11llll_opy_ (u"࠭ࡲࠨ෇"))
    bstack1l1lll11l_opy_ = bstack11llllll1l_opy_.read()
    bstack11llllll1l_opy_.close()
    if bstack1l11l1llll_opy_.username:
      bstack1l1lll11l_opy_ = bstack1l1lll11l_opy_.replace(bstack11llll_opy_ (u"࡚ࠧࡑࡘࡖࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠧ෈"), bstack1l11l1llll_opy_.username)
    if bstack1l11l1llll_opy_.key:
      bstack1l1lll11l_opy_ = bstack1l1lll11l_opy_.replace(bstack11llll_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪ෉"), bstack1l11l1llll_opy_.key)
    if bstack1l11l1llll_opy_.framework:
      bstack1l1lll11l_opy_ = bstack1l1lll11l_opy_.replace(bstack11llll_opy_ (u"ࠩ࡜ࡓ࡚ࡘ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍ්ࠪ"), bstack1l11l1llll_opy_.framework)
    file_name = bstack11llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭෋")
    file_path = os.path.abspath(file_name)
    bstack1l1111l111_opy_ = open(file_path, bstack11llll_opy_ (u"ࠫࡼ࠭෌"))
    bstack1l1111l111_opy_.write(bstack1l1lll11l_opy_)
    bstack1l1111l111_opy_.close()
    logger.info(bstack1111l11l1_opy_)
    try:
      os.environ[bstack11llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧ෍")] = bstack1l11l1llll_opy_.framework if bstack1l11l1llll_opy_.framework != None else bstack11llll_opy_ (u"ࠨࠢ෎")
      config = yaml.safe_load(bstack1l1lll11l_opy_)
      config[bstack11llll_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧා")] = bstack11llll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡵࡨࡸࡺࡶࠧැ")
      bstack1l1l111l11_opy_(bstack111lllll1_opy_, config)
    except Exception as e:
      logger.debug(bstack11111lll1_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack1l11l1l11l_opy_.format(str(e)))
def bstack1l1l111l11_opy_(bstack1lll111l1l_opy_, config, bstack1lll1l1ll_opy_={}):
  global bstack1l1l1l111_opy_
  global bstack11ll111ll1_opy_
  global bstack1111l1l1_opy_
  if not config:
    return
  bstack11l111ll11_opy_ = bstack11l111l1l1_opy_ if not bstack1l1l1l111_opy_ else (
    bstack1l11l1lll_opy_ if bstack11llll_opy_ (u"ࠩࡤࡴࡵ࠭ෑ") in config else (
        bstack11l11llll_opy_ if config.get(bstack11llll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧි")) else bstack11l111l111_opy_
    )
)
  bstack1l1lll1l1_opy_ = False
  bstack1l1ll1ll1l_opy_ = False
  if bstack1l1l1l111_opy_ is True:
      if bstack11llll_opy_ (u"ࠫࡦࡶࡰࠨී") in config:
          bstack1l1lll1l1_opy_ = True
      else:
          bstack1l1ll1ll1l_opy_ = True
  bstack111111111_opy_ = bstack1lllll111l_opy_.bstack11ll1111ll_opy_(config, bstack11ll111ll1_opy_)
  data = {
    bstack11llll_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧු"): config[bstack11llll_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ෕")],
    bstack11llll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪූ"): config[bstack11llll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ෗")],
    bstack11llll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ෘ"): bstack1lll111l1l_opy_,
    bstack11llll_opy_ (u"ࠪࡨࡪࡺࡥࡤࡶࡨࡨࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠧෙ"): os.environ.get(bstack11llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭ේ"), bstack11ll111ll1_opy_),
    bstack11llll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧෛ"): bstack111llll1l_opy_,
    bstack11llll_opy_ (u"࠭࡯ࡱࡶ࡬ࡱࡦࡲ࡟ࡩࡷࡥࡣࡺࡸ࡬ࠨො"): bstack1ll1lll11l_opy_(),
    bstack11llll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪෝ"): {
      bstack11llll_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ෞ"): str(config[bstack11llll_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩෟ")]) if bstack11llll_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪ෠") in config else bstack11llll_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࠧ෡"),
      bstack11llll_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫ࡖࡦࡴࡶ࡭ࡴࡴࠧ෢"): sys.version,
      bstack11llll_opy_ (u"࠭ࡲࡦࡨࡨࡶࡷ࡫ࡲࠨ෣"): bstack1l111111ll_opy_(os.getenv(bstack11llll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠤ෤"), bstack11llll_opy_ (u"ࠣࠤ෥"))),
      bstack11llll_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨࠫ෦"): bstack11llll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ෧"),
      bstack11llll_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࠬ෨"): bstack11l111ll11_opy_,
      bstack11llll_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹࡥ࡭ࡢࡲࠪ෩"): bstack111111111_opy_,
      bstack11llll_opy_ (u"࠭ࡴࡦࡵࡷ࡬ࡺࡨ࡟ࡶࡷ࡬ࡨࠬ෪"): os.environ[bstack11llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ෫")],
      bstack11llll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࡚ࡪࡸࡳࡪࡱࡱࠫ෬"): bstack11l1ll1l1_opy_(os.environ.get(bstack11llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫ෭"), bstack11ll111ll1_opy_)),
      bstack11llll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭෮"): config[bstack11llll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ෯")] if config[bstack11llll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ෰")] else bstack11llll_opy_ (u"ࠨࡵ࡯࡭ࡱࡳࡼࡴࠢ෱"),
      bstack11llll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩෲ"): str(config[bstack11llll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪෳ")]) if bstack11llll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ෴") in config else bstack11llll_opy_ (u"ࠥࡹࡳࡱ࡮ࡰࡹࡱࠦ෵"),
      bstack11llll_opy_ (u"ࠫࡴࡹࠧ෶"): sys.platform,
      bstack11llll_opy_ (u"ࠬ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠧ෷"): socket.gethostname(),
      bstack11llll_opy_ (u"࠭ࡳࡥ࡭ࡕࡹࡳࡏࡤࠨ෸"): bstack1111l1l1_opy_.get_property(bstack11llll_opy_ (u"ࠧࡴࡦ࡮ࡖࡺࡴࡉࡥࠩ෹"))
    }
  }
  if not bstack1111l1l1_opy_.get_property(bstack11llll_opy_ (u"ࠨࡵࡧ࡯ࡐ࡯࡬࡭ࡕ࡬࡫ࡳࡧ࡬ࠨ෺")) is None:
    data[bstack11llll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬ෻")][bstack11llll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡒ࡫ࡴࡢࡦࡤࡸࡦ࠭෼")] = {
      bstack11llll_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫ෽"): bstack11llll_opy_ (u"ࠬࡻࡳࡦࡴࡢ࡯࡮ࡲ࡬ࡦࡦࠪ෾"),
      bstack11llll_opy_ (u"࠭ࡳࡪࡩࡱࡥࡱ࠭෿"): bstack1111l1l1_opy_.get_property(bstack11llll_opy_ (u"ࠧࡴࡦ࡮ࡏ࡮ࡲ࡬ࡔ࡫ࡪࡲࡦࡲࠧ฀")),
      bstack11llll_opy_ (u"ࠨࡵ࡬࡫ࡳࡧ࡬ࡏࡷࡰࡦࡪࡸࠧก"): bstack1111l1l1_opy_.get_property(bstack11llll_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡑࡳࠬข"))
    }
  if bstack1lll111l1l_opy_ == bstack1l11111ll1_opy_:
    data[bstack11llll_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡳࡶࡴࡶࡥࡳࡶ࡬ࡩࡸ࠭ฃ")][bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡆࡳࡳ࡬ࡩࡨࠩค")] = bstack11l111l11l_opy_(config)
    data[bstack11llll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠨฅ")][bstack11llll_opy_ (u"࠭ࡩࡴࡒࡨࡶࡨࡿࡁࡶࡶࡲࡉࡳࡧࡢ࡭ࡧࡧࠫฆ")] = percy.bstack1ll11ll1l1_opy_
    data[bstack11llll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪง")][bstack11llll_opy_ (u"ࠨࡲࡨࡶࡨࡿࡂࡶ࡫࡯ࡨࡎࡪࠧจ")] = percy.bstack11l1l1l1l_opy_
  update(data[bstack11llll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬฉ")], bstack1lll1l1ll_opy_)
  try:
    response = bstack1l1111l1l_opy_(bstack11llll_opy_ (u"ࠪࡔࡔ࡙ࡔࠨช"), bstack11l1ll11l_opy_(bstack11l11l1ll_opy_), data, {
      bstack11llll_opy_ (u"ࠫࡦࡻࡴࡩࠩซ"): (config[bstack11llll_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧฌ")], config[bstack11llll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩญ")])
    })
    if response:
      logger.debug(bstack1ll11l1l11_opy_.format(bstack1lll111l1l_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack1lll11l1ll_opy_.format(str(e)))
def bstack1l111111ll_opy_(framework):
  return bstack11llll_opy_ (u"ࠢࡼࡿ࠰ࡴࡾࡺࡨࡰࡰࡤ࡫ࡪࡴࡴ࠰ࡽࢀࠦฎ").format(str(framework), __version__) if framework else bstack11llll_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࡻࡾࠤฏ").format(
    __version__)
def bstack1l1ll1l111_opy_():
  global CONFIG
  global bstack1ll1l1ll1l_opy_
  if bool(CONFIG):
    return
  try:
    bstack1ll1ll1lll_opy_()
    logger.debug(bstack1ll11111l1_opy_.format(str(CONFIG)))
    bstack1ll1l1ll1l_opy_ = bstack1ll1l1l1l1_opy_.bstack1l1111111l_opy_(CONFIG, bstack1ll1l1ll1l_opy_)
    bstack1lllllllll_opy_()
  except Exception as e:
    logger.error(bstack11llll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࡷࡳ࠰ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࠨฐ") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1llllll1l_opy_
  atexit.register(bstack11l11l1l1l_opy_)
  signal.signal(signal.SIGINT, bstack1l111lll1l_opy_)
  signal.signal(signal.SIGTERM, bstack1l111lll1l_opy_)
def bstack1llllll1l_opy_(exctype, value, traceback):
  global bstack1ll1111111_opy_
  try:
    for driver in bstack1ll1111111_opy_:
      bstack11l11l11ll_opy_(driver, bstack11llll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪฑ"), bstack11llll_opy_ (u"ࠦࡘ࡫ࡳࡴ࡫ࡲࡲࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪ࠽ࠤࡡࡴࠢฒ") + str(value))
  except Exception:
    pass
  logger.info(bstack1l1111111_opy_)
  bstack11ll1l1ll1_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack11ll1l1ll1_opy_(message=bstack11llll_opy_ (u"ࠬ࠭ณ"), bstack1lllll1ll_opy_ = False):
  global CONFIG
  bstack1l1111l11_opy_ = bstack11llll_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠨด") if bstack1lllll1ll_opy_ else bstack11llll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ต")
  try:
    if message:
      bstack1lll1l1ll_opy_ = {
        bstack1l1111l11_opy_ : str(message)
      }
      bstack1l1l111l11_opy_(bstack1l11111ll1_opy_, CONFIG, bstack1lll1l1ll_opy_)
    else:
      bstack1l1l111l11_opy_(bstack1l11111ll1_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack1llll111l_opy_.format(str(e)))
def bstack1l11llllll_opy_(bstack1lll1ll1ll_opy_, size):
  bstack1l1lll11l1_opy_ = []
  while len(bstack1lll1ll1ll_opy_) > size:
    bstack11l1l11l11_opy_ = bstack1lll1ll1ll_opy_[:size]
    bstack1l1lll11l1_opy_.append(bstack11l1l11l11_opy_)
    bstack1lll1ll1ll_opy_ = bstack1lll1ll1ll_opy_[size:]
  bstack1l1lll11l1_opy_.append(bstack1lll1ll1ll_opy_)
  return bstack1l1lll11l1_opy_
def bstack111l11ll1_opy_(args):
  if bstack11llll_opy_ (u"ࠨ࠯ࡰࠫถ") in args and bstack11llll_opy_ (u"ࠩࡳࡨࡧ࠭ท") in args:
    return True
  return False
def run_on_browserstack(bstack1ll1ll1ll1_opy_=None, bstack1ll1l11l1l_opy_=None, bstack1lll111l1_opy_=False):
  global CONFIG
  global bstack111l11l11_opy_
  global bstack11l111lll_opy_
  global bstack11ll111ll1_opy_
  global bstack1111l1l1_opy_
  bstack1lll1l11l1_opy_ = bstack11llll_opy_ (u"ࠪࠫธ")
  bstack1llll1l1l1_opy_(bstack1111111ll_opy_, logger)
  if bstack1ll1ll1ll1_opy_ and isinstance(bstack1ll1ll1ll1_opy_, str):
    bstack1ll1ll1ll1_opy_ = eval(bstack1ll1ll1ll1_opy_)
  if bstack1ll1ll1ll1_opy_:
    CONFIG = bstack1ll1ll1ll1_opy_[bstack11llll_opy_ (u"ࠫࡈࡕࡎࡇࡋࡊࠫน")]
    bstack111l11l11_opy_ = bstack1ll1ll1ll1_opy_[bstack11llll_opy_ (u"ࠬࡎࡕࡃࡡࡘࡖࡑ࠭บ")]
    bstack11l111lll_opy_ = bstack1ll1ll1ll1_opy_[bstack11llll_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨป")]
    bstack1111l1l1_opy_.set_property(bstack11llll_opy_ (u"ࠧࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩผ"), bstack11l111lll_opy_)
    bstack1lll1l11l1_opy_ = bstack11llll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨฝ")
  bstack1111l1l1_opy_.set_property(bstack11llll_opy_ (u"ࠩࡶࡨࡰࡘࡵ࡯ࡋࡧࠫพ"), uuid4().__str__())
  logger.debug(bstack11llll_opy_ (u"ࠪࡷࡩࡱࡒࡶࡰࡌࡨࡂ࠭ฟ") + bstack1111l1l1_opy_.get_property(bstack11llll_opy_ (u"ࠫࡸࡪ࡫ࡓࡷࡱࡍࡩ࠭ภ")))
  if not bstack1lll111l1_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack11111111l_opy_)
      return
    if sys.argv[1] == bstack11llll_opy_ (u"ࠬ࠳࠭ࡷࡧࡵࡷ࡮ࡵ࡮ࠨม") or sys.argv[1] == bstack11llll_opy_ (u"࠭࠭ࡷࠩย"):
      logger.info(bstack11llll_opy_ (u"ࠧࡃࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡐࡺࡶ࡫ࡳࡳࠦࡓࡅࡍࠣࡺࢀࢃࠧร").format(__version__))
      return
    if sys.argv[1] == bstack11llll_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧฤ"):
      bstack11l1l1l11_opy_()
      return
  args = sys.argv
  bstack1l1ll1l111_opy_()
  global bstack11lll11ll1_opy_
  global bstack1lll111lll_opy_
  global bstack1l111l1l11_opy_
  global bstack1l1l11lll1_opy_
  global bstack11l111ll1l_opy_
  global bstack11ll1111l1_opy_
  global bstack1l1l11lll_opy_
  global bstack1llll1ll1l_opy_
  global bstack1ll1ll111_opy_
  global bstack1llll1l111_opy_
  global bstack11llll1lll_opy_
  bstack1lll111lll_opy_ = len(CONFIG.get(bstack11llll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬล"), []))
  if not bstack1lll1l11l1_opy_:
    if args[1] == bstack11llll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪฦ") or args[1] == bstack11llll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠷ࠬว"):
      bstack1lll1l11l1_opy_ = bstack11llll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬศ")
      args = args[2:]
    elif args[1] == bstack11llll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬษ"):
      bstack1lll1l11l1_opy_ = bstack11llll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ส")
      args = args[2:]
    elif args[1] == bstack11llll_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧห"):
      bstack1lll1l11l1_opy_ = bstack11llll_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨฬ")
      args = args[2:]
    elif args[1] == bstack11llll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫอ"):
      bstack1lll1l11l1_opy_ = bstack11llll_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬฮ")
      args = args[2:]
    elif args[1] == bstack11llll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬฯ"):
      bstack1lll1l11l1_opy_ = bstack11llll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ะ")
      args = args[2:]
    elif args[1] == bstack11llll_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧั"):
      bstack1lll1l11l1_opy_ = bstack11llll_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨา")
      args = args[2:]
    else:
      if not bstack11llll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬำ") in CONFIG or str(CONFIG[bstack11llll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ิ")]).lower() in [bstack11llll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫี"), bstack11llll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠸࠭ึ")]:
        bstack1lll1l11l1_opy_ = bstack11llll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ื")
        args = args[1:]
      elif str(CONFIG[bstack11llll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ุࠪ")]).lower() == bstack11llll_opy_ (u"ࠨࡴࡲࡦࡴࡺูࠧ"):
        bstack1lll1l11l1_opy_ = bstack11llll_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨฺ")
        args = args[1:]
      elif str(CONFIG[bstack11llll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭฻")]).lower() == bstack11llll_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪ฼"):
        bstack1lll1l11l1_opy_ = bstack11llll_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ฽")
        args = args[1:]
      elif str(CONFIG[bstack11llll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ฾")]).lower() == bstack11llll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ฿"):
        bstack1lll1l11l1_opy_ = bstack11llll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨเ")
        args = args[1:]
      elif str(CONFIG[bstack11llll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬแ")]).lower() == bstack11llll_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪโ"):
        bstack1lll1l11l1_opy_ = bstack11llll_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫใ")
        args = args[1:]
      else:
        os.environ[bstack11llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧไ")] = bstack1lll1l11l1_opy_
        bstack1ll1l1lll_opy_(bstack1ll11l11l_opy_)
  os.environ[bstack11llll_opy_ (u"࠭ࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࡡࡘࡗࡊࡊࠧๅ")] = bstack1lll1l11l1_opy_
  bstack11ll111ll1_opy_ = bstack1lll1l11l1_opy_
  if cli.is_enabled(CONFIG):
    bstack1ll1ll11l1_opy_ = bstack11llll_opy_ (u"ࠧࡼ࠲ࢀ࠱ࡨࡻࡣࡶ࡯ࡥࡩࡷ࠭ๆ").format(bstack1lll1l11l1_opy_) if bstack1lll1l11l1_opy_ == bstack11llll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ็") and bstack1l1lll1l1l_opy_() else bstack1lll1l11l1_opy_
    bstack1lll1ll11l_opy_.invoke(Events.bstack11lllll1ll_opy_, bstack11lll1111l_opy_(
      sdk_version=__version__,
      path_config=bstack11llll1l1l_opy_(),
      path_project=os.getcwd(),
      test_framework=bstack1lll1l11l1_opy_,
      frameworks=[bstack1ll1ll11l1_opy_],
      framework_versions={
        bstack1ll1ll11l1_opy_: bstack11l1ll1l1_opy_(bstack11llll_opy_ (u"ࠩࡕࡳࡧࡵࡴࠨ่") if bstack1lll1l11l1_opy_ in [bstack11llll_opy_ (u"ࠪࡴࡦࡨ࡯ࡵ้ࠩ"), bstack11llll_opy_ (u"ࠫࡷࡵࡢࡰࡶ๊ࠪ"), bstack11llll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ๋࠭")] else bstack1lll1l11l1_opy_)
      },
      bs_config=CONFIG
    ))
    CONFIG[bstack11llll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠣ์")] = cli.config[bstack11llll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠤํ")]
    if bstack11l111lll_opy_:
      CONFIG[bstack11llll_opy_ (u"ࠣࡣࡳࡴࠧ๎")] = cli.config[bstack11llll_opy_ (u"ࠤࡤࡴࡵࠨ๏")]
      logger.info(bstack1ll111ll1_opy_.format(CONFIG[bstack11llll_opy_ (u"ࠪࡥࡵࡶࠧ๐")]))
  else:
    bstack1lll1ll11l_opy_.clear()
  global bstack11ll1llll_opy_
  global bstack1lll11l1l1_opy_
  if bstack1ll1ll1ll1_opy_:
    try:
      bstack111l1l1l1_opy_ = datetime.datetime.now()
      os.environ[bstack11llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭๑")] = bstack1lll1l11l1_opy_
      bstack1l1l111l11_opy_(bstack1l111lll1_opy_, CONFIG)
      cli.bstack1ll1l1l11l_opy_(bstack11llll_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽ࡷࡩࡱ࡟ࡵࡧࡶࡸࡤࡧࡴࡵࡧࡰࡴࡹ࡫ࡤࠣ๒"), datetime.datetime.now() - bstack111l1l1l1_opy_)
    except Exception as e:
      logger.debug(bstack111l111l1_opy_.format(str(e)))
  global bstack11l1l1lll1_opy_
  global bstack1lll11ll11_opy_
  global bstack1ll11l111_opy_
  global bstack1lll1lll1_opy_
  global bstack11ll1ll1l1_opy_
  global bstack11ll1l11l1_opy_
  global bstack111l11lll_opy_
  global bstack1ll1llll11_opy_
  global bstack11l1lll1ll_opy_
  global bstack1l1111lll_opy_
  global bstack11ll1l1l11_opy_
  global bstack1ll1111l1l_opy_
  global bstack1l1l1l1ll1_opy_
  global bstack1lll1l11ll_opy_
  global bstack1l11llll1l_opy_
  global bstack11l1ll111_opy_
  global bstack11lll1111_opy_
  global bstack1l1l1l1l1l_opy_
  global bstack1l1111l1l1_opy_
  global bstack11lll1l11_opy_
  global bstack1llll1llll_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack11l1l1lll1_opy_ = webdriver.Remote.__init__
    bstack1lll11ll11_opy_ = WebDriver.quit
    bstack1ll1111l1l_opy_ = WebDriver.close
    bstack1l11llll1l_opy_ = WebDriver.get
    bstack1llll1llll_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack11ll1llll_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    from bstack_utils.helper import bstack1l11l111l_opy_
    bstack1lll11l1l1_opy_ = bstack1l11l111l_opy_()
  except Exception as e:
    pass
  try:
    global bstack1ll1l111ll_opy_
    from QWeb.keywords import browser
    bstack1ll1l111ll_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack11lll1l1ll_opy_(CONFIG) and bstack1l1ll11ll_opy_():
    if bstack111l1111l_opy_() < version.parse(bstack1ll11llll1_opy_):
      logger.error(bstack1ll1l1ll1_opy_.format(bstack111l1111l_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack11l1ll111_opy_ = RemoteConnection._1lll1l111l_opy_
      except Exception as e:
        logger.error(bstack1lll1l111_opy_.format(str(e)))
  if not CONFIG.get(bstack11llll_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁࡶࡶࡲࡇࡦࡶࡴࡶࡴࡨࡐࡴ࡭ࡳࠨ๓"), False) and not bstack1ll1ll1ll1_opy_:
    logger.info(bstack1l1llllll_opy_)
  if not cli.is_enabled(CONFIG):
    if bstack11llll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ๔") in CONFIG and str(CONFIG[bstack11llll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ๕")]).lower() != bstack11llll_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨ๖"):
      bstack1ll1ll11l_opy_()
    elif bstack1lll1l11l1_opy_ != bstack11llll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ๗") or (bstack1lll1l11l1_opy_ == bstack11llll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ๘") and not bstack1ll1ll1ll1_opy_):
      bstack1lll1111ll_opy_()
  if (bstack1lll1l11l1_opy_ in [bstack11llll_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ๙"), bstack11llll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ๚"), bstack11llll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨ๛")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack1llll1111l_opy_
        bstack11ll1l11l1_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack1ll1l1111_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import bstack1l1ll1llll_opy_
        bstack11ll1ll1l1_opy_ = bstack1l1ll1llll_opy_.close
      except Exception as e:
        logger.debug(bstack11l1l11111_opy_ + str(e))
    except Exception as e:
      bstack1ll1l1llll_opy_(e, bstack1ll1l1111_opy_)
    if bstack1lll1l11l1_opy_ != bstack11llll_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ๜"):
      bstack1ll1ll111l_opy_()
    bstack1ll11l111_opy_ = Output.start_test
    bstack1lll1lll1_opy_ = Output.end_test
    bstack111l11lll_opy_ = TestStatus.__init__
    bstack11l1lll1ll_opy_ = pabot._run
    bstack1l1111lll_opy_ = QueueItem.__init__
    bstack11ll1l1l11_opy_ = pabot._create_command_for_execution
    bstack1l1111l1l1_opy_ = pabot._report_results
  if bstack1lll1l11l1_opy_ == bstack11llll_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ๝"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1ll1l1llll_opy_(e, bstack1l1l1111ll_opy_)
    bstack1l1l1l1ll1_opy_ = Runner.run_hook
    bstack1lll1l11ll_opy_ = Step.run
  if bstack1lll1l11l1_opy_ == bstack11llll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ๞"):
    try:
      from _pytest.config import Config
      bstack11lll1111_opy_ = Config.getoption
      from _pytest import runner
      bstack1l1l1l1l1l_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack1111l11l_opy_)
    try:
      from pytest_bdd import reporting
      bstack11lll1l11_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack11llll_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡳࠥࡸࡵ࡯ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡦࡵࡷࡷࠬ๟"))
  try:
    framework_name = bstack11llll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ๠") if bstack1lll1l11l1_opy_ in [bstack11llll_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬ๡"), bstack11llll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭๢"), bstack11llll_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ๣")] else bstack1l1lllll11_opy_(bstack1lll1l11l1_opy_)
    bstack1l11ll111_opy_ = {
      bstack11llll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࠪ๤"): bstack11llll_opy_ (u"ࠪࡿ࠵ࢃ࠭ࡤࡷࡦࡹࡲࡨࡥࡳࠩ๥").format(framework_name) if bstack1lll1l11l1_opy_ == bstack11llll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ๦") and bstack1l1lll1l1l_opy_() else framework_name,
      bstack11llll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ๧"): bstack11l1ll1l1_opy_(framework_name),
      bstack11llll_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫ๨"): __version__,
      bstack11llll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡹࡸ࡫ࡤࠨ๩"): bstack1lll1l11l1_opy_
    }
    if bstack1lll1l11l1_opy_ in bstack11lll1ll11_opy_:
      if bstack1l1l1l111_opy_ and bstack11llll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ๪") in CONFIG and CONFIG[bstack11llll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ๫")] == True:
        if bstack11llll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ๬") in CONFIG:
          os.environ[bstack11llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬ๭")] = os.getenv(bstack11llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭๮"), json.dumps(CONFIG[bstack11llll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭๯")]))
          CONFIG[bstack11llll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ๰")].pop(bstack11llll_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭๱"), None)
          CONFIG[bstack11llll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ๲")].pop(bstack11llll_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨ๳"), None)
        bstack1l11ll111_opy_[bstack11llll_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ๴")] = {
          bstack11llll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ๵"): bstack11llll_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠨ๶"),
          bstack11llll_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨ๷"): str(bstack111l1111l_opy_())
        }
    if bstack1lll1l11l1_opy_ not in [bstack11llll_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ๸")]:
      bstack1l11l111l1_opy_ = bstack1lll11ll_opy_.launch(CONFIG, bstack1l11ll111_opy_)
  except Exception as e:
    logger.debug(bstack1l1l1ll1l1_opy_.format(bstack11llll_opy_ (u"ࠩࡗࡩࡸࡺࡈࡶࡤࠪ๹"), str(e)))
  if bstack1lll1l11l1_opy_ == bstack11llll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ๺"):
    bstack1l111l1l11_opy_ = True
    if bstack1ll1ll1ll1_opy_ and bstack1lll111l1_opy_:
      bstack11ll1111l1_opy_ = CONFIG.get(bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ๻"), {}).get(bstack11llll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ๼"))
      bstack1l11lll1ll_opy_(bstack1ll11l111l_opy_)
    elif bstack1ll1ll1ll1_opy_:
      bstack11ll1111l1_opy_ = CONFIG.get(bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ๽"), {}).get(bstack11llll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ๾"))
      global bstack1ll1111111_opy_
      try:
        if bstack111l11ll1_opy_(bstack1ll1ll1ll1_opy_[bstack11llll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ๿")]) and multiprocessing.current_process().name == bstack11llll_opy_ (u"ࠩ࠳ࠫ຀"):
          bstack1ll1ll1ll1_opy_[bstack11llll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ກ")].remove(bstack11llll_opy_ (u"ࠫ࠲ࡳࠧຂ"))
          bstack1ll1ll1ll1_opy_[bstack11llll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ຃")].remove(bstack11llll_opy_ (u"࠭ࡰࡥࡤࠪຄ"))
          bstack1ll1ll1ll1_opy_[bstack11llll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ຅")] = bstack1ll1ll1ll1_opy_[bstack11llll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫຆ")][0]
          with open(bstack1ll1ll1ll1_opy_[bstack11llll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬງ")], bstack11llll_opy_ (u"ࠪࡶࠬຈ")) as f:
            file_content = f.read()
          bstack1lll11111l_opy_ = bstack11llll_opy_ (u"ࠦࠧࠨࡦࡳࡱࡰࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡷࡩࡱࠠࡪ࡯ࡳࡳࡷࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡻࡧ࠾ࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢ࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡿ࡫ࠨࡼࡿࠬ࠿ࠥ࡬ࡲࡰ࡯ࠣࡴࡩࡨࠠࡪ࡯ࡳࡳࡷࡺࠠࡑࡦࡥ࠿ࠥࡵࡧࡠࡦࡥࠤࡂࠦࡐࡥࡤ࠱ࡨࡴࡥࡢࡳࡧࡤ࡯ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡧࡩ࡫ࠦ࡭ࡰࡦࡢࡦࡷ࡫ࡡ࡬ࠪࡶࡩࡱ࡬ࠬࠡࡣࡵ࡫࠱ࠦࡴࡦ࡯ࡳࡳࡷࡧࡲࡺࠢࡀࠤ࠵࠯࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡴࡳࡻ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡦࡸࡧࠡ࠿ࠣࡷࡹࡸࠨࡪࡰࡷࠬࡦࡸࡧࠪ࠭࠴࠴࠮ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡪࡾࡣࡦࡲࡷࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡢࡵࠣࡩ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡰࡢࡵࡶࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡲ࡫ࡤࡪࡢࠩࡵࡨࡰ࡫࠲ࡡࡳࡩ࠯ࡸࡪࡳࡰࡰࡴࡤࡶࡾ࠯ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡔࡩࡨ࠮ࡥࡱࡢࡦࠥࡃࠠ࡮ࡱࡧࡣࡧࡸࡥࡢ࡭ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡐࡥࡤ࠱ࡨࡴࡥࡢࡳࡧࡤ࡯ࠥࡃࠠ࡮ࡱࡧࡣࡧࡸࡥࡢ࡭ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡐࡥࡤࠫ࠭࠳ࡹࡥࡵࡡࡷࡶࡦࡩࡥࠩࠫ࡟ࡲࠧࠨࠢຉ").format(str(bstack1ll1ll1ll1_opy_))
          bstack1l1ll11111_opy_ = bstack1lll11111l_opy_ + file_content
          bstack11lll1l111_opy_ = bstack1ll1ll1ll1_opy_[bstack11llll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨຊ")] + bstack11llll_opy_ (u"࠭࡟ࡣࡵࡷࡥࡨࡱ࡟ࡵࡧࡰࡴ࠳ࡶࡹࠨ຋")
          with open(bstack11lll1l111_opy_, bstack11llll_opy_ (u"ࠧࡸࠩຌ")):
            pass
          with open(bstack11lll1l111_opy_, bstack11llll_opy_ (u"ࠣࡹ࠮ࠦຍ")) as f:
            f.write(bstack1l1ll11111_opy_)
          import subprocess
          process_data = subprocess.run([bstack11llll_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯ࠤຎ"), bstack11lll1l111_opy_])
          if os.path.exists(bstack11lll1l111_opy_):
            os.unlink(bstack11lll1l111_opy_)
          os._exit(process_data.returncode)
        else:
          if bstack111l11ll1_opy_(bstack1ll1ll1ll1_opy_[bstack11llll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ຏ")]):
            bstack1ll1ll1ll1_opy_[bstack11llll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧຐ")].remove(bstack11llll_opy_ (u"ࠬ࠳࡭ࠨຑ"))
            bstack1ll1ll1ll1_opy_[bstack11llll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩຒ")].remove(bstack11llll_opy_ (u"ࠧࡱࡦࡥࠫຓ"))
            bstack1ll1ll1ll1_opy_[bstack11llll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫດ")] = bstack1ll1ll1ll1_opy_[bstack11llll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬຕ")][0]
          bstack1l11lll1ll_opy_(bstack1ll11l111l_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack1ll1ll1ll1_opy_[bstack11llll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ຖ")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack11llll_opy_ (u"ࠫࡤࡥ࡮ࡢ࡯ࡨࡣࡤ࠭ທ")] = bstack11llll_opy_ (u"ࠬࡥ࡟࡮ࡣ࡬ࡲࡤࡥࠧຘ")
          mod_globals[bstack11llll_opy_ (u"࠭࡟ࡠࡨ࡬ࡰࡪࡥ࡟ࠨນ")] = os.path.abspath(bstack1ll1ll1ll1_opy_[bstack11llll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪບ")])
          exec(open(bstack1ll1ll1ll1_opy_[bstack11llll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫປ")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack11llll_opy_ (u"ࠩࡆࡥࡺ࡭ࡨࡵࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠩຜ").format(str(e)))
          for driver in bstack1ll1111111_opy_:
            bstack1ll1l11l1l_opy_.append({
              bstack11llll_opy_ (u"ࠪࡲࡦࡳࡥࠨຝ"): bstack1ll1ll1ll1_opy_[bstack11llll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧພ")],
              bstack11llll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫຟ"): str(e),
              bstack11llll_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬຠ"): multiprocessing.current_process().name
            })
            bstack11l11l11ll_opy_(driver, bstack11llll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧມ"), bstack11llll_opy_ (u"ࠣࡕࡨࡷࡸ࡯࡯࡯ࠢࡩࡥ࡮ࡲࡥࡥࠢࡺ࡭ࡹ࡮࠺ࠡ࡞ࡱࠦຢ") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack1ll1111111_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack11l111lll_opy_, CONFIG, logger)
      bstack1l111111l1_opy_()
      bstack1lll1lllll_opy_()
      bstack11l11111_opy_ = {
        bstack11llll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬຣ"): args[0],
        bstack11llll_opy_ (u"ࠪࡇࡔࡔࡆࡊࡉࠪ຤"): CONFIG,
        bstack11llll_opy_ (u"ࠫࡍ࡛ࡂࡠࡗࡕࡐࠬລ"): bstack111l11l11_opy_,
        bstack11llll_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧ຦"): bstack11l111lll_opy_
      }
      percy.bstack1l111l1l1l_opy_()
      if bstack11llll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩວ") in CONFIG:
        bstack111ll111_opy_ = []
        manager = multiprocessing.Manager()
        bstack111l111l_opy_ = manager.list()
        if bstack111l11ll1_opy_(args):
          for index, platform in enumerate(CONFIG[bstack11llll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪຨ")]):
            if index == 0:
              bstack11l11111_opy_[bstack11llll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫຩ")] = args
            bstack111ll111_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack11l11111_opy_, bstack111l111l_opy_)))
        else:
          for index, platform in enumerate(CONFIG[bstack11llll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬສ")]):
            bstack111ll111_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack11l11111_opy_, bstack111l111l_opy_)))
        for t in bstack111ll111_opy_:
          t.start()
        for t in bstack111ll111_opy_:
          t.join()
        bstack1llll1ll1l_opy_ = list(bstack111l111l_opy_)
      else:
        if bstack111l11ll1_opy_(args):
          bstack11l11111_opy_[bstack11llll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ຫ")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack11l11111_opy_,))
          test.start()
          test.join()
        else:
          bstack1l11lll1ll_opy_(bstack1ll11l111l_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack11llll_opy_ (u"ࠫࡤࡥ࡮ࡢ࡯ࡨࡣࡤ࠭ຬ")] = bstack11llll_opy_ (u"ࠬࡥ࡟࡮ࡣ࡬ࡲࡤࡥࠧອ")
          mod_globals[bstack11llll_opy_ (u"࠭࡟ࡠࡨ࡬ࡰࡪࡥ࡟ࠨຮ")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack1lll1l11l1_opy_ == bstack11llll_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ຯ") or bstack1lll1l11l1_opy_ == bstack11llll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧະ"):
    percy.init(bstack11l111lll_opy_, CONFIG, logger)
    percy.bstack1l111l1l1l_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack1ll1l1llll_opy_(e, bstack1ll1l1111_opy_)
    bstack1l111111l1_opy_()
    bstack1l11lll1ll_opy_(bstack1lllll1111_opy_)
    if bstack1l1l1l111_opy_:
      bstack1lll1l1l11_opy_(bstack1lllll1111_opy_, args)
      if bstack11llll_opy_ (u"ࠩ࠰࠱ࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧັ") in args:
        i = args.index(bstack11llll_opy_ (u"ࠪ࠱࠲ࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨາ"))
        args.pop(i)
        args.pop(i)
      if bstack11llll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧຳ") not in CONFIG:
        CONFIG[bstack11llll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨິ")] = [{}]
        bstack1lll111lll_opy_ = 1
      if bstack11lll11ll1_opy_ == 0:
        bstack11lll11ll1_opy_ = 1
      args.insert(0, str(bstack11lll11ll1_opy_))
      args.insert(0, str(bstack11llll_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫີ")))
    if bstack1lll11ll_opy_.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack1ll11l1l1l_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack11l111l1ll_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack11llll_opy_ (u"ࠢࡓࡑࡅࡓ࡙ࡥࡏࡑࡖࡌࡓࡓ࡙ࠢຶ"),
        ).parse_args(bstack1ll11l1l1l_opy_)
        bstack1lll111l11_opy_ = args.index(bstack1ll11l1l1l_opy_[0]) if len(bstack1ll11l1l1l_opy_) > 0 else len(args)
        args.insert(bstack1lll111l11_opy_, str(bstack11llll_opy_ (u"ࠨ࠯࠰ࡰ࡮ࡹࡴࡦࡰࡨࡶࠬື")))
        args.insert(bstack1lll111l11_opy_ + 1, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11llll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡵࡳࡧࡵࡴࡠ࡮࡬ࡷࡹ࡫࡮ࡦࡴ࠱ࡴࡾຸ࠭"))))
        if bstack1lll1lll11_opy_(os.environ.get(bstack11llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࠨູ"))) and str(os.environ.get(bstack11llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࡡࡗࡉࡘ࡚ࡓࠨ຺"), bstack11llll_opy_ (u"ࠬࡴࡵ࡭࡮ࠪົ"))) != bstack11llll_opy_ (u"࠭࡮ࡶ࡮࡯ࠫຼ"):
          for bstack11lll111l_opy_ in bstack11l111l1ll_opy_:
            args.remove(bstack11lll111l_opy_)
          bstack1l1l11ll11_opy_ = os.environ.get(bstack11llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࡤ࡚ࡅࡔࡖࡖࠫຽ")).split(bstack11llll_opy_ (u"ࠨ࠮ࠪ຾"))
          for bstack11l1111111_opy_ in bstack1l1l11ll11_opy_:
            args.append(bstack11l1111111_opy_)
      except Exception as e:
        logger.error(bstack11llll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡢࡶࡷࡥࡨ࡮ࡩ࡯ࡩࠣࡰ࡮ࡹࡴࡦࡰࡨࡶࠥ࡬࡯ࡳࠢࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ࠰ࠣࡉࡷࡸ࡯ࡳࠢ࠰ࠤࠧ຿").format(e))
    pabot.main(args)
  elif bstack1lll1l11l1_opy_ == bstack11llll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫເ"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1ll1l1llll_opy_(e, bstack1ll1l1111_opy_)
    for a in args:
      if bstack11llll_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡔࡑࡇࡔࡇࡑࡕࡑࡎࡔࡄࡆ࡚ࠪແ") in a:
        bstack11l111ll1l_opy_ = int(a.split(bstack11llll_opy_ (u"ࠬࡀࠧໂ"))[1])
      if bstack11llll_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡊࡅࡇࡎࡒࡇࡆࡒࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪໃ") in a:
        bstack11ll1111l1_opy_ = str(a.split(bstack11llll_opy_ (u"ࠧ࠻ࠩໄ"))[1])
      if bstack11llll_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡄࡎࡌࡅࡗࡍࡓࠨ໅") in a:
        bstack1l1l11lll_opy_ = str(a.split(bstack11llll_opy_ (u"ࠩ࠽ࠫໆ"))[1])
    bstack1l11l1lll1_opy_ = None
    if bstack11llll_opy_ (u"ࠪ࠱࠲ࡨࡳࡵࡣࡦ࡯ࡤ࡯ࡴࡦ࡯ࡢ࡭ࡳࡪࡥࡹࠩ໇") in args:
      i = args.index(bstack11llll_opy_ (u"ࠫ࠲࠳ࡢࡴࡶࡤࡧࡰࡥࡩࡵࡧࡰࡣ࡮ࡴࡤࡦࡺ່ࠪ"))
      args.pop(i)
      bstack1l11l1lll1_opy_ = args.pop(i)
    if bstack1l11l1lll1_opy_ is not None:
      global bstack11ll1llll1_opy_
      bstack11ll1llll1_opy_ = bstack1l11l1lll1_opy_
    bstack1l11lll1ll_opy_(bstack1lllll1111_opy_)
    run_cli(args)
    if bstack11llll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ້ࠩ") in multiprocessing.current_process().__dict__.keys():
      for bstack1l11111ll_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1ll1l11l1l_opy_.append(bstack1l11111ll_opy_)
  elif bstack1lll1l11l1_opy_ == bstack11llll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ໊࠭"):
    percy.init(bstack11l111lll_opy_, CONFIG, logger)
    percy.bstack1l111l1l1l_opy_()
    bstack1l1ll1lll_opy_ = bstack11l11l11_opy_(args, logger, CONFIG, bstack1l1l1l111_opy_)
    bstack1l1ll1lll_opy_.bstack1111lll1_opy_()
    bstack1l111111l1_opy_()
    bstack1l1l11lll1_opy_ = True
    bstack1llll1l111_opy_ = bstack1l1ll1lll_opy_.bstack111l1l1l_opy_()
    bstack1l1ll1lll_opy_.bstack11l11111_opy_(bstack1lll1ll11_opy_)
    bstack11l11ll1l1_opy_ = bstack1l1ll1lll_opy_.bstack11111ll1_opy_(bstack1lllll1l11_opy_, {
      bstack11llll_opy_ (u"ࠧࡉࡗࡅࡣ࡚ࡘࡌࠨ໋"): bstack111l11l11_opy_,
      bstack11llll_opy_ (u"ࠨࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪ໌"): bstack11l111lll_opy_,
      bstack11llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬໍ"): bstack1l1l1l111_opy_
    })
    try:
      bstack11ll1ll11_opy_, bstack1ll11111l_opy_ = map(list, zip(*bstack11l11ll1l1_opy_))
      bstack1ll1ll111_opy_ = bstack11ll1ll11_opy_[0]
      for status_code in bstack1ll11111l_opy_:
        if status_code != 0:
          bstack11llll1lll_opy_ = status_code
          break
    except Exception as e:
      logger.debug(bstack11llll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡢࡸࡨࠤࡪࡸࡲࡰࡴࡶࠤࡦࡴࡤࠡࡵࡷࡥࡹࡻࡳࠡࡥࡲࡨࡪ࠴ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࠾ࠥࢁࡽࠣ໎").format(str(e)))
  elif bstack1lll1l11l1_opy_ == bstack11llll_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ໏"):
    try:
      from behave.__main__ import main as bstack1lll1ll1l1_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1ll1l1llll_opy_(e, bstack1l1l1111ll_opy_)
    bstack1l111111l1_opy_()
    bstack1l1l11lll1_opy_ = True
    bstack111l11l1_opy_ = 1
    if bstack11llll_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ໐") in CONFIG:
      bstack111l11l1_opy_ = CONFIG[bstack11llll_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭໑")]
    if bstack11llll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ໒") in CONFIG:
      bstack11l1l11l1_opy_ = int(bstack111l11l1_opy_) * int(len(CONFIG[bstack11llll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ໓")]))
    else:
      bstack11l1l11l1_opy_ = int(bstack111l11l1_opy_)
    config = Configuration(args)
    bstack1l1llllll1_opy_ = config.paths
    if len(bstack1l1llllll1_opy_) == 0:
      import glob
      pattern = bstack11llll_opy_ (u"ࠩ࠭࠮࠴࠰࠮ࡧࡧࡤࡸࡺࡸࡥࠨ໔")
      bstack1l1lllll1_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack1l1lllll1_opy_)
      config = Configuration(args)
      bstack1l1llllll1_opy_ = config.paths
    bstack111l1111_opy_ = [os.path.normpath(item) for item in bstack1l1llllll1_opy_]
    bstack1llll11111_opy_ = [os.path.normpath(item) for item in args]
    bstack1l1l111l1_opy_ = [item for item in bstack1llll11111_opy_ if item not in bstack111l1111_opy_]
    import platform as pf
    if pf.system().lower() == bstack11llll_opy_ (u"ࠪࡻ࡮ࡴࡤࡰࡹࡶࠫ໕"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack111l1111_opy_ = [str(PurePosixPath(PureWindowsPath(bstack11lll1l11l_opy_)))
                    for bstack11lll1l11l_opy_ in bstack111l1111_opy_]
    bstack111l1lll_opy_ = []
    for spec in bstack111l1111_opy_:
      bstack111l11ll_opy_ = []
      bstack111l11ll_opy_ += bstack1l1l111l1_opy_
      bstack111l11ll_opy_.append(spec)
      bstack111l1lll_opy_.append(bstack111l11ll_opy_)
    execution_items = []
    for bstack111l11ll_opy_ in bstack111l1lll_opy_:
      if bstack11llll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ໖") in CONFIG:
        for index, _ in enumerate(CONFIG[bstack11llll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ໗")]):
          item = {}
          item[bstack11llll_opy_ (u"࠭ࡡࡳࡩࠪ໘")] = bstack11llll_opy_ (u"ࠧࠡࠩ໙").join(bstack111l11ll_opy_)
          item[bstack11llll_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧ໚")] = index
          execution_items.append(item)
      else:
        item = {}
        item[bstack11llll_opy_ (u"ࠩࡤࡶ࡬࠭໛")] = bstack11llll_opy_ (u"ࠪࠤࠬໜ").join(bstack111l11ll_opy_)
        item[bstack11llll_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪໝ")] = 0
        execution_items.append(item)
    bstack1l1l111ll1_opy_ = bstack1l11llllll_opy_(execution_items, bstack11l1l11l1_opy_)
    for execution_item in bstack1l1l111ll1_opy_:
      bstack111ll111_opy_ = []
      for item in execution_item:
        bstack111ll111_opy_.append(bstack1ll11lll1l_opy_(name=str(item[bstack11llll_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫໞ")]),
                                             target=bstack1l11l11l1l_opy_,
                                             args=(item[bstack11llll_opy_ (u"࠭ࡡࡳࡩࠪໟ")],)))
      for t in bstack111ll111_opy_:
        t.start()
      for t in bstack111ll111_opy_:
        t.join()
  else:
    bstack1ll1l1lll_opy_(bstack1ll11l11l_opy_)
  if not bstack1ll1ll1ll1_opy_:
    bstack11l1llllll_opy_()
  bstack1ll1l1l1l1_opy_.bstack111l1ll11_opy_()
def browserstack_initialize(bstack1l1ll1l11l_opy_=None):
  run_on_browserstack(bstack1l1ll1l11l_opy_, None, True)
def bstack11l1llllll_opy_():
  global CONFIG
  global bstack11ll111ll1_opy_
  global bstack11llll1lll_opy_
  global bstack1l111ll1ll_opy_
  global bstack1111l1l1_opy_
  if cli.is_running():
    bstack1lll1ll11l_opy_.invoke(Events.bstack1ll1ll1l1l_opy_)
  bstack1lll11ll_opy_.stop()
  bstack1lll1l11_opy_.bstack1l111lllll_opy_()
  if bstack11llll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ໠") in CONFIG and str(CONFIG[bstack11llll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ໡")]).lower() != bstack11llll_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨ໢"):
    bstack1ll1l1111l_opy_, bstack1l1l1ll1ll_opy_ = bstack11l1ll1ll_opy_()
  else:
    bstack1ll1l1111l_opy_, bstack1l1l1ll1ll_opy_ = get_build_link()
  bstack1l1l1l11l_opy_(bstack1ll1l1111l_opy_)
  if bstack1ll1l1111l_opy_ is not None and bstack1l1l1ll11_opy_() != -1:
    sessions = bstack1l1111l11l_opy_(bstack1ll1l1111l_opy_)
    bstack11l111lll1_opy_(sessions, bstack1l1l1ll1ll_opy_)
  if bstack11ll111ll1_opy_ == bstack11llll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ໣") and bstack11llll1lll_opy_ != 0:
    sys.exit(bstack11llll1lll_opy_)
  if bstack11ll111ll1_opy_ == bstack11llll_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ໤") and bstack1l111ll1ll_opy_ != 0:
    sys.exit(bstack1l111ll1ll_opy_)
def bstack1l1l1l11l_opy_(new_id):
    global bstack111llll1l_opy_
    bstack111llll1l_opy_ = new_id
def bstack1l1lllll11_opy_(bstack1ll11ll11_opy_):
  if bstack1ll11ll11_opy_:
    return bstack1ll11ll11_opy_.capitalize()
  else:
    return bstack11llll_opy_ (u"ࠬ࠭໥")
def bstack1l1l1l111l_opy_(bstack11llll11l1_opy_):
  if bstack11llll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ໦") in bstack11llll11l1_opy_ and bstack11llll11l1_opy_[bstack11llll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ໧")] != bstack11llll_opy_ (u"ࠨࠩ໨"):
    return bstack11llll11l1_opy_[bstack11llll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ໩")]
  else:
    bstack1l111l11l_opy_ = bstack11llll_opy_ (u"ࠥࠦ໪")
    if bstack11llll_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫ໫") in bstack11llll11l1_opy_ and bstack11llll11l1_opy_[bstack11llll_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬ໬")] != None:
      bstack1l111l11l_opy_ += bstack11llll11l1_opy_[bstack11llll_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭໭")] + bstack11llll_opy_ (u"ࠢ࠭ࠢࠥ໮")
      if bstack11llll11l1_opy_[bstack11llll_opy_ (u"ࠨࡱࡶࠫ໯")] == bstack11llll_opy_ (u"ࠤ࡬ࡳࡸࠨ໰"):
        bstack1l111l11l_opy_ += bstack11llll_opy_ (u"ࠥ࡭ࡔ࡙ࠠࠣ໱")
      bstack1l111l11l_opy_ += (bstack11llll11l1_opy_[bstack11llll_opy_ (u"ࠫࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ໲")] or bstack11llll_opy_ (u"ࠬ࠭໳"))
      return bstack1l111l11l_opy_
    else:
      bstack1l111l11l_opy_ += bstack1l1lllll11_opy_(bstack11llll11l1_opy_[bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧ໴")]) + bstack11llll_opy_ (u"ࠢࠡࠤ໵") + (
              bstack11llll11l1_opy_[bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪ໶")] or bstack11llll_opy_ (u"ࠩࠪ໷")) + bstack11llll_opy_ (u"ࠥ࠰ࠥࠨ໸")
      if bstack11llll11l1_opy_[bstack11llll_opy_ (u"ࠫࡴࡹࠧ໹")] == bstack11llll_opy_ (u"ࠧ࡝ࡩ࡯ࡦࡲࡻࡸࠨ໺"):
        bstack1l111l11l_opy_ += bstack11llll_opy_ (u"ࠨࡗࡪࡰࠣࠦ໻")
      bstack1l111l11l_opy_ += bstack11llll11l1_opy_[bstack11llll_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫ໼")] or bstack11llll_opy_ (u"ࠨࠩ໽")
      return bstack1l111l11l_opy_
def bstack1l1l11l111_opy_(bstack1l11ll11ll_opy_):
  if bstack1l11ll11ll_opy_ == bstack11llll_opy_ (u"ࠤࡧࡳࡳ࡫ࠢ໾"):
    return bstack11llll_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿࡭ࡲࡦࡧࡱ࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧ࡭ࡲࡦࡧࡱࠦࡃࡉ࡯࡮ࡲ࡯ࡩࡹ࡫ࡤ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭໿")
  elif bstack1l11ll11ll_opy_ == bstack11llll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦༀ"):
    return bstack11llll_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡳࡧࡧ࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧࡸࡥࡥࠤࡁࡊࡦ࡯࡬ࡦࡦ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨ༁")
  elif bstack1l11ll11ll_opy_ == bstack11llll_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨ༂"):
    return bstack11llll_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡪࡶࡪ࡫࡮࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡪࡶࡪ࡫࡮ࠣࡀࡓࡥࡸࡹࡥࡥ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧ༃")
  elif bstack1l11ll11ll_opy_ == bstack11llll_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢ༄"):
    return bstack11llll_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࡷ࡫ࡤ࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡵࡩࡩࠨ࠾ࡆࡴࡵࡳࡷࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫ༅")
  elif bstack1l11ll11ll_opy_ == bstack11llll_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷࠦ༆"):
    return bstack11llll_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࠣࡦࡧࡤ࠷࠷࠼࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࠥࡨࡩࡦ࠹࠲࠷ࠤࡁࡘ࡮ࡳࡥࡰࡷࡷࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩ༇")
  elif bstack1l11ll11ll_opy_ == bstack11llll_opy_ (u"ࠧࡸࡵ࡯ࡰ࡬ࡲ࡬ࠨ༈"):
    return bstack11llll_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡤ࡯ࡥࡨࡱ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡤ࡯ࡥࡨࡱࠢ࠿ࡔࡸࡲࡳ࡯࡮ࡨ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧ༉")
  else:
    return bstack11llll_opy_ (u"ࠧ࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽ࡦࡱࡧࡣ࡬࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥࡦࡱࡧࡣ࡬ࠤࡁࠫ༊") + bstack1l1lllll11_opy_(
      bstack1l11ll11ll_opy_) + bstack11llll_opy_ (u"ࠨ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧ་")
def bstack1l1l1ll111_opy_(session):
  return bstack11llll_opy_ (u"ࠩ࠿ࡸࡷࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡲࡰࡹࠥࡂࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠦࡳࡦࡵࡶ࡭ࡴࡴ࠭࡯ࡣࡰࡩࠧࡄ࠼ࡢࠢ࡫ࡶࡪ࡬࠽ࠣࡽࢀࠦࠥࡺࡡࡳࡩࡨࡸࡂࠨ࡟ࡣ࡮ࡤࡲࡰࠨ࠾ࡼࡿ࠿࠳ࡦࡄ࠼࠰ࡶࡧࡂࢀࢃࡻࡾ࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࡃࢁࡽ࠽࠱ࡷࡨࡃࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࡀࡾࢁࡁ࠵ࡴࡥࡀ࠿ࡸࡩࠦࡡ࡭࡫ࡪࡲࡂࠨࡣࡦࡰࡷࡩࡷࠨࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࡄࡻࡾ࠾࠲ࡸࡩࡄ࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࡁࡿࢂࡂ࠯ࡵࡦࡁࡀ࠴ࡺࡲ࠿ࠩ༌").format(
    session[bstack11llll_opy_ (u"ࠪࡴࡺࡨ࡬ࡪࡥࡢࡹࡷࡲࠧ།")], bstack1l1l1l111l_opy_(session), bstack1l1l11l111_opy_(session[bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡷࡹࡧࡴࡶࡵࠪ༎")]),
    bstack1l1l11l111_opy_(session[bstack11llll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ༏")]),
    bstack1l1lllll11_opy_(session[bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧ༐")] or session[bstack11llll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧ༑")] or bstack11llll_opy_ (u"ࠨࠩ༒")) + bstack11llll_opy_ (u"ࠤࠣࠦ༓") + (session[bstack11llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ༔")] or bstack11llll_opy_ (u"ࠫࠬ༕")),
    session[bstack11llll_opy_ (u"ࠬࡵࡳࠨ༖")] + bstack11llll_opy_ (u"ࠨࠠࠣ༗") + session[bstack11llll_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱ༘ࠫ")], session[bstack11llll_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰ༙ࠪ")] or bstack11llll_opy_ (u"ࠩࠪ༚"),
    session[bstack11llll_opy_ (u"ࠪࡧࡷ࡫ࡡࡵࡧࡧࡣࡦࡺࠧ༛")] if session[bstack11llll_opy_ (u"ࠫࡨࡸࡥࡢࡶࡨࡨࡤࡧࡴࠨ༜")] else bstack11llll_opy_ (u"ࠬ࠭༝"))
def bstack11l111lll1_opy_(sessions, bstack1l1l1ll1ll_opy_):
  try:
    bstack1l11ll1lll_opy_ = bstack11llll_opy_ (u"ࠨࠢ༞")
    if not os.path.exists(bstack11l11111l1_opy_):
      os.mkdir(bstack11l11111l1_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11llll_opy_ (u"ࠧࡢࡵࡶࡩࡹࡹ࠯ࡳࡧࡳࡳࡷࡺ࠮ࡩࡶࡰࡰࠬ༟")), bstack11llll_opy_ (u"ࠨࡴࠪ༠")) as f:
      bstack1l11ll1lll_opy_ = f.read()
    bstack1l11ll1lll_opy_ = bstack1l11ll1lll_opy_.replace(bstack11llll_opy_ (u"ࠩࡾࠩࡗࡋࡓࡖࡎࡗࡗࡤࡉࡏࡖࡐࡗࠩࢂ࠭༡"), str(len(sessions)))
    bstack1l11ll1lll_opy_ = bstack1l11ll1lll_opy_.replace(bstack11llll_opy_ (u"ࠪࡿࠪࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠦࡿࠪ༢"), bstack1l1l1ll1ll_opy_)
    bstack1l11ll1lll_opy_ = bstack1l11ll1lll_opy_.replace(bstack11llll_opy_ (u"ࠫࢀࠫࡂࡖࡋࡏࡈࡤࡔࡁࡎࡇࠨࢁࠬ༣"),
                                              sessions[0].get(bstack11llll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣࡳࡧ࡭ࡦࠩ༤")) if sessions[0] else bstack11llll_opy_ (u"࠭ࠧ༥"))
    with open(os.path.join(bstack11l11111l1_opy_, bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠳ࡲࡦࡲࡲࡶࡹ࠴ࡨࡵ࡯࡯ࠫ༦")), bstack11llll_opy_ (u"ࠨࡹࠪ༧")) as stream:
      stream.write(bstack1l11ll1lll_opy_.split(bstack11llll_opy_ (u"ࠩࡾࠩࡘࡋࡓࡔࡋࡒࡒࡘࡥࡄࡂࡖࡄࠩࢂ࠭༨"))[0])
      for session in sessions:
        stream.write(bstack1l1l1ll111_opy_(session))
      stream.write(bstack1l11ll1lll_opy_.split(bstack11llll_opy_ (u"ࠪࡿ࡙ࠪࡅࡔࡕࡌࡓࡓ࡙࡟ࡅࡃࡗࡅࠪࢃࠧ༩"))[1])
    logger.info(bstack11llll_opy_ (u"ࠫࡌ࡫࡮ࡦࡴࡤࡸࡪࡪࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡢࡶ࡫࡯ࡨࠥࡧࡲࡵ࡫ࡩࡥࡨࡺࡳࠡࡣࡷࠤࢀࢃࠧ༪").format(bstack11l11111l1_opy_));
  except Exception as e:
    logger.debug(bstack1lll1l1ll1_opy_.format(str(e)))
def bstack1l1111l11l_opy_(bstack1ll1l1111l_opy_):
  global CONFIG
  try:
    bstack111l1l1l1_opy_ = datetime.datetime.now()
    host = bstack11llll_opy_ (u"ࠬࡧࡰࡪ࠯ࡦࡰࡴࡻࡤࠨ༫") if bstack11llll_opy_ (u"࠭ࡡࡱࡲࠪ༬") in CONFIG else bstack11llll_opy_ (u"ࠧࡢࡲ࡬ࠫ༭")
    user = CONFIG[bstack11llll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ༮")]
    key = CONFIG[bstack11llll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ༯")]
    bstack1ll111lll1_opy_ = bstack11llll_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩ༰") if bstack11llll_opy_ (u"ࠫࡦࡶࡰࠨ༱") in CONFIG else (bstack11llll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩ༲") if CONFIG.get(bstack11llll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪ༳")) else bstack11llll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩ༴"))
    url = bstack11llll_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡾࢁ࠿ࢁࡽࡁࡽࢀ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡼࡿ࠲ࡦࡺ࡯࡬ࡥࡵ࠲ࡿࢂ࠵ࡳࡦࡵࡶ࡭ࡴࡴࡳ࠯࡬ࡶࡳࡳ༵࠭").format(user, key, host, bstack1ll111lll1_opy_,
                                                                                bstack1ll1l1111l_opy_)
    headers = {
      bstack11llll_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨ༶"): bstack11llll_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ༷࠭"),
    }
    proxies = bstack1ll111111_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.json():
      cli.bstack1ll1l1l11l_opy_(bstack11llll_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼ࡪࡩࡹࡥࡳࡦࡵࡶ࡭ࡴࡴࡳࡠ࡮࡬ࡷࡹࠨ༸"), datetime.datetime.now() - bstack111l1l1l1_opy_)
      return list(map(lambda session: session[bstack11llll_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡶࡩࡸࡹࡩࡰࡰ༹ࠪ")], response.json()))
  except Exception as e:
    logger.debug(bstack1l1l1llll_opy_.format(str(e)))
def get_build_link():
  global CONFIG
  global bstack111llll1l_opy_
  try:
    if bstack11llll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ༺") in CONFIG:
      bstack111l1l1l1_opy_ = datetime.datetime.now()
      host = bstack11llll_opy_ (u"ࠧࡢࡲ࡬࠱ࡨࡲ࡯ࡶࡦࠪ༻") if bstack11llll_opy_ (u"ࠨࡣࡳࡴࠬ༼") in CONFIG else bstack11llll_opy_ (u"ࠩࡤࡴ࡮࠭༽")
      user = CONFIG[bstack11llll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ༾")]
      key = CONFIG[bstack11llll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ༿")]
      bstack1ll111lll1_opy_ = bstack11llll_opy_ (u"ࠬࡧࡰࡱ࠯ࡤࡹࡹࡵ࡭ࡢࡶࡨࠫཀ") if bstack11llll_opy_ (u"࠭ࡡࡱࡲࠪཁ") in CONFIG else bstack11llll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩག")
      url = bstack11llll_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡾࢁ࠿ࢁࡽࡁࡽࢀ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡼࡿ࠲ࡦࡺ࡯࡬ࡥࡵ࠱࡮ࡸࡵ࡮ࠨགྷ").format(user, key, host, bstack1ll111lll1_opy_)
      headers = {
        bstack11llll_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨང"): bstack11llll_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ཅ"),
      }
      if bstack11llll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ཆ") in CONFIG:
        params = {bstack11llll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪཇ"): CONFIG[bstack11llll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ཈")], bstack11llll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪཉ"): CONFIG[bstack11llll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪཊ")]}
      else:
        params = {bstack11llll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧཋ"): CONFIG[bstack11llll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ཌ")]}
      proxies = bstack1ll111111_opy_(CONFIG, url)
      response = requests.get(url, params=params, headers=headers, proxies=proxies)
      if response.json():
        bstack1lllll1l1_opy_ = response.json()[0][bstack11llll_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡤࡸ࡭ࡱࡪࠧཌྷ")]
        if bstack1lllll1l1_opy_:
          bstack1l1l1ll1ll_opy_ = bstack1lllll1l1_opy_[bstack11llll_opy_ (u"ࠬࡶࡵࡣ࡮࡬ࡧࡤࡻࡲ࡭ࠩཎ")].split(bstack11llll_opy_ (u"࠭ࡰࡶࡤ࡯࡭ࡨ࠳ࡢࡶ࡫࡯ࡨࠬཏ"))[0] + bstack11llll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡹ࠯ࠨཐ") + bstack1lllll1l1_opy_[
            bstack11llll_opy_ (u"ࠨࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫད")]
          logger.info(bstack11l1l11l1l_opy_.format(bstack1l1l1ll1ll_opy_))
          bstack111llll1l_opy_ = bstack1lllll1l1_opy_[bstack11llll_opy_ (u"ࠩ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬདྷ")]
          bstack1l1111llll_opy_ = CONFIG[bstack11llll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ན")]
          if bstack11llll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭པ") in CONFIG:
            bstack1l1111llll_opy_ += bstack11llll_opy_ (u"ࠬࠦࠧཕ") + CONFIG[bstack11llll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨབ")]
          if bstack1l1111llll_opy_ != bstack1lllll1l1_opy_[bstack11llll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬབྷ")]:
            logger.debug(bstack111lllll1l_opy_.format(bstack1lllll1l1_opy_[bstack11llll_opy_ (u"ࠨࡰࡤࡱࡪ࠭མ")], bstack1l1111llll_opy_))
          cli.bstack1ll1l1l11l_opy_(bstack11llll_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺ࡨࡧࡷࡣࡧࡻࡩ࡭ࡦࡢࡰ࡮ࡴ࡫ࠣཙ"), datetime.datetime.now() - bstack111l1l1l1_opy_)
          return [bstack1lllll1l1_opy_[bstack11llll_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ཚ")], bstack1l1l1ll1ll_opy_]
    else:
      logger.warn(bstack11l111l1l_opy_)
  except Exception as e:
    logger.debug(bstack1l1l1l1l11_opy_.format(str(e)))
  return [None, None]
def bstack11llll11l_opy_(url, bstack1llllll11l_opy_=False):
  global CONFIG
  global bstack111lllllll_opy_
  if not bstack111lllllll_opy_:
    hostname = bstack11l1l111l_opy_(url)
    is_private = bstack1l1111ll11_opy_(hostname)
    if (bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨཛ") in CONFIG and not bstack1lll1lll11_opy_(CONFIG[bstack11llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩཛྷ")])) and (is_private or bstack1llllll11l_opy_):
      bstack111lllllll_opy_ = hostname
def bstack11l1l111l_opy_(url):
  return urlparse(url).hostname
def bstack1l1111ll11_opy_(hostname):
  for bstack1l1l111lll_opy_ in bstack11l1llll11_opy_:
    regex = re.compile(bstack1l1l111lll_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack1lll1l1111_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False
def getAccessibilityResults(driver):
  global CONFIG
  global bstack11l111ll1l_opy_
  bstack1llllll111_opy_ = not (bstack1ll111l1_opy_(threading.current_thread(), bstack11llll_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪཝ"), None) and bstack1ll111l1_opy_(
          threading.current_thread(), bstack11llll_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ཞ"), None))
  bstack1l1ll1111l_opy_ = getattr(driver, bstack11llll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨཟ"), None) != True
  if not bstack11111l11_opy_.bstack1l1llll11_opy_(CONFIG, bstack11l111ll1l_opy_) or (bstack1l1ll1111l_opy_ and bstack1llllll111_opy_):
    logger.warning(bstack11llll_opy_ (u"ࠤࡑࡳࡹࠦࡡ࡯ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡳࡦࡵࡶ࡭ࡴࡴࠬࠡࡥࡤࡲࡳࡵࡴࠡࡴࡨࡸࡷ࡯ࡥࡷࡧࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡶࡪࡹࡵ࡭ࡶࡶ࠲ࠧའ"))
    return {}
  try:
    logger.debug(bstack11llll_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥࡨࡥࡧࡱࡵࡩࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡲࡦࡵࡸࡰࡹࡹࠧཡ"))
    logger.debug(perform_scan(driver))
    results = driver.execute_async_script(bstack11ll11l1l1_opy_.bstack1ll11lllll_opy_)
    return results
  except Exception:
    logger.error(bstack11llll_opy_ (u"ࠦࡓࡵࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳࠡࡹࡨࡶࡪࠦࡦࡰࡷࡱࡨ࠳ࠨར"))
    return {}
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack11l111ll1l_opy_
  bstack1llllll111_opy_ = not (bstack1ll111l1_opy_(threading.current_thread(), bstack11llll_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩལ"), None) and bstack1ll111l1_opy_(
          threading.current_thread(), bstack11llll_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬཤ"), None))
  bstack1l1ll1111l_opy_ = getattr(driver, bstack11llll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧཥ"), None) != True
  if not bstack11111l11_opy_.bstack1l1llll11_opy_(CONFIG, bstack11l111ll1l_opy_) or (bstack1l1ll1111l_opy_ and bstack1llllll111_opy_):
    logger.warning(bstack11llll_opy_ (u"ࠣࡐࡲࡸࠥࡧ࡮ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡹࡥࡴࡵ࡬ࡳࡳ࠲ࠠࡤࡣࡱࡲࡴࡺࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡷࡺࡳ࡭ࡢࡴࡼ࠲ࠧས"))
    return {}
  try:
    logger.debug(bstack11llll_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤࡧ࡫ࡦࡰࡴࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡳࡶ࡯ࡰࡥࡷࡿࠧཧ"))
    logger.debug(perform_scan(driver))
    bstack1l111ll111_opy_ = driver.execute_async_script(bstack11ll11l1l1_opy_.bstack11l11l1ll1_opy_)
    return bstack1l111ll111_opy_
  except Exception:
    logger.error(bstack11llll_opy_ (u"ࠥࡒࡴࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡶ࡯ࡰࡥࡷࡿࠠࡸࡣࡶࠤ࡫ࡵࡵ࡯ࡦ࠱ࠦཨ"))
    return {}
def perform_scan(driver, *args, **kwargs):
  global CONFIG
  global bstack11l111ll1l_opy_
  bstack1llllll111_opy_ = not (bstack1ll111l1_opy_(threading.current_thread(), bstack11llll_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨཀྵ"), None) and bstack1ll111l1_opy_(
          threading.current_thread(), bstack11llll_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫཪ"), None))
  bstack1l1ll1111l_opy_ = getattr(driver, bstack11llll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭ཫ"), None) != True
  if not bstack11111l11_opy_.bstack1l1llll11_opy_(CONFIG, bstack11l111ll1l_opy_) or (bstack1l1ll1111l_opy_ and bstack1llllll111_opy_):
    logger.warning(bstack11llll_opy_ (u"ࠢࡏࡱࡷࠤࡦࡴࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠱ࠦࡣࡢࡰࡱࡳࡹࠦࡲࡶࡰࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡨࡧ࡮࠯ࠤཬ"))
    return {}
  try:
    bstack1ll1111l1_opy_ = driver.execute_async_script(bstack11ll11l1l1_opy_.perform_scan, {bstack11llll_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࠨ཭"): kwargs.get(bstack11llll_opy_ (u"ࠩࡧࡶ࡮ࡼࡥࡳࡡࡦࡳࡲࡳࡡ࡯ࡦࠪ཮"), None) or bstack11llll_opy_ (u"ࠪࠫ཯")})
    return bstack1ll1111l1_opy_
  except Exception:
    logger.error(bstack11llll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡳࡷࡱࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡸࡩࡡ࡯࠰ࠥ཰"))
    return {}