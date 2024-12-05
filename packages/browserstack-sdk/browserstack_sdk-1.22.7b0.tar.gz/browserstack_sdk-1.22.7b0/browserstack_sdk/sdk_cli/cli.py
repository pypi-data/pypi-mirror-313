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
import subprocess
import threading
import time
import os
import sys
import grpc
import re
from browserstack_sdk import sdk_pb2_grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1111llllll_opy_ import bstack1111lllll1_opy_
from browserstack_sdk.sdk_cli.bstack111ll111l1_opy_ import bstack111l1lllll_opy_
from browserstack_sdk.sdk_cli.bstack1llll1ll1l1_opy_ import bstack1lllll111ll_opy_
from browserstack_sdk.sdk_cli.bstack11111111l1_opy_ import bstack1llllllll11_opy_
from browserstack_sdk.sdk_cli.bstack111l111ll1_opy_ import bstack111l111lll_opy_
from browserstack_sdk.sdk_cli.bstack1111l111l1_opy_ import bstack1111lll11l_opy_
from browserstack_sdk.sdk_cli.bstack1llll111ll1_opy_ import bstack1llll1llll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1ll11l_opy_ import bstack1lll1ll11l_opy_, Events, bstack11lllll11_opy_
from browserstack_sdk.sdk_cli.bstack1llllll1ll1_opy_ import bstack1llll1111l1_opy_
from browserstack_sdk.sdk_cli.bstack111ll1l1l1_opy_ import bstack111ll1l11l_opy_
from browserstack_sdk.sdk_cli.bstack111ll11ll1_opy_ import bstack11111l1lll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework
from bstack_utils.helper import bstack11ll11111_opy_, Notset, bstack1lllll11ll1_opy_, bstack1llllll1l1l_opy_, bstack1llllll1l11_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1111l1lll1_opy_, bstack1111ll1111_opy_, bstack1111l11111_opy_, bstack1llll111lll_opy_
from browserstack_sdk.sdk_cli.bstack111ll11ll1_opy_ import bstack111lll1ll1_opy_, bstack111ll1ll1l_opy_, bstack111ll1ll11_opy_
from bstack_utils.constants import *
from bstack_utils import bstack1ll1l1l1l1_opy_
from typing import Any, List, Union, Dict
import logging
import traceback
from google.protobuf.json_format import MessageToDict
from datetime import datetime, timedelta
from collections import defaultdict
logger = bstack1ll1l1l1l1_opy_.get_logger(__name__, bstack1ll1l1l1l1_opy_.bstack1lllllll111_opy_())
def bstack1llllll11l1_opy_(bs_config):
    bstack1llll1l11l1_opy_ = bstack11llll_opy_ (u"ࠪࠫဥ")
    try:
        bstack1lllll1l1ll_opy_ = bstack1llllll1l1l_opy_()
        bstack1llll1l11l1_opy_ = bstack1llllll1l11_opy_(bstack1lllll1l1ll_opy_)
        bstack1lllll111l1_opy_ = bstack1lllll11ll1_opy_(bstack1llll1l11l1_opy_, bstack1lllll1l1ll_opy_, bs_config)
        bstack1llll1l11l1_opy_ = bstack1lllll111l1_opy_ if bstack1lllll111l1_opy_ else bstack1llll1l11l1_opy_
        if not bstack1llll1l11l1_opy_:
            raise ValueError(bstack11llll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡧ࡫ࡱࡨ࡙ࠥࡄࡌࡡࡆࡐࡎࡥࡂࡊࡐࡢࡔࡆ࡚ࡈࠣဦ"))
    except Exception as ex:
        logger.debug(bstack11llll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡨࡴࡽ࡮࡭ࡱࡤࡨ࡮ࡴࡧࠡࡶ࡫ࡩࠥࡲࡡࡵࡧࡶࡸࠥࡨࡩ࡯ࡣࡵࡽࠧဧ"))
        bstack1llll1l11l1_opy_ = os.environ.get(bstack11llll_opy_ (u"ࠨࡓࡅࡍࡢࡇࡑࡏ࡟ࡃࡋࡑࡣࡕࡇࡔࡉࠤဨ"))
        if bstack1llll1l11l1_opy_:
            logger.debug(bstack11llll_opy_ (u"ࠢࡇࡣ࡯ࡰ࡮ࡴࡧࠡࡤࡤࡧࡰࠦࡴࡰࠢࡖࡈࡐࡥࡃࡍࡋࡢࡆࡎࡔ࡟ࡑࡃࡗࡌࠥ࡬ࡲࡰ࡯ࠣࡩࡳࡼࡩࡳࡱࡱࡱࡪࡴࡴ࠻ࠢࠥဩ") + str(bstack1llll1l11l1_opy_) + bstack11llll_opy_ (u"ࠣࠤဪ"))
        else:
            logger.debug(bstack11llll_opy_ (u"ࠤࡑࡳࠥࡼࡡ࡭࡫ࡧࠤࡘࡊࡋࡠࡅࡏࡍࡤࡈࡉࡏࡡࡓࡅ࡙ࡎࠠࡧࡱࡸࡲࡩࠦࡩ࡯ࠢࡨࡲࡻ࡯ࡲࡰࡰࡰࡩࡳࡺ࠻ࠡࡵࡨࡸࡺࡶࠠ࡮ࡣࡼࠤࡧ࡫ࠠࡪࡰࡦࡳࡲࡶ࡬ࡦࡶࡨ࠲ࠧါ"))
    return bstack1llll1l11l1_opy_
bstack1llll11l1ll_opy_ = bstack11llll_opy_ (u"ࠥ࠽࠾࠿࠹ࠣာ")
bstack1llll111l1l_opy_ = bstack11llll_opy_ (u"ࠦࡷ࡫ࡡࡥࡻࠥိ")
bstack1lllll11l11_opy_ = bstack11llll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡒࡉࡠࡄࡌࡒࡤ࡙ࡅࡔࡕࡌࡓࡓࡥࡉࡅࠤီ")
bstack1lll1ll11ll_opy_ = bstack11llll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡌࡊࡡࡅࡍࡓࡥࡌࡊࡕࡗࡉࡓࡥࡁࡅࡆࡕࠦု")
bstack1l1l1l111_opy_ = bstack11llll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠥူ")
bstack1lllll1lll1_opy_ = re.compile(bstack11llll_opy_ (u"ࡳࠤࠫࡃ࡮࠯࠮ࠫࠪࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡽࡄࡖ࠭࠳࠰ࠢေ"))
bstack1lllll11l1l_opy_ = bstack11llll_opy_ (u"ࠤࡧࡩࡻ࡫࡬ࡰࡲࡰࡩࡳࡺࠢဲ")
bstack1lll1llll11_opy_ = [
    Events.bstack11lllll1ll_opy_,
    Events.CONNECT,
    Events.bstack1ll1ll1l1l_opy_,
]
class SDKCLI:
    _111111llll_opy_ = None
    process: Union[None, Any]
    bstack1lll1ll1111_opy_: bool
    bstack1llll1lll11_opy_: bool
    bstack1lll1ll1lll_opy_: bool
    bin_session_id: Union[None, str]
    cli_bin_session_id: Union[None, str]
    cli_listen_addr: Union[None, str]
    bstack1lllll11lll_opy_: Union[None, grpc.Channel]
    bstack1lllllll11l_opy_: str
    test_framework: TestFramework
    bstack111ll11ll1_opy_: bstack11111l1lll_opy_
    config: Union[None, Dict[str, Any]]
    web_driver: bstack111l111lll_opy_
    bstack1llll1ll111_opy_: bstack1111lll11l_opy_
    bstack1llllll1lll_opy_: bstack1llll1llll1_opy_
    accessibility: bstack1lllll111ll_opy_
    ai: bstack1llllllll11_opy_
    bstack1llll1l111l_opy_: List[bstack111l1lllll_opy_]
    config_testhub: Any
    config_observability: Any
    config_accessibility: Any
    bstack1llll11l11l_opy_: Dict[str, timedelta]
    bstack1llll1l1l1l_opy_: str
    bstack1111llllll_opy_: bstack1111lllll1_opy_
    def __new__(cls):
        if not cls._111111llll_opy_:
            cls._111111llll_opy_ = super(SDKCLI, cls).__new__(cls)
        return cls._111111llll_opy_
    def __init__(self):
        self.process = None
        self.bstack1lll1ll1111_opy_ = False
        self.bstack1lllll11lll_opy_ = None
        self.bstack111l11l1ll_opy_ = None
        self.cli_bin_session_id = None
        self.cli_listen_addr = os.environ.get(bstack1lll1ll11ll_opy_, None)
        self.bstack1lll1lll1l1_opy_ = os.environ.get(bstack1lllll11l11_opy_, bstack11llll_opy_ (u"ࠥࠦဳ")) == bstack11llll_opy_ (u"ࠦࠧဴ")
        self.bstack1llll1lll11_opy_ = False
        self.bstack1lll1ll1lll_opy_ = False
        self.config = None
        self.config_testhub = None
        self.config_observability = None
        self.config_accessibility = None
        self.test_framework = None
        self.bstack111ll11ll1_opy_ = None
        self.bstack1lllllll11l_opy_=bstack11llll_opy_ (u"ࠧࠨဵ")
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
        self.bstack1llll11l11l_opy_ = defaultdict(lambda: timedelta(microseconds=0))
        self.bstack1111llllll_opy_ = bstack1111lllll1_opy_()
        self.web_driver = bstack111l111lll_opy_()
        self.bstack1llll1ll111_opy_ = bstack1111lll11l_opy_()
        self.bstack1llllll1lll_opy_ = None
        self.accessibility = None
        self.ai = None
        self.bstack1llll1l111l_opy_ = [
            self.web_driver,
            self.bstack1llll1ll111_opy_,
        ]
    def bstack11ll11111_opy_(self):
        return os.environ.get(bstack1l1l1l111_opy_).lower().__eq__(bstack11llll_opy_ (u"ࠨࡴࡳࡷࡨࠦံ"))
    def is_enabled(self, config):
        if bstack11llll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨ့ࠫ") in config and str(config[bstack11llll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬး")]).lower() != bstack11llll_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨ္"):
            return False
        bstack1lllll1ll1l_opy_ = [bstack11llll_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ်ࠥ")]
        return config.get(bstack11llll_opy_ (u"ࠦ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠢျ")) in bstack1lllll1ll1l_opy_ or os.environ.get(bstack11llll_opy_ (u"ࠬࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࡠࡗࡖࡉࡉ࠭ြ")) in bstack1lllll1ll1l_opy_
    def bstack11l11ll111_opy_(self):
        for event in bstack1lll1llll11_opy_:
            bstack1lll1ll11l_opy_.register(
                event, lambda event_name, *args, **kwargs: bstack1lll1ll11l_opy_.logger.debug(bstack11llll_opy_ (u"ࠨࡻࡦࡸࡨࡲࡹࡥ࡮ࡢ࡯ࡨࢁࠥࡃ࠾ࠡࡽࡤࡶ࡬ࡹࡽࠡࠤွ") + str(kwargs) + bstack11llll_opy_ (u"ࠢࠣှ"))
            )
        bstack1lll1ll11l_opy_.register(Events.bstack11lllll1ll_opy_, self.__1llll1lllll_opy_)
        bstack1lll1ll11l_opy_.register(Events.CONNECT, self.__1llll1l1111_opy_)
        bstack1lll1ll11l_opy_.register(Events.bstack1ll1ll1l1l_opy_, self.__1lllll11111_opy_)
    def bstack11llllll1_opy_(self):
        return not self.bstack1lll1lll1l1_opy_ and os.environ.get(bstack1lllll11l11_opy_, bstack11llll_opy_ (u"ࠣࠤဿ")) != bstack11llll_opy_ (u"ࠤࠥ၀")
    def is_running(self):
        if self.bstack1lll1lll1l1_opy_:
            return self.bstack1lll1ll1111_opy_
        else:
            return bool(self.bstack1lllll11lll_opy_)
    def bstack1llll11l1l1_opy_(self, module):
        return any(isinstance(m, module) for m in self.bstack1llll1l111l_opy_) and cli.is_running()
    def __1lll1ll1l11_opy_(self, bstack1lll1lll111_opy_=10):
        if self.bstack111l11l1ll_opy_:
            return
        bstack111l1l1l1_opy_ = datetime.now()
        cli_listen_addr = os.environ.get(bstack1lll1ll11ll_opy_, self.cli_listen_addr)
        self.logger.warning(bstack11llll_opy_ (u"ࠥ࡟ࠧ၁") + str(id(self)) + bstack11llll_opy_ (u"ࠦࡢࠦࡣࡰࡰࡱࡩࡨࡺࡩ࡯ࡩࠥ၂"))
        channel = grpc.insecure_channel(cli_listen_addr, options=[(bstack11llll_opy_ (u"ࠧ࡭ࡲࡱࡥ࠱ࡩࡳࡧࡢ࡭ࡧࡢ࡬ࡹࡺࡰࡠࡲࡵࡳࡽࡿࠢ၃"), 0), (bstack11llll_opy_ (u"ࠨࡧࡳࡲࡦ࠲ࡪࡴࡡࡣ࡮ࡨࡣ࡭ࡺࡴࡱࡵࡢࡴࡷࡵࡸࡺࠤ၄"), 0)])
        grpc.channel_ready_future(channel).result(timeout=bstack1lll1lll111_opy_)
        self.bstack1lllll11lll_opy_ = channel
        self.bstack111l11l1ll_opy_ = sdk_pb2_grpc.SDKStub(self.bstack1lllll11lll_opy_)
        self.bstack1ll1l1l11l_opy_(bstack11llll_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡩ࡯࡯ࡰࡨࡧࡹࠨ၅"), datetime.now() - bstack111l1l1l1_opy_)
        self.cli_listen_addr = cli_listen_addr
        os.environ[bstack1lll1ll11ll_opy_] = self.cli_listen_addr
        self.logger.warning(bstack11llll_opy_ (u"ࠣ࡝ࡾ࡭ࡩ࠮ࡳࡦ࡮ࡩ࠭ࢂࡣࠠࡤࡱࡱࡲࡪࡩࡴࡦࡦ࠽ࠤ࡮ࡹ࡟ࡤࡪ࡬ࡰࡩࡥࡰࡳࡱࡦࡩࡸࡹ࠽ࠣ၆") + str(self.bstack11llllll1_opy_()) + bstack11llll_opy_ (u"ࠤࠥ၇"))
    def __1lllll11111_opy_(self, event_name):
        if self.bstack11llllll1_opy_():
            self.logger.debug(bstack11llll_opy_ (u"ࠥࡧ࡭࡯࡬ࡥ࠯ࡳࡶࡴࡩࡥࡴࡵ࠽ࠤࡸࡺ࡯ࡱࡲ࡬ࡲ࡬ࠦࡃࡍࡋࠥ၈"))
        self.__1llllll11ll_opy_()
    def __1llll1lllll_opy_(self, event_name: str, data):
        self.bstack1lllllll11l_opy_ = bstack1llllll11l1_opy_(data.bs_config)
        if self.bstack11llllll1_opy_():
            self.__1llll1l1111_opy_(event_name, bstack11lllll11_opy_())
            return
        start = datetime.now()
        is_started = self.__1lllll1ll11_opy_()
        self.bstack1ll1l1l11l_opy_(bstack11llll_opy_ (u"ࠦࡸࡶࡡࡸࡰࡢࡸ࡮ࡳࡥࠣ၉"), datetime.now() - start)
        if is_started:
            start = datetime.now()
            self.__1lll1ll1l11_opy_()
            self.bstack1ll1l1l11l_opy_(bstack11llll_opy_ (u"ࠧࡩ࡯࡯ࡰࡨࡧࡹࡥࡴࡪ࡯ࡨࠦ၊"), datetime.now() - start)
            start = datetime.now()
            self.__1llllll111l_opy_(data)
            self.bstack1ll1l1l11l_opy_(bstack11llll_opy_ (u"ࠨࡳࡵࡣࡵࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡴࡪ࡯ࡨࠦ။"), datetime.now() - start)
    def __1llll1l1111_opy_(self, event_name: str, data: bstack11lllll11_opy_):
        if not self.bstack11llllll1_opy_():
            self.logger.warning(bstack11llll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡧࡴࡴ࡮ࡦࡥࡷ࠾ࠥࡴ࡯ࡵࠢࡤࠤࡨ࡮ࡩ࡭ࡦ࠰ࡴࡷࡵࡣࡦࡵࡶࠦ၌"))
            return
        bin_session_id = os.environ.get(bstack1lllll11l11_opy_)
        start = datetime.now()
        self.__1lll1ll1l11_opy_()
        self.bstack1ll1l1l11l_opy_(bstack11llll_opy_ (u"ࠣࡥࡲࡲࡳ࡫ࡣࡵࡡࡷ࡭ࡲ࡫ࠢ၍"), datetime.now() - start)
        self.cli_bin_session_id = bin_session_id
        self.logger.info(bstack11llll_opy_ (u"ࠤ࡞ࡿ࡮ࡪࠨࡴࡧ࡯ࡪ࠮ࢃ࡝ࠡࡥ࡫࡭ࡱࡪ࠭ࡱࡴࡲࡧࡪࡹࡳ࠻ࠢࡦࡳࡳࡴࡥࡤࡶࡨࡨࠥࡺ࡯ࠡࡧࡻ࡭ࡸࡺࡩ࡯ࡩࠣࡇࡑࡏࠠࠣ၎") + str(bin_session_id) + bstack11llll_opy_ (u"ࠥࠦ၏"))
        start = datetime.now()
        self.__1llll1l1l11_opy_()
        self.bstack1ll1l1l11l_opy_(bstack11llll_opy_ (u"ࠦࡸࡺࡡࡳࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡹ࡯࡭ࡦࠤၐ"), datetime.now() - start)
    def __1lll1ll11l1_opy_(self):
        if not self.bstack111l11l1ll_opy_ or not self.cli_bin_session_id:
            self.logger.warning(bstack11llll_opy_ (u"ࠧࡩࡡ࡯ࡰࡲࡸࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡥࠡ࡯ࡲࡨࡺࡲࡥࡴࠤၑ"))
            return
        if not self.bstack1llllll1lll_opy_ and self.config_observability and self.config_observability.success: # bstack111l1l1111_opy_
            self.bstack1llllll1lll_opy_ = bstack1llll1llll1_opy_() # bstack1llll1ll1ll_opy_
            self.bstack1llll1l111l_opy_.append(self.bstack1llllll1lll_opy_)
        if not self.accessibility and self.config_accessibility and self.config_accessibility.success:
            self.accessibility = bstack1lllll111ll_opy_()
            self.bstack1llll1l111l_opy_.append(self.accessibility)
        if not self.ai and isinstance(self.config, dict) and self.config.get(bstack11llll_opy_ (u"ࠨࡳࡦ࡮ࡩࡌࡪࡧ࡬ࠣၒ"), False) == True:
            self.ai = bstack1llllllll11_opy_()
            self.bstack1llll1l111l_opy_.append(self.ai)
        for mod in self.bstack1llll1l111l_opy_:
            if not mod.bstack111l111111_opy_():
                mod.configure(self.bstack111l11l1ll_opy_, self.cli_bin_session_id, self.bstack1111llllll_opy_)
    def __1llll11ll1l_opy_(self):
        for mod in self.bstack1llll1l111l_opy_:
            if mod.bstack111l111111_opy_():
                mod.configure(self.bstack111l11l1ll_opy_, None, None)
    def __1llllll111l_opy_(self, data):
        if not self.cli_bin_session_id or self.bstack1llll1lll11_opy_:
            return
        self.__1llll11l111_opy_(data)
        bstack111l1l1l1_opy_ = datetime.now()
        req = structs.StartBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.path_project = os.getcwd()
        req.language = bstack11llll_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࠢၓ")
        req.sdk_language = bstack11llll_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࠣၔ")
        req.path_config = data.path_config
        req.sdk_version = data.sdk_version
        req.test_framework = data.test_framework
        req.frameworks.extend(data.frameworks)
        req.framework_versions.update(data.framework_versions)
        req.env_vars.update({key: value for key, value in os.environ.items() if bool(bstack1lllll1lll1_opy_.search(key))})
        req.cli_args.extend(sys.argv)
        try:
            self.logger.info(bstack11llll_opy_ (u"ࠤ࡞ࠦၕ") + str(id(self)) + bstack11llll_opy_ (u"ࠥࡡࠥࡳࡡࡪࡰ࠰ࡴࡷࡵࡣࡦࡵࡶ࠾ࠥࡹࡴࡢࡴࡷࡣࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࠤၖ"))
            r = self.bstack111l11l1ll_opy_.StartBinSession(req)
            self.bstack1ll1l1l11l_opy_(bstack11llll_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡸࡦࡸࡴࡠࡤ࡬ࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࠨၗ"), datetime.now() - bstack111l1l1l1_opy_)
            os.environ[bstack1lllll11l11_opy_] = r.bin_session_id
            self.__1llll1lll1l_opy_(r)
            self.__1lll1ll11l1_opy_()
            self.bstack1111llllll_opy_.start()
            self.bstack1llll1lll11_opy_ = True
            self.logger.info(bstack11llll_opy_ (u"ࠧࡡࠢၘ") + str(id(self)) + bstack11llll_opy_ (u"ࠨ࡝ࠡ࡯ࡤ࡭ࡳ࠳ࡰࡳࡱࡦࡩࡸࡹ࠺ࠡࡥࡲࡲࡳ࡫ࡣࡵࡧࡧࠦၙ"))
        except grpc.bstack1lll1ll1l1l_opy_ as bstack1llll1l1ll1_opy_:
            self.logger.error(bstack11llll_opy_ (u"ࠢ࡜ࡽ࡬ࡨ࠭ࡹࡥ࡭ࡨࠬࢁࡢࠦࡴࡪ࡯ࡨࡳࡪࡻࡴ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤၚ") + str(bstack1llll1l1ll1_opy_) + bstack11llll_opy_ (u"ࠣࠤၛ"))
            traceback.print_exc()
            raise bstack1llll1l1ll1_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack11llll_opy_ (u"ࠤ࡞ࡿ࡮ࡪࠨࡴࡧ࡯ࡪ࠮ࢃ࡝ࠡࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨၜ") + str(e) + bstack11llll_opy_ (u"ࠥࠦၝ"))
            traceback.print_exc()
            raise e
    def __1llll1l1l11_opy_(self):
        if not self.bstack11llllll1_opy_() or not self.cli_bin_session_id or self.bstack1lll1ll1lll_opy_:
            return
        bstack111l1l1l1_opy_ = datetime.now()
        req = structs.ConnectBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.platform_index = int(os.environ.get(bstack11llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫၞ"), bstack11llll_opy_ (u"ࠬ࠶ࠧၟ")))
        try:
            self.logger.info(bstack11llll_opy_ (u"ࠨ࡛ࠣၠ") + str(id(self)) + bstack11llll_opy_ (u"ࠢ࡞ࠢࡦ࡬࡮ࡲࡤ࠮ࡲࡵࡳࡨ࡫ࡳࡴ࠼ࠣࡧࡴࡴ࡮ࡦࡥࡷࡣࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࠤၡ"))
            r = self.bstack111l11l1ll_opy_.ConnectBinSession(req)
            self.bstack1ll1l1l11l_opy_(bstack11llll_opy_ (u"ࠣࡩࡵࡴࡨࡀࡣࡰࡰࡱࡩࡨࡺ࡟ࡣ࡫ࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠧၢ"), datetime.now() - bstack111l1l1l1_opy_)
            self.__1llll1lll1l_opy_(r)
            self.__1lll1ll11l1_opy_()
            self.bstack1111llllll_opy_.start()
            self.bstack1lll1ll1lll_opy_ = True
            self.logger.info(bstack11llll_opy_ (u"ࠤ࡞ࠦၣ") + str(id(self)) + bstack11llll_opy_ (u"ࠥࡡࠥࡩࡨࡪ࡮ࡧ࠱ࡵࡸ࡯ࡤࡧࡶࡷ࠿ࠦࡣࡰࡰࡱࡩࡨࡺࡥࡥࠤၤ"))
        except grpc.bstack1lll1ll1l1l_opy_ as bstack1llll1l1ll1_opy_:
            self.logger.error(bstack11llll_opy_ (u"ࠦࡠࢁࡩࡥࠪࡶࡩࡱ࡬ࠩࡾ࡟ࠣࡸ࡮ࡳࡥࡰࡧࡸࡸ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨၥ") + str(bstack1llll1l1ll1_opy_) + bstack11llll_opy_ (u"ࠧࠨၦ"))
            traceback.print_exc()
            raise bstack1llll1l1ll1_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack11llll_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥၧ") + str(e) + bstack11llll_opy_ (u"ࠢࠣၨ"))
            traceback.print_exc()
            raise e
    def __1llll1lll1l_opy_(self, r):
        if not r.bin_session_id or not r.config or not isinstance(r.config, str):
            raise ValueError(bstack11llll_opy_ (u"ࠣࡷࡱࡩࡽࡶࡥࡤࡶࡨࡨࠥࡹࡥࡳࡸࡨࡶࠥࡸࡥࡴࡲࡲࡲࡸ࡫ࠢၩ") + str(r))
        self.config = json.loads(r.config)
        self.config_testhub = r.testhub
        self.config_observability = r.observability
        self.config_accessibility = r.accessibility
        self.cli_bin_session_id = r.bin_session_id
    def __1lllll1ll11_opy_(self, bstack1lll1lll111_opy_=10):
        if self.bstack1lll1ll1111_opy_:
            self.logger.warning(bstack11llll_opy_ (u"ࠤࡶࡸࡦࡸࡴ࠻ࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡶࡺࡴ࡮ࡪࡰࡪࠦၪ"))
            return True
        self.logger.warning(bstack11llll_opy_ (u"ࠥࡷࡹࡧࡲࡵࠤၫ"))
        if os.getenv(bstack11llll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡑࡏ࡟ࡆࡐ࡙ࠦၬ")) == bstack1lllll11l1l_opy_:
            self.cli_bin_session_id = bstack1lllll11l1l_opy_
            self.cli_listen_addr = bstack11llll_opy_ (u"ࠧࡻ࡮ࡪࡺ࠽࠳ࡹࡳࡰ࠰ࡵࡧ࡯࠲ࡶ࡬ࡢࡶࡩࡳࡷࡳ࠭ࠦࡵ࠱ࡷࡴࡩ࡫ࠣၭ") % (self.cli_bin_session_id)
            self.bstack1lll1ll1111_opy_ = True
            return True
        self.process = subprocess.Popen(
            [self.bstack1lllllll11l_opy_, bstack11llll_opy_ (u"ࠨࡳࡥ࡭ࠥၮ")],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=dict(os.environ),
            text=True,
            universal_newlines=True, # bstack1llll11lll1_opy_ compat for text=True in bstack1lll1lllll1_opy_ python
            encoding=bstack11llll_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨၯ"),
            bufsize=1,
            close_fds=True,
        )
        bstack1lllll1l111_opy_ = threading.Thread(target=self.__1lll1llll1l_opy_, args=(bstack1lll1lll111_opy_,))
        bstack1lllll1l111_opy_.start()
        bstack1lllll1l111_opy_.join()
        if self.process.returncode is not None:
            self.logger.warning(bstack11llll_opy_ (u"ࠣ࡝ࡾ࡭ࡩ࠮ࡳࡦ࡮ࡩ࠭ࢂࡣࠠࡴࡲࡤࡻࡳࡀࠠࡳࡧࡷࡹࡷࡴࡣࡰࡦࡨࡁࢀࡹࡥ࡭ࡨ࠱ࡴࡷࡵࡣࡦࡵࡶ࠲ࡷ࡫ࡴࡶࡴࡱࡧࡴࡪࡥࡾࠢࡲࡹࡹࡃࡻࡴࡧ࡯ࡪ࠳ࡶࡲࡰࡥࡨࡷࡸ࠴ࡳࡵࡦࡲࡹࡹ࠴ࡲࡦࡣࡧࠬ࠮ࢃࠠࡦࡴࡵࡁࠧၰ") + str(self.process.stderr.read()) + bstack11llll_opy_ (u"ࠤࠥၱ"))
        if not self.bstack1lll1ll1111_opy_:
            self.logger.warning(bstack11llll_opy_ (u"ࠥ࡟ࠧၲ") + str(id(self)) + bstack11llll_opy_ (u"ࠦࡢࠦࡣ࡭ࡧࡤࡲࡺࡶࠢၳ"))
            self.__1llllll11ll_opy_()
        self.logger.info(bstack11llll_opy_ (u"ࠧࡡࡻࡪࡦࠫࡷࡪࡲࡦࠪࡿࡠࠤࡵࡸ࡯ࡤࡧࡶࡷࡤࡸࡥࡢࡦࡼ࠾ࠥࠨၴ") + str(self.bstack1lll1ll1111_opy_) + bstack11llll_opy_ (u"ࠨࠢၵ"))
        return self.bstack1lll1ll1111_opy_
    def __1lll1llll1l_opy_(self, bstack1llll1ll11l_opy_=10):
        bstack1lll1lll11l_opy_ = time.time()
        while self.process and time.time() - bstack1lll1lll11l_opy_ < bstack1llll1ll11l_opy_:
            try:
                line = self.process.stdout.readline()
                if bstack11llll_opy_ (u"ࠢࡪࡦࡀࠦၶ") in line:
                    self.cli_bin_session_id = line.split(bstack11llll_opy_ (u"ࠣ࡫ࡧࡁࠧၷ"))[-1:][0].strip()
                    self.logger.info(bstack11llll_opy_ (u"ࠤࡦࡰ࡮ࡥࡢࡪࡰࡢࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪ࠺ࠣၸ") + str(self.cli_bin_session_id) + bstack11llll_opy_ (u"ࠥࠦၹ"))
                    continue
                if bstack11llll_opy_ (u"ࠦࡱ࡯ࡳࡵࡧࡱࡁࠧၺ") in line:
                    self.cli_listen_addr = line.split(bstack11llll_opy_ (u"ࠧࡲࡩࡴࡶࡨࡲࡂࠨၻ"))[-1:][0].strip()
                    self.logger.info(bstack11llll_opy_ (u"ࠨࡣ࡭࡫ࡢࡰ࡮ࡹࡴࡦࡰࡢࡥࡩࡪࡲ࠻ࠤၼ") + str(self.cli_listen_addr) + bstack11llll_opy_ (u"ࠢࠣၽ"))
                    continue
                if bstack11llll_opy_ (u"ࠣࡲࡲࡶࡹࡃࠢၾ") in line:
                    port = line.split(bstack11llll_opy_ (u"ࠤࡳࡳࡷࡺ࠽ࠣၿ"))[-1:][0].strip()
                    self.logger.info(bstack11llll_opy_ (u"ࠥࡴࡴࡸࡴ࠻ࠤႀ") + str(port) + bstack11llll_opy_ (u"ࠦࠧႁ"))
                    continue
                if line.strip() == bstack1llll111l1l_opy_ and self.cli_bin_session_id and self.cli_listen_addr:
                    if os.getenv(bstack11llll_opy_ (u"࡙ࠧࡄࡌࡡࡆࡐࡎࡥࡆࡍࡃࡊࡣࡎࡕ࡟ࡔࡖࡕࡉࡆࡓࠢႂ"), bstack11llll_opy_ (u"ࠨ࠱ࠣႃ")) == bstack11llll_opy_ (u"ࠢ࠲ࠤႄ"):
                        if not self.process.stdout.closed:
                            self.process.stdout.close()
                        if not self.process.stderr.closed:
                            self.process.stderr.close()
                    self.bstack1lll1ll1111_opy_ = True
                    return True
            except Exception as e:
                self.logger.warning(bstack11llll_opy_ (u"ࠣࡧࡵࡶࡴࡸ࠺ࠡࠤႅ") + str(e) + bstack11llll_opy_ (u"ࠤࠥႆ"))
        return False
    def __1llllll11ll_opy_(self):
        if self.bstack1lllll11lll_opy_:
            self.bstack1111llllll_opy_.stop()
            start = datetime.now()
            if self.bstack1lllll1111l_opy_():
                self.cli_bin_session_id = None
                if self.bstack1lll1ll1lll_opy_:
                    self.bstack1ll1l1l11l_opy_(bstack11llll_opy_ (u"ࠥࡷࡹࡵࡰࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡷ࡭ࡲ࡫ࠢႇ"), datetime.now() - start)
                else:
                    self.bstack1ll1l1l11l_opy_(bstack11llll_opy_ (u"ࠦࡸࡺ࡯ࡱࡡࡶࡩࡸࡹࡩࡰࡰࡢࡸ࡮ࡳࡥࠣႈ"), datetime.now() - start)
            self.__1llll11ll1l_opy_()
            start = datetime.now()
            self.bstack1lllll11lll_opy_.close()
            self.bstack1ll1l1l11l_opy_(bstack11llll_opy_ (u"ࠧࡪࡩࡴࡥࡲࡲࡳ࡫ࡣࡵࡡࡷ࡭ࡲ࡫ࠢႉ"), datetime.now() - start)
            self.bstack1lllll11lll_opy_ = None
        if self.process:
            self.logger.debug(bstack11llll_opy_ (u"ࠨࡳࡵࡱࡳࠦႊ"))
            start = datetime.now()
            self.process.terminate()
            self.bstack1ll1l1l11l_opy_(bstack11llll_opy_ (u"ࠢ࡬࡫࡯ࡰࡤࡺࡩ࡮ࡧࠥႋ"), datetime.now() - start)
            self.process = None
            if self.bstack1lll1lll1l1_opy_ and self.config_observability and self.config_testhub and self.config_testhub.testhub_events:
                self.bstack1l111l11ll_opy_()
                self.logger.info(
                    bstack11llll_opy_ (u"ࠣࡘ࡬ࡷ࡮ࡺࠠࡩࡶࡷࡴࡸࡀ࠯࠰ࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࢀࢃࠠࡵࡱࠣࡺ࡮࡫ࡷࠡࡤࡸ࡭ࡱࡪࠠࡳࡧࡳࡳࡷࡺࠬࠡ࡫ࡱࡷ࡮࡭ࡨࡵࡵ࠯ࠤࡦࡴࡤࠡ࡯ࡤࡲࡾࠦ࡭ࡰࡴࡨࠤࡩ࡫ࡢࡶࡩࡪ࡭ࡳ࡭ࠠࡪࡰࡩࡳࡷࡳࡡࡵ࡫ࡲࡲࠥࡧ࡬࡭ࠢࡤࡸࠥࡵ࡮ࡦࠢࡳࡰࡦࡩࡥࠢ࡞ࡱࠦႌ").format(
                        self.config_testhub.bstack11llll1111_opy_
                    )
                )
        self.bstack1lll1ll1111_opy_ = False
    def __1llll11l111_opy_(self, data):
        try:
            import selenium
            data.framework_versions[bstack11llll_opy_ (u"ࠤࡶࡩࡱ࡫࡮ࡪࡷࡰႍࠦ")] = selenium.__version__
            data.frameworks.append(bstack11llll_opy_ (u"ࠥࡷࡪࡲࡥ࡯࡫ࡸࡱࠧႎ"))
        except:
            pass
    def bstack1lll1ll111l_opy_(self, hub_url: str, platform_index: int, bstack1llll1ll1_opy_: Any):
        if self.bstack111ll11ll1_opy_:
            self.logger.warning(bstack11llll_opy_ (u"ࠦࡸࡱࡩࡱࡲࡨࡨࠥࡹࡥࡵࡷࡳࠤࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡀࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡵࡨࡸࠥࡻࡰࠣႏ"))
            return
        try:
            bstack111l1l1l1_opy_ = datetime.now()
            import selenium
            from selenium.webdriver.remote.webdriver import WebDriver
            from selenium.webdriver.common.service import Service
            framework = bstack11llll_opy_ (u"ࠧࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠢ႐")
            self.bstack111ll11ll1_opy_ = bstack111ll1l11l_opy_(
                hub_url,
                platform_index,
                framework_name=framework,
                framework_version=selenium.__version__,
                classes=[WebDriver],
                bstack111l1111ll_opy_={bstack11llll_opy_ (u"ࠨࡣࡳࡧࡤࡸࡪࡥ࡯ࡱࡶ࡬ࡳࡳࡹ࡟ࡧࡴࡲࡱࡤࡩࡡࡱࡵࠥ႑"): bstack1llll1ll1_opy_}
            )
            def bstack1llll111111_opy_(self):
                return
            if self.config.get(bstack11llll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠤ႒"), True):
                Service.start = bstack1llll111111_opy_
                Service.stop = bstack1llll111111_opy_
            def get_accessibility_results(driver):
                if self.accessibility and self.accessibility.is_enabled():
                    return self.accessibility.get_accessibility_results(driver, framework_name=framework)
            def get_accessibility_results_summary(driver):
                if self.accessibility and self.accessibility.is_enabled():
                    return self.accessibility.get_accessibility_results_summary(driver, framework_name=framework)
            def perform_scan(driver):
                if self.accessibility and self.accessibility.is_enabled():
                    return self.accessibility.perform_scan(driver, method=None, framework_name=framework)
            WebDriver.getAccessibilityResults = get_accessibility_results
            WebDriver.get_accessibility_results = get_accessibility_results
            WebDriver.getAccessibilityResultsSummary = get_accessibility_results_summary
            WebDriver.get_accessibility_results_summary = get_accessibility_results_summary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
            self.bstack1ll1l1l11l_opy_(bstack11llll_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠤ႓"), datetime.now() - bstack111l1l1l1_opy_)
        except Exception as e:
            self.logger.error(bstack11llll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࡷࡳࠤࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡀࠠࠣ႔") + str(e) + bstack11llll_opy_ (u"ࠥࠦ႕"))
    def bstack1lll1ll1ll1_opy_(self):
        if self.test_framework:
            self.logger.warning(bstack11llll_opy_ (u"ࠦࡸࡱࡩࡱࡲࡨࡨࠥࡹࡥࡵࡷࡳࠤࡵࡿࡴࡦࡵࡷ࠾ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡳࡦࡶࠣࡹࡵࠨ႖"))
            return
        try:
            import pytest
            self.test_framework = bstack1llll1111l1_opy_({ bstack11llll_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࠧ႗"): pytest.__version__ }, [bstack11llll_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࠨ႘")])
        except Exception as e:
            self.logger.error(bstack11llll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࡵࡱࠢࡳࡽࡹ࡫ࡳࡵ࠼ࠣࠦ႙") + str(e) + bstack11llll_opy_ (u"ࠣࠤႚ"))
        self.bstack1llll1l1lll_opy_()
    def bstack1llll1l1lll_opy_(self):
        if not self.bstack11ll11111_opy_():
            return
        bstack11lll1111_opy_ = None
        def bstack11111l111_opy_(config, startdir):
            return bstack11llll_opy_ (u"ࠤࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡿ࠵ࢃࠢႛ").format(bstack11llll_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠤႜ"))
        def bstack111l111ll_opy_():
            return
        def bstack1l11ll11l_opy_(self, name: str, default=Notset(), skip: bool = False):
            if str(name).lower() == bstack11llll_opy_ (u"ࠫࡩࡸࡩࡷࡧࡵࠫႝ"):
                return bstack11llll_opy_ (u"ࠧࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠦ႞")
            else:
                return bstack11lll1111_opy_(self, name, default, skip)
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            bstack11lll1111_opy_ = Config.getoption
            pytest_selenium.pytest_report_header = bstack11111l111_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack111l111ll_opy_
            Config.getoption = bstack1l11ll11l_opy_
        except Exception as e:
            self.logger.error(bstack11llll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡥࡹࡩࡨࠡࡲࡼࡸࡪࡹࡴࠡࡵࡨࡰࡪࡴࡩࡶ࡯ࠣࡪࡴࡸࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡀࠠࠣ႟") + str(e) + bstack11llll_opy_ (u"ࠢࠣႠ"))
    def bstack1llll11llll_opy_(self):
        bstack1lll1llllll_opy_ = MessageToDict(cli.config_testhub, preserving_proto_field_name=True)
        if isinstance(bstack1lll1llllll_opy_, dict):
            if cli.config_observability:
                bstack1lll1llllll_opy_.update(
                    {bstack11llll_opy_ (u"ࠣࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠣႡ"): MessageToDict(cli.config_observability, preserving_proto_field_name=True)}
                )
            if cli.config_accessibility:
                accessibility = MessageToDict(cli.config_accessibility, preserving_proto_field_name=True)
                if isinstance(accessibility, dict) and bstack11llll_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡶࡣࡹࡵ࡟ࡸࡴࡤࡴࠧႢ") in accessibility.get(bstack11llll_opy_ (u"ࠥࡳࡵࡺࡩࡰࡰࡶࠦႣ"), {}):
                    bstack1llll11111l_opy_ = accessibility.get(bstack11llll_opy_ (u"ࠦࡴࡶࡴࡪࡱࡱࡷࠧႤ"))
                    bstack1llll11111l_opy_.update({ bstack11llll_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡹࡔࡰ࡙ࡵࡥࡵࠨႥ"): bstack1llll11111l_opy_.pop(bstack11llll_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࡳࡠࡶࡲࡣࡼࡸࡡࡱࠤႦ")) })
                bstack1lll1llllll_opy_.update({bstack11llll_opy_ (u"ࠢࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠢႧ"): accessibility })
        return bstack1lll1llllll_opy_
    def bstack1lllll1111l_opy_(self, bstack1llll1l11ll_opy_: str = None, bstack1llll11ll11_opy_: str = None, bstack11ll11l11l_opy_: int = None):
        if not self.cli_bin_session_id or not self.bstack111l11l1ll_opy_:
            return
        bstack111l1l1l1_opy_ = datetime.now()
        req = structs.StopBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        if bstack11ll11l11l_opy_:
            req.bstack11ll11l11l_opy_ = bstack11ll11l11l_opy_
        if bstack1llll1l11ll_opy_:
            req.bstack1llll1l11ll_opy_ = bstack1llll1l11ll_opy_
        if bstack1llll11ll11_opy_:
            req.bstack1llll11ll11_opy_ = bstack1llll11ll11_opy_
        try:
            r = self.bstack111l11l1ll_opy_.StopBinSession(req)
            self.bstack1ll1l1l11l_opy_(bstack11llll_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡵࡱࡳࡣࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࠤႨ"), datetime.now() - bstack111l1l1l1_opy_)
            return r.success
        except grpc.RpcError as e:
            traceback.print_exc()
            raise e
    def bstack1ll1l1l11l_opy_(self, key: str, value: timedelta):
        tag = bstack11llll_opy_ (u"ࠤࡦ࡬࡮ࡲࡤ࠮ࡲࡵࡳࡨ࡫ࡳࡴࠤႩ") if self.bstack11llllll1_opy_() else bstack11llll_opy_ (u"ࠥࡱࡦ࡯࡮࠮ࡲࡵࡳࡨ࡫ࡳࡴࠤႪ")
        self.bstack1llll11l11l_opy_[bstack11llll_opy_ (u"ࠦ࠿ࠨႫ").join([tag + bstack11llll_opy_ (u"ࠧ࠳ࠢႬ") + str(id(self)), key])] += value
    def bstack1l111l11ll_opy_(self):
        if not os.getenv(bstack11llll_opy_ (u"ࠨࡄࡆࡄࡘࡋࡤࡖࡅࡓࡈࠥႭ"), bstack11llll_opy_ (u"ࠢ࠱ࠤႮ")) == bstack11llll_opy_ (u"ࠣ࠳ࠥႯ"):
            return
        bstack1llll1111ll_opy_ = dict()
        bstack1llllll1111_opy_ = []
        if self.test_framework:
            bstack1llllll1111_opy_.extend(list(self.test_framework.bstack1llllll1111_opy_.values()))
        if self.bstack111ll11ll1_opy_:
            bstack1llllll1111_opy_.extend(list(self.bstack111ll11ll1_opy_.bstack1llllll1111_opy_.values()))
        for instance in bstack1llllll1111_opy_:
            if not instance.platform_index in bstack1llll1111ll_opy_:
                bstack1llll1111ll_opy_[instance.platform_index] = defaultdict(lambda: timedelta(microseconds=0))
            report = bstack1llll1111ll_opy_[instance.platform_index]
            for k, v in instance.bstack11111l1l1l_opy_().items():
                report[k] += v
                report[k.split(bstack11llll_opy_ (u"ࠤ࠽ࠦႰ"))[0]] += v
        bstack1lllll1l11l_opy_ = sorted([(k, v) for k, v in self.bstack1llll11l11l_opy_.items()], key=lambda o: o[1], reverse=True)
        bstack1llll111l11_opy_ = 0
        for r in bstack1lllll1l11l_opy_:
            bstack1lllll1l1l1_opy_ = r[1].total_seconds()
            bstack1llll111l11_opy_ += bstack1lllll1l1l1_opy_
            self.logger.info(bstack11llll_opy_ (u"ࠥ࡟ࡵ࡫ࡲࡧ࡟ࠣࡧࡱ࡯࠺ࡼࡴ࡞࠴ࡢࢃ࠽ࠣႱ") + str(bstack1lllll1l1l1_opy_) + bstack11llll_opy_ (u"ࠦࠧႲ"))
        self.logger.info(bstack11llll_opy_ (u"ࠧ࠳࠭ࠣႳ"))
        bstack1lllll1llll_opy_ = []
        for platform_index, report in bstack1llll1111ll_opy_.items():
            bstack1lllll1llll_opy_.extend([(platform_index, k, v) for k, v in report.items()])
        bstack1lllll1llll_opy_.sort(key=lambda o: o[2], reverse=True)
        bstack1llllllll_opy_ = set()
        bstack1lll1lll1ll_opy_ = 0
        for r in bstack1lllll1llll_opy_:
            bstack1lllll1l1l1_opy_ = r[2].total_seconds()
            bstack1lll1lll1ll_opy_ += bstack1lllll1l1l1_opy_
            bstack1llllllll_opy_.add(r[0])
            self.logger.info(bstack11llll_opy_ (u"ࠨ࡛ࡱࡧࡵࡪࡢࠦࡴࡦࡵࡷ࠾ࡵࡲࡡࡵࡨࡲࡶࡲ࠳ࡻࡳ࡝࠳ࡡࢂࡀࡻࡳ࡝࠴ࡡࢂࡃࠢႴ") + str(bstack1lllll1l1l1_opy_) + bstack11llll_opy_ (u"ࠢࠣႵ"))
        if self.bstack11llllll1_opy_():
            self.logger.info(bstack11llll_opy_ (u"ࠣ࠯࠰ࠦႶ"))
            self.logger.info(bstack11llll_opy_ (u"ࠤ࡞ࡴࡪࡸࡦ࡞ࠢࡦࡰ࡮ࡀࡣࡩ࡫࡯ࡨ࠲ࡶࡲࡰࡥࡨࡷࡸࡃࡻࡵࡱࡷࡥࡱࡥࡣ࡭࡫ࢀࠤࡹ࡫ࡳࡵ࠼ࡳࡰࡦࡺࡦࡰࡴࡰࡷ࠲ࢁࡳࡵࡴࠫࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠯ࡽ࠾ࠤႷ") + str(bstack1lll1lll1ll_opy_) + bstack11llll_opy_ (u"ࠥࠦႸ"))
        else:
            self.logger.info(bstack11llll_opy_ (u"ࠦࡠࡶࡥࡳࡨࡠࠤࡨࡲࡩ࠻࡯ࡤ࡭ࡳ࠳ࡰࡳࡱࡦࡩࡸࡹ࠽ࠣႹ") + str(bstack1llll111l11_opy_) + bstack11llll_opy_ (u"ࠧࠨႺ"))
        self.logger.info(bstack11llll_opy_ (u"ࠨ࠭࠮ࠤႻ"))
cli = SDKCLI()