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
from datetime import datetime
import json
from browserstack_sdk.sdk_cli.bstack111ll11ll1_opy_ import (
    bstack111ll1ll1l_opy_,
    bstack111ll1ll11_opy_,
    bstack11111l1lll_opy_,
    bstack111lll1ll1_opy_,
)
from browserstack_sdk.sdk_cli.bstack111ll1l1l1_opy_ import bstack111ll1l11l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1111l1lll1_opy_, bstack1111l11111_opy_, bstack1111ll1111_opy_
from typing import Tuple, Dict, Any, List, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack111ll111l1_opy_ import bstack111l1lllll_opy_
from browserstack_sdk.sdk_cli.bstack1111l111l1_opy_ import bstack1111lll11l_opy_
import grpc
import traceback
class bstack1lllll111ll_opy_(bstack111l1lllll_opy_):
    bstack1111111lll_opy_ = False
    bstack1ll1ll1ll11_opy_ = bstack11llll_opy_ (u"ࠦࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠴ࡷࡦࡤࡧࡶ࡮ࡼࡥࡳࠤᄢ")
    bstack1ll1lll1l11_opy_ = bstack11llll_opy_ (u"ࠧࡸࡥ࡮ࡱࡷࡩ࠳ࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲࠣᄣ")
    bstack1ll1ll11lll_opy_ = bstack11llll_opy_ (u"ࠨࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡩ࡯࡫ࡷࠦᄤ")
    bstack1ll1ll11l11_opy_ = bstack11llll_opy_ (u"ࠢࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡪࡵࡢࡷࡨࡧ࡮࡯࡫ࡱ࡫ࠧᄥ")
    bstack1ll1ll11ll1_opy_ = bstack11llll_opy_ (u"ࠣࡦࡵ࡭ࡻ࡫ࡲࡠࡪࡤࡷࡤࡻࡲ࡭ࠤᄦ")
    scripts: Dict[str, Dict[str, str]]
    commands: Dict[str, Dict[str, Dict[str, List[str]]]]
    def __init__(self):
        super().__init__()
        self.scripts = dict()
        self.commands = dict()
        if not self.is_enabled():
            return
        bstack111ll1l11l_opy_.bstack111l1l1l1l_opy_((bstack111ll1ll1l_opy_.bstack111ll1l1ll_opy_, bstack111ll1ll11_opy_.bstack111l1llll1_opy_), self.bstack1ll1l1lllll_opy_)
        TestFramework.bstack111l1l1l1l_opy_((bstack1111l1lll1_opy_.TEST, bstack1111l11111_opy_.bstack111lll1l11_opy_), self.bstack1111ll1ll1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll1l1lllll_opy_(
        self,
        f: bstack111ll1l11l_opy_,
        driver: object,
        exec: Tuple[bstack111lll1ll1_opy_, str],
        bstack111l1l1l11_opy_: Tuple[bstack111ll1ll1l_opy_, bstack111ll1ll11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        bstack111l1l1l1_opy_ = datetime.now()
        self.bstack1ll1ll11111_opy_(f, exec, *args, **kwargs)
        instance, method_name = exec
        instance.bstack1ll1l1l11l_opy_(bstack11llll_opy_ (u"ࠤࡤ࠵࠶ࡿ࠺ࡪࡰ࡬ࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡩ࡯࡯ࡨ࡬࡫ࠧᄧ"), datetime.now() - bstack111l1l1l1_opy_)
        if (
            not f.bstack1ll1lll1lll_opy_(method_name)
            or f.bstack1ll1ll1ll1l_opy_(method_name, *args)
            or f.bstack1ll1lll111l_opy_(method_name, *args)
        ):
            return
        if not f.bstack111lll1l1l_opy_(instance, bstack1lllll111ll_opy_.bstack1ll1ll11lll_opy_, False):
            if not bstack1lllll111ll_opy_.bstack1111111lll_opy_:
                self.logger.warning(bstack11llll_opy_ (u"ࠥ࡟ࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࡂࠨᄨ") + str(f.platform_index) + bstack11llll_opy_ (u"ࠦࡢࠦࡡ࠲࠳ࡼࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠣ࡬ࡦࡼࡥࠡࡰࡲࡸࠥࡨࡥࡦࡰࠣࡷࡪࡺࠠࡧࡱࡵࠤࡹ࡮ࡩࡴࠢࡶࡩࡸࡹࡩࡰࡰࠥᄩ"))
                bstack1lllll111ll_opy_.bstack1111111lll_opy_ = True
            return
        bstack1ll1ll1lll1_opy_ = self.scripts.get(f.framework_name, {})
        if not bstack1ll1ll1lll1_opy_:
            platform_index = f.bstack111lll1l1l_opy_(instance, bstack111ll1l11l_opy_.bstack111l11l111_opy_, 0)
            self.logger.debug(bstack11llll_opy_ (u"ࠧࡴ࡯ࠡࡣ࠴࠵ࡾࠦࡳࡤࡴ࡬ࡴࡹࡹࠠࡧࡱࡵࠤࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࡂࢁࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾࡽࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࠥᄪ") + str(f.framework_name) + bstack11llll_opy_ (u"ࠨࠢᄫ"))
            return
        bstack1lllllll1ll_opy_ = f.bstack111111111l_opy_(*args)
        if not bstack1lllllll1ll_opy_:
            self.logger.debug(bstack11llll_opy_ (u"ࠢ࡮࡫ࡶࡷ࡮ࡴࡧࠡࡥࡲࡱࡲࡧ࡮ࡥࡡࡱࡥࡲ࡫ࠠࡧࡱࡵࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࢁࡦ࠯ࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࡿࠣࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥ࠾ࠤᄬ") + str(method_name) + bstack11llll_opy_ (u"ࠣࠤᄭ"))
            return
        bstack1ll1ll111ll_opy_ = f.bstack111lll1l1l_opy_(instance, bstack1lllll111ll_opy_.bstack1ll1ll11ll1_opy_, False)
        if bstack1lllllll1ll_opy_ == bstack11llll_opy_ (u"ࠤࡪࡩࡹࠨᄮ") and not bstack1ll1ll111ll_opy_:
            f.bstack111l1l11ll_opy_(instance, bstack1lllll111ll_opy_.bstack1ll1ll11ll1_opy_, True)
        if not bstack1ll1ll111ll_opy_:
            self.logger.debug(bstack11llll_opy_ (u"ࠥࡲࡴࠦࡕࡓࡎࠣࡰࡴࡧࡤࡦࡦࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࢀ࡬࠮ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࡾࠢࡦࡳࡲࡳࡡ࡯ࡦࡢࡲࡦࡳࡥ࠾ࠤᄯ") + str(bstack1lllllll1ll_opy_) + bstack11llll_opy_ (u"ࠦࠧᄰ"))
            return
        scripts_to_run = self.commands.get(f.framework_name, {}).get(method_name, {}).get(bstack1lllllll1ll_opy_, [])
        if not scripts_to_run:
            self.logger.debug(bstack11llll_opy_ (u"ࠧࡴ࡯ࠡࡣ࠴࠵ࡾࠦࡳࡤࡴ࡬ࡴࡹࡹࠠࡧࡱࡵࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࢁࡦ࠯ࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࡿࠣࡧࡴࡳ࡭ࡢࡰࡧࡣࡳࡧ࡭ࡦ࠿ࠥᄱ") + str(bstack1lllllll1ll_opy_) + bstack11llll_opy_ (u"ࠨࠢᄲ"))
            return
        self.logger.info(bstack11llll_opy_ (u"ࠢࡳࡷࡱࡲ࡮ࡴࡧࠡࡽ࡯ࡩࡳ࠮ࡳࡤࡴ࡬ࡴࡹࡹ࡟ࡵࡱࡢࡶࡺࡴࠩࡾࠢࡶࡧࡷ࡯ࡰࡵࡵࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࢀ࡬࠮ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࡾࠢࡦࡳࡲࡳࡡ࡯ࡦࡢࡲࡦࡳࡥ࠾ࠤᄳ") + str(bstack1lllllll1ll_opy_) + bstack11llll_opy_ (u"ࠣࠤᄴ"))
        scripts = [(s, bstack1ll1ll1lll1_opy_[s]) for s in scripts_to_run if s in bstack1ll1ll1lll1_opy_]
        for bstack1ll1ll1l111_opy_, bstack1ll1ll1l1l1_opy_ in scripts:
            try:
                bstack111l1l1l1_opy_ = datetime.now()
                result = (
                    self.perform_scan(driver, method=bstack1lllllll1ll_opy_, framework_name=f.framework_name)
                    if bstack1ll1ll1l111_opy_ == bstack11llll_opy_ (u"ࠤࡶࡧࡦࡴࠢᄵ")
                    else driver.execute_async_script(bstack1ll1ll1l1l1_opy_)
                )
                instance.bstack1ll1l1l11l_opy_(bstack11llll_opy_ (u"ࠥࡥ࠶࠷ࡹ࠻ࠤᄶ") + bstack1ll1ll1l111_opy_, datetime.now() - bstack111l1l1l1_opy_)
                if isinstance(result, dict) and not result.get(bstack11llll_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷࠧᄷ"), True):
                    self.logger.warning(bstack11llll_opy_ (u"ࠧࡹ࡫ࡪࡲࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡲ࡬ࠦࡲࡦ࡯ࡤ࡭ࡳ࡯࡮ࡨࠢࡶࡧࡷ࡯ࡰࡵࡵ࠽ࠤࠧᄸ") + str(result) + bstack11llll_opy_ (u"ࠨࠢᄹ"))
                    break
            except Exception as e:
                self.logger.error(bstack11llll_opy_ (u"ࠢࡦࡴࡵࡳࡷࠦࡥࡹࡧࡦࡹࡹ࡯࡮ࡨࠢࡶࡧࡷ࡯ࡰࡵ࠿ࡾࡷࡨࡸࡩࡱࡶࡢࡲࡦࡳࡥࡾࠢࡨࡶࡷࡵࡲ࠾ࠤᄺ") + str(e) + bstack11llll_opy_ (u"ࠣࠤᄻ"))
    def bstack1111ll1ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1111ll1111_opy_,
        bstack111l1l1l11_opy_: Tuple[bstack1111l1lll1_opy_, bstack1111l11111_opy_],
        *args,
        **kwargs,
    ):
        bstack1111l1ll1l_opy_ = f.bstack111lll1l1l_opy_(instance, bstack1111lll11l_opy_.bstack1111llll1l_opy_, [])
        if not bstack1111l1ll1l_opy_:
            self.logger.debug(bstack11llll_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᄼ") + str(kwargs) + bstack11llll_opy_ (u"ࠥࠦᄽ"))
            return
        if len(bstack1111l1ll1l_opy_) > 1:
            self.logger.debug(bstack11llll_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࢁ࡬ࡦࡰࠫࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡸ࠯ࡽࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᄾ") + str(kwargs) + bstack11llll_opy_ (u"ࠧࠨᄿ"))
        bstack1111ll1l1l_opy_, bstack1ll1l1llll1_opy_ = bstack1111l1ll1l_opy_[0]
        driver = bstack1111ll1l1l_opy_()
        if not driver:
            self.logger.debug(bstack11llll_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᅀ") + str(kwargs) + bstack11llll_opy_ (u"ࠢࠣᅁ"))
            return
        test_name = f.bstack111lll1l1l_opy_(instance, TestFramework.bstack1ll1ll1l11l_opy_)
        if not test_name:
            self.logger.debug(bstack11llll_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡰࡤࡱࡪࠨᅂ"))
            return
        return self.perform_scan(driver, method=test_name, framework_name=bstack1ll1l1llll1_opy_.framework_name)
    def perform_scan(self, driver: object, method: Union[None, str], framework_name: str):
        bstack111l1l1l1_opy_ = datetime.now()
        bstack1ll1ll1l1l1_opy_ = self.scripts.get(framework_name, {}).get(bstack11llll_opy_ (u"ࠤࡶࡧࡦࡴࠢᅃ"), None)
        if not bstack1ll1ll1l1l1_opy_:
            self.logger.debug(bstack11llll_opy_ (u"ࠥࡴࡪࡸࡦࡰࡴࡰࡣࡸࡩࡡ࡯࠼ࠣࡱ࡮ࡹࡳࡪࡰࡪࠤࠬࡹࡣࡢࡰࠪࠤࡸࡩࡲࡪࡲࡷࠤ࡫ࡵࡲࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࠥᅄ") + str(framework_name) + bstack11llll_opy_ (u"ࠦࠥࠨᅅ"))
            return
        instance = bstack11111l1lll_opy_.bstack1ll1ll111l1_opy_(driver)
        if instance:
            if not bstack11111l1lll_opy_.bstack111lll1l1l_opy_(instance, bstack1lllll111ll_opy_.bstack1ll1ll11l11_opy_, False):
                bstack11111l1lll_opy_.bstack111l1l11ll_opy_(instance, bstack1lllll111ll_opy_.bstack1ll1ll11l11_opy_, True)
            else:
                self.logger.info(bstack11llll_opy_ (u"ࠧࡶࡥࡳࡨࡲࡶࡲࡥࡳࡤࡣࡱ࠾ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡩ࡯ࠢࡳࡶࡴ࡭ࡲࡦࡵࡶࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࢁࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࡽࠡ࡯ࡨࡸ࡭ࡵࡤ࠾ࠤᅆ") + str(method) + bstack11llll_opy_ (u"ࠨࠢᅇ"))
                return
        self.logger.info(bstack11llll_opy_ (u"ࠢࡱࡧࡵࡪࡴࡸ࡭ࡠࡵࡦࡥࡳࡀࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࢀࠤࡲ࡫ࡴࡩࡱࡧࡁࠧᅈ") + str(method) + bstack11llll_opy_ (u"ࠣࠤᅉ"))
        result = driver.execute_async_script(bstack1ll1ll1l1l1_opy_, {bstack11llll_opy_ (u"ࠤࡰࡩࡹ࡮࡯ࡥࠤᅊ"): method if method else bstack11llll_opy_ (u"ࠥࠦᅋ")})
        if instance:
            bstack11111l1lll_opy_.bstack111l1l11ll_opy_(instance, bstack1lllll111ll_opy_.bstack1ll1ll11l11_opy_, False)
            instance.bstack1ll1l1l11l_opy_(bstack11llll_opy_ (u"ࠦࡦ࠷࠱ࡺ࠼ࡳࡩࡷ࡬࡯ࡳ࡯ࡢࡷࡨࡧ࡮ࠣᅌ"), datetime.now() - bstack111l1l1l1_opy_)
        return result
    def get_accessibility_results(self, driver: object, framework_name):
        bstack1ll1ll1l1l1_opy_ = self.scripts.get(framework_name, {}).get(bstack11llll_opy_ (u"ࠧ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࠤᅍ"), None)
        if not bstack1ll1ll1l1l1_opy_:
            self.logger.debug(bstack11llll_opy_ (u"ࠨ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࠨࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࠬࠦࡳࡤࡴ࡬ࡴࡹࠦࡦࡰࡴࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࠧᅎ") + str(framework_name) + bstack11llll_opy_ (u"ࠢࠣᅏ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack111l1l1l1_opy_ = datetime.now()
        result = driver.execute_async_script(bstack1ll1ll1l1l1_opy_)
        instance = bstack11111l1lll_opy_.bstack1ll1ll111l1_opy_(driver)
        if instance:
            instance.bstack1ll1l1l11l_opy_(bstack11llll_opy_ (u"ࠣࡣ࠴࠵ࡾࡀࡧࡦࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡶࡪࡹࡵ࡭ࡶࡶࠦᅐ"), datetime.now() - bstack111l1l1l1_opy_)
        return result
    def get_accessibility_results_summary(self, driver: object, framework_name):
        bstack1ll1ll1l1l1_opy_ = self.scripts.get(framework_name, {}).get(bstack11llll_opy_ (u"ࠤࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࡙ࡵ࡮࡯ࡤࡶࡾࠨᅑ"), None)
        if not bstack1ll1ll1l1l1_opy_:
            self.logger.debug(bstack11llll_opy_ (u"ࠥࡱ࡮ࡹࡳࡪࡰࡪࠤࠬ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࡕࡸࡱࡲࡧࡲࡺࠩࠣࡷࡨࡸࡩࡱࡶࠣࡪࡴࡸࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࠤᅒ") + str(framework_name) + bstack11llll_opy_ (u"ࠦࠧᅓ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack111l1l1l1_opy_ = datetime.now()
        result = driver.execute_async_script(bstack1ll1ll1l1l1_opy_)
        instance = bstack11111l1lll_opy_.bstack1ll1ll111l1_opy_(driver)
        if instance:
            instance.bstack1ll1l1l11l_opy_(bstack11llll_opy_ (u"ࠧࡧ࠱࠲ࡻ࠽࡫ࡪࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡳࡧࡶࡹࡱࡺࡳࡠࡵࡸࡱࡲࡧࡲࡺࠤᅔ"), datetime.now() - bstack111l1l1l1_opy_)
        return result
    def bstack1ll1lll1111_opy_(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str,
    ):
        self.bstack111l1l1lll_opy_()
        req = structs.AccessibilityConfigRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        try:
            r = self.bstack111l11l1ll_opy_.AccessibilityConfig(req)
            if not r.success:
                self.logger.debug(bstack11llll_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣᅕ") + str(r) + bstack11llll_opy_ (u"ࠢࠣᅖ"))
            else:
                self.bstack1ll1ll1l1ll_opy_(framework_name, r)
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11llll_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨᅗ") + str(e) + bstack11llll_opy_ (u"ࠤࠥᅘ"))
            traceback.print_exc()
            raise e
    def bstack1ll1ll1l1ll_opy_(self, framework_name: str, result: structs.AccessibilityConfigResponse) -> bool:
        if not result.success or not result.accessibility.success:
            return False
        if result.accessibility.options:
            options = result.accessibility.options
            if options.scripts:
                self.scripts[framework_name] = {row.name: row.command for row in options.scripts}
            if options.commands_to_wrap and options.commands_to_wrap.commands:
                scripts_to_run = [s for s in options.commands_to_wrap.scripts_to_run]
                if not scripts_to_run:
                    return False
                bstack1ll1ll11l1l_opy_ = dict()
                for command in options.commands_to_wrap.commands:
                    if command.library == self.bstack1ll1ll1ll11_opy_ and command.module == self.bstack1ll1lll1l11_opy_:
                        if command.method and not command.method in bstack1ll1ll11l1l_opy_:
                            bstack1ll1ll11l1l_opy_[command.method] = dict()
                        if command.name and not command.name in bstack1ll1ll11l1l_opy_[command.method]:
                            bstack1ll1ll11l1l_opy_[command.method][command.name] = list()
                        bstack1ll1ll11l1l_opy_[command.method][command.name].extend(scripts_to_run)
                self.commands[framework_name] = bstack1ll1ll11l1l_opy_
        return bool(self.commands.get(framework_name, None))
    def bstack1ll1ll11111_opy_(
        self,
        f: bstack111ll1l11l_opy_,
        exec: Tuple[bstack111lll1ll1_opy_, str],
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if bstack11111l1lll_opy_.bstack111l11l1l1_opy_(instance, bstack1lllll111ll_opy_.bstack1ll1ll11lll_opy_):
            return
        if not f.bstack1111l11ll1_opy_(instance):
            if not bstack1lllll111ll_opy_.bstack1111111lll_opy_:
                self.logger.warning(bstack11llll_opy_ (u"ࠥࡥ࠶࠷ࡹࠡࡨ࡯ࡳࡼࠦࡤࡪࡵࡤࡦࡱ࡫ࡤࠡࡨࡲࡶࠥࡴ࡯࡯࠯ࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡ࡫ࡱࡪࡷࡧࠢᅙ"))
                bstack1lllll111ll_opy_.bstack1111111lll_opy_ = True
            return
        if f.bstack111l111l11_opy_(method_name, *args):
            bstack1ll1lll11l1_opy_ = False
            desired_capabilities = f.bstack1ll1lll11ll_opy_(instance)
            if isinstance(desired_capabilities, dict):
                hub_url = f.bstack1ll1ll1llll_opy_(instance)
                platform_index = f.bstack111lll1l1l_opy_(instance, bstack111ll1l11l_opy_.bstack111l11l111_opy_, 0)
                bstack1ll1ll1111l_opy_ = datetime.now()
                r = self.bstack1ll1lll1111_opy_(platform_index, f.framework_name, f.framework_version, hub_url)
                instance.bstack1ll1l1l11l_opy_(bstack11llll_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡦࡳࡳ࡬ࡩࡨࠤᅚ"), datetime.now() - bstack1ll1ll1111l_opy_)
                bstack1ll1lll11l1_opy_ = r.success
            else:
                self.logger.error(bstack11llll_opy_ (u"ࠧࡳࡩࡴࡵ࡬ࡲ࡬ࠦࡤࡦࡵ࡬ࡶࡪࡪࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࡃࠢᅛ") + str(desired_capabilities) + bstack11llll_opy_ (u"ࠨࠢᅜ"))
            f.bstack111l1l11ll_opy_(instance, bstack1lllll111ll_opy_.bstack1ll1ll11lll_opy_, bstack1ll1lll11l1_opy_)