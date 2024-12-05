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
    bstack111lll1ll1_opy_,
)
from browserstack_sdk.sdk_cli.bstack111ll1l1l1_opy_ import bstack111ll1l11l_opy_
from typing import Tuple, Callable, Any
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack111ll111l1_opy_ import bstack111l1lllll_opy_
import traceback
import os
import time
class bstack1llllllll11_opy_(bstack111l1lllll_opy_):
    bstack1111111lll_opy_ = False
    def __init__(self):
        super().__init__()
        bstack111ll1l11l_opy_.bstack111l1l1l1l_opy_((bstack111ll1ll1l_opy_.bstack111ll1l1ll_opy_, bstack111ll1ll11_opy_.bstack111l1llll1_opy_), self.bstack111lll1111_opy_)
    def is_enabled(self) -> bool:
        return True
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
        hub_url = f.hub_url(driver)
        if f.bstack11111lll1l_opy_(hub_url):
            if not bstack1llllllll11_opy_.bstack1111111lll_opy_:
                self.logger.warning(bstack11llll_opy_ (u"ࠦࡱࡵࡣࡢ࡮ࠣࡷࡪࡲࡦ࠮ࡪࡨࡥࡱࠦࡦ࡭ࡱࡺࠤࡩ࡯ࡳࡢࡤ࡯ࡩࡩࠦࡦࡰࡴࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢ࡬ࡲ࡫ࡸࡡࠡࡵࡨࡷࡸ࡯࡯࡯ࡵࠣ࡬ࡺࡨ࡟ࡶࡴ࡯ࡁࠧဃ") + str(hub_url) + bstack11llll_opy_ (u"ࠧࠨင"))
                bstack1llllllll11_opy_.bstack1111111lll_opy_ = True
            return
        bstack1lllllll1ll_opy_ = f.bstack111111111l_opy_(*args)
        bstack1111111l11_opy_ = f.bstack1lllllllll1_opy_(*args)
        if bstack1lllllll1ll_opy_ and bstack1lllllll1ll_opy_.lower() == bstack11llll_opy_ (u"ࠨࡦࡪࡰࡧࡩࡱ࡫࡭ࡦࡰࡷࠦစ") and bstack1111111l11_opy_:
            framework_session_id = f.session_id(driver)
            locator_type, locator_value = bstack1111111l11_opy_.get(bstack11llll_opy_ (u"ࠢࡶࡵ࡬ࡲ࡬ࠨဆ"), None), bstack1111111l11_opy_.get(bstack11llll_opy_ (u"ࠣࡸࡤࡰࡺ࡫ࠢဇ"), None)
            if not framework_session_id or not locator_type or not locator_value:
                self.logger.warning(bstack11llll_opy_ (u"ࠤࡾࡧࡴࡳ࡭ࡢࡰࡧࡣࡳࡧ࡭ࡦࡿ࠽ࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠥࡵࡲࠡࡣࡵ࡫ࡸ࠴ࡵࡴ࡫ࡱ࡫ࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࢂࠦ࡯ࡳࠢࡤࡶ࡬ࡹ࠮ࡷࡣ࡯ࡹࡪࡃࠢဈ") + str(locator_value) + bstack11llll_opy_ (u"ࠥࠦဉ"))
                return
            def bstack1111111l1l_opy_(driver, bstack1llllllllll_opy_, *args, **kwargs):
                from selenium.common.exceptions import NoSuchElementException
                try:
                    result = bstack1llllllllll_opy_(driver, *args, **kwargs)
                    response = self.bstack11111111ll_opy_(
                        framework_session_id=framework_session_id,
                        is_success=True,
                        locator_type=locator_type,
                        locator_value=locator_value,
                    )
                    if response and response.execute_script:
                        driver.execute_script(response.execute_script)
                        self.logger.info(bstack11llll_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷ࠲ࡹࡣࡳ࡫ࡳࡸ࠿ࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࢂࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࡃࠢည") + str(locator_value) + bstack11llll_opy_ (u"ࠧࠨဋ"))
                    else:
                        self.logger.warning(bstack11llll_opy_ (u"ࠨࡳࡶࡥࡦࡩࡸࡹ࠭࡯ࡱ࠰ࡷࡨࡸࡩࡱࡶ࠽ࠤࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࢀࠤࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࢂࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠾ࠤဌ") + str(response) + bstack11llll_opy_ (u"ࠢࠣဍ"))
                    return result
                except NoSuchElementException as e:
                    locator = (locator_type, locator_value)
                    return self.__1111111111_opy_(
                        driver, bstack1llllllllll_opy_, e, framework_session_id, locator, *args, **kwargs
                    )
            bstack1111111l1l_opy_.__name__ = bstack1lllllll1ll_opy_
            return bstack1111111l1l_opy_
    def __1111111111_opy_(
        self,
        driver,
        bstack1llllllllll_opy_: Callable,
        exception,
        framework_session_id: str,
        locator: Tuple[str, str],
        *args,
        **kwargs,
    ):
        try:
            locator_type, locator_value = locator
            response = self.bstack11111111ll_opy_(
                framework_session_id=framework_session_id,
                is_success=False,
                locator_type=locator_type,
                locator_value=locator_value,
            )
            if response and response.execute_script:
                driver.execute_script(response.execute_script)
                self.logger.info(bstack11llll_opy_ (u"ࠣࡨࡤ࡭ࡱࡻࡲࡦ࠯࡫ࡩࡦࡲࡩ࡯ࡩ࠰ࡸࡷ࡯ࡧࡨࡧࡵࡩࡩࡀࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࢃࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫࠽ࠣဎ") + str(locator_value) + bstack11llll_opy_ (u"ࠤࠥဏ"))
                bstack1lllllll1l1_opy_ = self.bstack1llllllll1l_opy_(
                    framework_session_id=framework_session_id,
                    locator_type=locator_type,
                )
                self.logger.info(bstack11llll_opy_ (u"ࠥࡪࡦ࡯࡬ࡶࡴࡨ࠱࡭࡫ࡡ࡭࡫ࡱ࡫࠲ࡸࡥࡴࡷ࡯ࡸ࠿ࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࢂࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫ࡽࠡࡪࡨࡥࡱ࡯࡮ࡨࡡࡵࡩࡸࡻ࡬ࡵ࠿ࠥတ") + str(bstack1lllllll1l1_opy_) + bstack11llll_opy_ (u"ࠦࠧထ"))
                if bstack1lllllll1l1_opy_.success and args and len(args) > 1:
                    args[1].update(
                        {
                            bstack11llll_opy_ (u"ࠧࡻࡳࡪࡰࡪࠦဒ"): bstack1lllllll1l1_opy_.locator_type,
                            bstack11llll_opy_ (u"ࠨࡶࡢ࡮ࡸࡩࠧဓ"): bstack1lllllll1l1_opy_.locator_value,
                        }
                    )
                    return bstack1llllllllll_opy_(driver, *args, **kwargs)
                elif os.environ.get(bstack11llll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡊࡡࡇࡉࡇ࡛ࡇࠣန"), False):
                    self.logger.info(bstack1111111ll1_opy_ (u"ࠣࡨࡤ࡭ࡱࡻࡲࡦ࠯࡫ࡩࡦࡲࡩ࡯ࡩ࠰ࡶࡪࡹࡵ࡭ࡶ࠰ࡱ࡮ࡹࡳࡪࡰࡪ࠾ࠥࡹ࡬ࡦࡧࡳࠬ࠸࠶ࠩࠡ࡮ࡨࡸࡹ࡯࡮ࡨࠢࡼࡳࡺࠦࡩ࡯ࡵࡳࡩࡨࡺࠠࡵࡪࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࠥ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࠡ࡮ࡲ࡫ࡸࠨပ"))
                    time.sleep(300)
            else:
                self.logger.warning(bstack11llll_opy_ (u"ࠤࡩࡥ࡮ࡲࡵࡳࡧ࠰ࡲࡴ࠳ࡳࡤࡴ࡬ࡴࡹࡀࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࢃࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥࡾࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࡁࠧဖ") + str(response) + bstack11llll_opy_ (u"ࠥࠦဗ"))
        except Exception as err:
            self.logger.warning(bstack11llll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡷࡵࡩ࠲࡮ࡥࡢ࡮࡬ࡲ࡬࠳ࡲࡦࡵࡸࡰࡹࡀࠠࡦࡴࡵࡳࡷࡀࠠࠣဘ") + str(err) + bstack11llll_opy_ (u"ࠧࠨမ"))
        raise exception
    def bstack11111111ll_opy_(
        self,
        framework_session_id: str,
        is_success: bool,
        locator_type: str,
        locator_value: str,
        platform_index=bstack11llll_opy_ (u"ࠨ࠰ࠣယ"),
    ):
        self.bstack111l1l1lll_opy_()
        req = structs.AISelfHealStepRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.is_success = is_success
        req.test_name = bstack11llll_opy_ (u"ࠢࠣရ")
        req.locator_type = locator_type
        req.locator_value = locator_value
        try:
            r = self.bstack111l11l1ll_opy_.AISelfHealStep(req)
            self.logger.info(bstack11llll_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࠥလ") + str(r) + bstack11llll_opy_ (u"ࠤࠥဝ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11llll_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣသ") + str(e) + bstack11llll_opy_ (u"ࠦࠧဟ"))
            traceback.print_exc()
            raise e
    def bstack1llllllll1l_opy_(self, framework_session_id: str, locator_type: str, platform_index=bstack11llll_opy_ (u"ࠧ࠶ࠢဠ")):
        self.bstack111l1l1lll_opy_()
        req = structs.AISelfHealGetRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.locator_type = locator_type
        try:
            r = self.bstack111l11l1ll_opy_.AISelfHealGetResult(req)
            self.logger.info(bstack11llll_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣအ") + str(r) + bstack11llll_opy_ (u"ࠢࠣဢ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11llll_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨဣ") + str(e) + bstack11llll_opy_ (u"ࠤࠥဤ"))
            traceback.print_exc()
            raise e