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
import re
import sys
import json
import time
import shutil
import tempfile
import requests
import subprocess
from threading import Thread
from os.path import expanduser
from bstack_utils.constants import *
from requests.auth import HTTPBasicAuth
from bstack_utils.helper import bstack11l1ll11l_opy_, bstack1l1111l1l_opy_
class bstack1ll1lll1ll_opy_:
  working_dir = os.getcwd()
  bstack11lllllll_opy_ = False
  config = {}
  binary_path = bstack11llll_opy_ (u"ࠬ࠭ᣋ")
  bstack11lll1l11ll_opy_ = bstack11llll_opy_ (u"࠭ࠧᣌ")
  bstack11l1l1l11l_opy_ = False
  bstack11lll11ll1l_opy_ = None
  bstack11llll11l11_opy_ = {}
  bstack11lll11ll11_opy_ = 300
  bstack11lll1l111l_opy_ = False
  logger = None
  bstack11lll1lll1l_opy_ = False
  bstack1ll11ll1l1_opy_ = False
  bstack11l1l1l1l_opy_ = None
  bstack11llllll1ll_opy_ = bstack11llll_opy_ (u"ࠧࠨᣍ")
  bstack11lll1l11l1_opy_ = {
    bstack11llll_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨᣎ") : 1,
    bstack11llll_opy_ (u"ࠩࡩ࡭ࡷ࡫ࡦࡰࡺࠪᣏ") : 2,
    bstack11llll_opy_ (u"ࠪࡩࡩ࡭ࡥࠨᣐ") : 3,
    bstack11llll_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࠫᣑ") : 4
  }
  def __init__(self) -> None: pass
  def bstack11lll11l1ll_opy_(self):
    bstack11llll11lll_opy_ = bstack11llll_opy_ (u"ࠬ࠭ᣒ")
    bstack11llll11ll1_opy_ = sys.platform
    bstack11llll11111_opy_ = bstack11llll_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬᣓ")
    if re.match(bstack11llll_opy_ (u"ࠢࡥࡣࡵࡻ࡮ࡴࡼ࡮ࡣࡦࠤࡴࡹࠢᣔ"), bstack11llll11ll1_opy_) != None:
      bstack11llll11lll_opy_ = bstack1l1ll11llll_opy_ + bstack11llll_opy_ (u"ࠣ࠱ࡳࡩࡷࡩࡹ࠮ࡱࡶࡼ࠳ࢀࡩࡱࠤᣕ")
      self.bstack11llllll1ll_opy_ = bstack11llll_opy_ (u"ࠩࡰࡥࡨ࠭ᣖ")
    elif re.match(bstack11llll_opy_ (u"ࠥࡱࡸࡽࡩ࡯ࡾࡰࡷࡾࡹࡼ࡮࡫ࡱ࡫ࡼࢂࡣࡺࡩࡺ࡭ࡳࢂࡢࡤࡥࡺ࡭ࡳࢂࡷࡪࡰࡦࡩࢁ࡫࡭ࡤࡾࡺ࡭ࡳ࠹࠲ࠣᣗ"), bstack11llll11ll1_opy_) != None:
      bstack11llll11lll_opy_ = bstack1l1ll11llll_opy_ + bstack11llll_opy_ (u"ࠦ࠴ࡶࡥࡳࡥࡼ࠱ࡼ࡯࡮࠯ࡼ࡬ࡴࠧᣘ")
      bstack11llll11111_opy_ = bstack11llll_opy_ (u"ࠧࡶࡥࡳࡥࡼ࠲ࡪࡾࡥࠣᣙ")
      self.bstack11llllll1ll_opy_ = bstack11llll_opy_ (u"࠭ࡷࡪࡰࠪᣚ")
    else:
      bstack11llll11lll_opy_ = bstack1l1ll11llll_opy_ + bstack11llll_opy_ (u"ࠢ࠰ࡲࡨࡶࡨࡿ࠭࡭࡫ࡱࡹࡽ࠴ࡺࡪࡲࠥᣛ")
      self.bstack11llllll1ll_opy_ = bstack11llll_opy_ (u"ࠨ࡮࡬ࡲࡺࡾࠧᣜ")
    return bstack11llll11lll_opy_, bstack11llll11111_opy_
  def bstack11lllll111l_opy_(self):
    try:
      bstack11llll111l1_opy_ = [os.path.join(expanduser(bstack11llll_opy_ (u"ࠤࢁࠦᣝ")), bstack11llll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᣞ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack11llll111l1_opy_:
        if(self.bstack11llll1lll1_opy_(path)):
          return path
      raise bstack11llll_opy_ (u"࡚ࠦࡴࡡ࡭ࡤࡨࠤࡹࡵࠠࡥࡱࡺࡲࡱࡵࡡࡥࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠣᣟ")
    except Exception as e:
      self.logger.error(bstack11llll_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡨ࡬ࡲࡩࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦࠢࡳࡥࡹ࡮ࠠࡧࡱࡵࠤࡵ࡫ࡲࡤࡻࠣࡨࡴࡽ࡮࡭ࡱࡤࡨ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࠰ࠤࢀࢃࠢᣠ").format(e))
  def bstack11llll1lll1_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack11lll1lll11_opy_(self, bstack11llll11lll_opy_, bstack11llll11111_opy_):
    try:
      bstack11llllll11l_opy_ = self.bstack11lllll111l_opy_()
      bstack11lll1l1l1l_opy_ = os.path.join(bstack11llllll11l_opy_, bstack11llll_opy_ (u"࠭ࡰࡦࡴࡦࡽ࠳ࢀࡩࡱࠩᣡ"))
      bstack11lllllll11_opy_ = os.path.join(bstack11llllll11l_opy_, bstack11llll11111_opy_)
      if os.path.exists(bstack11lllllll11_opy_):
        self.logger.info(bstack11llll_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡦࡰࡷࡱࡨࠥ࡯࡮ࠡࡽࢀ࠰ࠥࡹ࡫ࡪࡲࡳ࡭ࡳ࡭ࠠࡥࡱࡺࡲࡱࡵࡡࡥࠤᣢ").format(bstack11lllllll11_opy_))
        return bstack11lllllll11_opy_
      if os.path.exists(bstack11lll1l1l1l_opy_):
        self.logger.info(bstack11llll_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡻ࡫ࡳࠤ࡫ࡵࡵ࡯ࡦࠣ࡭ࡳࠦࡻࡾ࠮ࠣࡹࡳࢀࡩࡱࡲ࡬ࡲ࡬ࠨᣣ").format(bstack11lll1l1l1l_opy_))
        return self.bstack11lllll1l1l_opy_(bstack11lll1l1l1l_opy_, bstack11llll11111_opy_)
      self.logger.info(bstack11llll_opy_ (u"ࠤࡇࡳࡼࡴ࡬ࡰࡣࡧ࡭ࡳ࡭ࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡦࡳࡱࡰࠤࢀࢃࠢᣤ").format(bstack11llll11lll_opy_))
      response = bstack1l1111l1l_opy_(bstack11llll_opy_ (u"ࠪࡋࡊ࡚ࠧᣥ"), bstack11llll11lll_opy_, {}, {})
      if response.status_code == 200:
        with open(bstack11lll1l1l1l_opy_, bstack11llll_opy_ (u"ࠫࡼࡨࠧᣦ")) as file:
          file.write(response.content)
        self.logger.info(bstack11llll_opy_ (u"ࠧࡊ࡯ࡸࡰ࡯ࡳࡦࡪࡥࡥࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡣࡱࡨࠥࡹࡡࡷࡧࡧࠤࡦࡺࠠࡼࡿࠥᣧ").format(bstack11lll1l1l1l_opy_))
        return self.bstack11lllll1l1l_opy_(bstack11lll1l1l1l_opy_, bstack11llll11111_opy_)
      else:
        raise(bstack11llll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠤࡹ࡮ࡥࠡࡨ࡬ࡰࡪ࠴ࠠࡔࡶࡤࡸࡺࡹࠠࡤࡱࡧࡩ࠿ࠦࡻࡾࠤᣨ").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack11llll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼ࠾ࠥࢁࡽࠣᣩ").format(e))
  def bstack11lll1l1lll_opy_(self, bstack11llll11lll_opy_, bstack11llll11111_opy_):
    try:
      retry = 2
      bstack11lllllll11_opy_ = None
      bstack11lllll11l1_opy_ = False
      while retry > 0:
        bstack11lllllll11_opy_ = self.bstack11lll1lll11_opy_(bstack11llll11lll_opy_, bstack11llll11111_opy_)
        bstack11lllll11l1_opy_ = self.bstack11llll1l11l_opy_(bstack11llll11lll_opy_, bstack11llll11111_opy_, bstack11lllllll11_opy_)
        if bstack11lllll11l1_opy_:
          break
        retry -= 1
      return bstack11lllllll11_opy_, bstack11lllll11l1_opy_
    except Exception as e:
      self.logger.error(bstack11llll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡬࡫ࡴࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡱࡣࡷ࡬ࠧᣪ").format(e))
    return bstack11lllllll11_opy_, False
  def bstack11llll1l11l_opy_(self, bstack11llll11lll_opy_, bstack11llll11111_opy_, bstack11lllllll11_opy_, bstack11lllllll1l_opy_ = 0):
    if bstack11lllllll1l_opy_ > 1:
      return False
    if bstack11lllllll11_opy_ == None or os.path.exists(bstack11lllllll11_opy_) == False:
      self.logger.warn(bstack11llll_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡲࡤࡸ࡭ࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥ࠮ࠣࡶࡪࡺࡲࡺ࡫ࡱ࡫ࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠢᣫ"))
      return False
    bstack11llllll1l1_opy_ = bstack11llll_opy_ (u"ࠥࡢ࠳࠰ࡀࡱࡧࡵࡧࡾࡢ࠯ࡤ࡮࡬ࠤࡡࡪ࠮࡝ࡦ࠮࠲ࡡࡪࠫࠣᣬ")
    command = bstack11llll_opy_ (u"ࠫࢀࢃࠠ࠮࠯ࡹࡩࡷࡹࡩࡰࡰࠪᣭ").format(bstack11lllllll11_opy_)
    bstack11llll1l1l1_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack11llllll1l1_opy_, bstack11llll1l1l1_opy_) != None:
      return True
    else:
      self.logger.error(bstack11llll_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࡩࡨࡦࡥ࡮ࠤ࡫ࡧࡩ࡭ࡧࡧࠦᣮ"))
      return False
  def bstack11lllll1l1l_opy_(self, bstack11lll1l1l1l_opy_, bstack11llll11111_opy_):
    try:
      working_dir = os.path.dirname(bstack11lll1l1l1l_opy_)
      shutil.unpack_archive(bstack11lll1l1l1l_opy_, working_dir)
      bstack11lllllll11_opy_ = os.path.join(working_dir, bstack11llll11111_opy_)
      os.chmod(bstack11lllllll11_opy_, 0o755)
      return bstack11lllllll11_opy_
    except Exception as e:
      self.logger.error(bstack11llll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡸࡲࡿ࡯ࡰࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠢᣯ"))
  def bstack11lll1ll111_opy_(self):
    try:
      bstack11lll1l1ll1_opy_ = self.config.get(bstack11llll_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ᣰ"))
      bstack11lll1ll111_opy_ = bstack11lll1l1ll1_opy_ or (bstack11lll1l1ll1_opy_ is None and self.bstack11lllllll_opy_)
      if not bstack11lll1ll111_opy_ or self.config.get(bstack11llll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫᣱ"), None) not in bstack1l1ll1111l1_opy_:
        return False
      self.bstack11l1l1l11l_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack11llll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡪࡥࡵࡧࡦࡸࠥࡶࡥࡳࡥࡼ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦᣲ").format(e))
  def bstack11llll1llll_opy_(self):
    try:
      bstack11llll1llll_opy_ = self.bstack11llllllll1_opy_
      return bstack11llll1llll_opy_
    except Exception as e:
      self.logger.error(bstack11llll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡦࡶࡨࡧࡹࠦࡰࡦࡴࡦࡽࠥࡩࡡࡱࡶࡸࡶࡪࠦ࡭ࡰࡦࡨ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦᣳ").format(e))
  def init(self, bstack11lllllll_opy_, config, logger):
    self.bstack11lllllll_opy_ = bstack11lllllll_opy_
    self.config = config
    self.logger = logger
    if not self.bstack11lll1ll111_opy_():
      return
    self.bstack11llll11l11_opy_ = config.get(bstack11llll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᣴ"), {})
    self.bstack11llllllll1_opy_ = config.get(bstack11llll_opy_ (u"ࠬࡶࡥࡳࡥࡼࡇࡦࡶࡴࡶࡴࡨࡑࡴࡪࡥࠨᣵ"))
    try:
      bstack11llll11lll_opy_, bstack11llll11111_opy_ = self.bstack11lll11l1ll_opy_()
      bstack11lllllll11_opy_, bstack11lllll11l1_opy_ = self.bstack11lll1l1lll_opy_(bstack11llll11lll_opy_, bstack11llll11111_opy_)
      if bstack11lllll11l1_opy_:
        self.binary_path = bstack11lllllll11_opy_
        thread = Thread(target=self.bstack11llllll111_opy_)
        thread.start()
      else:
        self.bstack11lll1lll1l_opy_ = True
        self.logger.error(bstack11llll_opy_ (u"ࠨࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡱࡧࡵࡧࡾࠦࡰࡢࡶ࡫ࠤ࡫ࡵࡵ࡯ࡦࠣ࠱ࠥࢁࡽ࠭ࠢࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡕ࡫ࡲࡤࡻࠥ᣶").format(bstack11lllllll11_opy_))
    except Exception as e:
      self.logger.error(bstack11llll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡳࡩࡷࡩࡹ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣ᣷").format(e))
  def bstack11lllllllll_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack11llll_opy_ (u"ࠨ࡮ࡲ࡫ࠬ᣸"), bstack11llll_opy_ (u"ࠩࡳࡩࡷࡩࡹ࠯࡮ࡲ࡫ࠬ᣹"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack11llll_opy_ (u"ࠥࡔࡺࡹࡨࡪࡰࡪࠤࡵ࡫ࡲࡤࡻࠣࡰࡴ࡭ࡳࠡࡣࡷࠤࢀࢃࠢ᣺").format(logfile))
      self.bstack11lll1l11ll_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack11llll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡧࡷࠤࡵ࡫ࡲࡤࡻࠣࡰࡴ࡭ࠠࡱࡣࡷ࡬࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧ᣻").format(e))
  def bstack11llllll111_opy_(self):
    bstack11llll11l1l_opy_ = self.bstack11lll11llll_opy_()
    if bstack11llll11l1l_opy_ == None:
      self.bstack11lll1lll1l_opy_ = True
      self.logger.error(bstack11llll_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡹࡵ࡫ࡦࡰࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩ࠲ࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡳࡩࡷࡩࡹࠣ᣼"))
      return False
    command_args = [bstack11llll_opy_ (u"ࠨࡡࡱࡲ࠽ࡩࡽ࡫ࡣ࠻ࡵࡷࡥࡷࡺࠢ᣽") if self.bstack11lllllll_opy_ else bstack11llll_opy_ (u"ࠧࡦࡺࡨࡧ࠿ࡹࡴࡢࡴࡷࠫ᣾")]
    bstack11llll1ll11_opy_ = self.bstack11lllll1lll_opy_()
    if bstack11llll1ll11_opy_ != None:
      command_args.append(bstack11llll_opy_ (u"ࠣ࠯ࡦࠤࢀࢃࠢ᣿").format(bstack11llll1ll11_opy_))
    env = os.environ.copy()
    env[bstack11llll_opy_ (u"ࠤࡓࡉࡗࡉ࡙ࡠࡖࡒࡏࡊࡔࠢᤀ")] = bstack11llll11l1l_opy_
    env[bstack11llll_opy_ (u"ࠥࡘࡍࡥࡂࡖࡋࡏࡈࡤ࡛ࡕࡊࡆࠥᤁ")] = os.environ.get(bstack11llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩᤂ"), bstack11llll_opy_ (u"ࠬ࠭ᤃ"))
    bstack11lll1l1111_opy_ = [self.binary_path]
    self.bstack11lllllllll_opy_()
    self.bstack11lll11ll1l_opy_ = self.bstack11lll1ll1ll_opy_(bstack11lll1l1111_opy_ + command_args, env)
    self.logger.debug(bstack11llll_opy_ (u"ࠨࡓࡵࡣࡵࡸ࡮ࡴࡧࠡࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠢᤄ"))
    bstack11lllllll1l_opy_ = 0
    while self.bstack11lll11ll1l_opy_.poll() == None:
      bstack11lllll1111_opy_ = self.bstack11lll1l1l11_opy_()
      if bstack11lllll1111_opy_:
        self.logger.debug(bstack11llll_opy_ (u"ࠢࡉࡧࡤࡰࡹ࡮ࠠࡄࡪࡨࡧࡰࠦࡳࡶࡥࡦࡩࡸࡹࡦࡶ࡮ࠥᤅ"))
        self.bstack11lll1l111l_opy_ = True
        return True
      bstack11lllllll1l_opy_ += 1
      self.logger.debug(bstack11llll_opy_ (u"ࠣࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠠࡓࡧࡷࡶࡾࠦ࠭ࠡࡽࢀࠦᤆ").format(bstack11lllllll1l_opy_))
      time.sleep(2)
    self.logger.error(bstack11llll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡵ࡫ࡲࡤࡻ࠯ࠤࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠣࡊࡦ࡯࡬ࡦࡦࠣࡥ࡫ࡺࡥࡳࠢࡾࢁࠥࡧࡴࡵࡧࡰࡴࡹࡹࠢᤇ").format(bstack11lllllll1l_opy_))
    self.bstack11lll1lll1l_opy_ = True
    return False
  def bstack11lll1l1l11_opy_(self, bstack11lllllll1l_opy_ = 0):
    if bstack11lllllll1l_opy_ > 10:
      return False
    try:
      bstack11lll1llll1_opy_ = os.environ.get(bstack11llll_opy_ (u"ࠪࡔࡊࡘࡃ࡚ࡡࡖࡉࡗ࡜ࡅࡓࡡࡄࡈࡉࡘࡅࡔࡕࠪᤈ"), bstack11llll_opy_ (u"ࠫ࡭ࡺࡴࡱ࠼࠲࠳ࡱࡵࡣࡢ࡮࡫ࡳࡸࡺ࠺࠶࠵࠶࠼ࠬᤉ"))
      bstack11llll1l111_opy_ = bstack11lll1llll1_opy_ + bstack1l1ll1l11ll_opy_
      response = requests.get(bstack11llll1l111_opy_)
      data = response.json()
      self.bstack11l1l1l1l_opy_ = data.get(bstack11llll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࠫᤊ"), {}).get(bstack11llll_opy_ (u"࠭ࡩࡥࠩᤋ"), None)
      return True
    except:
      self.logger.debug(bstack11llll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦ࡯ࡤࡥࡸࡶࡷ࡫ࡤࠡࡹ࡫࡭ࡱ࡫ࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤ࡭࡫ࡡ࡭ࡶ࡫ࠤࡨ࡮ࡥࡤ࡭ࠣࡶࡪࡹࡰࡰࡰࡶࡩࠧᤌ"))
      return False
  def bstack11lll11llll_opy_(self):
    bstack11llll1111l_opy_ = bstack11llll_opy_ (u"ࠨࡣࡳࡴࠬᤍ") if self.bstack11lllllll_opy_ else bstack11llll_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫᤎ")
    bstack11llll111ll_opy_ = bstack11llll_opy_ (u"ࠥࡹࡳࡪࡥࡧ࡫ࡱࡩࡩࠨᤏ") if self.config.get(bstack11llll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪᤐ")) is None else True
    bstack1l11l1lll1l_opy_ = bstack11llll_opy_ (u"ࠧࡧࡰࡪ࠱ࡤࡴࡵࡥࡰࡦࡴࡦࡽ࠴࡭ࡥࡵࡡࡳࡶࡴࡰࡥࡤࡶࡢࡸࡴࡱࡥ࡯ࡁࡱࡥࡲ࡫࠽ࡼࡿࠩࡸࡾࡶࡥ࠾ࡽࢀࠪࡵ࡫ࡲࡤࡻࡀࡿࢂࠨᤑ").format(self.config[bstack11llll_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫᤒ")], bstack11llll1111l_opy_, bstack11llll111ll_opy_)
    if self.bstack11llllllll1_opy_:
      bstack1l11l1lll1l_opy_ += bstack11llll_opy_ (u"ࠢࠧࡲࡨࡶࡨࡿ࡟ࡤࡣࡳࡸࡺࡸࡥࡠ࡯ࡲࡨࡪࡃࡻࡾࠤᤓ").format(self.bstack11llllllll1_opy_)
    uri = bstack11l1ll11l_opy_(bstack1l11l1lll1l_opy_)
    try:
      response = bstack1l1111l1l_opy_(bstack11llll_opy_ (u"ࠨࡉࡈࡘࠬᤔ"), uri, {}, {bstack11llll_opy_ (u"ࠩࡤࡹࡹ࡮ࠧᤕ"): (self.config[bstack11llll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᤖ")], self.config[bstack11llll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧᤗ")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack11l1l1l11l_opy_ = data.get(bstack11llll_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭ᤘ"))
        self.bstack11llllllll1_opy_ = data.get(bstack11llll_opy_ (u"࠭ࡰࡦࡴࡦࡽࡤࡩࡡࡱࡶࡸࡶࡪࡥ࡭ࡰࡦࡨࠫᤙ"))
        os.environ[bstack11llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡆࡔࡆ࡝ࠬᤚ")] = str(self.bstack11l1l1l11l_opy_)
        os.environ[bstack11llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡇࡕࡇ࡞ࡥࡃࡂࡒࡗ࡙ࡗࡋ࡟ࡎࡑࡇࡉࠬᤛ")] = str(self.bstack11llllllll1_opy_)
        if bstack11llll111ll_opy_ == bstack11llll_opy_ (u"ࠤࡸࡲࡩ࡫ࡦࡪࡰࡨࡨࠧᤜ") and str(self.bstack11l1l1l11l_opy_).lower() == bstack11llll_opy_ (u"ࠥࡸࡷࡻࡥࠣᤝ"):
          self.bstack1ll11ll1l1_opy_ = True
        if bstack11llll_opy_ (u"ࠦࡹࡵ࡫ࡦࡰࠥᤞ") in data:
          return data[bstack11llll_opy_ (u"ࠧࡺ࡯࡬ࡧࡱࠦ᤟")]
        else:
          raise bstack11llll_opy_ (u"࠭ࡔࡰ࡭ࡨࡲࠥࡔ࡯ࡵࠢࡉࡳࡺࡴࡤࠡ࠯ࠣࡿࢂ࠭ᤠ").format(data)
      else:
        raise bstack11llll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡳࡩࡷࡩࡹࠡࡶࡲ࡯ࡪࡴࠬࠡࡔࡨࡷࡵࡵ࡮ࡴࡧࠣࡷࡹࡧࡴࡶࡵࠣ࠱ࠥࢁࡽ࠭ࠢࡕࡩࡸࡶ࡯࡯ࡵࡨࠤࡇࡵࡤࡺࠢ࠰ࠤࢀࢃࠢᤡ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack11llll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡳࡩࡷࡩࡹࠡࡲࡵࡳ࡯࡫ࡣࡵࠤᤢ").format(e))
  def bstack11lllll1lll_opy_(self):
    bstack11lllll1ll1_opy_ = os.path.join(tempfile.gettempdir(), bstack11llll_opy_ (u"ࠤࡳࡩࡷࡩࡹࡄࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠧᤣ"))
    try:
      if bstack11llll_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫᤤ") not in self.bstack11llll11l11_opy_:
        self.bstack11llll11l11_opy_[bstack11llll_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬᤥ")] = 2
      with open(bstack11lllll1ll1_opy_, bstack11llll_opy_ (u"ࠬࡽࠧᤦ")) as fp:
        json.dump(self.bstack11llll11l11_opy_, fp)
      return bstack11lllll1ll1_opy_
    except Exception as e:
      self.logger.error(bstack11llll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡦࡶࡪࡧࡴࡦࠢࡳࡩࡷࡩࡹࠡࡥࡲࡲ࡫࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨᤧ").format(e))
  def bstack11lll1ll1ll_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack11llllll1ll_opy_ == bstack11llll_opy_ (u"ࠧࡸ࡫ࡱࠫᤨ"):
        bstack11lllll1l11_opy_ = [bstack11llll_opy_ (u"ࠨࡥࡰࡨ࠳࡫ࡸࡦࠩᤩ"), bstack11llll_opy_ (u"ࠩ࠲ࡧࠬᤪ")]
        cmd = bstack11lllll1l11_opy_ + cmd
      cmd = bstack11llll_opy_ (u"ࠪࠤࠬᤫ").join(cmd)
      self.logger.debug(bstack11llll_opy_ (u"ࠦࡗࡻ࡮࡯࡫ࡱ࡫ࠥࢁࡽࠣ᤬").format(cmd))
      with open(self.bstack11lll1l11ll_opy_, bstack11llll_opy_ (u"ࠧࡧࠢ᤭")) as bstack11lll1ll11l_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack11lll1ll11l_opy_, text=True, stderr=bstack11lll1ll11l_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack11lll1lll1l_opy_ = True
      self.logger.error(bstack11llll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡲࡨࡶࡨࡿࠠࡸ࡫ࡷ࡬ࠥࡩ࡭ࡥࠢ࠰ࠤࢀࢃࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱ࠾ࠥࢁࡽࠣ᤮").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack11lll1l111l_opy_:
        self.logger.info(bstack11llll_opy_ (u"ࠢࡔࡶࡲࡴࡵ࡯࡮ࡨࠢࡓࡩࡷࡩࡹࠣ᤯"))
        cmd = [self.binary_path, bstack11llll_opy_ (u"ࠣࡧࡻࡩࡨࡀࡳࡵࡱࡳࠦᤰ")]
        self.bstack11lll1ll1ll_opy_(cmd)
        self.bstack11lll1l111l_opy_ = False
    except Exception as e:
      self.logger.error(bstack11llll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡰࡲࠣࡷࡪࡹࡳࡪࡱࡱࠤࡼ࡯ࡴࡩࠢࡦࡳࡲࡳࡡ࡯ࡦࠣ࠱ࠥࢁࡽ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠤᤱ").format(cmd, e))
  def bstack1l111l1l1l_opy_(self):
    if not self.bstack11l1l1l11l_opy_:
      return
    try:
      bstack11llll1ll1l_opy_ = 0
      while not self.bstack11lll1l111l_opy_ and bstack11llll1ll1l_opy_ < self.bstack11lll11ll11_opy_:
        if self.bstack11lll1lll1l_opy_:
          self.logger.info(bstack11llll_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡶࡩࡹࡻࡰࠡࡨࡤ࡭ࡱ࡫ࡤࠣᤲ"))
          return
        time.sleep(1)
        bstack11llll1ll1l_opy_ += 1
      os.environ[bstack11llll_opy_ (u"ࠫࡕࡋࡒࡄ࡛ࡢࡆࡊ࡙ࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࠪᤳ")] = str(self.bstack11llll1l1ll_opy_())
      self.logger.info(bstack11llll_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡸ࡫ࡴࡶࡲࠣࡧࡴࡳࡰ࡭ࡧࡷࡩࡩࠨᤴ"))
    except Exception as e:
      self.logger.error(bstack11llll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡩࡹࡻࡰࠡࡲࡨࡶࡨࡿࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢᤵ").format(e))
  def bstack11llll1l1ll_opy_(self):
    if self.bstack11lllllll_opy_:
      return
    try:
      bstack11lll1ll1l1_opy_ = [platform[bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬᤶ")].lower() for platform in self.config.get(bstack11llll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᤷ"), [])]
      bstack11lllll11ll_opy_ = sys.maxsize
      bstack11lll11lll1_opy_ = bstack11llll_opy_ (u"ࠩࠪᤸ")
      for browser in bstack11lll1ll1l1_opy_:
        if browser in self.bstack11lll1l11l1_opy_:
          bstack11lll1lllll_opy_ = self.bstack11lll1l11l1_opy_[browser]
        if bstack11lll1lllll_opy_ < bstack11lllll11ll_opy_:
          bstack11lllll11ll_opy_ = bstack11lll1lllll_opy_
          bstack11lll11lll1_opy_ = browser
      return bstack11lll11lll1_opy_
    except Exception as e:
      self.logger.error(bstack11llll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪࡰࡧࠤࡧ࡫ࡳࡵࠢࡳࡰࡦࡺࡦࡰࡴࡰ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀ᤹ࠦ").format(e))
  @classmethod
  def bstack11ll11llll_opy_(self):
    return os.getenv(bstack11llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࠩ᤺"), bstack11llll_opy_ (u"ࠬࡌࡡ࡭ࡵࡨ᤻ࠫ")).lower()
  @classmethod
  def bstack11111l1l1_opy_(self):
    return os.getenv(bstack11llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡅࡓࡅ࡜ࡣࡈࡇࡐࡕࡗࡕࡉࡤࡓࡏࡅࡇࠪ᤼"), bstack11llll_opy_ (u"ࠧࠨ᤽"))