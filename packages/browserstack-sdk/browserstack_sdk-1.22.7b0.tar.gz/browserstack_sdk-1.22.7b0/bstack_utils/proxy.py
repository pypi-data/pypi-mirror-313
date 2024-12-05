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
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack1l1lll11lll_opy_
bstack1111l1l1_opy_ = Config.bstack111ll1ll_opy_()
def bstack1l1lll11l1l_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1l1lll1l1l1_opy_(bstack1l1lll1l1ll_opy_, bstack1l1lll1l111_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1l1lll1l1ll_opy_):
        with open(bstack1l1lll1l1ll_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1l1lll11l1l_opy_(bstack1l1lll1l1ll_opy_):
        pac = get_pac(url=bstack1l1lll1l1ll_opy_)
    else:
        raise Exception(bstack11llll_opy_ (u"ࠨࡒࡤࡧࠥ࡬ࡩ࡭ࡧࠣࡨࡴ࡫ࡳࠡࡰࡲࡸࠥ࡫ࡸࡪࡵࡷ࠾ࠥࢁࡽࠨች").format(bstack1l1lll1l1ll_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack11llll_opy_ (u"ࠤ࠻࠲࠽࠴࠸࠯࠺ࠥቾ"), 80))
        bstack1l1lll1l11l_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1l1lll1l11l_opy_ = bstack11llll_opy_ (u"ࠪ࠴࠳࠶࠮࠱࠰࠳ࠫቿ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1l1lll1l111_opy_, bstack1l1lll1l11l_opy_)
    return proxy_url
def bstack11lll1l1ll_opy_(config):
    return bstack11llll_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧኀ") in config or bstack11llll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩኁ") in config
def bstack11l1lll1l_opy_(config):
    if not bstack11lll1l1ll_opy_(config):
        return
    if config.get(bstack11llll_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩኂ")):
        return config.get(bstack11llll_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪኃ"))
    if config.get(bstack11llll_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬኄ")):
        return config.get(bstack11llll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ኅ"))
def bstack1ll111111_opy_(config, bstack1l1lll1l111_opy_):
    proxy = bstack11l1lll1l_opy_(config)
    proxies = {}
    if config.get(bstack11llll_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ኆ")) or config.get(bstack11llll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨኇ")):
        if proxy.endswith(bstack11llll_opy_ (u"ࠬ࠴ࡰࡢࡥࠪኈ")):
            proxies = bstack11l1ll1l11_opy_(proxy, bstack1l1lll1l111_opy_)
        else:
            proxies = {
                bstack11llll_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬ኉"): proxy
            }
    bstack1111l1l1_opy_.set_property(bstack11llll_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡙ࡥࡵࡶ࡬ࡲ࡬ࡹࠧኊ"), proxies)
    return proxies
def bstack11l1ll1l11_opy_(bstack1l1lll1l1ll_opy_, bstack1l1lll1l111_opy_):
    proxies = {}
    global bstack1l1lll1ll11_opy_
    if bstack11llll_opy_ (u"ࠨࡒࡄࡇࡤࡖࡒࡐ࡚࡜ࠫኋ") in globals():
        return bstack1l1lll1ll11_opy_
    try:
        proxy = bstack1l1lll1l1l1_opy_(bstack1l1lll1l1ll_opy_, bstack1l1lll1l111_opy_)
        if bstack11llll_opy_ (u"ࠤࡇࡍࡗࡋࡃࡕࠤኌ") in proxy:
            proxies = {}
        elif bstack11llll_opy_ (u"ࠥࡌ࡙࡚ࡐࠣኍ") in proxy or bstack11llll_opy_ (u"ࠦࡍ࡚ࡔࡑࡕࠥ኎") in proxy or bstack11llll_opy_ (u"࡙ࠧࡏࡄࡍࡖࠦ኏") in proxy:
            bstack1l1lll11ll1_opy_ = proxy.split(bstack11llll_opy_ (u"ࠨࠠࠣነ"))
            if bstack11llll_opy_ (u"ࠢ࠻࠱࠲ࠦኑ") in bstack11llll_opy_ (u"ࠣࠤኒ").join(bstack1l1lll11ll1_opy_[1:]):
                proxies = {
                    bstack11llll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨና"): bstack11llll_opy_ (u"ࠥࠦኔ").join(bstack1l1lll11ll1_opy_[1:])
                }
            else:
                proxies = {
                    bstack11llll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪን"): str(bstack1l1lll11ll1_opy_[0]).lower() + bstack11llll_opy_ (u"ࠧࡀ࠯࠰ࠤኖ") + bstack11llll_opy_ (u"ࠨࠢኗ").join(bstack1l1lll11ll1_opy_[1:])
                }
        elif bstack11llll_opy_ (u"ࠢࡑࡔࡒ࡜࡞ࠨኘ") in proxy:
            bstack1l1lll11ll1_opy_ = proxy.split(bstack11llll_opy_ (u"ࠣࠢࠥኙ"))
            if bstack11llll_opy_ (u"ࠤ࠽࠳࠴ࠨኚ") in bstack11llll_opy_ (u"ࠥࠦኛ").join(bstack1l1lll11ll1_opy_[1:]):
                proxies = {
                    bstack11llll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪኜ"): bstack11llll_opy_ (u"ࠧࠨኝ").join(bstack1l1lll11ll1_opy_[1:])
                }
            else:
                proxies = {
                    bstack11llll_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬኞ"): bstack11llll_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣኟ") + bstack11llll_opy_ (u"ࠣࠤአ").join(bstack1l1lll11ll1_opy_[1:])
                }
        else:
            proxies = {
                bstack11llll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨኡ"): proxy
            }
    except Exception as e:
        print(bstack11llll_opy_ (u"ࠥࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠢኢ"), bstack1l1lll11lll_opy_.format(bstack1l1lll1l1ll_opy_, str(e)))
    bstack1l1lll1ll11_opy_ = proxies
    return proxies