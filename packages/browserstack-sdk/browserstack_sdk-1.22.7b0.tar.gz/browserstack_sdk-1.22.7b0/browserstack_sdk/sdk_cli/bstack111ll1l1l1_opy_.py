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
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack111ll11ll1_opy_ import (
    bstack11111l1lll_opy_,
    bstack111lll1ll1_opy_,
    bstack111ll1ll1l_opy_,
    bstack111ll1ll11_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
class bstack111ll1l11l_opy_(bstack11111l1lll_opy_):
    bstack1ll11l11ll1_opy_ = bstack11llll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠣᆝ")
    NAME = bstack11llll_opy_ (u"ࠤࡶࡩࡱ࡫࡮ࡪࡷࡰࠦᆞ")
    bstack1lll111l111_opy_ = bstack11llll_opy_ (u"ࠥ࡬ࡺࡨ࡟ࡶࡴ࡯ࠦᆟ")
    bstack1lll11l1ll1_opy_ = bstack11llll_opy_ (u"ࠦ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠦᆠ")
    bstack1ll11l1l1ll_opy_ = bstack11llll_opy_ (u"ࠧ࡯࡮ࡱࡷࡷࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥᆡ")
    bstack1ll111lllll_opy_ = bstack11llll_opy_ (u"ࠨࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᆢ")
    bstack1lll11lllll_opy_ = bstack11llll_opy_ (u"ࠢࡪࡵࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡ࡫ࡹࡧࠨᆣ")
    bstack1ll11l1ll1l_opy_ = bstack11llll_opy_ (u"ࠣࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠧᆤ")
    bstack1ll11l111l1_opy_ = bstack11llll_opy_ (u"ࠤࡨࡲࡩ࡫ࡤࡠࡣࡷࠦᆥ")
    bstack111l11l111_opy_ = bstack11llll_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࠦᆦ")
    bstack111l111l1l_opy_ = bstack11llll_opy_ (u"ࠦࡳ࡫ࡷࡴࡧࡶࡷ࡮ࡵ࡮ࠣᆧ")
    bstack1ll11l11l1l_opy_ = bstack11llll_opy_ (u"ࠧ࡭ࡥࡵࠤᆨ")
    bstack1ll1lll1l1l_opy_ = bstack11llll_opy_ (u"ࠨࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥᆩ")
    bstack1ll111lll1l_opy_ = bstack11llll_opy_ (u"ࠢࡸ࠵ࡦࡩࡽ࡫ࡣࡶࡶࡨࡷࡨࡸࡩࡱࡶࠥᆪ")
    bstack1ll11l1l111_opy_ = bstack11llll_opy_ (u"ࠣࡹ࠶ࡧࡪࡾࡥࡤࡷࡷࡩࡸࡩࡲࡪࡲࡷࡥࡸࡿ࡮ࡤࠤᆫ")
    bstack1ll11l1111l_opy_ = bstack11llll_opy_ (u"ࠤࡴࡹ࡮ࡺࠢᆬ")
    bstack1ll1l1111l1_opy_: Dict[str, List[Callable]] = dict()
    bstack111ll11111_opy_: str
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack111l1111ll_opy_: Any
    bstack1ll11l11lll_opy_: Dict
    def __init__(
        self,
        bstack111ll11111_opy_: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        bstack111l1111ll_opy_: Dict[str, Any],
        methods=[bstack11llll_opy_ (u"ࠥࡣࡤ࡯࡮ࡪࡶࡢࡣࠧᆭ"), bstack11llll_opy_ (u"ࠦࡸࡺࡡࡳࡶࡢࡷࡪࡹࡳࡪࡱࡱࠦᆮ"), bstack11llll_opy_ (u"ࠧ࡫ࡸࡦࡥࡸࡸࡪࠨᆯ"), bstack11llll_opy_ (u"ࠨࡱࡶ࡫ࡷࠦᆰ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.bstack111ll11111_opy_ = bstack111ll11111_opy_
        self.platform_index = platform_index
        self.bstack1ll11ll1111_opy_(methods)
        self.bstack111l1111ll_opy_ = bstack111l1111ll_opy_
    @staticmethod
    def session_id(target: object, strict=True):
        return bstack11111l1lll_opy_.get_data(bstack111ll1l11l_opy_.bstack1lll11l1ll1_opy_, target, strict)
    @staticmethod
    def hub_url(target: object, strict=True):
        return bstack11111l1lll_opy_.get_data(bstack111ll1l11l_opy_.bstack1lll111l111_opy_, target, strict)
    @staticmethod
    def bstack1ll11l111ll_opy_(target: object, strict=True):
        return bstack11111l1lll_opy_.get_data(bstack111ll1l11l_opy_.bstack1ll11l1l1ll_opy_, target, strict)
    @staticmethod
    def capabilities(target: object, strict=True):
        return bstack11111l1lll_opy_.get_data(bstack111ll1l11l_opy_.bstack1ll111lllll_opy_, target, strict)
    @staticmethod
    def bstack1111l11ll1_opy_(instance: bstack111lll1ll1_opy_) -> bool:
        return bstack11111l1lll_opy_.bstack111lll1l1l_opy_(instance, bstack111ll1l11l_opy_.bstack1lll11lllll_opy_, False)
    @staticmethod
    def bstack1ll1ll1llll_opy_(instance: bstack111lll1ll1_opy_, default_value=None):
        return bstack11111l1lll_opy_.bstack111lll1l1l_opy_(instance, bstack111ll1l11l_opy_.bstack1lll111l111_opy_, default_value)
    @staticmethod
    def bstack1ll1lll11ll_opy_(instance: bstack111lll1ll1_opy_, default_value=None):
        return bstack11111l1lll_opy_.bstack111lll1l1l_opy_(instance, bstack111ll1l11l_opy_.bstack1ll111lllll_opy_, default_value)
    @staticmethod
    def bstack11111lll1l_opy_(hub_url: str, bstack1ll11l11l11_opy_=bstack11llll_opy_ (u"ࠢ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠦᆱ")):
        try:
            bstack1ll111llll1_opy_ = str(urlparse(hub_url).netloc) if hub_url else None
            return bstack1ll111llll1_opy_.endswith(bstack1ll11l11l11_opy_)
        except:
            pass
        return False
    @staticmethod
    def bstack1ll1lll1lll_opy_(method_name: str):
        return method_name == bstack11llll_opy_ (u"ࠣࡧࡻࡩࡨࡻࡴࡦࠤᆲ")
    @staticmethod
    def bstack111l111l11_opy_(method_name: str, *args):
        return (
            bstack111ll1l11l_opy_.bstack1ll1lll1lll_opy_(method_name)
            and bstack111ll1l11l_opy_.bstack111l1111l1_opy_(*args) == bstack111ll1l11l_opy_.bstack111l111l1l_opy_
        )
    @staticmethod
    def bstack1ll1ll1ll1l_opy_(method_name: str, *args):
        if not bstack111ll1l11l_opy_.bstack1ll1lll1lll_opy_(method_name):
            return False
        if not bstack111ll1l11l_opy_.bstack1ll111lll1l_opy_ in bstack111ll1l11l_opy_.bstack111l1111l1_opy_(*args):
            return False
        bstack1111111l11_opy_ = bstack111ll1l11l_opy_.bstack1lllllllll1_opy_(*args)
        return bstack1111111l11_opy_ and bstack11llll_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤᆳ") in bstack1111111l11_opy_ and bstack11llll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦᆴ") in bstack1111111l11_opy_[bstack11llll_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦᆵ")]
    @staticmethod
    def bstack1ll1lll111l_opy_(method_name: str, *args):
        if not bstack111ll1l11l_opy_.bstack1ll1lll1lll_opy_(method_name):
            return False
        if not bstack111ll1l11l_opy_.bstack1ll111lll1l_opy_ in bstack111ll1l11l_opy_.bstack111l1111l1_opy_(*args):
            return False
        bstack1111111l11_opy_ = bstack111ll1l11l_opy_.bstack1lllllllll1_opy_(*args)
        return (
            bstack1111111l11_opy_
            and bstack11llll_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࠧᆶ") in bstack1111111l11_opy_
            and bstack11llll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡶࡧࡷ࡯ࡰࡵࠤᆷ") in bstack1111111l11_opy_[bstack11llll_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢᆸ")]
        )
    @staticmethod
    def bstack111l1111l1_opy_(*args):
        return str(bstack111ll1l11l_opy_.bstack111111111l_opy_(*args)).lower()
    @staticmethod
    def bstack111111111l_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1lllllllll1_opy_(*args):
        return args[1] if len(args) > 1 and isinstance(args[1], dict) else None
    @staticmethod
    def bstack1lll1l1l1l_opy_(driver):
        command_executor = getattr(driver, bstack11llll_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦᆹ"), None)
        if not command_executor:
            return None
        hub_url = str(command_executor) if isinstance(command_executor, (str, bytes)) else None
        hub_url = str(command_executor._url) if not hub_url and getattr(command_executor, bstack11llll_opy_ (u"ࠤࡢࡹࡷࡲࠢᆺ"), None) else None
        if not hub_url:
            client_config = getattr(command_executor, bstack11llll_opy_ (u"ࠥࡣࡨࡲࡩࡦࡰࡷࡣࡨࡵ࡮ࡧ࡫ࡪࠦᆻ"), None)
            if not client_config:
                return None
            hub_url = getattr(client_config, bstack11llll_opy_ (u"ࠦࡷ࡫࡭ࡰࡶࡨࡣࡸ࡫ࡲࡷࡧࡵࡣࡦࡪࡤࡳࠤᆼ"), None)
        return hub_url
    def bstack111l1ll11l_opy_(self, instance, driver, hub_url: str):
        result = False
        if not hub_url:
            return result
        command_executor = getattr(driver, bstack11llll_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣᆽ"), None)
        if command_executor:
            if isinstance(command_executor, (str, bytes)):
                setattr(driver, bstack11llll_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤᆾ"), hub_url)
                result = True
            elif hasattr(command_executor, bstack11llll_opy_ (u"ࠢࡠࡷࡵࡰࠧᆿ")):
                setattr(command_executor, bstack11llll_opy_ (u"ࠣࡡࡸࡶࡱࠨᇀ"), hub_url)
                result = True
        if result:
            self.bstack111ll11111_opy_ = hub_url
            bstack111ll1l11l_opy_.bstack111l1l11ll_opy_(instance, bstack111ll1l11l_opy_.bstack1lll111l111_opy_, hub_url)
            bstack111ll1l11l_opy_.bstack111l1l11ll_opy_(
                instance, bstack111ll1l11l_opy_.bstack1lll11lllll_opy_, bstack111ll1l11l_opy_.bstack11111lll1l_opy_(hub_url)
            )
        return result
    @staticmethod
    def bstack1ll11lll1l1_opy_(bstack111l1l1l11_opy_: Tuple[bstack111ll1ll1l_opy_, bstack111ll1ll11_opy_]):
        return bstack11llll_opy_ (u"ࠤ࠽ࠦᇁ").join((bstack111ll1ll1l_opy_(bstack111l1l1l11_opy_[0]).name, bstack111ll1ll11_opy_(bstack111l1l1l11_opy_[1]).name))
    @staticmethod
    def bstack111l1l1l1l_opy_(bstack111l1l1l11_opy_: Tuple[bstack111ll1ll1l_opy_, bstack111ll1ll11_opy_], callback: Callable):
        bstack1ll11llllll_opy_ = bstack111ll1l11l_opy_.bstack1ll11lll1l1_opy_(bstack111l1l1l11_opy_)
        if not bstack1ll11llllll_opy_ in bstack111ll1l11l_opy_.bstack1ll1l1111l1_opy_:
            bstack111ll1l11l_opy_.bstack1ll1l1111l1_opy_[bstack1ll11llllll_opy_] = []
        bstack111ll1l11l_opy_.bstack1ll1l1111l1_opy_[bstack1ll11llllll_opy_].append(callback)
    def bstack1ll11ll1lll_opy_(self, instance: bstack111lll1ll1_opy_, method_name: str, bstack1ll11ll11l1_opy_: timedelta, *args, **kwargs):
        if not instance or method_name in (bstack11llll_opy_ (u"ࠥࡷࡹࡧࡲࡵࡡࡶࡩࡸࡹࡩࡰࡰࠥᇂ")):
            return
        cmd = args[0] if method_name == bstack11llll_opy_ (u"ࠦࡪࡾࡥࡤࡷࡷࡩࠧᇃ") and args and type(args) in [list, tuple] and isinstance(args[0], str) else None
        bstack1ll11l1l1l1_opy_ = bstack11llll_opy_ (u"ࠧࡀࠢᇄ").join(map(str, filter(None, [method_name, cmd])))
        instance.bstack1ll1l1l11l_opy_(bstack11llll_opy_ (u"ࠨࡤࡳ࡫ࡹࡩࡷࡀࠢᇅ") + bstack1ll11l1l1l1_opy_, bstack1ll11ll11l1_opy_)
    def bstack1ll11ll11ll_opy_(
        self,
        target: object,
        exec: Tuple[bstack111lll1ll1_opy_, str],
        bstack111l1l1l11_opy_: Tuple[bstack111ll1ll1l_opy_, bstack111ll1ll11_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1ll11lll11l_opy_, bstack1ll11l1ll11_opy_ = bstack111l1l1l11_opy_
        bstack1ll11llllll_opy_ = bstack111ll1l11l_opy_.bstack1ll11lll1l1_opy_(bstack111l1l1l11_opy_)
        self.logger.debug(bstack11llll_opy_ (u"ࠢࡰࡰࡢ࡬ࡴࡵ࡫࠻ࠢࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫࠽ࡼ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࢃࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᇆ") + str(kwargs) + bstack11llll_opy_ (u"ࠣࠤᇇ"))
        if bstack1ll11lll11l_opy_ == bstack111ll1ll1l_opy_.bstack111l1ll111_opy_:
            if bstack1ll11l1ll11_opy_ == bstack111ll1ll11_opy_.bstack111lll1l11_opy_ and not bstack111ll1l11l_opy_.bstack1lll11l1ll1_opy_ in instance.data:
                session_id = getattr(target, bstack11llll_opy_ (u"ࠤࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠨᇈ"), None)
                if session_id:
                    instance.data[bstack111ll1l11l_opy_.bstack1lll11l1ll1_opy_] = session_id
        elif (
            bstack1ll11lll11l_opy_ == bstack111ll1ll1l_opy_.bstack111ll1l1ll_opy_
            and bstack111ll1l11l_opy_.bstack111l1111l1_opy_(*args) == bstack111ll1l11l_opy_.bstack111l111l1l_opy_
        ):
            if bstack1ll11l1ll11_opy_ == bstack111ll1ll11_opy_.bstack111l1llll1_opy_:
                hub_url = bstack111ll1l11l_opy_.bstack1lll1l1l1l_opy_(target)
                if hub_url:
                    instance.data.update(
                        {
                            bstack111ll1l11l_opy_.bstack1lll111l111_opy_: hub_url,
                            bstack111ll1l11l_opy_.bstack1lll11lllll_opy_: bstack111ll1l11l_opy_.bstack11111lll1l_opy_(hub_url),
                            bstack111ll1l11l_opy_.bstack111l11l111_opy_: int(
                                os.environ.get(bstack11llll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠥᇉ"), str(self.platform_index))
                            ),
                        }
                    )
                bstack1111111l11_opy_ = bstack111ll1l11l_opy_.bstack1lllllllll1_opy_(*args)
                bstack1ll11l111ll_opy_ = bstack1111111l11_opy_.get(bstack11llll_opy_ (u"ࠦࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥᇊ"), None) if bstack1111111l11_opy_ else None
                if isinstance(bstack1ll11l111ll_opy_, dict):
                    instance.data[bstack111ll1l11l_opy_.bstack1ll11l1l1ll_opy_] = copy.deepcopy(bstack1ll11l111ll_opy_)
                    instance.data[bstack111ll1l11l_opy_.bstack1ll111lllll_opy_] = bstack1ll11l111ll_opy_
            elif bstack1ll11l1ll11_opy_ == bstack111ll1ll11_opy_.bstack111lll1l11_opy_:
                if isinstance(result, dict):
                    framework_session_id = result.get(bstack11llll_opy_ (u"ࠧࡼࡡ࡭ࡷࡨࠦᇋ"), dict()).get(bstack11llll_opy_ (u"ࠨࡳࡦࡵࡶ࡭ࡴࡴࡉࡥࠤᇌ"), None)
                    if framework_session_id:
                        instance.data.update(
                            {
                                bstack111ll1l11l_opy_.bstack1lll11l1ll1_opy_: framework_session_id,
                                bstack111ll1l11l_opy_.bstack1ll11l1ll1l_opy_: datetime.now(tz=timezone.utc),
                            }
                        )
        elif (
            bstack1ll11lll11l_opy_ == bstack111ll1ll1l_opy_.bstack111ll1l1ll_opy_
            and bstack111ll1l11l_opy_.bstack111l1111l1_opy_(*args) == bstack111ll1l11l_opy_.bstack1ll11l1111l_opy_
            and bstack1ll11l1ll11_opy_ == bstack111ll1ll11_opy_.bstack111lll1l11_opy_
        ):
            instance.data[bstack111ll1l11l_opy_.bstack1ll11l111l1_opy_] = datetime.now(tz=timezone.utc)
        if bstack1ll11llllll_opy_ in bstack111ll1l11l_opy_.bstack1ll1l1111l1_opy_:
            bstack1ll11l11111_opy_ = None
            for callback in bstack111ll1l11l_opy_.bstack1ll1l1111l1_opy_[bstack1ll11llllll_opy_]:
                try:
                    bstack1ll11l1l11l_opy_ = callback(self, target, exec, bstack111l1l1l11_opy_, result, *args, **kwargs)
                    if bstack1ll11l11111_opy_ == None:
                        bstack1ll11l11111_opy_ = bstack1ll11l1l11l_opy_
                except Exception as e:
                    self.logger.error(bstack11llll_opy_ (u"ࠢࡦࡴࡵࡳࡷࠦࡩ࡯ࡸࡲ࡯࡮ࡴࡧࠡࡥࡤࡰࡱࡨࡡࡤ࡭࠽ࠤࠧᇍ") + str(e) + bstack11llll_opy_ (u"ࠣࠤᇎ"))
                    traceback.print_exc()
            if bstack1ll11l1ll11_opy_ == bstack111ll1ll11_opy_.bstack111l1llll1_opy_ and callable(bstack1ll11l11111_opy_):
                return bstack1ll11l11111_opy_
            elif bstack1ll11l1ll11_opy_ == bstack111ll1ll11_opy_.bstack111lll1l11_opy_ and bstack1ll11l11111_opy_:
                return bstack1ll11l11111_opy_
    def bstack1ll11ll1l1l_opy_(
        self, method_name, previous_state: bstack111ll1ll1l_opy_, *args, **kwargs
    ) -> bstack111ll1ll1l_opy_:
        if method_name == bstack11llll_opy_ (u"ࠤࡢࡣ࡮ࡴࡩࡵࡡࡢࠦᇏ") or method_name == bstack11llll_opy_ (u"ࠥࡷࡹࡧࡲࡵࡡࡶࡩࡸࡹࡩࡰࡰࠥᇐ"):
            return bstack111ll1ll1l_opy_.bstack111l1ll111_opy_
        if method_name == bstack11llll_opy_ (u"ࠦࡶࡻࡩࡵࠤᇑ"):
            return bstack111ll1ll1l_opy_.QUIT
        if method_name == bstack11llll_opy_ (u"ࠧ࡫ࡸࡦࡥࡸࡸࡪࠨᇒ"):
            if previous_state != bstack111ll1ll1l_opy_.NONE:
                bstack1lllllll1ll_opy_ = bstack111ll1l11l_opy_.bstack111l1111l1_opy_(*args)
                if bstack1lllllll1ll_opy_ == bstack111ll1l11l_opy_.bstack111l111l1l_opy_:
                    return bstack111ll1ll1l_opy_.bstack111l1ll111_opy_
            return bstack111ll1ll1l_opy_.bstack111ll1l1ll_opy_
        return bstack111ll1ll1l_opy_.NONE