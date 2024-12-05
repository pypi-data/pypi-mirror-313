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
import grpc
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack111ll111l1_opy_ import bstack111l1lllll_opy_
from browserstack_sdk.sdk_cli.bstack111ll11ll1_opy_ import (
    bstack111ll1ll1l_opy_,
    bstack111ll1ll11_opy_,
    bstack111lll1ll1_opy_,
)
from browserstack_sdk.sdk_cli.bstack111ll1l1l1_opy_ import bstack111ll1l11l_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack11ll1l1l1l_opy_
import threading
import bstack_utils.accessibility as bstack11111l11_opy_
import os
class bstack111l111lll_opy_(bstack111l1lllll_opy_):
    bstack111ll1lll1_opy_ = bstack11llll_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤ࡯࡮ࡪࡶࠥྲྀ")
    bstack111l1lll1l_opy_ = bstack11llll_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡳࡵࡣࡵࡸࠧཷ")
    bstack111l1l111l_opy_ = bstack11llll_opy_ (u"ࠧࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡴࡶࡲࡴࠧླྀ")
    def __init__(self):
        super().__init__()
        bstack111ll1l11l_opy_.bstack111l1l1l1l_opy_((bstack111ll1ll1l_opy_.bstack111l1ll111_opy_, bstack111ll1ll11_opy_.bstack111l1llll1_opy_), self.bstack111l11111l_opy_)
        bstack111ll1l11l_opy_.bstack111l1l1l1l_opy_((bstack111ll1ll1l_opy_.bstack111ll1l1ll_opy_, bstack111ll1ll11_opy_.bstack111l1llll1_opy_), self.bstack111lll1111_opy_)
        bstack111ll1l11l_opy_.bstack111l1l1l1l_opy_((bstack111ll1ll1l_opy_.bstack111ll1l1ll_opy_, bstack111ll1ll11_opy_.bstack111lll1l11_opy_), self.bstack111ll111ll_opy_)
        bstack111ll1l11l_opy_.bstack111l1l1l1l_opy_((bstack111ll1ll1l_opy_.QUIT, bstack111ll1ll11_opy_.bstack111lll1l11_opy_), self.bstack111l11l11l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack111l11111l_opy_(
        self,
        f: bstack111ll1l11l_opy_,
        driver: object,
        exec: Tuple[bstack111lll1ll1_opy_, str],
        bstack111l1l1l11_opy_: Tuple[bstack111ll1ll1l_opy_, bstack111ll1ll11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11llll_opy_ (u"ࠨ࡟ࡠ࡫ࡱ࡭ࡹࡥ࡟ࠣཹ"):
            return
        def wrapped(driver, init, *args, **kwargs):
            self.bstack111l11ll1l_opy_(instance, f, kwargs)
            self.logger.debug(bstack11llll_opy_ (u"ࠢࡥࡴ࡬ࡺࡪࡸ࠮ࡼ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࢃࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸ࠾ࡽࡩ࠲ࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࢂࡀࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨེ") + str(kwargs) + bstack11llll_opy_ (u"ࠣࠤཻ"))
            threading.current_thread().bstackSessionDriver = driver
            return init(driver, *args, **kwargs)
        return wrapped
    def bstack111lll1111_opy_(
        self,
        f: bstack111ll1l11l_opy_,
        driver: object,
        exec: Tuple[bstack111lll1ll1_opy_, str],
        bstack111l1l1l11_opy_: Tuple[bstack111ll1ll1l_opy_, bstack111ll1ll11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if f.bstack111lll1l1l_opy_(instance, bstack111l111lll_opy_.bstack111ll1lll1_opy_, False):
            return
        if not f.bstack111l11l1l1_opy_(instance, bstack111ll1l11l_opy_.bstack111l11l111_opy_):
            return
        platform_index = f.bstack111lll1l1l_opy_(instance, bstack111ll1l11l_opy_.bstack111l11l111_opy_)
        if f.bstack111l111l11_opy_(method_name, *args) and len(args) > 1:
            bstack111l1l1l1_opy_ = datetime.now()
            hub_url = bstack111ll1l11l_opy_.hub_url(driver)
            self.logger.warning(bstack11llll_opy_ (u"ࠤ࡫ࡹࡧࡥࡵࡳ࡮ࡀོࠦ") + str(hub_url) + bstack11llll_opy_ (u"ཽࠥࠦ"))
            bstack111ll11l1l_opy_ = args[1][bstack11llll_opy_ (u"ࠦࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥཾ")] if isinstance(args[1], dict) and bstack11llll_opy_ (u"ࠧࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦཿ") in args[1] else None
            bstack111l1l1ll1_opy_ = bstack11llll_opy_ (u"ࠨࡡ࡭ࡹࡤࡽࡸࡓࡡࡵࡥ࡫ྀࠦ")
            if isinstance(bstack111ll11l1l_opy_, dict):
                bstack111l1l1l1_opy_ = datetime.now()
                r = self.bstack111lll11ll_opy_(
                    instance.ref(),
                    platform_index,
                    f.framework_name,
                    f.framework_version,
                    hub_url
                )
                instance.bstack1ll1l1l11l_opy_(bstack11llll_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡪࡰ࡬ࡸཱྀࠧ"), datetime.now() - bstack111l1l1l1_opy_)
                try:
                    if not r.success:
                        self.logger.info(bstack11llll_opy_ (u"ࠣࡵࡲࡱࡪࡺࡨࡪࡰࡪࠤࡼ࡫࡮ࡵࠢࡺࡶࡴࡴࡧ࠻ࠢࠥྂ") + str(r) + bstack11llll_opy_ (u"ࠤࠥྃ"))
                        return
                    if r.hub_url:
                        f.bstack111l1ll11l_opy_(instance, driver, r.hub_url)
                        f.bstack111l1l11ll_opy_(instance, bstack111l111lll_opy_.bstack111ll1lll1_opy_, True)
                except Exception as e:
                    self.logger.error(bstack11llll_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤ྄"), e)
    def bstack111ll111ll_opy_(
        self,
        f: bstack111ll1l11l_opy_,
        driver: object,
        exec: Tuple[bstack111lll1ll1_opy_, str],
        bstack111l1l1l11_opy_: Tuple[bstack111ll1ll1l_opy_, bstack111ll1ll11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack111lll1l1l_opy_(instance, bstack111l111lll_opy_.bstack111l1lll1l_opy_, False):
            return
        ref = instance.ref()
        hub_url = bstack111ll1l11l_opy_.hub_url(driver)
        if not hub_url:
            self.logger.warning(bstack11llll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡵࡷࡪࠦࡨࡶࡤࡢࡹࡷࡲ࠽ࠣ྅") + str(hub_url) + bstack11llll_opy_ (u"ࠧࠨ྆"))
            return
        framework_session_id = bstack111ll1l11l_opy_.session_id(driver)
        if not framework_session_id:
            self.logger.warning(bstack11llll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡥࡷࡹࡥࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤ࠾ࠤ྇") + str(framework_session_id) + bstack11llll_opy_ (u"ࠢࠣྈ"))
            return
        if bstack111ll1l11l_opy_.bstack111l1111l1_opy_(*args) == bstack111ll1l11l_opy_.bstack111l111l1l_opy_:
            bstack111l1l1l1_opy_ = datetime.now()
            r = self.bstack111ll1111l_opy_(
                ref,
                f.bstack111lll1l1l_opy_(instance, bstack111ll1l11l_opy_.bstack111l11l111_opy_, 0),
                f.framework_name,
                f.framework_version,
                framework_session_id,
                hub_url,
            )
            instance.bstack1ll1l1l11l_opy_(bstack11llll_opy_ (u"ࠣࡩࡵࡴࡨࡀࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡵࡷࡥࡷࡺࠢྉ"), datetime.now() - bstack111l1l1l1_opy_)
            f.bstack111l1l11ll_opy_(instance, bstack111l111lll_opy_.bstack111l1lll1l_opy_, r.success)
    def bstack111l11l11l_opy_(
        self,
        f: bstack111ll1l11l_opy_,
        driver: object,
        exec: Tuple[bstack111lll1ll1_opy_, str],
        bstack111l1l1l11_opy_: Tuple[bstack111ll1ll1l_opy_, bstack111ll1ll11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack111lll1l1l_opy_(instance, bstack111l111lll_opy_.bstack111l1l111l_opy_, False):
            return
        ref = instance.ref()
        framework_session_id = bstack111ll1l11l_opy_.session_id(driver)
        hub_url = bstack111ll1l11l_opy_.hub_url(driver)
        bstack111l1l1l1_opy_ = datetime.now()
        r = self.bstack111l11ll11_opy_(
            ref,
            f.bstack111lll1l1l_opy_(instance, bstack111ll1l11l_opy_.bstack111l11l111_opy_, 0),
            f.framework_name,
            f.framework_version,
            framework_session_id,
            hub_url,
        )
        instance.bstack1ll1l1l11l_opy_(bstack11llll_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡶࡸࡴࡶࠢྊ"), datetime.now() - bstack111l1l1l1_opy_)
        f.bstack111l1l11ll_opy_(instance, bstack111l111lll_opy_.bstack111l1l111l_opy_, r.success)
    def bstack111lll111l_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        self.logger.debug(bstack11llll_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲࡠ࡫ࡱ࡭ࡹࡀࠠࠣྋ") + str(req) + bstack11llll_opy_ (u"ࠦࠧྌ"))
        try:
            r = self.bstack111l11l1ll_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack11llll_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࡳࡶࡥࡦࡩࡸࡹ࠽ࠣྍ") + str(r.success) + bstack11llll_opy_ (u"ࠨࠢྎ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11llll_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧྏ") + str(e) + bstack11llll_opy_ (u"ࠣࠤྐ"))
            traceback.print_exc()
            raise e
    def bstack111lll11ll_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str
    ):
        self.bstack111l1l1lll_opy_()
        req = structs.AutomationFrameworkInitRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        self.logger.debug(bstack11llll_opy_ (u"ࠤࡵࡩ࡬࡯ࡳࡵࡧࡵࡣ࡮ࡴࡩࡵ࠼ࠣࠦྑ") + str(req) + bstack11llll_opy_ (u"ࠥࠦྒ"))
        try:
            r = self.bstack111l11l1ll_opy_.AutomationFrameworkInit(req)
            if not r.success:
                self.logger.debug(bstack11llll_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࡹࡵࡤࡥࡨࡷࡸࡃࠢྒྷ") + str(r.success) + bstack11llll_opy_ (u"ࠧࠨྔ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11llll_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦྕ") + str(e) + bstack11llll_opy_ (u"ࠢࠣྖ"))
            traceback.print_exc()
            raise e
    def bstack111ll1111l_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack111l1l1lll_opy_()
        req = structs.AutomationFrameworkStartRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        self.logger.debug(bstack11llll_opy_ (u"ࠣࡴࡨ࡫࡮ࡹࡴࡦࡴࡢࡷࡹࡧࡲࡵ࠼ࠣࠦྗ") + str(req) + bstack11llll_opy_ (u"ࠤࠥ྘"))
        try:
            r = self.bstack111l11l1ll_opy_.AutomationFrameworkStart(req)
            if not r.success:
                self.logger.debug(bstack11llll_opy_ (u"ࠥࡶࡪࡩࡥࡪࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࠧྙ") + str(r) + bstack11llll_opy_ (u"ࠦࠧྚ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11llll_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥྛ") + str(e) + bstack11llll_opy_ (u"ࠨࠢྜ"))
            traceback.print_exc()
            raise e
    def bstack111l11ll11_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack111l1l1lll_opy_()
        req = structs.AutomationFrameworkStopRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        self.logger.debug(bstack11llll_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡶࡸࡴࡶ࠺ࠡࠤྜྷ") + str(req) + bstack11llll_opy_ (u"ࠣࠤྞ"))
        try:
            r = self.bstack111l11l1ll_opy_.AutomationFrameworkStop(req)
            if not r.success:
                self.logger.debug(bstack11llll_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦྟ") + str(r) + bstack11llll_opy_ (u"ࠥࠦྠ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11llll_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤྡ") + str(e) + bstack11llll_opy_ (u"ࠧࠨྡྷ"))
            traceback.print_exc()
            raise e
    def bstack111l11ll1l_opy_(self, instance: bstack111lll1ll1_opy_, f: bstack111ll1l11l_opy_, kwargs):
        bstack111l11lll1_opy_ = version.parse(f.framework_version)
        bstack111l1ll1l1_opy_ = kwargs.get(bstack11llll_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡳࡳࡹࠢྣ"))
        bstack111l1ll1ll_opy_ = kwargs.get(bstack11llll_opy_ (u"ࠢࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢྤ"))
        bstack111ll11l11_opy_ = {}
        bstack111l11llll_opy_ = {}
        bstack111ll1llll_opy_ = None
        bstack111lll11l1_opy_ = {}
        if bstack111l1ll1ll_opy_ is not None or bstack111l1ll1l1_opy_ is not None: # check top level caps
            if bstack111l1ll1ll_opy_ is not None:
                bstack111lll11l1_opy_[bstack11llll_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨྥ")] = bstack111l1ll1ll_opy_
            if bstack111l1ll1l1_opy_ is not None and callable(getattr(bstack111l1ll1l1_opy_, bstack11llll_opy_ (u"ࠤࡷࡳࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦྦ"))):
                bstack111lll11l1_opy_[bstack11llll_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࡣࡦࡹ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ྦྷ")] = bstack111l1ll1l1_opy_.to_capabilities()
        response = self.bstack111lll111l_opy_(f.platform_index, instance.ref(), json.dumps(bstack111lll11l1_opy_).encode(bstack11llll_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥྨ")))
        if response is not None and response.capabilities:
            bstack111ll11l11_opy_ = json.loads(response.capabilities.decode(bstack11llll_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦྩ")))
            if not bstack111ll11l11_opy_: # empty caps bstack111ll1l111_opy_ bstack111ll11lll_opy_ bstack111l1lll11_opy_ bstack111l1l1111_opy_ or error in processing
                return
            bstack111l1l11l1_opy_ = json.loads(os.environ.get(bstack11llll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࠧྪ"), bstack11llll_opy_ (u"ࠢࡼࡿࠥྫ")))
            if bstack11111l11_opy_.bstack1l1llll11_opy_(bstack111l1l11l1_opy_, f.platform_index) and bstack11111l11_opy_.bstack11ll11ll11_opy_(bstack111ll11l11_opy_, bstack111l1ll1l1_opy_, bstack111l1ll1ll_opy_):
                threading.current_thread().a11yPlatform = True
                bstack11111l11_opy_.set_capabilities(bstack111ll11l11_opy_, bstack111l1l11l1_opy_)
            bstack111ll1llll_opy_ = f.bstack111l1111ll_opy_[bstack11llll_opy_ (u"ࠣࡥࡵࡩࡦࡺࡥࡠࡱࡳࡸ࡮ࡵ࡮ࡴࡡࡩࡶࡴࡳ࡟ࡤࡣࡳࡷࠧྫྷ")](bstack111ll11l11_opy_)
        if bstack111l1ll1l1_opy_ is not None and bstack111l11lll1_opy_ >= version.parse(bstack11llll_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨྭ")):
            bstack111l11llll_opy_ = None
        if (
                not bstack111l1ll1l1_opy_ and not bstack111l1ll1ll_opy_
        ) or (
                bstack111l11lll1_opy_ < version.parse(bstack11llll_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩྮ"))
        ):
            bstack111l11llll_opy_ = {}
            bstack111l11llll_opy_.update(bstack111ll11l11_opy_)
        self.logger.info(bstack11ll1l1l1l_opy_)
        if bstack111l11lll1_opy_ >= version.parse(bstack11llll_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫྯ")):
            if bstack111l1ll1ll_opy_ is not None:
                del kwargs[bstack11llll_opy_ (u"ࠧࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧྰ")]
            kwargs.update(
                {
                    bstack11llll_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤྱ"): f.bstack111ll11111_opy_,
                    bstack11llll_opy_ (u"ࠢࡰࡲࡷ࡭ࡴࡴࡳࠣྲ"): bstack111ll1llll_opy_,
                    bstack11llll_opy_ (u"ࠣ࡭ࡨࡩࡵࡥࡡ࡭࡫ࡹࡩࠧླ"): True,
                    bstack11llll_opy_ (u"ࠤࡩ࡭ࡱ࡫࡟ࡥࡧࡷࡩࡨࡺ࡯ࡳࠤྴ"): None,
                }
            )
        elif bstack111l11lll1_opy_ >= version.parse(bstack11llll_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩྵ")):
            kwargs.update(
                {
                    bstack11llll_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢྶ"): f.bstack111ll11111_opy_,
                    bstack11llll_opy_ (u"ࠧࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧྷ"): bstack111l11llll_opy_,
                    bstack11llll_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡳࡳࡹࠢྸ"): bstack111ll1llll_opy_,
                    bstack11llll_opy_ (u"ࠢ࡬ࡧࡨࡴࡤࡧ࡬ࡪࡸࡨࠦྐྵ"): True,
                    bstack11llll_opy_ (u"ࠣࡨ࡬ࡰࡪࡥࡤࡦࡶࡨࡧࡹࡵࡲࠣྺ"): None,
                }
            )
        elif bstack111l11lll1_opy_ >= version.parse(bstack11llll_opy_ (u"ࠩ࠵࠲࠺࠹࠮࠱ࠩྻ")):
            kwargs.update(
                {
                    bstack11llll_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨྼ"): f.bstack111ll11111_opy_,
                    bstack11llll_opy_ (u"ࠦࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦ྽"): bstack111l11llll_opy_,
                    bstack11llll_opy_ (u"ࠧࡱࡥࡦࡲࡢࡥࡱ࡯ࡶࡦࠤ྾"): True,
                    bstack11llll_opy_ (u"ࠨࡦࡪ࡮ࡨࡣࡩ࡫ࡴࡦࡥࡷࡳࡷࠨ྿"): None,
                }
            )
        else:
            kwargs.update(
                {
                    bstack11llll_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥ࿀"): f.bstack111ll11111_opy_,
                    bstack11llll_opy_ (u"ࠣࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣ࿁"): bstack111l11llll_opy_,
                    bstack11llll_opy_ (u"ࠤ࡮ࡩࡪࡶ࡟ࡢ࡮࡬ࡺࡪࠨ࿂"): True,
                    bstack11llll_opy_ (u"ࠥࡪ࡮ࡲࡥࡠࡦࡨࡸࡪࡩࡴࡰࡴࠥ࿃"): None,
                }
            )