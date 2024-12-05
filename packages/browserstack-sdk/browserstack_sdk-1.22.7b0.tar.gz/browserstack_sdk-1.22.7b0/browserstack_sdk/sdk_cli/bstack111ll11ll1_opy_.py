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
from typing import Dict, Tuple, Callable, Type, List, Any
import abc
from datetime import datetime, timezone, timedelta
from browserstack_sdk.sdk_cli.bstack1111ll111l_opy_ import bstack1111l1llll_opy_, bstack1111l1l11l_opy_
class bstack111ll1ll11_opy_(Enum):
    bstack111l1llll1_opy_ = 0
    bstack111lll1l11_opy_ = 1
    def __repr__(self) -> str:
        return bstack11llll_opy_ (u"ࠦࡍࡵ࡯࡬ࡕࡷࡥࡹ࡫࠮ࡼࡿࠥᆋ").format(self.name)
class bstack111ll1ll1l_opy_(Enum):
    NONE = 0
    bstack111l1ll111_opy_ = 1
    bstack111ll1l1ll_opy_ = 2
    bstack1ll11lll111_opy_ = 3
    QUIT = 4
    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented
    def __repr__(self) -> str:
        return bstack11llll_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡗࡹࡧࡴࡦ࠰ࡾࢁࠧᆌ").format(self.name)
class bstack111lll1ll1_opy_(bstack1111l1llll_opy_):
    framework_name: str
    framework_version: str
    state: bstack111ll1ll1l_opy_
    previous_state: bstack111ll1ll1l_opy_
    bstack11111l1ll1_opy_: datetime
    bstack1ll1l1l1lll_opy_: datetime
    def __init__(
        self,
        context: bstack1111l1l11l_opy_,
        framework_name: str,
        framework_version: str,
        state=bstack111ll1ll1l_opy_.NONE,
    ):
        super().__init__(context)
        self.framework_name = framework_name
        self.framework_version = framework_version
        self.state = state
        self.previous_state = bstack111ll1ll1l_opy_.NONE
        self.bstack11111l1ll1_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1ll1l1l1lll_opy_ = datetime.now(tz=timezone.utc)
    def bstack111l1l11ll_opy_(self, bstack1ll1l11ll11_opy_: bstack111ll1ll1l_opy_):
        bstack1ll11llll11_opy_ = bstack111ll1ll1l_opy_(bstack1ll1l11ll11_opy_).name
        if not bstack1ll11llll11_opy_:
            return False
        if bstack1ll1l11ll11_opy_ == self.state:
            return False
        if (
            bstack1ll1l11ll11_opy_ == bstack111ll1ll1l_opy_.NONE
            or (self.state != bstack111ll1ll1l_opy_.NONE and bstack1ll1l11ll11_opy_ == bstack111ll1ll1l_opy_.bstack111l1ll111_opy_)
            or (self.state < bstack111ll1ll1l_opy_.bstack111l1ll111_opy_ and bstack1ll1l11ll11_opy_ == bstack111ll1ll1l_opy_.bstack111ll1l1ll_opy_)
            or (self.state < bstack111ll1ll1l_opy_.bstack111l1ll111_opy_ and bstack1ll1l11ll11_opy_ == bstack111ll1ll1l_opy_.QUIT)
        ):
            raise ValueError(bstack11llll_opy_ (u"ࠨࡩ࡯ࡸࡤࡰ࡮ࡪࠠࡴࡶࡤࡸࡪࠦࡴࡳࡣࡱࡷ࡮ࡺࡩࡰࡰ࠽ࠤࠧᆍ") + str(self.state) + bstack11llll_opy_ (u"ࠢࠡ࠿ࡁࠤࠧᆎ") + str(bstack1ll1l11ll11_opy_))
        self.previous_state = self.state
        self.state = bstack1ll1l11ll11_opy_
        self.bstack1ll1l1l1lll_opy_ = datetime.now(tz=timezone.utc)
        return True
