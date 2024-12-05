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
import sys
import logging
import tarfile
import io
import os
import time
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack1l1ll1l11l1_opy_, bstack1l1ll11l1l1_opy_
import tempfile
import json
bstack1l1111llll1_opy_ = os.getenv(bstack11llll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡊࡣࡋࡏࡌࡆࠤᡞ"), None) or os.path.join(tempfile.gettempdir(), bstack11llll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡦࡨࡦࡺ࡭࠮࡭ࡱࡪࠦᡟ"))
bstack1l1111l1ll1_opy_ = os.path.join(bstack11llll_opy_ (u"ࠥࡰࡴ࡭ࠢᡠ"), bstack11llll_opy_ (u"ࠫࡸࡪ࡫࠮ࡥ࡯࡭࠲ࡪࡥࡣࡷࡪ࠲ࡱࡵࡧࠨᡡ"))
logging.Formatter.converter = time.gmtime
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack11llll_opy_ (u"ࠬࠫࠨࡢࡵࡦࡸ࡮ࡳࡥࠪࡵࠣ࡟ࠪ࠮࡮ࡢ࡯ࡨ࠭ࡸࡣ࡛ࠦࠪ࡯ࡩࡻ࡫࡬࡯ࡣࡰࡩ࠮ࡹ࡝ࠡ࠯ࠣࠩ࠭ࡳࡥࡴࡵࡤ࡫ࡪ࠯ࡳࠨᡢ"),
      datefmt=bstack11llll_opy_ (u"࡚࠭ࠥ࠯ࠨࡱ࠲ࠫࡤࡕࠧࡋ࠾ࠪࡓ࠺ࠦࡕ࡝ࠫᡣ"),
      stream=sys.stdout
    )
  return logger
