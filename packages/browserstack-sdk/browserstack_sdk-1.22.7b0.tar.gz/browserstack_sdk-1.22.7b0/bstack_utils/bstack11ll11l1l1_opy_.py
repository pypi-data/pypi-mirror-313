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
class bstack11lll111l1l_opy_(object):
  bstack11ll1ll11l_opy_ = os.path.join(os.path.expanduser(bstack11llll_opy_ (u"ࠨࢀࠪ᤾")), bstack11llll_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ᤿"))
  bstack11lll111ll1_opy_ = os.path.join(bstack11ll1ll11l_opy_, bstack11llll_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷ࠳ࡰࡳࡰࡰࠪ᥀"))
  commands_to_wrap = None
  perform_scan = None
  bstack1ll11lllll_opy_ = None
  bstack11l11l1ll1_opy_ = None
  bstack11lll111lll_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack11llll_opy_ (u"ࠫ࡮ࡴࡳࡵࡣࡱࡧࡪ࠭᥁")):
      cls.instance = super(bstack11lll111l1l_opy_, cls).__new__(cls)
      cls.instance.bstack11lll111l11_opy_()
    return cls.instance
  def bstack11lll111l11_opy_(self):
    try:
      with open(self.bstack11lll111ll1_opy_, bstack11llll_opy_ (u"ࠬࡸࠧ᥂")) as bstack11ll111l1l_opy_:
        bstack11lll11l11l_opy_ = bstack11ll111l1l_opy_.read()
        data = json.loads(bstack11lll11l11l_opy_)
        if bstack11llll_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳࠨ᥃") in data:
          self.bstack11lll11l1l1_opy_(data[bstack11llll_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࠩ᥄")])
        if bstack11llll_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࠩ᥅") in data:
          self.bstack11lll11l111_opy_(data[bstack11llll_opy_ (u"ࠩࡶࡧࡷ࡯ࡰࡵࡵࠪ᥆")])
    except:
      pass
  def bstack11lll11l111_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts[bstack11llll_opy_ (u"ࠪࡷࡨࡧ࡮ࠨ᥇")]
      self.bstack1ll11lllll_opy_ = scripts[bstack11llll_opy_ (u"ࠫ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࠨ᥈")]
      self.bstack11l11l1ll1_opy_ = scripts[bstack11llll_opy_ (u"ࠬ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࡕࡸࡱࡲࡧࡲࡺࠩ᥉")]
      self.bstack11lll111lll_opy_ = scripts[bstack11llll_opy_ (u"࠭ࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶࠫ᥊")]
  def bstack11lll11l1l1_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def store(self):
    try:
      with open(self.bstack11lll111ll1_opy_, bstack11llll_opy_ (u"ࠧࡸࠩ᥋")) as file:
        json.dump({
          bstack11llll_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡵࠥ᥌"): self.commands_to_wrap,
          bstack11llll_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࡵࠥ᥍"): {
            bstack11llll_opy_ (u"ࠥࡷࡨࡧ࡮ࠣ᥎"): self.perform_scan,
            bstack11llll_opy_ (u"ࠦ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࠣ᥏"): self.bstack1ll11lllll_opy_,
            bstack11llll_opy_ (u"ࠧ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࡕࡸࡱࡲࡧࡲࡺࠤᥐ"): self.bstack11l11l1ll1_opy_,
            bstack11llll_opy_ (u"ࠨࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶࠦᥑ"): self.bstack11lll111lll_opy_
          }
        }, file)
    except:
      pass
  def bstack1111l1ll1_opy_(self, bstack1lllllll1ll_opy_):
    try:
      return any(command.get(bstack11llll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᥒ")) == bstack1lllllll1ll_opy_ for command in self.commands_to_wrap)
    except:
      return False
bstack11ll11l1l1_opy_ = bstack11lll111l1l_opy_()