class bstack11111l1lll_opy_(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1llllll1111_opy_: Dict[str, bstack111lll1ll1_opy_] = dict()
    framework_name: str
    framework_version: str
    classes: List[Type]
    def __init__(
        self,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
    ):
        self.framework_name = framework_name
        self.framework_version = framework_version
        self.classes = classes
    @abc.abstractmethod
    def bstack1ll11ll1lll_opy_(self, instance: bstack111lll1ll1_opy_, method_name: str, bstack1ll11ll11l1_opy_: timedelta, *args, **kwargs):
        return
    @abc.abstractmethod
    def bstack1ll11ll1l1l_opy_(
        self, method_name, previous_state: bstack111ll1ll1l_opy_, *args, **kwargs
    ) -> bstack111ll1ll1l_opy_:
        return
    @abc.abstractmethod
    def bstack1ll11ll11ll_opy_(
        self,
        target: object,
        exec: Tuple[bstack111lll1ll1_opy_, str],
        bstack111l1l1l11_opy_: Tuple[bstack111ll1ll1l_opy_, bstack111ll1ll11_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable:
        return
    def bstack1ll11ll1111_opy_(self, bstack1ll11ll111l_opy_: List[str]):
        for clazz in self.classes:
            for method_name in bstack1ll11ll111l_opy_:
                bstack1ll11l1llll_opy_ = getattr(clazz, method_name, None)
                if not callable(bstack1ll11l1llll_opy_):
                    self.logger.warning(bstack11llll_opy_ (u"ࠣࡷࡱࡴࡦࡺࡣࡩࡧࡧࠤࡲ࡫ࡴࡩࡱࡧ࠾ࠥࠨᆏ") + str(method_name) + bstack11llll_opy_ (u"ࠤࠥᆐ"))
                    continue
                bstack1ll11lll11l_opy_ = self.bstack1ll11ll1l1l_opy_(
                    method_name, previous_state=bstack111ll1ll1l_opy_.NONE
                )
                bstack1ll11ll1l11_opy_ = self.bstack1ll11ll1ll1_opy_(
                    method_name,
                    (bstack1ll11lll11l_opy_ if bstack1ll11lll11l_opy_ else bstack111ll1ll1l_opy_.NONE),
                    bstack1ll11l1llll_opy_,
                )
                if not callable(bstack1ll11ll1l11_opy_):
                    self.logger.warning(bstack11llll_opy_ (u"ࠥࡱࡪࡺࡨࡰࡦࠣࡲࡴࡺࠠࡱࡣࡷࡧ࡭࡫ࡤ࠻ࠢࡾࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥࡾࠢࠫࡿࡸ࡫࡬ࡧ࠰ࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࢀ࠾ࠥࠨᆑ") + str(self.framework_version) + bstack11llll_opy_ (u"ࠦ࠮ࠨᆒ"))
                    continue
                setattr(clazz, method_name, bstack1ll11ll1l11_opy_)
    def bstack1ll11ll1ll1_opy_(
        self,
        method_name: str,
        bstack1ll11lll11l_opy_: bstack111ll1ll1l_opy_,
        bstack1ll11l1llll_opy_: Callable,
    ):
        def wrapped(target, *args, **kwargs):
            bstack111l1l1l1_opy_ = datetime.now()
            (bstack1ll11lll11l_opy_,) = wrapped.__vars__
            bstack1ll11lll11l_opy_ = (
                bstack1ll11lll11l_opy_
                if bstack1ll11lll11l_opy_ and bstack1ll11lll11l_opy_ != bstack111ll1ll1l_opy_.NONE
                else self.bstack1ll11ll1l1l_opy_(method_name, previous_state=bstack1ll11lll11l_opy_, *args, **kwargs)
            )
            if bstack1ll11lll11l_opy_ == bstack111ll1ll1l_opy_.bstack111l1ll111_opy_:
                ctx = bstack1111l1llll_opy_.create_context(target)
                bstack11111l1lll_opy_.bstack1llllll1111_opy_[ctx.id] = bstack111lll1ll1_opy_(
                    ctx, self.framework_name, self.framework_version, bstack1ll11lll11l_opy_
                )
                self.logger.debug(bstack11llll_opy_ (u"ࠧࡽࡲࡢࡲࡳࡩࡩࠦ࡭ࡦࡶ࡫ࡳࡩࠦࡣࡳࡧࡤࡸࡪࡪ࠺ࠡࡽࡷࡥࡷ࡭ࡥࡵ࠰ࡢࡣࡨࡲࡡࡴࡵࡢࡣࢂࠦ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࡁࢀࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࢀࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡧࡹࡾ࠽ࡼࡥࡷࡼ࠳࡯ࡤࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷࡂࠨᆓ") + str(bstack11111l1lll_opy_.bstack1llllll1111_opy_.keys()) + bstack11llll_opy_ (u"ࠨࠢᆔ"))
            else:
                self.logger.debug(bstack11llll_opy_ (u"ࠢࡸࡴࡤࡴࡵ࡫ࡤࠡ࡯ࡨࡸ࡭ࡵࡤࠡ࡫ࡱࡺࡴࡱࡥࡥ࠼ࠣࡿࡹࡧࡲࡨࡧࡷ࠲ࡤࡥࡣ࡭ࡣࡶࡷࡤࡥࡽࠡ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࡃࡻ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࢂࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳ࠾ࠤᆕ") + str(bstack11111l1lll_opy_.bstack1llllll1111_opy_.keys()) + bstack11llll_opy_ (u"ࠣࠤᆖ"))
            instance = bstack11111l1lll_opy_.bstack1ll1ll111l1_opy_(target)
            if bstack1ll11lll11l_opy_ == bstack111ll1ll1l_opy_.NONE or not instance:
                ctx = bstack1111l1llll_opy_.create_context(target)
                self.logger.warning(bstack11llll_opy_ (u"ࠤࡺࡶࡦࡶࡰࡦࡦࠣࡱࡪࡺࡨࡰࡦࠣࡹࡳࡺࡲࡢࡥ࡮ࡩࡩࡀࠠࡼ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࢃࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂࠦࡣࡵࡺࡀࡿࡨࡺࡸࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷࡂࠨᆗ") + str(bstack11111l1lll_opy_.bstack1llllll1111_opy_.keys()) + bstack11llll_opy_ (u"ࠥࠦᆘ"))
                return bstack1ll11l1llll_opy_(target, *args, **kwargs)
            bstack1111111l1l_opy_ = self.bstack1ll11ll11ll_opy_(
                target,
                (instance, method_name),
                (bstack1ll11lll11l_opy_, bstack111ll1ll11_opy_.bstack111l1llll1_opy_),
                None,
                *args,
                **kwargs,
            )
            if instance.bstack111l1l11ll_opy_(bstack1ll11lll11l_opy_):
                self.logger.debug(bstack11llll_opy_ (u"ࠦࡦࡶࡰ࡭࡫ࡨࡨࠥࡹࡴࡢࡶࡨ࠱ࡹࡸࡡ࡯ࡵ࡬ࡸ࡮ࡵ࡮࠻ࠢࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡶࡲࡦࡸ࡬ࡳࡺࡹ࡟ࡴࡶࡤࡸࡪࢃࠠ࠾ࡀࠣࡿ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࡳࡵࡣࡷࡩࢂࠦࠨࡼࡶࡼࡴࡪ࠮ࡴࡢࡴࡪࡩࡹ࠯ࡽ࠯ࡽࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫ࡽࠡࡽࡤࡶ࡬ࡹࡽࠪࠢ࡞ࠦᆙ") + str(instance.ref()) + bstack11llll_opy_ (u"ࠧࡣࠢᆚ"))
            result = (
                bstack1111111l1l_opy_(target, bstack1ll11l1llll_opy_, *args, **kwargs)
                if callable(bstack1111111l1l_opy_)
                else bstack1ll11l1llll_opy_(target, *args, **kwargs)
            )
            bstack1ll11l1lll1_opy_ = self.bstack1ll11ll11ll_opy_(
                target,
                (instance, method_name),
                (bstack1ll11lll11l_opy_, bstack111ll1ll11_opy_.bstack111lll1l11_opy_),
                result,
                *args,
                **kwargs,
            )
            self.bstack1ll11ll1lll_opy_(instance, method_name, datetime.now() - bstack111l1l1l1_opy_, *args, **kwargs)
            return bstack1ll11l1lll1_opy_ if bstack1ll11l1lll1_opy_ else result
        wrapped.__name__ = method_name
        wrapped.__vars__ = (bstack1ll11lll11l_opy_,)
        return wrapped
    @staticmethod
    def bstack1ll1ll111l1_opy_(target: object, strict=True):
        ctx = bstack1111l1llll_opy_.create_context(target)
        instance = bstack11111l1lll_opy_.bstack1llllll1111_opy_.get(ctx.id, None)
        if instance and instance.bstack11111l1l11_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1lll1l1ll1l_opy_(
        ctx: bstack1111l1l11l_opy_, state: bstack111ll1ll1l_opy_, reverse=True
    ) -> List[bstack111lll1ll1_opy_]:
        return sorted(
            filter(
                lambda t: t.state == state
                and t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                bstack11111l1lll_opy_.bstack1llllll1111_opy_.values(),
            ),
            key=lambda t: t.bstack11111l1ll1_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack111l11l1l1_opy_(instance: bstack111lll1ll1_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack111lll1l1l_opy_(instance: bstack111lll1ll1_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack111l1l11ll_opy_(instance: bstack111lll1ll1_opy_, key: str, value: Any) -> bool:
        instance.data[key] = value
        bstack11111l1lll_opy_.logger.debug(bstack11llll_opy_ (u"ࠨࡳࡦࡶࡢࡷࡹࡧࡴࡦ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡ࡭ࡨࡽࡂࢁ࡫ࡦࡻࢀࠤࡻࡧ࡬ࡶࡧࡀࠦᆛ") + str(value) + bstack11llll_opy_ (u"ࠢࠣᆜ"))
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = bstack11111l1lll_opy_.bstack1ll1ll111l1_opy_(target, strict)
        return bstack11111l1lll_opy_.bstack111lll1l1l_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = bstack11111l1lll_opy_.bstack1ll1ll111l1_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True