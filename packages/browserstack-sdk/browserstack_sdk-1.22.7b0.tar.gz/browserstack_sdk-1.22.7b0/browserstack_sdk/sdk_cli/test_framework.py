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
import logging
from enum import Enum
import os
import threading
import traceback
from typing import Dict, List, Any, Callable, Tuple, Union
import abc
from datetime import datetime, timezone
from dataclasses import dataclass
from browserstack_sdk.sdk_cli.bstack1111ll111l_opy_ import bstack1111l1llll_opy_, bstack1111l1l11l_opy_
class bstack1111l11111_opy_(Enum):
    bstack111l1llll1_opy_ = 0
    bstack111lll1l11_opy_ = 1
    def __repr__(self) -> str:
        return bstack11llll_opy_ (u"ࠢࡕࡧࡶࡸࡍࡵ࡯࡬ࡕࡷࡥࡹ࡫࠮ࡼࡿࠥᅝ").format(self.name)
class bstack1111l1lll1_opy_(Enum):
    NONE = 0
    bstack1ll1l1l1ll1_opy_ = 1
    LOG = 2
    bstack1lll1l11lll_opy_ = 3
    bstack1ll1l11l1ll_opy_ = 4
    bstack1ll1l111l1l_opy_ = 5
    bstack1ll1l111l11_opy_ = 6
    TEST = 7
    bstack1ll1l1l1l11_opy_ = 8
    bstack1ll1l1ll1l1_opy_ = 9
    bstack1ll1l11llll_opy_ = 10
    bstack1ll1lllll1l_opy_ = 11
    bstack1ll1l1l1111_opy_ = 12
    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented
    def __repr__(self) -> str:
        return bstack11llll_opy_ (u"ࠣࡖࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡔࡶࡤࡸࡪ࠴ࡻࡾࠤᅞ").format(self.name)
