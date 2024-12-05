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
from collections import defaultdict
from threading import Lock
from dataclasses import dataclass
import logging
import traceback
from typing import List, Dict, Any
import threading
@dataclass
class bstack11lll1111l_opy_:
    sdk_version: str
    path_config: str
    path_project: str
    test_framework: str
    frameworks: List[str]
    framework_versions: Dict[str, str]
    bs_config: Dict[str, Any]
@dataclass
class bstack11lllll11_opy_:
    pass
class Events:
    bstack11lllll1ll_opy_ = bstack11llll_opy_ (u"ࠥࡦࡴࡵࡴࡴࡶࡵࡥࡵࠨ࿭")
    CONNECT = bstack11llll_opy_ (u"ࠦࡨࡵ࡮࡯ࡧࡦࡸࠧ࿮")
    bstack1ll1ll1l1l_opy_ = bstack11llll_opy_ (u"ࠧࡹࡨࡶࡶࡧࡳࡼࡴࠢ࿯")
    CONFIG = bstack11llll_opy_ (u"ࠨࡣࡰࡰࡩ࡭࡬ࠨ࿰")
    bstack11111l1111_opy_ = bstack11llll_opy_ (u"ࠢࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡶࠦ࿱")
class bstack111111ll1l_opy_:
    bstack1111llll11_opy_ = bstack11llll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠣ࿲")
    FINISHED = bstack11llll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࠥ࿳")
class bstack1111ll1lll_opy_:
    bstack1111llll11_opy_ = bstack11llll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡴࡸࡲࡤࡹࡴࡢࡴࡷࡩࡩࠨ࿴")
    FINISHED = bstack11llll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤࠣ࿵")
class bstack11111l111l_opy_:
    bstack1111llll11_opy_ = bstack11llll_opy_ (u"ࠧ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠣ࿶")
    FINISHED = bstack11llll_opy_ (u"ࠨࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࠥ࿷")
class bstack111111lll1_opy_:
    bstack11111l11l1_opy_ = bstack11llll_opy_ (u"ࠢࡤࡤࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡩࡲࡦࡣࡷࡩࡩࠨ࿸")
class bstack111111ll11_opy_:
    _111111llll_opy_ = None
    def __new__(cls):
        if not cls._111111llll_opy_:
            cls._111111llll_opy_ = super(bstack111111ll11_opy_, cls).__new__(cls)
        return cls._111111llll_opy_
    def __init__(self):
        self._hooks = defaultdict(list)
        self._lock = Lock()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def clear(self):
        with self._lock:
            self._hooks = defaultdict(list)
    def register(self, event_name, callback):
        with self._lock:
            if not callable(callback):
                raise ValueError(bstack11llll_opy_ (u"ࠣࡅࡤࡰࡱࡨࡡࡤ࡭ࠣࡶࡪࡷࡵࡪࡴࡨࡨࠥ࡬࡯ࡳࠢࠥ࿹") + event_name)
            self.logger.debug(bstack11llll_opy_ (u"ࠤࡵࡩ࡬࡯ࡳࡵࡧࡵࡩࡩࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫ࠡࡽࡨࡺࡪࡴࡴࡠࡰࡤࡱࡪࢃࠠࠣ࿺") + str(threading.get_ident()) + bstack11llll_opy_ (u"ࠥࠦ࿻"))
            self._hooks[event_name].append(callback)
    def invoke(self, event_name, *args, **kwargs):
        with self._lock:
            callbacks = self._hooks.get(event_name, [])
            if not callbacks:
                return
            self.logger.debug(bstack11llll_opy_ (u"ࠦ࡮ࡴࡶࡰ࡭࡬ࡲ࡬ࠦࡻ࡭ࡧࡱࠬࡨࡧ࡬࡭ࡤࡤࡧࡰࡹࠩࡾࠢࡦࡥࡱࡲࡢࡢࡥ࡮ࡷࠥ࡬࡯ࡳࠢࡨࡺࡪࡴࡴࠡࠩࠥ࿼") + str(event_name) + bstack11llll_opy_ (u"ࠧ࠭ࠢ࿽"))
            for callback in callbacks:
                try:
                    self.logger.debug(bstack11llll_opy_ (u"ࠨࡩ࡯ࡸࡲ࡯ࡪࡪࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬ࠢࡩࡳࡷࠦࡥࡷࡧࡱࡸࠥ࠭ࡻࡦࡸࡨࡲࡹࡥ࡮ࡢ࡯ࡨࢁࠬࠦࠢ࿾") + str(threading.get_ident()) + bstack11llll_opy_ (u"ࠢࠣ࿿"))
                    callback(event_name, *args, **kwargs)
                except Exception as e:
                    self.logger.error(bstack11llll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࡹࡳࡰ࡯࡮ࡨࠢࡦࡥࡱࡲࡢࡢࡥ࡮ࠤ࡫ࡵࡲࠡࡧࡹࡩࡳࡺࠠࠨࡽࡨࡺࡪࡴࡴࡠࡰࡤࡱࡪࢃࠧ࠻ࠢࠥက") + str(e) + bstack11llll_opy_ (u"ࠤࠥခ"))
                    traceback.print_exc()
bstack1lll1ll11l_opy_ = bstack111111ll11_opy_()