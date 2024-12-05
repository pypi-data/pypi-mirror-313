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
import re
from bstack_utils.bstack1l1ll1ll11_opy_ import bstack1l1llll11l1_opy_
def bstack1l1l1l1l1l1_opy_(fixture_name):
    if fixture_name.startswith(bstack11llll_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᗐ")):
        return bstack11llll_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᗑ")
    elif fixture_name.startswith(bstack11llll_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᗒ")):
        return bstack11llll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭࡮ࡱࡧࡹࡱ࡫ࠧᗓ")
    elif fixture_name.startswith(bstack11llll_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᗔ")):
        return bstack11llll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᗕ")
    elif fixture_name.startswith(bstack11llll_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᗖ")):
        return bstack11llll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭࡮ࡱࡧࡹࡱ࡫ࠧᗗ")
def bstack1l1l1l1ll11_opy_(fixture_name):
    return bool(re.match(bstack11llll_opy_ (u"࠭࡞ࡠࡺࡸࡲ࡮ࡺ࡟ࠩࡵࡨࡸࡺࡶࡼࡵࡧࡤࡶࡩࡵࡷ࡯ࠫࡢࠬ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࢂ࡭ࡰࡦࡸࡰࡪ࠯࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫᗘ"), fixture_name))
def bstack1l1l1l1l1ll_opy_(fixture_name):
    return bool(re.match(bstack11llll_opy_ (u"ࠧ࡟ࡡࡻࡹࡳ࡯ࡴࡠࠪࡶࡩࡹࡻࡰࡽࡶࡨࡥࡷࡪ࡯ࡸࡰࠬࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨᗙ"), fixture_name))
def bstack1l1l1l1llll_opy_(fixture_name):
    return bool(re.match(bstack11llll_opy_ (u"ࠨࡠࡢࡼࡺࡴࡩࡵࡡࠫࡷࡪࡺࡵࡱࡾࡷࡩࡦࡸࡤࡰࡹࡱ࠭ࡤࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨᗚ"), fixture_name))
def bstack1l1l1l1ll1l_opy_(fixture_name):
    if fixture_name.startswith(bstack11llll_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᗛ")):
        return bstack11llll_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫᗜ"), bstack11llll_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩᗝ")
    elif fixture_name.startswith(bstack11llll_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᗞ")):
        return bstack11llll_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬᗟ"), bstack11llll_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫᗠ")
    elif fixture_name.startswith(bstack11llll_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᗡ")):
        return bstack11llll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱ࠱࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ᗢ"), bstack11llll_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧᗣ")
    elif fixture_name.startswith(bstack11llll_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᗤ")):
        return bstack11llll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭࡮ࡱࡧࡹࡱ࡫ࠧᗥ"), bstack11llll_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡇࡌࡍࠩᗦ")
    return None, None
def bstack1l1l1l1l11l_opy_(hook_name):
    if hook_name in [bstack11llll_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ᗧ"), bstack11llll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪᗨ")]:
        return hook_name.capitalize()
    return hook_name
def bstack1l1l1ll111l_opy_(hook_name):
    if hook_name in [bstack11llll_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪᗩ"), bstack11llll_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠩᗪ")]:
        return bstack11llll_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩᗫ")
    elif hook_name in [bstack11llll_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫᗬ"), bstack11llll_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫᗭ")]:
        return bstack11llll_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫᗮ")
    elif hook_name in [bstack11llll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬᗯ"), bstack11llll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫᗰ")]:
        return bstack11llll_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧᗱ")
    elif hook_name in [bstack11llll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭ᗲ"), bstack11llll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸ࠭ᗳ")]:
        return bstack11llll_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡇࡌࡍࠩᗴ")
    return hook_name
def bstack1l1l1l1lll1_opy_(node, scenario):
    if hasattr(node, bstack11llll_opy_ (u"ࠧࡤࡣ࡯ࡰࡸࡶࡥࡤࠩᗵ")):
        parts = node.nodeid.rsplit(bstack11llll_opy_ (u"ࠣ࡝ࠥᗶ"))
        params = parts[-1]
        return bstack11llll_opy_ (u"ࠤࡾࢁࠥࡡࡻࡾࠤᗷ").format(scenario.name, params)
    return scenario.name
def bstack1l1l1ll11ll_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack11llll_opy_ (u"ࠪࡧࡦࡲ࡬ࡴࡲࡨࡧࠬᗸ")):
            examples = list(node.callspec.params[bstack11llll_opy_ (u"ࠫࡤࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡨࡼࡦࡳࡰ࡭ࡧࠪᗹ")].values())
        return examples
    except:
        return []
def bstack1l1l1ll11l1_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1l1l1ll1111_opy_(report):
    try:
        status = bstack11llll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᗺ")
        if report.passed or (report.failed and hasattr(report, bstack11llll_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣᗻ"))):
            status = bstack11llll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᗼ")
        elif report.skipped:
            status = bstack11llll_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᗽ")
        bstack1l1llll11l1_opy_(status)
    except:
        pass
def bstack1ll11llll_opy_(status):
    try:
        bstack1l1l1l1l111_opy_ = bstack11llll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᗾ")
        if status == bstack11llll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᗿ"):
            bstack1l1l1l1l111_opy_ = bstack11llll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᘀ")
        elif status == bstack11llll_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ᘁ"):
            bstack1l1l1l1l111_opy_ = bstack11llll_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᘂ")
        bstack1l1llll11l1_opy_(bstack1l1l1l1l111_opy_)
    except:
        pass
def bstack1l1l1ll1l11_opy_(item=None, report=None, summary=None, extra=None):
    return