class bstack1111ll1111_opy_(bstack1111l1llll_opy_):
    bstack1ll1l11l1l1_opy_: List[str]
    bstack1ll11llll1l_opy_: Dict[str, str]
    state: bstack1111l1lll1_opy_
    bstack11111l1ll1_opy_: datetime
    bstack1ll1l1l1lll_opy_: datetime
    def __init__(
        self,
        context: bstack1111l1l11l_opy_,
        bstack1ll1l11l1l1_opy_: List[str],
        bstack1ll11llll1l_opy_: Dict[str, str],
        state=bstack1111l1lll1_opy_.NONE,
    ):
        super().__init__(context)
        self.bstack1ll1l11l1l1_opy_ = bstack1ll1l11l1l1_opy_
        self.bstack1ll11llll1l_opy_ = bstack1ll11llll1l_opy_
        self.state = state
        self.bstack11111l1ll1_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1ll1l1l1lll_opy_ = datetime.now(tz=timezone.utc)
    def bstack111l1l11ll_opy_(self, bstack1ll1l11ll11_opy_: bstack1111l1lll1_opy_):
        bstack1ll11llll11_opy_ = bstack1111l1lll1_opy_(bstack1ll1l11ll11_opy_).name
        if not bstack1ll11llll11_opy_:
            return False
        if bstack1ll1l11ll11_opy_ == self.state:
            return False
        self.state = bstack1ll1l11ll11_opy_
        self.bstack1ll1l1l1lll_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class bstack1ll1l1ll1ll_opy_:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class bstack1llll111lll_opy_:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1lll11l11ll_opy_ = bstack11llll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠧᅟ")
    bstack1111l1ll11_opy_ = bstack11llll_opy_ (u"ࠥࡸࡪࡹࡴࡠ࡫ࡧࠦᅠ")
    bstack1ll1ll1l11l_opy_ = bstack11llll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡱࡥࡲ࡫ࠢᅡ")
    bstack1ll1l1lll1l_opy_ = bstack11llll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪ࡮ࡲࡥࡠࡲࡤࡸ࡭ࠨᅢ")
    bstack1ll1l11lll1_opy_ = bstack11llll_opy_ (u"ࠨࡴࡦࡵࡷࡣࡹࡧࡧࡴࠤᅣ")
    bstack1ll1l1l11ll_opy_ = bstack11llll_opy_ (u"ࠢࡵࡧࡶࡸࡤࡸࡥࡴࡷ࡯ࡸࠧᅤ")
    bstack1ll1llll1ll_opy_ = bstack11llll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡲࡦࡵࡸࡰࡹࡥࡡࡵࠤᅥ")
    bstack1lll11l1l11_opy_ = bstack11llll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠦᅦ")
    bstack1lll111111l_opy_ = bstack11llll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡧࡱࡨࡪࡪ࡟ࡢࡶࠥᅧ")
    bstack1ll1l111lll_opy_ = bstack11llll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡯ࡳࡨࡧࡴࡪࡱࡱࠦᅨ")
    bstack1lll11l1l1l_opy_ = bstack11llll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࠦᅩ")
    bstack1lll1l1ll11_opy_ = bstack11llll_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣᅪ")
    bstack1ll1l11ll1l_opy_ = bstack11llll_opy_ (u"ࠢࡵࡧࡶࡸࡤࡩ࡯ࡥࡧࠥᅫ")
    bstack1ll1l1l11l1_opy_ = bstack11llll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡲࡦࡴࡸࡲࡤࡴࡡ࡮ࡧࠥᅬ")
    bstack111l11l111_opy_ = bstack11llll_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࠥᅭ")
    bstack1ll1l1l1l1l_opy_ = bstack11llll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨࡤ࡭ࡱࡻࡲࡦࠤᅮ")
    bstack1ll1l1ll111_opy_ = bstack11llll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠣᅯ")
    bstack1ll11lllll1_opy_ = bstack11llll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡰࡴ࡭ࡳࠣᅰ")
    bstack1ll11lll1ll_opy_ = bstack11llll_opy_ (u"ࠨࡥࡷࡧࡱࡸࡤࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠤᅱ")
    bstack1ll1l111111_opy_ = bstack11llll_opy_ (u"ࠢࡦࡸࡨࡲࡹࡥࡥ࡯ࡦࡨࡨࡤࡧࡴࠣᅲ")
    bstack1ll1l1111ll_opy_ = bstack11llll_opy_ (u"ࠣࡪࡲࡳࡰࡥࡩࡥࠤᅳ")
    bstack1ll1l1ll11l_opy_ = bstack11llll_opy_ (u"ࠤ࡫ࡳࡴࡱ࡟ࡳࡧࡶࡹࡱࡺࠢᅴ")
    bstack1ll1l1l111l_opy_ = bstack11llll_opy_ (u"ࠥ࡬ࡴࡵ࡫ࡠ࡮ࡲ࡫ࡸࠨᅵ")
    bstack1ll1l111ll1_opy_ = bstack11llll_opy_ (u"ࠦࡵ࡫࡮ࡥ࡫ࡱ࡫ࠧᅶ")
    bstack1ll1l11l11l_opy_ = bstack11llll_opy_ (u"ࠧࡶࡥ࡯ࡦ࡬ࡲ࡬ࠨᅷ")
    bstack1lll11ll1ll_opy_ = bstack11llll_opy_ (u"ࠨࡔࡆࡕࡗࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࠣᅸ")
    bstack1lll1l1l11l_opy_ = bstack11llll_opy_ (u"ࠢࡕࡇࡖࡘࡤࡒࡏࡈࠤᅹ")
    bstack1llllll1111_opy_: Dict[str, bstack1111ll1111_opy_] = dict()
    bstack1ll1l1111l1_opy_: Dict[str, List[Callable]] = dict()
    bstack1ll1l11l1l1_opy_: List[str]
    bstack1ll11llll1l_opy_: Dict[str, str]
    def __init__(
        self,
        bstack1ll1l11l1l1_opy_: List[str],
        bstack1ll11llll1l_opy_: Dict[str, str],
    ):
        self.bstack1ll1l11l1l1_opy_ = bstack1ll1l11l1l1_opy_
        self.bstack1ll11llll1l_opy_ = bstack1ll11llll1l_opy_
    def track_event(
        self,
        context: bstack1ll1l1ll1ll_opy_,
        test_framework_state: bstack1111l1lll1_opy_,
        test_hook_state: bstack1111l11111_opy_,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack11llll_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᅺ") + str(kwargs) + bstack11llll_opy_ (u"ࠤࠥᅻ"))
    def bstack1ll1l11111l_opy_(
        self,
        instance: bstack1111ll1111_opy_,
        bstack111l1l1l11_opy_: Tuple[bstack1111l1lll1_opy_, bstack1111l11111_opy_],
        *args,
        **kwargs,
    ):
        bstack1ll11llllll_opy_ = TestFramework.bstack1ll11lll1l1_opy_(bstack111l1l1l11_opy_)
        if not bstack1ll11llllll_opy_ in TestFramework.bstack1ll1l1111l1_opy_:
            return
        self.logger.debug(bstack11llll_opy_ (u"ࠥ࡭ࡳࡼ࡯࡬࡫ࡱ࡫ࠥࠨᅼ") + str(len(TestFramework.bstack1ll1l1111l1_opy_[bstack1ll11llllll_opy_])) + bstack11llll_opy_ (u"ࠦࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࡳࠣᅽ"))
        for callback in TestFramework.bstack1ll1l1111l1_opy_[bstack1ll11llllll_opy_]:
            try:
                callback(self, instance, bstack111l1l1l11_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack11llll_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠤ࡮ࡴࡶࡰ࡭࡬ࡲ࡬ࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫࠻ࠢࠥᅾ") + str(e) + bstack11llll_opy_ (u"ࠨࠢᅿ"))
                traceback.print_exc()
    @staticmethod
    def bstack1ll1ll111l1_opy_(target: object, strict=True):
        if target is None:
            return None
        ctx = bstack1111l1llll_opy_.create_context(target)
        instance = TestFramework.bstack1llllll1111_opy_.get(ctx.id, None)
        if instance and instance.bstack11111l1l11_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1lll111ll11_opy_(reverse=True) -> List[bstack1111ll1111_opy_]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.bstack1llllll1111_opy_.values(),
            ),
            key=lambda t: t.bstack11111l1ll1_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1lll1l1ll1l_opy_(ctx: bstack1111l1l11l_opy_, reverse=True) -> List[bstack1111ll1111_opy_]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.bstack1llllll1111_opy_.values(),
            ),
            key=lambda t: t.bstack11111l1ll1_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack111l11l1l1_opy_(instance: bstack1111ll1111_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack111lll1l1l_opy_(instance: bstack1111ll1111_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack111l1l11ll_opy_(instance: bstack1111ll1111_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack11llll_opy_ (u"ࠢࡴࡧࡷࡣࡸࡺࡡࡵࡧ࠽ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࡵࡩ࡫࠮ࠩࡾࠢ࡮ࡩࡾࡃࡻ࡬ࡧࡼࢁࠥࡼࡡ࡭ࡷࡨࡁࠧᆀ") + str(value) + bstack11llll_opy_ (u"ࠣࠤᆁ"))
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1ll1l11l111_opy_(instance: bstack1111ll1111_opy_, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack11llll_opy_ (u"ࠤࡶࡩࡹࡥࡳࡵࡣࡷࡩࡤ࡫࡮ࡵࡴ࡬ࡩࡸࡀࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥ࡫࡮ࡵࡴ࡬ࡩࡸࡃࠢᆂ") + str(entries) + bstack11llll_opy_ (u"ࠥࠦᆃ"))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack1ll1l1lll11_opy_(instance: bstack1111l1lll1_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack11llll_opy_ (u"ࠦࡺࡶࡤࡢࡶࡨࡣࡸࡺࡡࡵࡧ࠽ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࡵࡩ࡫࠮ࠩࡾࠢ࡮ࡩࡾࡃࡻ࡬ࡧࡼࢁࠥࡼࡡ࡭ࡷࡨࡁࠧᆄ") + str(value) + bstack11llll_opy_ (u"ࠧࠨᆅ"))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.bstack1ll1ll111l1_opy_(target, strict)
        return TestFramework.bstack111lll1l1l_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.bstack1ll1ll111l1_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1ll11lll1l1_opy_(bstack111l1l1l11_opy_: Tuple[bstack1111l1lll1_opy_, bstack1111l11111_opy_]):
        return bstack11llll_opy_ (u"ࠨ࠺ࠣᆆ").join((bstack1111l1lll1_opy_(bstack111l1l1l11_opy_[0]).name, bstack1111l11111_opy_(bstack111l1l1l11_opy_[1]).name))
    @staticmethod
    def bstack111l1l1l1l_opy_(bstack111l1l1l11_opy_: Tuple[bstack1111l1lll1_opy_, bstack1111l11111_opy_], callback: Callable):
        bstack1ll11llllll_opy_ = TestFramework.bstack1ll11lll1l1_opy_(bstack111l1l1l11_opy_)
        TestFramework.logger.debug(bstack11llll_opy_ (u"ࠢࡴࡧࡷࡣ࡭ࡵ࡯࡬ࡡࡦࡥࡱࡲࡢࡢࡥ࡮࠾ࠥ࡮࡯ࡰ࡭ࡢࡶࡪ࡭ࡩࡴࡶࡵࡽࡤࡱࡥࡺ࠿ࠥᆇ") + str(bstack1ll11llllll_opy_) + bstack11llll_opy_ (u"ࠣࠤᆈ"))
        if not bstack1ll11llllll_opy_ in TestFramework.bstack1ll1l1111l1_opy_:
            TestFramework.bstack1ll1l1111l1_opy_[bstack1ll11llllll_opy_] = []
        TestFramework.bstack1ll1l1111l1_opy_[bstack1ll11llllll_opy_].append(callback)
    @staticmethod
    def bstack1lll111ll1l_opy_(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack11llll_opy_ (u"ࠤࡥࡹ࡮ࡲࡴࡪࡰࡶࠦᆉ"):
            return klass.__qualname__
        return module + bstack11llll_opy_ (u"ࠥ࠲ࠧᆊ") + klass.__qualname__
    @staticmethod
    def bstack1lll11ll1l1_opy_(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}