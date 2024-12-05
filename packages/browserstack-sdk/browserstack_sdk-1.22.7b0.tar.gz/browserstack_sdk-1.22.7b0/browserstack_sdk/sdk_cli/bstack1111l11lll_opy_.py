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
from browserstack_sdk.sdk_cli.bstack111ll111l1_opy_ import bstack111l1lllll_opy_
from browserstack_sdk.sdk_cli.bstack111ll11ll1_opy_ import (
    bstack111ll1ll1l_opy_,
    bstack111ll1ll11_opy_,
    bstack11111l1lll_opy_,
    bstack111lll1ll1_opy_,
)
from browserstack_sdk.sdk_cli.bstack111ll1l1l1_opy_ import bstack111ll1l11l_opy_
from browserstack_sdk.sdk_cli.bstack1111ll111l_opy_ import bstack1111l1l11l_opy_
from typing import Tuple, Dict, Any, List, Callable
from browserstack_sdk.sdk_cli.bstack111ll111l1_opy_ import bstack111l1lllll_opy_
import weakref
class bstack11111llll1_opy_(bstack111l1lllll_opy_):
    bstack1111l11l11_opy_: str
    frameworks: List[str]
    drivers: Dict[str, Tuple[Callable, bstack111lll1ll1_opy_]]
    def __init__(self, bstack1111l11l11_opy_: str, frameworks: List[str]):
        super().__init__()
        self.drivers = dict()
        self.bstack1111l11l11_opy_ = bstack1111l11l11_opy_
        self.frameworks = frameworks
        if any(bstack111ll1l11l_opy_.NAME in f.lower().strip() for f in frameworks):
            bstack111ll1l11l_opy_.bstack111l1l1l1l_opy_(
                (bstack111ll1ll1l_opy_.bstack111ll1l1ll_opy_, bstack111ll1ll11_opy_.bstack111l1llll1_opy_), self.__11111ll1l1_opy_
            )
            bstack111ll1l11l_opy_.bstack111l1l1l1l_opy_(
                (bstack111ll1ll1l_opy_.QUIT, bstack111ll1ll11_opy_.bstack111lll1l11_opy_), self.__11111lll11_opy_
            )
    def __11111ll1l1_opy_(
        self,
        f: bstack111ll1l11l_opy_,
        driver: object,
        exec: Tuple[bstack111lll1ll1_opy_, str],
        bstack111l1l1l11_opy_: Tuple[bstack111ll1ll1l_opy_, bstack111ll1ll11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if instance.ref() in self.drivers or bstack11111l1lll_opy_.bstack111lll1l1l_opy_(instance, self.bstack1111l11l11_opy_, False):
            return
        if not f.bstack11111lll1l_opy_(f.hub_url(driver)):
            return
        self.drivers[instance.ref()] = weakref.ref(driver), instance
        bstack11111l1lll_opy_.bstack111l1l11ll_opy_(instance, self.bstack1111l11l11_opy_, True)
        self.logger.debug(bstack11llll_opy_ (u"ࠤࡢࡣࡴࡴ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡ࡬ࡲ࡮ࡺ࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦ࿥") + str(instance.ref()) + bstack11llll_opy_ (u"ࠥࠦ࿦"))
    def __11111lll11_opy_(
        self,
        f: bstack111ll1l11l_opy_,
        driver: object,
        exec: Tuple[bstack111lll1ll1_opy_, str],
        bstack111l1l1l11_opy_: Tuple[bstack111ll1ll1l_opy_, bstack111ll1ll11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if not instance.ref() in self.drivers:
            return
        self.bstack11111ll111_opy_(instance)
        self.logger.debug(bstack11llll_opy_ (u"ࠦࡤࡥ࡯࡯ࡡࡶࡩࡱ࡫࡮ࡪࡷࡰࡣࡶࡻࡩࡵ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨ࿧") + str(instance.ref()) + bstack11llll_opy_ (u"ࠧࠨ࿨"))
    def bstack1111l11l1l_opy_(self, context: bstack1111l1l11l_opy_, reverse=True) -> List[Tuple[Callable, bstack111lll1ll1_opy_]]:
        matches = []
        for data in self.drivers.values():
            if (
                bstack111ll1l11l_opy_.bstack1111l11ll1_opy_(data[1])
                and data[1].bstack11111ll1ll_opy_(context)
                and getattr(data[0](), bstack11llll_opy_ (u"ࠨࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠥ࿩"), False)
            ):
                matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack11111l1ll1_opy_, reverse=reverse)
    def bstack11111ll11l_opy_(self, instance: bstack111lll1ll1_opy_) -> bool:
        return instance and instance.ref() in self.drivers
    def bstack11111ll111_opy_(self, instance: bstack111lll1ll1_opy_) -> bool:
        if self.bstack11111ll11l_opy_(instance):
            self.drivers.pop(instance.ref())
            bstack11111l1lll_opy_.bstack111l1l11ll_opy_(instance, self.bstack1111l11l11_opy_, False)
            return True
        return False