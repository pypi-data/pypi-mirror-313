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
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1111ll111l_opy_ import bstack1111l1llll_opy_
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1111l1lll1_opy_,
    bstack1111ll1111_opy_,
    bstack1111l11111_opy_,
    bstack1ll1l1ll1ll_opy_,
    bstack1llll111lll_opy_,
)
import traceback
class bstack1llll1111l1_opy_(TestFramework):
    bstack1ll111111l1_opy_ = bstack11llll_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࡸࠨᇓ")
    bstack1ll111l11l1_opy_ = bstack11llll_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࡣࡸࡺࡡࡳࡶࡨࡨࠧᇔ")
    bstack1ll111l1ll1_opy_ = bstack11llll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࠢᇕ")
    bstack1ll11111ll1_opy_ = bstack11llll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡲࡡࡴࡶࡢࡷࡹࡧࡲࡵࡧࡧࠦᇖ")
    bstack1ll111l1111_opy_ = bstack11llll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥ࡬ࡢࡵࡷࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࠨᇗ")
    bstack1ll1llll111_opy_: bool
    bstack1l1llllll1l_opy_ = [
        bstack1111l1lll1_opy_.bstack1ll1l1l1ll1_opy_,
        bstack1111l1lll1_opy_.bstack1ll1l1l1111_opy_,
        bstack1111l1lll1_opy_.bstack1ll1l111l1l_opy_,
        bstack1111l1lll1_opy_.bstack1ll1l111l11_opy_,
    ]
    def __init__(
        self,
        bstack1ll11llll1l_opy_: Dict[str, str],
        bstack1ll1l11l1l1_opy_: List[str]=[bstack11llll_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷࠦᇘ")],
    ):
        super().__init__(bstack1ll1l11l1l1_opy_, bstack1ll11llll1l_opy_)
        self.bstack1ll1llll111_opy_ = any(bstack11llll_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࠧᇙ") in item.lower() for item in bstack1ll1l11l1l1_opy_)
    def track_event(
        self,
        context: bstack1ll1l1ll1ll_opy_,
        test_framework_state: bstack1111l1lll1_opy_,
        test_hook_state: bstack1111l11111_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack1111l1lll1_opy_.NONE:
            self.logger.warning(bstack11llll_opy_ (u"ࠨࡩࡨࡰࡲࡶࡪࡪࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬ࠢࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀࠤࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࡃࠢᇚ") + str(test_hook_state) + bstack11llll_opy_ (u"ࠢࠣᇛ"))
            return
        if not self.bstack1ll1llll111_opy_:
            self.logger.warning(bstack11llll_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰࡶࡹࡵࡶ࡯ࡳࡶࡨࡨࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫࠾ࠤᇜ") + str(str(self.bstack1ll1l11l1l1_opy_)) + bstack11llll_opy_ (u"ࠤࠥᇝ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack11llll_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲࡪࡾࡰࡦࡥࡷࡩࡩࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᇞ") + str(kwargs) + bstack11llll_opy_ (u"ࠦࠧᇟ"))
            return
        instance = self.__1l1lllll1l1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack11llll_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡨࡢࡰࡧࡰࡪࡪࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥࡧࡲࡨࡵࡀࠦᇠ") + str(args) + bstack11llll_opy_ (u"ࠨࠢᇡ"))
            return
        try:
            if not TestFramework.bstack111l11l1l1_opy_(instance, TestFramework.bstack1111l1ll11_opy_) and test_hook_state == bstack1111l11111_opy_.bstack111l1llll1_opy_:
                test = bstack1llll1111l1_opy_.__1ll111lll11_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack11llll_opy_ (u"ࠢ࡭ࡱࡤࡨࡪࡪࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢᇢ") + str(test_hook_state) + bstack11llll_opy_ (u"ࠣࠤᇣ"))
            if test_framework_state == bstack1111l1lll1_opy_.TEST:
                if test_hook_state == bstack1111l11111_opy_.bstack111l1llll1_opy_ and not TestFramework.bstack111l11l1l1_opy_(instance, TestFramework.bstack1lll11l1l11_opy_):
                    TestFramework.bstack111l1l11ll_opy_(instance, TestFramework.bstack1lll11l1l11_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack11llll_opy_ (u"ࠤࡶࡩࡹࠦࡴࡦࡵࡷ࠱ࡸࡺࡡࡳࡶࠣࡪࡴࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢᇤ") + str(test_hook_state) + bstack11llll_opy_ (u"ࠥࠦᇥ"))
                elif test_hook_state == bstack1111l11111_opy_.bstack111lll1l11_opy_ and not TestFramework.bstack111l11l1l1_opy_(instance, TestFramework.bstack1lll111111l_opy_):
                    TestFramework.bstack111l1l11ll_opy_(instance, TestFramework.bstack1lll111111l_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack11llll_opy_ (u"ࠦࡸ࡫ࡴࠡࡶࡨࡷࡹ࠳ࡥ࡯ࡦࠣࡪࡴࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢᇦ") + str(test_hook_state) + bstack11llll_opy_ (u"ࠧࠨᇧ"))
            elif test_framework_state == bstack1111l1lll1_opy_.LOG and test_hook_state == bstack1111l11111_opy_.bstack111lll1l11_opy_:
                bstack1llll1111l1_opy_.__1ll1111l1l1_opy_(instance, *args)
            elif test_framework_state == bstack1111l1lll1_opy_.bstack1ll1lllll1l_opy_ and test_hook_state == bstack1111l11111_opy_.bstack111lll1l11_opy_:
                self.__1ll11111111_opy_(instance, *args)
            elif test_framework_state in bstack1llll1111l1_opy_.bstack1l1llllll1l_opy_:
                self.__1l1lllll111_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack11llll_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢᇨ") + str(instance.ref()) + bstack11llll_opy_ (u"ࠢࠣᇩ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1ll1l11111l_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
    def __1ll111l11ll_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack11llll_opy_ (u"ࠣࡩࡨࡸࡤࡸࡥࡴࡷ࡯ࡸࠧᇪ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1lll11ll1l1_opy_(rep, [bstack11llll_opy_ (u"ࠤࡺ࡬ࡪࡴࠢᇫ"), bstack11llll_opy_ (u"ࠥࡳࡺࡺࡣࡰ࡯ࡨࠦᇬ"), bstack11llll_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦᇭ"), bstack11llll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧᇮ"), bstack11llll_opy_ (u"ࠨࡳ࡬࡫ࡳࡴࡪࡪࠢᇯ"), bstack11llll_opy_ (u"ࠢ࡭ࡱࡱ࡫ࡷ࡫ࡰࡳࡶࡨࡼࡹࠨᇰ")])
        return None
    def __1ll11111111_opy_(self, instance: bstack1111ll1111_opy_, *args):
        result = self.__1ll111l11ll_opy_(*args)
        if not result:
            return
        failure = None
        bstack111llll11l_opy_ = None
        if result.get(bstack11llll_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤᇱ"), None) == bstack11llll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤᇲ") and len(args) > 1 and getattr(args[1], bstack11llll_opy_ (u"ࠥࡩࡽࡩࡩ࡯ࡨࡲࠦᇳ"), None) is not None:
            failure = [{bstack11llll_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧᇴ"): [args[1].excinfo.exconly(), result.get(bstack11llll_opy_ (u"ࠧࡲ࡯࡯ࡩࡵࡩࡵࡸࡴࡦࡺࡷࠦᇵ"), None)]}]
            bstack111llll11l_opy_ = bstack11llll_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢᇶ") if bstack11llll_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࠥᇷ") in getattr(args[1].excinfo, bstack11llll_opy_ (u"ࠣࡶࡼࡴࡪࡴࡡ࡮ࡧࠥᇸ"), bstack11llll_opy_ (u"ࠤࠥᇹ")) else bstack11llll_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦᇺ")
        bstack1l1llll1ll1_opy_ = result.get(bstack11llll_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧᇻ"), TestFramework.bstack1ll1l111ll1_opy_)
        if bstack1l1llll1ll1_opy_ != TestFramework.bstack1ll1l111ll1_opy_:
            TestFramework.bstack111l1l11ll_opy_(instance, TestFramework.bstack1ll1llll1ll_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack1ll1l11l111_opy_(instance, {
            TestFramework.bstack1ll1l1l1l1l_opy_: failure,
            TestFramework.bstack1ll1l1ll111_opy_: bstack111llll11l_opy_,
            TestFramework.bstack1ll1l1l11ll_opy_: bstack1l1llll1ll1_opy_,
        })
    def __1l1lllll1l1_opy_(
        self,
        context: bstack1ll1l1ll1ll_opy_,
        test_framework_state: bstack1111l1lll1_opy_,
        test_hook_state: bstack1111l11111_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack1111l1lll1_opy_.bstack1lll1l11lll_opy_:
            instance = self.__1l1lllllll1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack1ll111ll1ll_opy_ bstack1ll111l111l_opy_ this to be bstack11llll_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᇼ")
            if test_framework_state == bstack1111l1lll1_opy_.bstack1ll1l11l1ll_opy_:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__1ll111l1l1l_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1111l1lll1_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack11llll_opy_ (u"ࠨ࡮ࡰࡦࡨࠦᇽ"), None), bstack11llll_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᇾ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack11llll_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᇿ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1ll1ll111l1_opy_(target) if target else None
        return instance
    def __1l1lllll111_opy_(
        self,
        instance: bstack1111ll1111_opy_,
        test_framework_state: bstack1111l1lll1_opy_,
        test_hook_state: bstack1111l11111_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack1ll1111ll1l_opy_ = TestFramework.bstack111lll1l1l_opy_(instance, bstack1llll1111l1_opy_.bstack1ll111l11l1_opy_, {})
        if not key in bstack1ll1111ll1l_opy_:
            bstack1ll1111ll1l_opy_[key] = []
        bstack1l1llllll11_opy_ = TestFramework.bstack111lll1l1l_opy_(instance, bstack1llll1111l1_opy_.bstack1ll111l1ll1_opy_, {})
        if not key in bstack1l1llllll11_opy_:
            bstack1l1llllll11_opy_[key] = []
        bstack1ll1111l111_opy_ = {
            bstack1llll1111l1_opy_.bstack1ll111l11l1_opy_: bstack1ll1111ll1l_opy_,
            bstack1llll1111l1_opy_.bstack1ll111l1ll1_opy_: bstack1l1llllll11_opy_,
        }
        if test_hook_state == bstack1111l11111_opy_.bstack111l1llll1_opy_:
            hook = {
                bstack11llll_opy_ (u"ࠤ࡮ࡩࡾࠨሀ"): key,
                TestFramework.bstack1ll1l1111ll_opy_: uuid4().__str__(),
                TestFramework.bstack1ll1l1ll11l_opy_: TestFramework.bstack1ll1l11l11l_opy_,
                TestFramework.bstack1ll11lll1ll_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1ll1l1l111l_opy_: [],
            }
            bstack1ll1111ll1l_opy_[key].append(hook)
            bstack1ll1111l111_opy_[bstack1llll1111l1_opy_.bstack1ll11111ll1_opy_] = key
        elif test_hook_state == bstack1111l11111_opy_.bstack111lll1l11_opy_:
            bstack1ll111ll111_opy_ = bstack1ll1111ll1l_opy_.get(key, [])
            hook = bstack1ll111ll111_opy_.pop() if bstack1ll111ll111_opy_ else None
            if hook:
                result = self.__1ll111l11ll_opy_(*args)
                if result:
                    bstack1l1llll1lll_opy_ = result.get(bstack11llll_opy_ (u"ࠥࡳࡺࡺࡣࡰ࡯ࡨࠦሁ"), TestFramework.bstack1ll1l11l11l_opy_)
                    if bstack1l1llll1lll_opy_ != TestFramework.bstack1ll1l11l11l_opy_:
                        hook[TestFramework.bstack1ll1l1ll11l_opy_] = bstack1l1llll1lll_opy_
                hook[TestFramework.bstack1ll1l111111_opy_] = datetime.now(tz=timezone.utc)
                bstack1l1llllll11_opy_[key].append(hook)
                bstack1ll1111l111_opy_[bstack1llll1111l1_opy_.bstack1ll111l1111_opy_] = key
        TestFramework.bstack1ll1l11l111_opy_(instance, bstack1ll1111l111_opy_)
        self.logger.debug(bstack11llll_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢ࡬ࡴࡵ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࡰ࡫ࡹࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡨࡰࡱ࡮ࡷࡤࡹࡴࡢࡴࡷࡩࡩࡃࡻࡩࡱࡲ࡯ࡸࡥࡳࡵࡣࡵࡸࡪࡪࡽࠡࡪࡲࡳࡰࡹ࡟ࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥ࠿ࠥሂ") + str(bstack1l1llllll11_opy_) + bstack11llll_opy_ (u"ࠧࠨሃ"))
    def __1l1lllllll1_opy_(
        self,
        context: bstack1ll1l1ll1ll_opy_,
        test_framework_state: bstack1111l1lll1_opy_,
        test_hook_state: bstack1111l11111_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1lll11ll1l1_opy_(args[0], [bstack11llll_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧሄ"), bstack11llll_opy_ (u"ࠢࡢࡴࡪࡲࡦࡳࡥࠣህ"), bstack11llll_opy_ (u"ࠣࡲࡤࡶࡦࡳࡳࠣሆ"), bstack11llll_opy_ (u"ࠤ࡬ࡨࡸࠨሇ"), bstack11llll_opy_ (u"ࠥࡹࡳ࡯ࡴࡵࡧࡶࡸࠧለ"), bstack11llll_opy_ (u"ࠦࡧࡧࡳࡦ࡫ࡧࠦሉ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scope = request.scope if hasattr(request, bstack11llll_opy_ (u"ࠧࡹࡣࡰࡲࡨࠦሊ")) else fixturedef.get(bstack11llll_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧላ"), None)
        fixturename = request.fixturename if hasattr(request, bstack11llll_opy_ (u"ࠢࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࠧሌ")) else None
        node = request.node if hasattr(request, bstack11llll_opy_ (u"ࠣࡰࡲࡨࡪࠨል")) else None
        target = request.node.nodeid if hasattr(node, bstack11llll_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤሎ")) else None
        baseid = fixturedef.get(bstack11llll_opy_ (u"ࠥࡦࡦࡹࡥࡪࡦࠥሏ"), None) or bstack11llll_opy_ (u"ࠦࠧሐ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack11llll_opy_ (u"ࠧࡥࡰࡺࡨࡸࡲࡨ࡯ࡴࡦ࡯ࠥሑ")):
            target = bstack1llll1111l1_opy_.__1ll111ll1l1_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack11llll_opy_ (u"ࠨ࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠣሒ")) else None
            if target and not TestFramework.bstack1ll1ll111l1_opy_(target):
                self.__1ll111l1l1l_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack11llll_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡦࡸࡨࡲࡹࡀࠠࡧࡣ࡯ࡰࡧࡧࡣ࡬ࠢࡷࡥࡷ࡭ࡥࡵ࠿ࡾࡸࡦࡸࡧࡦࡶࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࡾࠢࡱࡳࡩ࡫࠽ࡼࡰࡲࡨࡪࢃࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࠤሓ") + str(test_hook_state) + bstack11llll_opy_ (u"ࠣࠤሔ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack11llll_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡨ࡬ࡼࡹࡻࡲࡦࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡨࡪ࡬࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡦࡨࡪࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡴࡢࡴࡪࡩࡹࡃࠢሕ") + str(target) + bstack11llll_opy_ (u"ࠥࠦሖ"))
            return None
        instance = TestFramework.bstack1ll1ll111l1_opy_(target)
        if not instance:
            self.logger.warning(bstack11llll_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡪ࡮ࡾࡴࡶࡴࡨࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡨࡢࡰࡧࡰࡪࡪࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࡿࠣࡷࡨࡵࡰࡦ࠿ࡾࡷࡨࡵࡰࡦࡿࠣࡦࡦࡹࡥࡪࡦࡀࡿࡧࡧࡳࡦ࡫ࡧࢁࠥࡺࡡࡳࡩࡨࡸࡂࠨሗ") + str(target) + bstack11llll_opy_ (u"ࠧࠨመ"))
            return None
        bstack1ll11111l11_opy_ = TestFramework.bstack111lll1l1l_opy_(instance, bstack1llll1111l1_opy_.bstack1ll111111l1_opy_, {})
        if os.getenv(bstack11llll_opy_ (u"ࠨࡓࡅࡍࡢࡇࡑࡏ࡟ࡇࡎࡄࡋࡤࡌࡉ࡙ࡖࡘࡖࡊ࡙ࠢሙ"), bstack11llll_opy_ (u"ࠢ࠲ࠤሚ")) == bstack11llll_opy_ (u"ࠣ࠳ࠥማ"):
            bstack1l1lllll11l_opy_ = bstack11llll_opy_ (u"ࠤ࠽ࠦሜ").join((scope, fixturename))
            bstack1ll111ll11l_opy_ = datetime.now(tz=timezone.utc)
            bstack1l1lllll1ll_opy_ = {
                bstack11llll_opy_ (u"ࠥ࡯ࡪࡿࠢም"): bstack1l1lllll11l_opy_,
                bstack11llll_opy_ (u"ࠦࡹࡧࡧࡴࠤሞ"): bstack1llll1111l1_opy_.__1ll111l1lll_opy_(request.node),
                bstack11llll_opy_ (u"ࠧ࡬ࡩࡹࡶࡸࡶࡪࠨሟ"): fixturedef,
                bstack11llll_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧሠ"): scope,
                bstack11llll_opy_ (u"ࠢࡵࡻࡳࡩࠧሡ"): None,
            }
            try:
                if test_hook_state == bstack1111l11111_opy_.bstack111lll1l11_opy_ and callable(getattr(args[-1], bstack11llll_opy_ (u"ࠣࡩࡨࡸࡤࡸࡥࡴࡷ࡯ࡸࠧሢ"), None)):
                    bstack1l1lllll1ll_opy_[bstack11llll_opy_ (u"ࠤࡷࡽࡵ࡫ࠢሣ")] = TestFramework.bstack1lll111ll1l_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1111l11111_opy_.bstack111l1llll1_opy_:
                bstack1l1lllll1ll_opy_[bstack11llll_opy_ (u"ࠥࡹࡺ࡯ࡤࠣሤ")] = uuid4().__str__()
                bstack1l1lllll1ll_opy_[bstack1llll1111l1_opy_.bstack1ll11lll1ll_opy_] = bstack1ll111ll11l_opy_
            elif test_hook_state == bstack1111l11111_opy_.bstack111lll1l11_opy_:
                bstack1l1lllll1ll_opy_[bstack1llll1111l1_opy_.bstack1ll1l111111_opy_] = bstack1ll111ll11l_opy_
            if bstack1l1lllll11l_opy_ in bstack1ll11111l11_opy_:
                bstack1ll11111l11_opy_[bstack1l1lllll11l_opy_].update(bstack1l1lllll1ll_opy_)
                self.logger.debug(bstack11llll_opy_ (u"ࠦࡺࡶࡤࡢࡶࡨࡨࠥ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࡿࠣࡷࡨࡵࡰࡦ࠿ࡾࡷࡨࡵࡰࡦࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡁࠧሥ") + str(bstack1ll11111l11_opy_[bstack1l1lllll11l_opy_]) + bstack11llll_opy_ (u"ࠧࠨሦ"))
            else:
                bstack1ll11111l11_opy_[bstack1l1lllll11l_opy_] = bstack1l1lllll1ll_opy_
                self.logger.debug(bstack11llll_opy_ (u"ࠨࡳࡢࡸࡨࡨࠥ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࡿࠣࡷࡨࡵࡰࡦ࠿ࡾࡷࡨࡵࡰࡦࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡁࢀࡺࡥࡴࡶࡢࡪ࡮ࡾࡴࡶࡴࡨࢁࠥࡺࡲࡢࡥ࡮ࡩࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࡳ࠾ࠤሧ") + str(len(bstack1ll11111l11_opy_)) + bstack11llll_opy_ (u"ࠢࠣረ"))
        TestFramework.bstack111l1l11ll_opy_(instance, bstack1llll1111l1_opy_.bstack1ll111111l1_opy_, bstack1ll11111l11_opy_)
        self.logger.debug(bstack11llll_opy_ (u"ࠣࡵࡤࡺࡪࡪࠠࡧ࡫ࡻࡸࡺࡸࡥࡴ࠿ࡾࡰࡪࡴࠨࡵࡴࡤࡧࡰ࡫ࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࠬࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣሩ") + str(instance.ref()) + bstack11llll_opy_ (u"ࠤࠥሪ"))
        return instance
    def __1ll111l1l1l_opy_(
        self,
        context: bstack1ll1l1ll1ll_opy_,
        test_framework_state: bstack1111l1lll1_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack1111l1llll_opy_.create_context(target)
        ob = bstack1111ll1111_opy_(ctx, self.bstack1ll1l11l1l1_opy_, self.bstack1ll11llll1l_opy_, test_framework_state)
        TestFramework.bstack1ll1l11l111_opy_(ob, {
            TestFramework.bstack1lll11l1l1l_opy_: context.test_framework_name,
            TestFramework.bstack1lll1l1ll11_opy_: context.test_framework_version,
            TestFramework.bstack1ll11lllll1_opy_: [],
            bstack1llll1111l1_opy_.bstack1ll111111l1_opy_: {},
            bstack1llll1111l1_opy_.bstack1ll111l1ll1_opy_: {},
            bstack1llll1111l1_opy_.bstack1ll111l11l1_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack111l1l11ll_opy_(ob, TestFramework.bstack1ll1l111lll_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack111l1l11ll_opy_(ob, TestFramework.bstack111l11l111_opy_, context.platform_index)
        TestFramework.bstack1llllll1111_opy_[ctx.id] = ob
        self.logger.debug(bstack11llll_opy_ (u"ࠥࡷࡦࡼࡥࡥࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤࡨࡺࡸ࠯࡫ࡧࡁࢀࡩࡴࡹ࠰࡬ࡨࢂࠦࡴࡢࡴࡪࡩࡹࡃࡻࡵࡣࡵ࡫ࡪࡺࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࡴ࠿ࠥራ") + str(TestFramework.bstack1llllll1111_opy_.keys()) + bstack11llll_opy_ (u"ࠦࠧሬ"))
        return ob
    @staticmethod
    def bstack1ll1lllllll_opy_(instance: bstack1111ll1111_opy_, bstack111l1l1l11_opy_: Tuple[bstack1111l1lll1_opy_, bstack1111l11111_opy_]):
        bstack1ll111111ll_opy_ = (
            bstack1llll1111l1_opy_.bstack1ll11111ll1_opy_
            if bstack111l1l1l11_opy_[1] == bstack1111l11111_opy_.bstack111l1llll1_opy_
            else bstack1llll1111l1_opy_.bstack1ll111l1111_opy_
        )
        hook = bstack1llll1111l1_opy_.bstack1ll1111l1ll_opy_(instance, bstack1ll111111ll_opy_)
        entries = hook.get(TestFramework.bstack1ll1l1l111l_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack111lll1l1l_opy_(instance, TestFramework.bstack1ll11lllll1_opy_, []))
        return entries
    @staticmethod
    def bstack1lll1l11111_opy_(instance: bstack1111ll1111_opy_, bstack111l1l1l11_opy_: Tuple[bstack1111l1lll1_opy_, bstack1111l11111_opy_]):
        bstack1ll111111ll_opy_ = (
            bstack1llll1111l1_opy_.bstack1ll11111ll1_opy_
            if bstack111l1l1l11_opy_[1] == bstack1111l11111_opy_.bstack111l1llll1_opy_
            else bstack1llll1111l1_opy_.bstack1ll111l1111_opy_
        )
        bstack1llll1111l1_opy_.bstack1ll1111llll_opy_(instance, bstack1ll111111ll_opy_)
        TestFramework.bstack111lll1l1l_opy_(instance, TestFramework.bstack1ll11lllll1_opy_, []).clear()
    @staticmethod
    def bstack1ll1111l1ll_opy_(instance: bstack1111ll1111_opy_, bstack1ll111111ll_opy_: str):
        bstack1ll11111l1l_opy_ = (
            bstack1llll1111l1_opy_.bstack1ll111l1ll1_opy_
            if bstack1ll111111ll_opy_ == bstack1llll1111l1_opy_.bstack1ll111l1111_opy_
            else bstack1llll1111l1_opy_.bstack1ll111l11l1_opy_
        )
        bstack1ll1111lll1_opy_ = TestFramework.bstack111lll1l1l_opy_(instance, bstack1ll111111ll_opy_, None)
        bstack1ll1111l11l_opy_ = TestFramework.bstack111lll1l1l_opy_(instance, bstack1ll11111l1l_opy_, None) if bstack1ll1111lll1_opy_ else None
        return (
            bstack1ll1111l11l_opy_[bstack1ll1111lll1_opy_][-1]
            if isinstance(bstack1ll1111l11l_opy_, dict) and len(bstack1ll1111l11l_opy_.get(bstack1ll1111lll1_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack1ll1111llll_opy_(instance: bstack1111ll1111_opy_, bstack1ll111111ll_opy_: str):
        hook = bstack1llll1111l1_opy_.bstack1ll1111l1ll_opy_(instance, bstack1ll111111ll_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1ll1l1l111l_opy_, []).clear()
    @staticmethod
    def __1ll1111l1l1_opy_(instance: bstack1111ll1111_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack11llll_opy_ (u"ࠧ࡭ࡥࡵࡡࡵࡩࡨࡵࡲࡥࡵࠥር"), None)):
            return
        if os.getenv(bstack11llll_opy_ (u"ࠨࡓࡅࡍࡢࡇࡑࡏ࡟ࡇࡎࡄࡋࡤࡒࡏࡈࡕࠥሮ"), bstack11llll_opy_ (u"ࠢ࠲ࠤሯ")) != bstack11llll_opy_ (u"ࠣ࠳ࠥሰ"):
            bstack1llll1111l1_opy_.logger.warning(bstack11llll_opy_ (u"ࠤ࡬࡫ࡳࡵࡲࡪࡰࡪࠤࡨࡧࡰ࡭ࡱࡪࠦሱ"))
            return
        bstack1ll11111lll_opy_ = {
            bstack11llll_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤሲ"): (bstack1llll1111l1_opy_.bstack1ll11111ll1_opy_, bstack1llll1111l1_opy_.bstack1ll111l11l1_opy_),
            bstack11llll_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨሳ"): (bstack1llll1111l1_opy_.bstack1ll111l1111_opy_, bstack1llll1111l1_opy_.bstack1ll111l1ll1_opy_),
        }
        for when in (bstack11llll_opy_ (u"ࠧࡹࡥࡵࡷࡳࠦሴ"), bstack11llll_opy_ (u"ࠨࡣࡢ࡮࡯ࠦስ"), bstack11llll_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤሶ")):
            bstack1ll1111ll11_opy_ = args[1].get_records(when)
            if not bstack1ll1111ll11_opy_:
                continue
            records = [
                bstack1llll111lll_opy_(
                    kind=TestFramework.bstack1lll1l1l11l_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack11llll_opy_ (u"ࠣ࡮ࡨࡺࡪࡲ࡮ࡢ࡯ࡨࠦሷ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack11llll_opy_ (u"ࠤࡦࡶࡪࡧࡴࡦࡦࠥሸ")) and r.created
                        else None
                    ),
                )
                for r in bstack1ll1111ll11_opy_
                if isinstance(getattr(r, bstack11llll_opy_ (u"ࠥࡱࡪࡹࡳࡢࡩࡨࠦሹ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack1ll111l1l11_opy_, bstack1ll11111l1l_opy_ = bstack1ll11111lll_opy_.get(when, (None, None))
            bstack1ll1111111l_opy_ = TestFramework.bstack111lll1l1l_opy_(instance, bstack1ll111l1l11_opy_, None) if bstack1ll111l1l11_opy_ else None
            bstack1ll1111l11l_opy_ = TestFramework.bstack111lll1l1l_opy_(instance, bstack1ll11111l1l_opy_, None) if bstack1ll1111111l_opy_ else None
            if isinstance(bstack1ll1111l11l_opy_, dict) and len(bstack1ll1111l11l_opy_.get(bstack1ll1111111l_opy_, [])) > 0:
                hook = bstack1ll1111l11l_opy_[bstack1ll1111111l_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack1ll1l1l111l_opy_ in hook:
                    hook[TestFramework.bstack1ll1l1l111l_opy_].extend(records)
                    continue
            bstack1ll11l11_opy_ = TestFramework.bstack111lll1l1l_opy_(instance, TestFramework.bstack1ll11lllll1_opy_, [])
            bstack1ll11l11_opy_.extend(records)
    @staticmethod
    def __1ll111lll11_opy_(test) -> Dict[str, Any]:
        test_id = bstack1llll1111l1_opy_.__1ll111ll1l1_opy_(test.location) if hasattr(test, bstack11llll_opy_ (u"ࠦࡱࡵࡣࡢࡶ࡬ࡳࡳࠨሺ")) else getattr(test, bstack11llll_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧሻ"), None)
        test_name = test.name if hasattr(test, bstack11llll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦሼ")) else None
        bstack1l1llllllll_opy_ = test.fspath.strpath if hasattr(test, bstack11llll_opy_ (u"ࠢࡧࡵࡳࡥࡹ࡮ࠢሽ")) and test.fspath else None
        if not test_id or not test_name or not bstack1l1llllllll_opy_:
            return None
        code = None
        if hasattr(test, bstack11llll_opy_ (u"ࠣࡱࡥ࡮ࠧሾ")):
            try:
                import inspect
                code = inspect.getsource(test.obj)
            except:
                pass
        return {
            TestFramework.bstack1lll11l11ll_opy_: uuid4().__str__(),
            TestFramework.bstack1111l1ll11_opy_: test_id,
            TestFramework.bstack1ll1ll1l11l_opy_: test_name,
            TestFramework.bstack1ll1l1l11l1_opy_: getattr(test, bstack11llll_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤሿ"), None),
            TestFramework.bstack1ll1l1lll1l_opy_: os.path.relpath(bstack1l1llllllll_opy_, start=os.getcwd()),
            TestFramework.bstack1ll1l11lll1_opy_: bstack1llll1111l1_opy_.__1ll111l1lll_opy_(test),
            TestFramework.bstack1ll1l11ll1l_opy_: code,
            TestFramework.bstack1ll1l1l11ll_opy_: TestFramework.bstack1ll1l111ll1_opy_,
        }
    @staticmethod
    def __1ll111l1lll_opy_(test) -> List[str]:
        return (
            [getattr(f, bstack11llll_opy_ (u"ࠥࡲࡦࡳࡥࠣቀ"), None) for f in test.own_markers if getattr(f, bstack11llll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤቁ"), None)]
            if isinstance(getattr(test, bstack11llll_opy_ (u"ࠧࡵࡷ࡯ࡡࡰࡥࡷࡱࡥࡳࡵࠥቂ"), None), list)
            else []
        )
    @staticmethod
    def __1ll111ll1l1_opy_(location):
        return bstack11llll_opy_ (u"ࠨ࠺࠻ࠤቃ").join(filter(lambda x: isinstance(x, str), location))