def bstack1lllllll111_opy_():
  bstack1l1111ll111_opy_ = os.environ.get(bstack11llll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡊࡐࡄࡖ࡞ࡥࡄࡆࡄࡘࡋࠧᡤ"), bstack11llll_opy_ (u"ࠣࡨࡤࡰࡸ࡫ࠢᡥ"))
  return logging.DEBUG if bstack1l1111ll111_opy_.lower() == bstack11llll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢᡦ") else logging.INFO
def bstack1lll1l11111_opy_():
  global bstack1l1111llll1_opy_
  if os.path.exists(bstack1l1111llll1_opy_):
    os.remove(bstack1l1111llll1_opy_)
  if os.path.exists(bstack1l1111l1ll1_opy_):
    os.remove(bstack1l1111l1ll1_opy_)
def bstack111l1ll11_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def bstack1l1111111l_opy_(config, log_level):
  bstack1l1111lllll_opy_ = log_level
  if bstack11llll_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬᡧ") in config and config[bstack11llll_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭ᡨ")] in bstack1l1ll1l11l1_opy_:
    bstack1l1111lllll_opy_ = bstack1l1ll1l11l1_opy_[config[bstack11llll_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧᡩ")]]
  if config.get(bstack11llll_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁࡶࡶࡲࡇࡦࡶࡴࡶࡴࡨࡐࡴ࡭ࡳࠨᡪ"), False):
    logging.getLogger().setLevel(bstack1l1111lllll_opy_)
    return bstack1l1111lllll_opy_
  global bstack1l1111llll1_opy_
  bstack111l1ll11_opy_()
  bstack1l111l1111l_opy_ = logging.Formatter(
    fmt=bstack11llll_opy_ (u"ࠧࠦࠪࡤࡷࡨࡺࡩ࡮ࡧࠬࡷࠥࡡࠥࠩࡰࡤࡱࡪ࠯ࡳ࡞࡝ࠨࠬࡱ࡫ࡶࡦ࡮ࡱࡥࡲ࡫ࠩࡴ࡟ࠣ࠱ࠥࠫࠨ࡮ࡧࡶࡷࡦ࡭ࡥࠪࡵࠪᡫ"),
    datefmt=bstack11llll_opy_ (u"ࠨࠧ࡜࠱ࠪࡳ࠭ࠦࡦࡗࠩࡍࡀࠥࡎ࠼ࠨࡗ࡟࠭ᡬ"),
  )
  bstack1l1111l1l1l_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack1l1111llll1_opy_)
  file_handler.setFormatter(bstack1l111l1111l_opy_)
  bstack1l1111l1l1l_opy_.setFormatter(bstack1l111l1111l_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack1l1111l1l1l_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack11llll_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࠲ࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸ࠮ࡳࡧࡰࡳࡹ࡫࠮ࡳࡧࡰࡳࡹ࡫࡟ࡤࡱࡱࡲࡪࡩࡴࡪࡱࡱࠫᡭ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack1l1111l1l1l_opy_.setLevel(bstack1l1111lllll_opy_)
  logging.getLogger().addHandler(bstack1l1111l1l1l_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack1l1111lllll_opy_
def bstack1l1111ll11l_opy_(config):
  try:
    bstack1l111l11111_opy_ = set(bstack1l1ll11l1l1_opy_)
    bstack1l1111l1lll_opy_ = bstack11llll_opy_ (u"ࠪࠫᡮ")
    with open(bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡲࡲࠧᡯ")) as bstack1l1111ll1l1_opy_:
      bstack1l1111l11ll_opy_ = bstack1l1111ll1l1_opy_.read()
      bstack1l1111l1lll_opy_ = re.sub(bstack11llll_opy_ (u"ࡷ࠭࡞ࠩ࡞ࡶ࠯࠮ࡅࠣ࠯ࠬࠧࡠࡳ࠭ᡰ"), bstack11llll_opy_ (u"࠭ࠧᡱ"), bstack1l1111l11ll_opy_, flags=re.M)
      bstack1l1111l1lll_opy_ = re.sub(
        bstack11llll_opy_ (u"ࡲࠨࡠࠫࡠࡸ࠱ࠩࡀࠪࠪᡲ") + bstack11llll_opy_ (u"ࠨࡾࠪᡳ").join(bstack1l111l11111_opy_) + bstack11llll_opy_ (u"ࠩࠬ࠲࠯ࠪࠧᡴ"),
        bstack11llll_opy_ (u"ࡵࠫࡡ࠸࠺ࠡ࡝ࡕࡉࡉࡇࡃࡕࡇࡇࡡࠬᡵ"),
        bstack1l1111l1lll_opy_, flags=re.M | re.I
      )
    def bstack1l1111ll1ll_opy_(dic):
      bstack1l1111lll1l_opy_ = {}
      for key, value in dic.items():
        if key in bstack1l111l11111_opy_:
          bstack1l1111lll1l_opy_[key] = bstack11llll_opy_ (u"ࠫࡠࡘࡅࡅࡃࡆࡘࡊࡊ࡝ࠨᡶ")
        else:
          if isinstance(value, dict):
            bstack1l1111lll1l_opy_[key] = bstack1l1111ll1ll_opy_(value)
          else:
            bstack1l1111lll1l_opy_[key] = value
      return bstack1l1111lll1l_opy_
    bstack1l1111lll1l_opy_ = bstack1l1111ll1ll_opy_(config)
    return {
      bstack11llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡳ࡬ࠨᡷ"): bstack1l1111l1lll_opy_,
      bstack11llll_opy_ (u"࠭ࡦࡪࡰࡤࡰࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩᡸ"): json.dumps(bstack1l1111lll1l_opy_)
    }
  except Exception as e:
    return {}
def bstack1ll1ll11_opy_(config):
  global bstack1l1111llll1_opy_
  try:
    if config.get(bstack11llll_opy_ (u"ࠧࡥ࡫ࡶࡥࡧࡲࡥࡂࡷࡷࡳࡈࡧࡰࡵࡷࡵࡩࡑࡵࡧࡴࠩ᡹"), False):
      return
    uuid = os.getenv(bstack11llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭᡺"))
    if not uuid or uuid == bstack11llll_opy_ (u"ࠩࡱࡹࡱࡲࠧ᡻"):
      return
    bstack1l1111lll11_opy_ = [bstack11llll_opy_ (u"ࠪࡶࡪࡷࡵࡪࡴࡨࡱࡪࡴࡴࡴ࠰ࡷࡼࡹ࠭᡼"), bstack11llll_opy_ (u"ࠫࡕ࡯ࡰࡧ࡫࡯ࡩࠬ᡽"), bstack11llll_opy_ (u"ࠬࡶࡹࡱࡴࡲ࡮ࡪࡩࡴ࠯ࡶࡲࡱࡱ࠭᡾"), bstack1l1111llll1_opy_, bstack1l1111l1ll1_opy_]
    bstack111l1ll11_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstack11llll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࠳࡬ࡰࡩࡶ࠱ࠬ᡿") + uuid + bstack11llll_opy_ (u"ࠧ࠯ࡶࡤࡶ࠳࡭ࡺࠨᢀ"))
    with tarfile.open(output_file, bstack11llll_opy_ (u"ࠣࡹ࠽࡫ࡿࠨᢁ")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack1l1111lll11_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack1l1111ll11l_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack1l1111l1l11_opy_ = data.encode()
        tarinfo.size = len(bstack1l1111l1l11_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack1l1111l1l11_opy_))
    multipart_data = MultipartEncoder(
      fields= {
        bstack11llll_opy_ (u"ࠩࡧࡥࡹࡧࠧᢂ"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack11llll_opy_ (u"ࠪࡶࡧ࠭ᢃ")), bstack11llll_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱ࡻ࠱࡬ࢀࡩࡱࠩᢄ")),
        bstack11llll_opy_ (u"ࠬࡩ࡬ࡪࡧࡱࡸࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧᢅ"): uuid
      }
    )
    response = requests.post(
      bstack11llll_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࡶࡲ࡯ࡳࡦࡪ࠭ࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡧࡱ࡯ࡥ࡯ࡶ࠰ࡰࡴ࡭ࡳ࠰ࡷࡳࡰࡴࡧࡤࠣᢆ"),
      data=multipart_data,
      headers={bstack11llll_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭ᢇ"): multipart_data.content_type},
      auth=(config[bstack11llll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪᢈ")], config[bstack11llll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬᢉ")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack11llll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡸࡴࡱࡵࡡࡥࠢ࡯ࡳ࡬ࡹ࠺ࠡࠩᢊ") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack11llll_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡪࡴࡤࡪࡰࡪࠤࡱࡵࡧࡴ࠼ࠪᢋ") + str(e))
  finally:
    try:
      bstack1lll1l11111_opy_()
    except:
      pass