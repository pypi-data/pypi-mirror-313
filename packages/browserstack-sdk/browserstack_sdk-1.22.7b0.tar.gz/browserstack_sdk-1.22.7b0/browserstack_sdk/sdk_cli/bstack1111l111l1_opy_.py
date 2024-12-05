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
import traceback
import grpc
import threading
from browserstack_sdk.sdk_cli.bstack111ll11ll1_opy_ import (
    bstack111ll1ll1l_opy_,
    bstack111ll1ll11_opy_,
    bstack111lll1ll1_opy_,
    bstack1111l1l11l_opy_,
)
from browserstack_sdk.sdk_cli.bstack111ll1l1l1_opy_ import bstack111ll1l11l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1111l1lll1_opy_, bstack1111l11111_opy_, bstack1111ll1111_opy_
from browserstack_sdk.sdk_cli.bstack1111l11lll_opy_ import bstack11111llll1_opy_
from datetime import datetime
from browserstack_sdk import sdk_pb2 as structs
from typing import Tuple, List, Any
from browserstack_sdk.sdk_cli.bstack1lll1ll11l_opy_ import bstack1lll1ll11l_opy_, Events, bstack11lllll11_opy_, bstack1111ll1lll_opy_
from browserstack_sdk.sdk_cli.bstack1111ll111l_opy_ import bstack1111l1llll_opy_
class bstack1111lll11l_opy_(bstack11111llll1_opy_):
    bstack1111ll11ll_opy_ = bstack11llll_opy_ (u"ࠢࡵࡧࡶࡸࡤࡪࡲࡪࡸࡨࡶࡸࠨ࿇")
    bstack1111llll1l_opy_ = bstack11llll_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡹࠢ࿈")
    bstack1111ll1l11_opy_ = bstack11llll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠤ࿉")
    bstack1111lll1ll_opy_ = bstack11llll_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡡࡵࡩ࡫ࡹࠢ࿊")
    bstack1111lll1l1_opy_ = bstack11llll_opy_ (u"ࠦࡨࡨࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡦࡶࡪࡧࡴࡦࡦࠥ࿋")
    bstack11111lllll_opy_ = bstack11llll_opy_ (u"ࠧࡩࡢࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡲࡦࡳࡥࠣ࿌")
    bstack1111l111ll_opy_ = bstack11llll_opy_ (u"ࠨࡣࡣࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡸࡺࡡࡵࡷࡶࠦ࿍")
    def __init__(self):
        super().__init__(bstack1111l11l11_opy_=self.bstack1111ll11ll_opy_, frameworks=[bstack111ll1l11l_opy_.NAME])
        if not self.is_enabled():
            return
        bstack1lll1ll11l_opy_.register(bstack1111ll1lll_opy_.bstack1111llll11_opy_, self.bstack1111ll11l1_opy_)
        bstack1lll1ll11l_opy_.register(bstack1111ll1lll_opy_.FINISHED, self.bstack1111ll1ll1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1111l1l1ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1111ll1111_opy_,
        bstack111l1l1l11_opy_: Tuple[bstack1111l1lll1_opy_, bstack1111l11111_opy_],
        *args,
        **kwargs,
    ):
        bstack1111l1ll1l_opy_ = self.bstack1111l1l1l1_opy_(instance.context)
        if not bstack1111l1ll1l_opy_:
            self.logger.debug(bstack11llll_opy_ (u"ࠢࡴࡧࡷࡣࡦࡩࡴࡪࡸࡨࡣࡩࡸࡩࡷࡧࡵࡷ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࠥ࿎") + str(bstack111l1l1l11_opy_) + bstack11llll_opy_ (u"ࠣࠤ࿏"))
        f.bstack111l1l11ll_opy_(instance, bstack1111lll11l_opy_.bstack1111llll1l_opy_, bstack1111l1ll1l_opy_)
    def bstack1111ll11l1_opy_(
        self,
        event_name: str,
        *args,
    ):
        context = bstack1111l1llll_opy_.create_context(event_name)
        bstack1111l1ll1l_opy_ = self.bstack1111l1l1l1_opy_(context)
        if not bstack1111l1ll1l_opy_:
            return
        for bstack1111ll1l1l_opy_, bstack1111l1l111_opy_ in bstack1111l1ll1l_opy_:
            if not bstack111ll1l11l_opy_.bstack1111l11ll1_opy_(bstack1111l1l111_opy_):
                continue
            driver = bstack1111ll1l1l_opy_()
            if not driver:
                continue
            driver.execute_script(
                bstack11llll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠢ࿐").format(
                    json.dumps(
                        {
                            bstack11llll_opy_ (u"ࠥࡥࡨࡺࡩࡰࡰࠥ࿑"): bstack11llll_opy_ (u"ࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࿒"),
                            bstack11llll_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࿓"): {bstack11llll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ࿔"): args[0]},
                        }
                    )
                )
            )
    def bstack1111l1111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1111ll1111_opy_,
        bstack111l1l1l11_opy_: Tuple[bstack1111l1lll1_opy_, bstack1111l11111_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1111l1l1ll_opy_(f, instance, bstack111l1l1l11_opy_, *args, **kwargs)
        if f.bstack111lll1l1l_opy_(instance, bstack1111lll11l_opy_.bstack11111lllll_opy_, False):
            return
        test_name = f.bstack111lll1l1l_opy_(instance, TestFramework.bstack1111l1ll11_opy_, None)
        if not test_name:
            self.logger.debug(bstack11llll_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡰࡤࡱࡪࠨ࿕"))
            return
        bstack1111l1ll1l_opy_ = f.bstack111lll1l1l_opy_(instance, bstack1111lll11l_opy_.bstack1111llll1l_opy_, [])
        if not bstack1111l1ll1l_opy_:
            return
        for bstack1111ll1l1l_opy_, bstack1111l1l111_opy_ in bstack1111l1ll1l_opy_:
            if not bstack111ll1l11l_opy_.bstack1111l11ll1_opy_(bstack1111l1l111_opy_):
                continue
            driver = bstack1111ll1l1l_opy_()
            if not driver:
                continue
            driver.execute_script(
                bstack11llll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂࠨ࿖").format(
                    json.dumps(
                        {
                            bstack11llll_opy_ (u"ࠤࡤࡧࡹ࡯࡯࡯ࠤ࿗"): bstack11llll_opy_ (u"ࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࿘"),
                            bstack11llll_opy_ (u"ࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࿙"): {bstack11llll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ࿚"): test_name},
                        }
                    )
                )
            )
        f.bstack111l1l11ll_opy_(instance, bstack1111lll11l_opy_.bstack11111lllll_opy_, True)
    def bstack1111ll1ll1_opy_(
        self,
        event_name: str,
        *args
    ):
        context = bstack1111l1llll_opy_.create_context(event_name)
        bstack1111l1ll1l_opy_ = self.bstack1111l1l1l1_opy_(context)
        if not bstack1111l1ll1l_opy_:
            pass
        driver = bstack1111l1ll1l_opy_[0][0]()
        driver.execute_script(
            bstack11llll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠦ࿛").format(
                json.dumps(
                    {
                        bstack11llll_opy_ (u"ࠢࡢࡥࡷ࡭ࡴࡴࠢ࿜"): bstack11llll_opy_ (u"ࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦ࿝"),
                        bstack11llll_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧ࿞"): {bstack11llll_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࠥ࿟"): threading.current_thread().testStatus },
                    }
                )
            )
        )
    def bstack1111lll111_opy_(
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
        if not f.bstack1111l11ll1_opy_(instance):
            return
        if f.bstack111lll1l1l_opy_(instance, bstack1111lll11l_opy_.bstack1111l111ll_opy_, False):
            return
        driver.execute_script(
            bstack11llll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠤ࿠").format(
                json.dumps(
                    {
                        bstack11llll_opy_ (u"ࠧࡧࡣࡵ࡫ࡲࡲࠧ࿡"): bstack11llll_opy_ (u"ࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤ࿢"),
                        bstack11llll_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࿣"): {bstack11llll_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣ࿤"): result},
                    }
                )
            )
        )
        f.bstack111l1l11ll_opy_(instance, bstack1111lll11l_opy_.bstack1111l111ll_opy_, True)
    def bstack1111l1l1l1_opy_(self, context: bstack1111l1l11l_opy_):
        bstack1111l1ll1l_opy_ = self.bstack1111l11l1l_opy_(context, reverse=True)
        return [f for f in bstack1111l1ll1l_opy_ if f[1].state != bstack111ll1ll1l_opy_.QUIT]