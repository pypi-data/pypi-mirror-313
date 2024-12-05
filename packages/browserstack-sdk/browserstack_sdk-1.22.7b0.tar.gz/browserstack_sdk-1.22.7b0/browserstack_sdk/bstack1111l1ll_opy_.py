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
import multiprocessing
import os
import json
from time import sleep
import bstack_utils.accessibility as bstack11111l11_opy_
from browserstack_sdk.bstack111llll1_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack1111l11l_opy_
class bstack11l11l11_opy_:
    def __init__(self, args, logger, bstack111lll1l_opy_, bstack1111l111_opy_):
        self.args = args
        self.logger = logger
        self.bstack111lll1l_opy_ = bstack111lll1l_opy_
        self.bstack1111l111_opy_ = bstack1111l111_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack111l1111_opy_ = []
        self.bstack1111ll1l_opy_ = None
        self.bstack111l1lll_opy_ = []
        self.bstack111111ll_opy_ = self.bstack111l1l1l_opy_()
        self.bstack111l11l1_opy_ = -1
    def bstack11l11111_opy_(self, bstack11l11l1l_opy_):
        self.parse_args()
        self.bstack1111llll_opy_()
        self.bstack111l1l11_opy_(bstack11l11l1l_opy_)
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack11111lll_opy_():
        import importlib
        if getattr(importlib, bstack11llll_opy_ (u"ࠫ࡫࡯࡮ࡥࡡ࡯ࡳࡦࡪࡥࡳࠩএ"), False):
            bstack11l111ll_opy_ = importlib.find_loader(bstack11llll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠧঐ"))
        else:
            bstack11l111ll_opy_ = importlib.util.find_spec(bstack11llll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠨ঑"))
    def bstack111ll11l_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack111l11l1_opy_ = -1
        if self.bstack1111l111_opy_ and bstack11llll_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ঒") in self.bstack111lll1l_opy_:
            self.bstack111l11l1_opy_ = int(self.bstack111lll1l_opy_[bstack11llll_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨও")])
        try:
            bstack111lllll_opy_ = [bstack11llll_opy_ (u"ࠩ࠰࠱ࡩࡸࡩࡷࡧࡵࠫঔ"), bstack11llll_opy_ (u"ࠪ࠱࠲ࡶ࡬ࡶࡩ࡬ࡲࡸ࠭ক"), bstack11llll_opy_ (u"ࠫ࠲ࡶࠧখ")]
            if self.bstack111l11l1_opy_ >= 0:
                bstack111lllll_opy_.extend([bstack11llll_opy_ (u"ࠬ࠳࠭࡯ࡷࡰࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭গ"), bstack11llll_opy_ (u"࠭࠭࡯ࠩঘ")])
            for arg in bstack111lllll_opy_:
                self.bstack111ll11l_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack1111llll_opy_(self):
        bstack1111ll1l_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack1111ll1l_opy_ = bstack1111ll1l_opy_
        return bstack1111ll1l_opy_
    def bstack1111lll1_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            self.bstack11111lll_opy_()
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack1111l11l_opy_)
    def bstack111l1l11_opy_(self, bstack11l11l1l_opy_):
        bstack1111l1l1_opy_ = Config.bstack111ll1ll_opy_()
        if bstack11l11l1l_opy_:
            self.bstack1111ll1l_opy_.append(bstack11llll_opy_ (u"ࠧ࠮࠯ࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫঙ"))
            self.bstack1111ll1l_opy_.append(bstack11llll_opy_ (u"ࠨࡖࡵࡹࡪ࠭চ"))
        if bstack1111l1l1_opy_.bstack11l1111l_opy_():
            self.bstack1111ll1l_opy_.append(bstack11llll_opy_ (u"ࠩ࠰࠱ࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨছ"))
            self.bstack1111ll1l_opy_.append(bstack11llll_opy_ (u"ࠪࡘࡷࡻࡥࠨজ"))
        self.bstack1111ll1l_opy_.append(bstack11llll_opy_ (u"ࠫ࠲ࡶࠧঝ"))
        self.bstack1111ll1l_opy_.append(bstack11llll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡴࡱࡻࡧࡪࡰࠪঞ"))
        self.bstack1111ll1l_opy_.append(bstack11llll_opy_ (u"࠭࠭࠮ࡦࡵ࡭ࡻ࡫ࡲࠨট"))
        self.bstack1111ll1l_opy_.append(bstack11llll_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧঠ"))
        if self.bstack111l11l1_opy_ > 1:
            self.bstack1111ll1l_opy_.append(bstack11llll_opy_ (u"ࠨ࠯ࡱࠫড"))
            self.bstack1111ll1l_opy_.append(str(self.bstack111l11l1_opy_))
    def bstack111111l1_opy_(self):
        bstack111l1lll_opy_ = []
        for spec in self.bstack111l1111_opy_:
            bstack111l11ll_opy_ = [spec]
            bstack111l11ll_opy_ += self.bstack1111ll1l_opy_
            bstack111l1lll_opy_.append(bstack111l11ll_opy_)
        self.bstack111l1lll_opy_ = bstack111l1lll_opy_
        return bstack111l1lll_opy_
    def bstack111l1l1l_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack111111ll_opy_ = True
            return True
        except Exception as e:
            self.bstack111111ll_opy_ = False
        return self.bstack111111ll_opy_
    def bstack11111ll1_opy_(self, bstack111ll1l1_opy_, bstack11l11111_opy_):
        bstack11l11111_opy_[bstack11llll_opy_ (u"ࠩࡆࡓࡓࡌࡉࡈࠩঢ")] = self.bstack111lll1l_opy_
        multiprocessing.set_start_method(bstack11llll_opy_ (u"ࠪࡷࡵࡧࡷ࡯ࠩণ"))
        bstack111ll111_opy_ = []
        manager = multiprocessing.Manager()
        bstack111l111l_opy_ = manager.list()
        if bstack11llll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧত") in self.bstack111lll1l_opy_:
            for index, platform in enumerate(self.bstack111lll1l_opy_[bstack11llll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨথ")]):
                bstack111ll111_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack111ll1l1_opy_,
                                                            args=(self.bstack1111ll1l_opy_, bstack11l11111_opy_, bstack111l111l_opy_)))
            bstack111lll11_opy_ = len(self.bstack111lll1l_opy_[bstack11llll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩদ")])
        else:
            bstack111ll111_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack111ll1l1_opy_,
                                                        args=(self.bstack1111ll1l_opy_, bstack11l11111_opy_, bstack111l111l_opy_)))
            bstack111lll11_opy_ = 1
        i = 0
        for t in bstack111ll111_opy_:
            os.environ[bstack11llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧধ")] = str(i)
            if bstack11llll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫন") in self.bstack111lll1l_opy_:
                os.environ[bstack11llll_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃࠪ঩")] = json.dumps(self.bstack111lll1l_opy_[bstack11llll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭প")][i % bstack111lll11_opy_])
            i += 1
            t.start()
        for t in bstack111ll111_opy_:
            t.join()
        return list(bstack111l111l_opy_)
    @staticmethod
    def bstack111l1ll1_opy_(driver, bstack1111ll11_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack11llll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨফ"), None)
        if item and getattr(item, bstack11llll_opy_ (u"ࠬࡥࡡ࠲࠳ࡼࡣࡹ࡫ࡳࡵࡡࡦࡥࡸ࡫ࠧব"), None) and not getattr(item, bstack11llll_opy_ (u"࠭࡟ࡢ࠳࠴ࡽࡤࡹࡴࡰࡲࡢࡨࡴࡴࡥࠨভ"), False):
            logger.info(
                bstack11llll_opy_ (u"ࠢࡂࡷࡷࡳࡲࡧࡴࡦࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡵ࡮ࠡࡪࡤࡷࠥ࡫࡮ࡥࡧࡧ࠲ࠥࡖࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡩࡳࡷࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡪࡵࠣࡹࡳࡪࡥࡳࡹࡤࡽ࠳ࠨম"))
            bstack11l111l1_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack11111l11_opy_.bstack11111l1l_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)