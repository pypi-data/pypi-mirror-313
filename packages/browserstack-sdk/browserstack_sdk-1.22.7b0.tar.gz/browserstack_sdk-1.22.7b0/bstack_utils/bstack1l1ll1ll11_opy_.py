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
import os
import threading
from bstack_utils.config import Config
from bstack_utils.helper import bstack1l1lll1lll1_opy_, bstack11l1l111l_opy_, bstack1ll111l1_opy_, bstack1l1111ll11_opy_, \
    bstack1l1lll1llll_opy_
def bstack11l11l1l1l_opy_(bstack1l1llll1111_opy_):
    for driver in bstack1l1llll1111_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack11l11l11ll_opy_(driver, status, reason=bstack11llll_opy_ (u"ࠬ࠭቉")):
    bstack1111l1l1_opy_ = Config.bstack111ll1ll_opy_()
    if bstack1111l1l1_opy_.bstack11l1111l_opy_():
        return
    bstack11l1lllll1_opy_ = bstack1l111lll11_opy_(bstack11llll_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩቊ"), bstack11llll_opy_ (u"ࠧࠨቋ"), status, reason, bstack11llll_opy_ (u"ࠨࠩቌ"), bstack11llll_opy_ (u"ࠩࠪቍ"))
    driver.execute_script(bstack11l1lllll1_opy_)
def bstack11ll111lll_opy_(page, status, reason=bstack11llll_opy_ (u"ࠪࠫ቎")):
    try:
        if page is None:
            return
        bstack1111l1l1_opy_ = Config.bstack111ll1ll_opy_()
        if bstack1111l1l1_opy_.bstack11l1111l_opy_():
            return
        bstack11l1lllll1_opy_ = bstack1l111lll11_opy_(bstack11llll_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧ቏"), bstack11llll_opy_ (u"ࠬ࠭ቐ"), status, reason, bstack11llll_opy_ (u"࠭ࠧቑ"), bstack11llll_opy_ (u"ࠧࠨቒ"))
        page.evaluate(bstack11llll_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤቓ"), bstack11l1lllll1_opy_)
    except Exception as e:
        print(bstack11llll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣࡪࡴࡸࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࢀࢃࠢቔ"), e)
def bstack1l111lll11_opy_(type, name, status, reason, bstack1ll11lll1_opy_, bstack1l11l1ll1l_opy_):
    bstack111l11l1l_opy_ = {
        bstack11llll_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪቕ"): type,
        bstack11llll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧቖ"): {}
    }
    if type == bstack11llll_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧ቗"):
        bstack111l11l1l_opy_[bstack11llll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩቘ")][bstack11llll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭቙")] = bstack1ll11lll1_opy_
        bstack111l11l1l_opy_[bstack11llll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫቚ")][bstack11llll_opy_ (u"ࠩࡧࡥࡹࡧࠧቛ")] = json.dumps(str(bstack1l11l1ll1l_opy_))
    if type == bstack11llll_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫቜ"):
        bstack111l11l1l_opy_[bstack11llll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧቝ")][bstack11llll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ቞")] = name
    if type == bstack11llll_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩ቟"):
        bstack111l11l1l_opy_[bstack11llll_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪበ")][bstack11llll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨቡ")] = status
        if status == bstack11llll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩቢ") and str(reason) != bstack11llll_opy_ (u"ࠥࠦባ"):
            bstack111l11l1l_opy_[bstack11llll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧቤ")][bstack11llll_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬብ")] = json.dumps(str(reason))
    bstack1l1ll11l11_opy_ = bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫቦ").format(json.dumps(bstack111l11l1l_opy_))
    return bstack1l1ll11l11_opy_
def bstack11llll11l_opy_(url, config, logger, bstack1llllll11l_opy_=False):
    hostname = bstack11l1l111l_opy_(url)
    is_private = bstack1l1111ll11_opy_(hostname)
    try:
        if is_private or bstack1llllll11l_opy_:
            file_path = bstack1l1lll1lll1_opy_(bstack11llll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧቧ"), bstack11llll_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧቨ"), logger)
            if os.environ.get(bstack11llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡏࡑࡗࡣࡘࡋࡔࡠࡇࡕࡖࡔࡘࠧቩ")) and eval(
                    os.environ.get(bstack11llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨቪ"))):
                return
            if (bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨቫ") in config and not config[bstack11llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩቬ")]):
                os.environ[bstack11llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫቭ")] = str(True)
                bstack1l1llll11ll_opy_ = {bstack11llll_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩቮ"): hostname}
                bstack1l1lll1llll_opy_(bstack11llll_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧቯ"), bstack11llll_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧተ"), bstack1l1llll11ll_opy_, logger)
    except Exception as e:
        pass
def bstack111ll1lll_opy_(caps, bstack1l1lll1ll1l_opy_):
    if bstack11llll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫቱ") in caps:
        caps[bstack11llll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬቲ")][bstack11llll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࠫታ")] = True
        if bstack1l1lll1ll1l_opy_:
            caps[bstack11llll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧቴ")][bstack11llll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩት")] = bstack1l1lll1ll1l_opy_
    else:
        caps[bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱ࠭ቶ")] = True
        if bstack1l1lll1ll1l_opy_:
            caps[bstack11llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪቷ")] = bstack1l1lll1ll1l_opy_
def bstack1l1llll11l1_opy_(bstack11lll111_opy_):
    bstack1l1llll111l_opy_ = bstack1ll111l1_opy_(threading.current_thread(), bstack11llll_opy_ (u"ࠪࡸࡪࡹࡴࡔࡶࡤࡸࡺࡹࠧቸ"), bstack11llll_opy_ (u"ࠫࠬቹ"))
    if bstack1l1llll111l_opy_ == bstack11llll_opy_ (u"ࠬ࠭ቺ") or bstack1l1llll111l_opy_ == bstack11llll_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧቻ"):
        threading.current_thread().testStatus = bstack11lll111_opy_
    else:
        if bstack11lll111_opy_ == bstack11llll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧቼ"):
            threading.current_thread().testStatus = bstack11lll111_opy_