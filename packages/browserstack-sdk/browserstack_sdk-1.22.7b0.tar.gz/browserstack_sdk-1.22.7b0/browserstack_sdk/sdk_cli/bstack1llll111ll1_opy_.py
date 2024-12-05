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
from datetime import datetime, timezone
import os
from typing import Any, Tuple, Callable, List
from browserstack_sdk.sdk_cli.bstack111ll11ll1_opy_ import bstack111lll1ll1_opy_, bstack111ll1ll1l_opy_, bstack111ll1ll11_opy_
from browserstack_sdk.sdk_cli.bstack111ll111l1_opy_ import bstack111l1lllll_opy_
from browserstack_sdk.sdk_cli.bstack1111l111l1_opy_ import bstack1111lll11l_opy_
from browserstack_sdk.sdk_cli.bstack111ll1l1l1_opy_ import bstack111ll1l11l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1111l1lll1_opy_, bstack1111ll1111_opy_, bstack1111l11111_opy_, bstack1llll111lll_opy_
from browserstack_sdk.sdk_cli.bstack1llllll1ll1_opy_ import bstack1llll1111l1_opy_
from json import dumps, JSONEncoder
import grpc
from browserstack_sdk import sdk_pb2 as structs
import sys
import traceback
bstack1ll1llll11l_opy_ = [bstack11llll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧႼ"), bstack11llll_opy_ (u"ࠣࡲࡤࡶࡪࡴࡴࠣႽ"), bstack11llll_opy_ (u"ࠤࡦࡳࡳ࡬ࡩࡨࠤႾ"), bstack11llll_opy_ (u"ࠥࡷࡪࡹࡳࡪࡱࡱࠦႿ"), bstack11llll_opy_ (u"ࠦࡵࡧࡴࡩࠤჀ")]
bstack1lll11lll1l_opy_ = {
    bstack11llll_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡶࡹࡵࡪࡲࡲ࠳ࡏࡴࡦ࡯ࠥჁ"): bstack1ll1llll11l_opy_,
    bstack11llll_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡰࡺࡶ࡫ࡳࡳ࠴ࡐࡢࡥ࡮ࡥ࡬࡫ࠢჂ"): bstack1ll1llll11l_opy_,
    bstack11llll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡱࡻࡷ࡬ࡴࡴ࠮ࡎࡱࡧࡹࡱ࡫ࠢჃ"): bstack1ll1llll11l_opy_,
    bstack11llll_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡲࡼࡸ࡭ࡵ࡮࠯ࡅ࡯ࡥࡸࡹࠢჄ"): bstack1ll1llll11l_opy_,
    bstack11llll_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡳࡽࡹ࡮࡯࡯࠰ࡉࡹࡳࡩࡴࡪࡱࡱࠦჅ"): bstack1ll1llll11l_opy_
    + [
        bstack11llll_opy_ (u"ࠥࡳࡷ࡯ࡧࡪࡰࡤࡰࡳࡧ࡭ࡦࠤ჆"),
        bstack11llll_opy_ (u"ࠦࡰ࡫ࡹࡸࡱࡵࡨࡸࠨჇ"),
        bstack11llll_opy_ (u"ࠧ࡬ࡩࡹࡶࡸࡶࡪ࡯࡮ࡧࡱࠥ჈"),
        bstack11llll_opy_ (u"ࠨ࡫ࡦࡻࡺࡳࡷࡪࡳࠣ჉"),
        bstack11llll_opy_ (u"ࠢࡤࡣ࡯ࡰࡸࡶࡥࡤࠤ჊"),
        bstack11llll_opy_ (u"ࠣࡥࡤࡰࡱࡵࡢ࡫ࠤ჋"),
        bstack11llll_opy_ (u"ࠤࡶࡸࡦࡸࡴࠣ჌"),
        bstack11llll_opy_ (u"ࠥࡷࡹࡵࡰࠣჍ"),
        bstack11llll_opy_ (u"ࠦࡩࡻࡲࡢࡶ࡬ࡳࡳࠨ჎"),
        bstack11llll_opy_ (u"ࠧࡽࡨࡦࡰࠥ჏"),
    ],
    bstack11llll_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴࡭ࡢ࡫ࡱ࠲ࡘ࡫ࡳࡴ࡫ࡲࡲࠧა"): [bstack11llll_opy_ (u"ࠢࡴࡶࡤࡶࡹࡶࡡࡵࡪࠥბ"), bstack11llll_opy_ (u"ࠣࡶࡨࡷࡹࡹࡦࡢ࡫࡯ࡩࡩࠨგ"), bstack11llll_opy_ (u"ࠤࡷࡩࡸࡺࡳࡤࡱ࡯ࡰࡪࡩࡴࡦࡦࠥდ"), bstack11llll_opy_ (u"ࠥ࡭ࡹ࡫࡭ࡴࠤე")],
    bstack11llll_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡨࡵ࡮ࡧ࡫ࡪ࠲ࡈࡵ࡮ࡧ࡫ࡪࠦვ"): [bstack11llll_opy_ (u"ࠧ࡯࡮ࡷࡱࡦࡥࡹ࡯࡯࡯ࡡࡳࡥࡷࡧ࡭ࡴࠤზ"), bstack11llll_opy_ (u"ࠨࡡࡳࡩࡶࠦთ")],
    bstack11llll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡧ࡫ࡻࡸࡺࡸࡥࡴ࠰ࡉ࡭ࡽࡺࡵࡳࡧࡇࡩ࡫ࠨი"): [bstack11llll_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢკ"), bstack11llll_opy_ (u"ࠤࡤࡶ࡬ࡴࡡ࡮ࡧࠥლ"), bstack11llll_opy_ (u"ࠥࡪࡺࡴࡣࠣმ"), bstack11llll_opy_ (u"ࠦࡵࡧࡲࡢ࡯ࡶࠦნ"), bstack11llll_opy_ (u"ࠧࡻ࡮ࡪࡶࡷࡩࡸࡺࠢო"), bstack11llll_opy_ (u"ࠨࡩࡥࡵࠥპ")],
    bstack11llll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡧ࡫ࡻࡸࡺࡸࡥࡴ࠰ࡖࡹࡧࡘࡥࡲࡷࡨࡷࡹࠨჟ"): [bstack11llll_opy_ (u"ࠣࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࠨრ"), bstack11llll_opy_ (u"ࠤࡳࡥࡷࡧ࡭ࠣს"), bstack11llll_opy_ (u"ࠥࡴࡦࡸࡡ࡮ࡡ࡬ࡲࡩ࡫ࡸࠣტ")],
    bstack11llll_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡷࡻ࡮࡯ࡧࡵ࠲ࡈࡧ࡬࡭ࡋࡱࡪࡴࠨუ"): [bstack11llll_opy_ (u"ࠧࡽࡨࡦࡰࠥფ"), bstack11llll_opy_ (u"ࠨࡲࡦࡵࡸࡰࡹࠨქ")],
    bstack11llll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮࡮ࡣࡵ࡯࠳ࡹࡴࡳࡷࡦࡸࡺࡸࡥࡴ࠰ࡑࡳࡩ࡫ࡋࡦࡻࡺࡳࡷࡪࡳࠣღ"): [bstack11llll_opy_ (u"ࠣࡰࡲࡨࡪࠨყ"), bstack11llll_opy_ (u"ࠤࡳࡥࡷ࡫࡮ࡵࠤშ")],
    bstack11llll_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡱࡦࡸ࡫࠯ࡵࡷࡶࡺࡩࡴࡶࡴࡨࡷ࠳ࡓࡡࡳ࡭ࠥჩ"): [bstack11llll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤც"), bstack11llll_opy_ (u"ࠧࡧࡲࡨࡵࠥძ"), bstack11llll_opy_ (u"ࠨ࡫ࡸࡣࡵ࡫ࡸࠨწ")],
}
class bstack1llll1llll1_opy_(bstack111l1lllll_opy_):
    bstack1lll1111ll1_opy_ = bstack11llll_opy_ (u"ࠢࡵࡧࡶࡸࡤࡪࡥࡧࡧࡵࡶࡪࡪࠢჭ")
    bstack1lll11111ll_opy_ = bstack11llll_opy_ (u"ࠣࡋࡑࡊࡔࠨხ")
    bstack1lll1111111_opy_ = bstack11llll_opy_ (u"ࠤࡈࡖࡗࡕࡒࠣჯ")
    bstack1lll111l11l_opy_: Callable
    bstack1lll1111l1l_opy_: Callable
    def __init__(self):
        super().__init__()
        if os.getenv(bstack11llll_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡋࡒࡁࡈࡡࡒ࠵࠶࡟ࠢჰ"), bstack11llll_opy_ (u"ࠦ࠶ࠨჱ")) != bstack11llll_opy_ (u"ࠧ࠷ࠢჲ") or not self.is_enabled():
            self.logger.warning(bstack11llll_opy_ (u"ࠨࠢჳ") + str(self.__class__.__name__) + bstack11llll_opy_ (u"ࠢࠡࡦ࡬ࡷࡦࡨ࡬ࡦࡦࠥჴ"))
            return
        TestFramework.bstack111l1l1l1l_opy_((bstack1111l1lll1_opy_.TEST, bstack1111l11111_opy_.bstack111lll1l11_opy_), self.bstack1111ll1ll1_opy_)
        for event in bstack1111l1lll1_opy_:
            for state in bstack1111l11111_opy_:
                TestFramework.bstack111l1l1l1l_opy_((event, state), self.bstack1lll1111l11_opy_)
        bstack111ll1l11l_opy_.bstack111l1l1l1l_opy_((bstack111ll1ll1l_opy_.bstack111ll1l1ll_opy_, bstack111ll1ll11_opy_.bstack111lll1l11_opy_), self.bstack1lll11llll1_opy_)
        self.bstack1lll111l11l_opy_ = sys.stdout.write
        sys.stdout.write = self.bstack1lll11l1lll_opy_(bstack1llll1llll1_opy_.bstack1lll11111ll_opy_, self.bstack1lll111l11l_opy_)
        self.bstack1lll1111l1l_opy_ = sys.stderr.write
        sys.stderr.write = self.bstack1lll11l1lll_opy_(bstack1llll1llll1_opy_.bstack1lll1111111_opy_, self.bstack1lll1111l1l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1lll1111l11_opy_(
        self,
        f: TestFramework,
        instance: bstack1111ll1111_opy_,
        bstack111l1l1l11_opy_: Tuple[bstack1111l1lll1_opy_, bstack1111l11111_opy_],
        *args,
        **kwargs,
    ):
        if f.bstack1ll1llll111_opy_ and instance:
            bstack1lll11ll11l_opy_ = datetime.now()
            test_framework_state, test_hook_state = bstack111l1l1l11_opy_
            if test_framework_state == bstack1111l1lll1_opy_.bstack1lll1l11lll_opy_:
                return
            elif test_framework_state == bstack1111l1lll1_opy_.LOG:
                bstack111l1l1l1_opy_ = datetime.now()
                entries = bstack1llll1111l1_opy_.bstack1ll1lllllll_opy_(instance, bstack111l1l1l11_opy_)
                if entries:
                    self.bstack1ll1llllll1_opy_(instance, entries)
                    instance.bstack1ll1l1l11l_opy_(bstack11llll_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࠣჵ"), datetime.now() - bstack111l1l1l1_opy_)
                    bstack1llll1111l1_opy_.bstack1lll1l11111_opy_(instance, bstack111l1l1l11_opy_)
                instance.bstack1ll1l1l11l_opy_(bstack11llll_opy_ (u"ࠤࡲ࠵࠶ࡿ࠺ࡰࡰࡢࡥࡱࡲ࡟ࡵࡧࡶࡸࡤ࡫ࡶࡦࡰࡷࡷࠧჶ"), datetime.now() - bstack1lll11ll11l_opy_)
                return # do not send this event with the bstack1lll1111lll_opy_ bstack1lll11l11l1_opy_
            elif (
                test_framework_state == bstack1111l1lll1_opy_.TEST
                and test_hook_state == bstack1111l11111_opy_.bstack111lll1l11_opy_
                and not f.bstack111l11l1l1_opy_(instance, TestFramework.bstack1ll1llll1ll_opy_)
            ):
                self.logger.warning(bstack11llll_opy_ (u"ࠥࡨࡷࡵࡰࡱ࡫ࡱ࡫ࠥࡪࡵࡦࠢࡷࡳࠥࡲࡡࡤ࡭ࠣࡳ࡫ࠦࡲࡦࡵࡸࡰࡹࡹࠠࠣჷ") + str(TestFramework.bstack111l11l1l1_opy_(instance, TestFramework.bstack1ll1llll1ll_opy_)) + bstack11llll_opy_ (u"ࠦࠧჸ"))
                f.bstack111l1l11ll_opy_(instance, bstack1llll1llll1_opy_.bstack1lll1111ll1_opy_, True)
                return # do not send this event bstack1lll1l11l1l_opy_ bstack1ll1lllll11_opy_
            elif (
                f.bstack111lll1l1l_opy_(instance, bstack1llll1llll1_opy_.bstack1lll1111ll1_opy_, False)
                and test_framework_state == bstack1111l1lll1_opy_.bstack1ll1lllll1l_opy_
                and test_hook_state == bstack1111l11111_opy_.bstack111lll1l11_opy_
                and f.bstack111l11l1l1_opy_(instance, TestFramework.bstack1ll1llll1ll_opy_)
            ):
                self.logger.warning(bstack11llll_opy_ (u"ࠧ࡯࡮࡫ࡧࡦࡸ࡮ࡴࡧࠡࡖࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡔࡶࡤࡸࡪ࠴ࡔࡆࡕࡗ࠰࡚ࠥࡥࡴࡶࡋࡳࡴࡱࡓࡵࡣࡷࡩ࠳ࡖࡏࡔࡖࠣࠦჹ") + str(TestFramework.bstack111l11l1l1_opy_(instance, TestFramework.bstack1ll1llll1ll_opy_)) + bstack11llll_opy_ (u"ࠨࠢჺ"))
                self.bstack1lll1111l11_opy_(f, instance, (bstack1111l1lll1_opy_.TEST, bstack1111l11111_opy_.bstack111lll1l11_opy_), *args, **kwargs)
            bstack111l1l1l1_opy_ = datetime.now()
            data = instance.data.copy()
            bstack1lll1l1l111_opy_ = sorted(
                filter(lambda x: x.get(bstack11llll_opy_ (u"ࠢࡦࡸࡨࡲࡹࡥࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠥ჻"), None), data.pop(bstack11llll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫ࡳࠣჼ"), {}).values()),
                key=lambda x: x[bstack11llll_opy_ (u"ࠤࡨࡺࡪࡴࡴࡠࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠧჽ")],
            )
            if bstack1111lll11l_opy_.bstack1111llll1l_opy_ in data:
                data.pop(bstack1111lll11l_opy_.bstack1111llll1l_opy_)
            data.update({bstack11llll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࠥჾ"): bstack1lll1l1l111_opy_})
            instance.bstack1ll1l1l11l_opy_(bstack11llll_opy_ (u"ࠦ࡯ࡹ࡯࡯࠼ࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴࠤჿ"), datetime.now() - bstack111l1l1l1_opy_)
            bstack111l1l1l1_opy_ = datetime.now()
            event_json = dumps(data, cls=bstack1ll1lll1ll1_opy_)
            instance.bstack1ll1l1l11l_opy_(bstack11llll_opy_ (u"ࠧࡰࡳࡰࡰ࠽ࡳࡳࡥࡡ࡭࡮ࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺࡳࠣᄀ"), datetime.now() - bstack111l1l1l1_opy_)
            self.bstack1lll11l11l1_opy_(instance, bstack111l1l1l11_opy_, event_json=event_json)
            instance.bstack1ll1l1l11l_opy_(bstack11llll_opy_ (u"ࠨ࡯࠲࠳ࡼ࠾ࡴࡴ࡟ࡢ࡮࡯ࡣࡹ࡫ࡳࡵࡡࡨࡺࡪࡴࡴࡴࠤᄁ"), datetime.now() - bstack1lll11ll11l_opy_)
    def bstack1111ll1ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1111ll1111_opy_,
        bstack111l1l1l11_opy_: Tuple[bstack1111l1lll1_opy_, bstack1111l11111_opy_],
        *args,
        **kwargs,
    ):
        bstack1111l1ll1l_opy_ = [d for _, d in f.bstack111lll1l1l_opy_(instance, bstack1111lll11l_opy_.bstack1111llll1l_opy_, [])]
        if not bstack1111l1ll1l_opy_:
            return
        self.bstack1lll11l111l_opy_(f, instance, bstack1111l1ll1l_opy_, bstack111l1l1l11_opy_)
    def bstack1lll11l111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1111ll1111_opy_,
        bstack1111l1ll1l_opy_: List[bstack111lll1ll1_opy_],
        bstack111l1l1l11_opy_: Tuple[bstack1111l1lll1_opy_, bstack1111l11111_opy_],
    ):
        if f.bstack111lll1l1l_opy_(instance, bstack1111lll11l_opy_.bstack1111lll1l1_opy_, False):
            return
        self.bstack111l1l1lll_opy_()
        bstack111l1l1l1_opy_ = datetime.now()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack111lll1l1l_opy_(instance, TestFramework.bstack111l11l111_opy_)
        req.test_framework_name = TestFramework.bstack111lll1l1l_opy_(instance, TestFramework.bstack1lll11l1l1l_opy_)
        req.test_framework_version = TestFramework.bstack111lll1l1l_opy_(instance, TestFramework.bstack1lll1l1ll11_opy_)
        req.test_framework_state = bstack111l1l1l11_opy_[0].name
        req.test_hook_state = bstack111l1l1l11_opy_[1].name
        req.bstack11ll1l11_opy_ = TestFramework.bstack111lll1l1l_opy_(instance, TestFramework.bstack1lll11l11ll_opy_)
        for driver in bstack1111l1ll1l_opy_:
            session = req.bstack1lll1l1111l_opy_.add()
            session.bstack1lll111l1l1_opy_ = (
                bstack11llll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠨᄂ")
                if bstack111ll1l11l_opy_.bstack111lll1l1l_opy_(driver, bstack111ll1l11l_opy_.bstack1lll11lllll_opy_, False)
                else bstack11llll_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࡡࡪࡶ࡮ࡪࠢᄃ")
            )
            session.ref = driver.ref()
            session.hub_url = bstack111ll1l11l_opy_.bstack111lll1l1l_opy_(driver, bstack111ll1l11l_opy_.bstack1lll111l111_opy_, bstack11llll_opy_ (u"ࠤࠥᄄ"))
            session.framework_name = driver.framework_name
            session.framework_version = driver.framework_version
            session.framework_session_id = bstack111ll1l11l_opy_.bstack111lll1l1l_opy_(driver, bstack111ll1l11l_opy_.bstack1lll11l1ll1_opy_, bstack11llll_opy_ (u"ࠥࠦᄅ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        try:
            r = self.bstack111l11l1ll_opy_.TestSessionEvent(req)
            instance.bstack1ll1l1l11l_opy_(bstack11llll_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟ࡵࡧࡶࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡥࡷࡧࡱࡸࠧᄆ"), datetime.now() - bstack111l1l1l1_opy_)
            f.bstack111l1l11ll_opy_(instance, bstack1111lll11l_opy_.bstack1111lll1l1_opy_, r.success)
            if not r.success:
                self.logger.info(bstack11llll_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢᄇ") + str(r) + bstack11llll_opy_ (u"ࠨࠢᄈ"))
        except grpc.RpcError as e:
            self.logger.error(bstack11llll_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᄉ") + str(e) + bstack11llll_opy_ (u"ࠣࠤᄊ"))
            traceback.print_exc()
            raise e
    def bstack1lll11llll1_opy_(
        self,
        f: bstack111ll1l11l_opy_,
        _driver: object,
        exec: Tuple[bstack111lll1ll1_opy_, str],
        _1lll1l11ll1_opy_: Tuple[bstack111ll1ll1l_opy_, bstack111ll1ll11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if not bstack111ll1l11l_opy_.bstack1ll1lll1lll_opy_(method_name):
            return
        if f.bstack111111111l_opy_(*args) != bstack111ll1l11l_opy_.bstack1ll1lll1l1l_opy_:
            return
        bstack1lll11ll11l_opy_ = datetime.now()
        screenshot = result.get(bstack11llll_opy_ (u"ࠤࡹࡥࡱࡻࡥࠣᄋ"), None) if isinstance(result, dict) else None
        if not isinstance(screenshot, str) or len(screenshot) <= 0:
            self.logger.warning(bstack11llll_opy_ (u"ࠥ࡭ࡳࡼࡡ࡭࡫ࡧࠤࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠡ࡫ࡰࡥ࡬࡫ࠠࡣࡣࡶࡩ࠻࠺ࠠࡴࡶࡵࠦᄌ"))
            return
        bstack1lll1l1lll1_opy_ = self.bstack1lll1l11l11_opy_(instance)
        if bstack1lll1l1lll1_opy_:
            entry = bstack1llll111lll_opy_(TestFramework.bstack1lll11ll1ll_opy_, screenshot)
            self.bstack1ll1llllll1_opy_(bstack1lll1l1lll1_opy_, [entry])
            instance.bstack1ll1l1l11l_opy_(bstack11llll_opy_ (u"ࠦࡴ࠷࠱ࡺ࠼ࡲࡲࡤࡧࡦࡵࡧࡵࡣࡪࡾࡥࡤࡷࡷࡩࠧᄍ"), datetime.now() - bstack1lll11ll11l_opy_)
        else:
            self.logger.warning(bstack11llll_opy_ (u"ࠧࡻ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤࡹ࡫ࡳࡵࠢࡩࡳࡷࠦࡷࡩ࡫ࡦ࡬ࠥࡺࡨࡪࡵࠣࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠠࡸࡣࡶࠤࡹࡧ࡫ࡦࡰࠣࡦࡾࠦࡤࡳ࡫ࡹࡩࡷࡃࠢᄎ") + str(instance.ref()) + bstack11llll_opy_ (u"ࠨࠢᄏ"))
    def bstack1ll1llllll1_opy_(
        self,
        bstack1lll1l1lll1_opy_: bstack1111ll1111_opy_,
        entries: List[bstack1llll111lll_opy_],
    ):
        self.bstack111l1l1lll_opy_()
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack111lll1l1l_opy_(bstack1lll1l1lll1_opy_, TestFramework.bstack111l11l111_opy_)
        req.execution_context.hash = str(bstack1lll1l1lll1_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1lll1l1lll1_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1lll1l1lll1_opy_.context.process_id)
        for entry in entries:
            log_entry = req.bstack1ll11l11_opy_.add()
            log_entry.test_framework_name = TestFramework.bstack111lll1l1l_opy_(bstack1lll1l1lll1_opy_, TestFramework.bstack1lll11l1l1l_opy_)
            log_entry.test_framework_version = TestFramework.bstack111lll1l1l_opy_(bstack1lll1l1lll1_opy_, TestFramework.bstack1lll1l1ll11_opy_)
            log_entry.uuid = TestFramework.bstack111lll1l1l_opy_(bstack1lll1l1lll1_opy_, TestFramework.bstack1lll11l11ll_opy_)
            log_entry.test_framework_state = bstack1lll1l1lll1_opy_.state.name
            log_entry.message = entry.message.encode(bstack11llll_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᄐ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
        def bstack1ll1llll1l1_opy_():
            bstack111l1l1l1_opy_ = datetime.now()
            try:
                self.bstack111l11l1ll_opy_.LogCreatedEvent(req)
                if entry.kind == TestFramework.bstack1lll11ll1ll_opy_:
                    bstack1lll1l1lll1_opy_.bstack1ll1l1l11l_opy_(bstack11llll_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧᄑ"), datetime.now() - bstack111l1l1l1_opy_)
                else:
                    bstack1lll1l1lll1_opy_.bstack1ll1l1l11l_opy_(bstack11llll_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࡡ࡯ࡳ࡬ࠨᄒ"), datetime.now() - bstack111l1l1l1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11llll_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣᄓ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1111llllll_opy_.enqueue(bstack1ll1llll1l1_opy_)
    def bstack1lll11l11l1_opy_(
        self,
        instance: bstack1111ll1111_opy_,
        bstack111l1l1l11_opy_: Tuple[bstack1111l1lll1_opy_, bstack1111l11111_opy_],
        event_json=None,
    ):
        self.bstack111l1l1lll_opy_()
        req = structs.TestFrameworkEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack111lll1l1l_opy_(instance, TestFramework.bstack111l11l111_opy_)
        req.test_framework_name = TestFramework.bstack111lll1l1l_opy_(instance, TestFramework.bstack1lll11l1l1l_opy_)
        req.test_framework_version = TestFramework.bstack111lll1l1l_opy_(instance, TestFramework.bstack1lll1l1ll11_opy_)
        req.test_framework_state = bstack111l1l1l11_opy_[0].name
        req.test_hook_state = bstack111l1l1l11_opy_[1].name
        started_at = TestFramework.bstack111lll1l1l_opy_(instance, TestFramework.bstack1lll11l1l11_opy_, None)
        if started_at:
            req.started_at = started_at.isoformat()
        ended_at = TestFramework.bstack111lll1l1l_opy_(instance, TestFramework.bstack1lll111111l_opy_, None)
        if ended_at:
            req.ended_at = ended_at.isoformat()
        req.uuid = instance.ref()
        req.event_json = (event_json if event_json else dumps(instance.data, cls=bstack1ll1lll1ll1_opy_)).encode(bstack11llll_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥᄔ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        def bstack1ll1llll1l1_opy_():
            bstack111l1l1l1_opy_ = datetime.now()
            try:
                self.bstack111l11l1ll_opy_.TestFrameworkEvent(req)
                instance.bstack1ll1l1l11l_opy_(bstack11llll_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡨࡺࡪࡴࡴࠣᄕ"), datetime.now() - bstack111l1l1l1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11llll_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦᄖ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1111llllll_opy_.enqueue(bstack1ll1llll1l1_opy_)
    def bstack1lll11l1111_opy_(self, event_url: str, bstack1l11l1ll_opy_: dict) -> bool:
        return True # always return True so that old bstack1lll111llll_opy_ bstack1lll111lll1_opy_'t bstack1lll111l1ll_opy_
    def bstack1lll1l11l11_opy_(self, instance: bstack111lll1ll1_opy_):
        bstack1lll11111l1_opy_ = TestFramework.bstack1lll1l1ll1l_opy_(instance.context)
        for t in bstack1lll11111l1_opy_:
            bstack1111l1ll1l_opy_ = TestFramework.bstack111lll1l1l_opy_(t, bstack1111lll11l_opy_.bstack1111llll1l_opy_, [])
            if any(instance is d[1] for d in bstack1111l1ll1l_opy_):
                return t
    def bstack1lll1l1l1l1_opy_(self, message):
        self.bstack1lll111l11l_opy_(message + bstack11llll_opy_ (u"ࠢ࡝ࡰࠥᄗ"))
    def log_error(self, message):
        self.bstack1lll1111l1l_opy_(message + bstack11llll_opy_ (u"ࠣ࡞ࡱࠦᄘ"))
    def bstack1lll11l1lll_opy_(self, level, original_func):
        def bstack1lll1l111ll_opy_(*args):
            return_value = original_func(*args)
            if not args or not isinstance(args[0], str) or not args[0].strip():
                return return_value
            message = args[0].strip()
            bstack1lll11111l1_opy_ = TestFramework.bstack1lll111ll11_opy_()
            if not bstack1lll11111l1_opy_:
                return return_value
            bstack1lll1l1lll1_opy_ = next(
                (
                    instance
                    for instance in bstack1lll11111l1_opy_
                    if TestFramework.bstack111l11l1l1_opy_(instance, TestFramework.bstack1lll11l11ll_opy_)
                ),
                None,
            )
            if not bstack1lll1l1lll1_opy_:
                return
            entry = bstack1llll111lll_opy_(TestFramework.bstack1lll1l1l11l_opy_, message, level)
            self.bstack1ll1llllll1_opy_(bstack1lll1l1lll1_opy_, [entry])
            return return_value
        return bstack1lll1l111ll_opy_
class bstack1ll1lll1ll1_opy_(JSONEncoder):
    def __init__(self, **kwargs):
        self.bstack1lll11lll11_opy_ = set()
        kwargs[bstack11llll_opy_ (u"ࠤࡶ࡯࡮ࡶ࡫ࡦࡻࡶࠦᄙ")] = True
        super().__init__(**kwargs)
    def default(self, obj):
        return bstack1lll1l1l1ll_opy_(obj, self.bstack1lll11lll11_opy_)
def bstack1lll1l1llll_opy_(obj):
    return isinstance(obj, (str, int, float, bool, type(None)))
def bstack1lll1l1l1ll_opy_(obj, bstack1lll11lll11_opy_=None, max_depth=3):
    if bstack1lll11lll11_opy_ is None:
        bstack1lll11lll11_opy_ = set()
    if id(obj) in bstack1lll11lll11_opy_ or max_depth <= 0:
        return None
    max_depth -= 1
    bstack1lll11lll11_opy_.add(id(obj))
    if isinstance(obj, datetime):
        return obj.isoformat()
    bstack1lll11ll111_opy_ = TestFramework.bstack1lll111ll1l_opy_(obj)
    bstack1lll1l111l1_opy_ = next((k.lower() in bstack1lll11ll111_opy_.lower() for k in bstack1lll11lll1l_opy_.keys()), None)
    if bstack1lll1l111l1_opy_:
        obj = TestFramework.bstack1lll11ll1l1_opy_(obj, bstack1lll11lll1l_opy_[bstack1lll1l111l1_opy_])
    if not isinstance(obj, dict):
        keys = []
        if hasattr(obj, bstack11llll_opy_ (u"ࠥࡣࡤࡹ࡬ࡰࡶࡶࡣࡤࠨᄚ")):
            keys = getattr(obj, bstack11llll_opy_ (u"ࠦࡤࡥࡳ࡭ࡱࡷࡷࡤࡥࠢᄛ"), [])
        elif hasattr(obj, bstack11llll_opy_ (u"ࠧࡥ࡟ࡥ࡫ࡦࡸࡤࡥࠢᄜ")):
            keys = getattr(obj, bstack11llll_opy_ (u"ࠨ࡟ࡠࡦ࡬ࡧࡹࡥ࡟ࠣᄝ"), {}).keys()
        else:
            keys = dir(obj)
        obj = {k: getattr(obj, k, None) for k in keys if not str(k).startswith(bstack11llll_opy_ (u"ࠢࡠࠤᄞ"))}
        if not obj and bstack1lll11ll111_opy_ == bstack11llll_opy_ (u"ࠣࡲࡤࡸ࡭ࡲࡩࡣ࠰ࡓࡳࡸ࡯ࡸࡑࡣࡷ࡬ࠧᄟ"):
            obj = {bstack11llll_opy_ (u"ࠤࡳࡥࡹ࡮ࠢᄠ"): str(obj)}
    result = {}
    for key, value in obj.items():
        if not bstack1lll1l1llll_opy_(key) or str(key).startswith(bstack11llll_opy_ (u"ࠥࡣࠧᄡ")):
            continue
        if value is not None and bstack1lll1l1llll_opy_(value):
            result[key] = value
        elif isinstance(value, dict):
            r = bstack1lll1l1l1ll_opy_(value, bstack1lll11lll11_opy_, max_depth)
            if r is not None:
                result[key] = r
        elif isinstance(value, (list, tuple, set, frozenset)):
            result[key] = list(filter(None, [bstack1lll1l1l1ll_opy_(o, bstack1lll11lll11_opy_, max_depth) for o in value]))
    return result or None