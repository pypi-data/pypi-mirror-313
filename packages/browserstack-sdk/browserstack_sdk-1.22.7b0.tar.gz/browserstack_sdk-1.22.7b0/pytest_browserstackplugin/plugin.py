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
import atexit
import datetime
import inspect
import logging
import os
import signal
import threading
from uuid import uuid4
from bstack_utils.percy_sdk import PercySDK
import tempfile
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack11lll1ll1_opy_, bstack11111llll_opy_, update, bstack1llll1ll1_opy_,
                                       bstack11111l111_opy_, bstack111l111ll_opy_, bstack1ll1lllll1_opy_, bstack11llllllll_opy_,
                                       bstack11l1ll11l1_opy_, bstack1ll1l1l1ll_opy_, bstack1ll1l1llll_opy_, bstack1lll11l11l_opy_,
                                       bstack11l1111ll_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack1l11l11111_opy_)
from browserstack_sdk.bstack1111l1ll_opy_ import bstack11l11l11_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack1ll1l1l1l1_opy_
from bstack_utils.capture import bstack1ll11l1l_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack1ll111lll_opy_, bstack1ll11llll1_opy_, bstack1ll11l1lll_opy_, \
    bstack11l1111l1_opy_
from bstack_utils.helper import bstack1ll111l1_opy_, bstack1l11l1ll111_opy_, bstack1l111l1l_opy_, bstack1l1ll11ll_opy_, bstack1l111lll11l_opy_, bstack1l111ll1_opy_, \
    bstack1l111llll1l_opy_, \
    bstack1l11lll1l1l_opy_, bstack111l1111l_opy_, bstack1lll1l1l1l_opy_, bstack1l11ll1l1ll_opy_, bstack1l1lll1l1l_opy_, Notset, \
    bstack1ll11l1111_opy_, bstack1l11l1l11l1_opy_, bstack1l111l11lll_opy_, Result, bstack1l11lllll11_opy_, bstack1l11l1l11ll_opy_, bstack1l11llll_opy_, \
    bstack1l1l1l11l1_opy_, bstack1ll1l111l1_opy_, bstack1lll1lll11_opy_, bstack1l11l111l11_opy_
from bstack_utils.bstack1l1ll1lll11_opy_ import bstack1l1ll1ll11l_opy_
from bstack_utils.messages import bstack1l1llll1ll_opy_, bstack1lllll111_opy_, bstack11ll1l1l1l_opy_, bstack1l111l1l1_opy_, bstack1111l11l_opy_, \
    bstack1lll1l111_opy_, bstack1ll1l1ll1_opy_, bstack1l11lll11_opy_, bstack1lll111ll_opy_, bstack111l1ll1l_opy_, \
    bstack11ll111ll_opy_, bstack11llll111l_opy_
from bstack_utils.proxy import bstack11l1lll1l_opy_, bstack11l1ll1l11_opy_
from bstack_utils.bstack1lll11ll1_opy_ import bstack1l1l1ll1l11_opy_, bstack1l1l1l1l11l_opy_, bstack1l1l1ll111l_opy_, bstack1l1l1l1l1ll_opy_, \
    bstack1l1l1l1llll_opy_, bstack1l1l1l1lll1_opy_, bstack1l1l1ll11l1_opy_, bstack1ll11llll_opy_, bstack1l1l1ll1111_opy_
from bstack_utils.bstack1l11lllll1_opy_ import bstack1l1llll11l_opy_
from bstack_utils.bstack1l1ll1ll11_opy_ import bstack1l111lll11_opy_, bstack11llll11l_opy_, bstack111ll1lll_opy_, \
    bstack11l11l11ll_opy_, bstack11ll111lll_opy_
from bstack_utils.bstack1l1l1lll_opy_ import bstack1lll11l1_opy_
from bstack_utils.bstack11llll1l_opy_ import bstack1lll1l11_opy_
import bstack_utils.accessibility as bstack11111l11_opy_
from bstack_utils.bstack1llll1ll_opy_ import bstack1lll11ll_opy_
from bstack_utils.bstack11ll11l1l1_opy_ import bstack11ll11l1l1_opy_
from browserstack_sdk.__init__ import bstack1l1ll1l11_opy_
from browserstack_sdk.sdk_cli.bstack1llll111ll1_opy_ import bstack1llll1llll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1ll11l_opy_ import bstack1lll1ll11l_opy_, Events, bstack11lllll11_opy_
from browserstack_sdk.sdk_cli.test_framework import bstack1ll1l1ll1ll_opy_, bstack1111l1lll1_opy_, bstack1111l11111_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack1lll1ll11l_opy_ import bstack1lll1ll11l_opy_, Events, bstack11lllll11_opy_, bstack1111ll1lll_opy_
bstack11l1l1lll1_opy_ = None
bstack1lll11ll11_opy_ = None
bstack111l11lll_opy_ = None
bstack1ll1llll11_opy_ = None
bstack1l1111lll_opy_ = None
bstack11ll1l1l11_opy_ = None
bstack11l1ll111_opy_ = None
bstack1ll1111l1l_opy_ = None
bstack1l11llll1l_opy_ = None
bstack11ll1llll_opy_ = None
bstack11lll1111_opy_ = None
bstack1l1l1l1l1l_opy_ = None
bstack11lll1l11_opy_ = None
bstack1l1l11llll_opy_ = bstack11llll_opy_ (u"ࠨࠩᬨ")
CONFIG = {}
bstack11l111lll_opy_ = False
bstack111l11l11_opy_ = bstack11llll_opy_ (u"ࠩࠪᬩ")
bstack11ll1111l1_opy_ = bstack11llll_opy_ (u"ࠪࠫᬪ")
bstack1l111l1l11_opy_ = False
bstack1ll1111111_opy_ = []
bstack1ll1l1ll1l_opy_ = bstack1ll111lll_opy_
bstack11l1lll11ll_opy_ = bstack11llll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫᬫ")
bstack1l1lll1ll1_opy_ = {}
bstack1l1lll1ll_opy_ = False
logger = bstack1ll1l1l1l1_opy_.get_logger(__name__, bstack1ll1l1ll1l_opy_)
store = {
    bstack11llll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᬬ"): []
}
bstack11l1lll1111_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_11llll11_opy_ = {}
current_test_uuid = None
cli_context = bstack1ll1l1ll1ll_opy_(
    test_framework_name=bstack11llll_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࠨᬭ"),
    test_framework_version=pytest.__version__,
    platform_index=-1,
)
def bstack1ll1lll1l1_opy_(page, bstack11l1l1ll11_opy_):
    try:
        page.evaluate(bstack11llll_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣᬮ"),
                      bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠬᬯ") + json.dumps(
                          bstack11l1l1ll11_opy_) + bstack11llll_opy_ (u"ࠤࢀࢁࠧᬰ"))
    except Exception as e:
        print(bstack11llll_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥࢁࡽࠣᬱ"), e)
def bstack1l11l1111_opy_(page, message, level):
    try:
        page.evaluate(bstack11llll_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧᬲ"), bstack11llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪᬳ") + json.dumps(
            message) + bstack11llll_opy_ (u"࠭ࠬࠣ࡮ࡨࡺࡪࡲࠢ࠻᬴ࠩ") + json.dumps(level) + bstack11llll_opy_ (u"ࠧࡾࡿࠪᬵ"))
    except Exception as e:
        print(bstack11llll_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡦࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠡࡽࢀࠦᬶ"), e)
def pytest_configure(config):
    global bstack111l11l11_opy_
    global CONFIG
    bstack1111l1l1_opy_ = Config.bstack111ll1ll_opy_()
    config.args = bstack1lll1l11_opy_.bstack1l1l1ll1ll1_opy_(config.args)
    bstack1111l1l1_opy_.bstack1l1lll1lll_opy_(bstack1lll1lll11_opy_(config.getoption(bstack11llll_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ᬷ"))))
    if cli.is_running():
        bstack1lll1ll11l_opy_.invoke(Events.CONNECT, bstack11lllll11_opy_())
        cli_context.platform_index = int(os.environ.get(bstack11llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᬸ"), bstack11llll_opy_ (u"ࠫ࠵࠭ᬹ")))
        config = json.loads(os.environ.get(bstack11llll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࠦᬺ"), bstack11llll_opy_ (u"ࠨࡻࡾࠤᬻ")))
        cli.bstack1lll1ll111l_opy_(bstack1lll1l1l1l_opy_(bstack111l11l11_opy_, CONFIG), cli_context.platform_index, bstack1llll1ll1_opy_)
    if cli.bstack1llll11l1l1_opy_(bstack1llll1llll1_opy_):
        cli.bstack1lll1ll1ll1_opy_()
        logger.warning(bstack11llll_opy_ (u"ࠢࡄࡎࡌࠤ࡮ࡹࠠࡢࡥࡷ࡭ࡻ࡫ࠠࡧࡱࡵࠤࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࡂࠨᬼ") + str(cli_context.platform_index) + bstack11llll_opy_ (u"ࠣࠤᬽ"))
        cli.test_framework.track_event(cli_context, bstack1111l1lll1_opy_.bstack1ll1l1l1ll1_opy_, bstack1111l11111_opy_.bstack111l1llll1_opy_, config)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    when = getattr(call, bstack11llll_opy_ (u"ࠤࡺ࡬ࡪࡴࠢᬾ"), None)
    if cli.bstack1llll11l1l1_opy_(bstack1llll1llll1_opy_) and when == bstack11llll_opy_ (u"ࠥࡧࡦࡲ࡬ࠣᬿ"):
        cli.test_framework.track_event(cli_context, bstack1111l1lll1_opy_.bstack1ll1lllll1l_opy_, bstack1111l11111_opy_.bstack111l1llll1_opy_, item, call)
    outcome = yield
    if cli.bstack1llll11l1l1_opy_(bstack1llll1llll1_opy_):
        if when == bstack11llll_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥᭀ"):
            cli.test_framework.track_event(cli_context, bstack1111l1lll1_opy_.bstack1ll1l111l1l_opy_, bstack1111l11111_opy_.bstack111lll1l11_opy_, item, call, outcome)
        elif when == bstack11llll_opy_ (u"ࠧࡩࡡ࡭࡮ࠥᭁ"):
            cli.test_framework.track_event(cli_context, bstack1111l1lll1_opy_.bstack1ll1lllll1l_opy_, bstack1111l11111_opy_.bstack111lll1l11_opy_, item, call, outcome)
        elif when == bstack11llll_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࠣᭂ"):
            cli.test_framework.track_event(cli_context, bstack1111l1lll1_opy_.bstack1ll1l111l11_opy_, bstack1111l11111_opy_.bstack111lll1l11_opy_, item, call, outcome)
        return # skip all existing bstack11l1ll1ll11_opy_
    bstack11l1lll1ll1_opy_ = item.config.getoption(bstack11llll_opy_ (u"ࠧࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩᭃ"))
    plugins = item.config.getoption(bstack11llll_opy_ (u"ࠣࡲ࡯ࡹ࡬࡯࡮ࡴࠤ᭄"))
    report = outcome.get_result()
    bstack11ll1111l1l_opy_(item, call, report)
    if bstack11llll_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡱ࡮ࡸ࡫࡮ࡴࠢᭅ") not in plugins or bstack1l1lll1l1l_opy_():
        return
    summary = []
    driver = getattr(item, bstack11llll_opy_ (u"ࠥࡣࡩࡸࡩࡷࡧࡵࠦᭆ"), None)
    page = getattr(item, bstack11llll_opy_ (u"ࠦࡤࡶࡡࡨࡧࠥᭇ"), None)
    try:
        if (driver == None or driver.session_id == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None or cli.is_running()):
        bstack11ll11111l1_opy_(item, report, summary, bstack11l1lll1ll1_opy_)
    if (page is not None):
        bstack11l1ll1llll_opy_(item, report, summary, bstack11l1lll1ll1_opy_)
def bstack11ll11111l1_opy_(item, report, summary, bstack11l1lll1ll1_opy_):
    if report.when == bstack11llll_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫᭈ") and report.skipped:
        bstack1l1l1ll1111_opy_(report)
    if report.when in [bstack11llll_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧᭉ"), bstack11llll_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤᭊ")]:
        return
    if not bstack1l111lll11l_opy_():
        return
    try:
        if (str(bstack11l1lll1ll1_opy_).lower() != bstack11llll_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᭋ") and not cli.is_running()):
            item._driver.execute_script(
                bstack11llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿ࠦࠧᭌ") + json.dumps(
                    report.nodeid) + bstack11llll_opy_ (u"ࠪࢁࢂ࠭᭍"))
        os.environ[bstack11llll_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࡣ࡙ࡋࡓࡕࡡࡑࡅࡒࡋࠧ᭎")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack11llll_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫࠺ࠡࡽ࠳ࢁࠧ᭏").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11llll_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣ᭐")))
    bstack11l11111l_opy_ = bstack11llll_opy_ (u"ࠢࠣ᭑")
    bstack1l1l1ll1111_opy_(report)
    bstack1lll1ll11l_opy_.invoke(bstack1111ll1lll_opy_.FINISHED)
    if not passed:
        try:
            bstack11l11111l_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack11llll_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡩࡥ࡮ࡲࡵࡳࡧࠣࡶࡪࡧࡳࡰࡰ࠽ࠤࢀ࠶ࡽࠣ᭒").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack11l11111l_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack11llll_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦ᭓")))
        bstack11l11111l_opy_ = bstack11llll_opy_ (u"ࠥࠦ᭔")
        if not passed:
            try:
                bstack11l11111l_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11llll_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥ࡬ࡡࡪ࡮ࡸࡶࡪࠦࡲࡦࡣࡶࡳࡳࡀࠠࡼ࠲ࢀࠦ᭕").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack11l11111l_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack11llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣ࡫ࡱࡪࡴࠨࠬࠡ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡦࡤࡸࡦࠨ࠺ࠡࠩ᭖")
                    + json.dumps(bstack11llll_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠧࠢ᭗"))
                    + bstack11llll_opy_ (u"ࠢ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿࠥ᭘")
                )
            else:
                item._driver.execute_script(
                    bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦࡪࡸࡲࡰࡴࠥ࠰ࠥࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡪࡡࡵࡣࠥ࠾ࠥ࠭᭙")
                    + json.dumps(str(bstack11l11111l_opy_))
                    + bstack11llll_opy_ (u"ࠤ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࠧ᭚")
                )
        except Exception as e:
            summary.append(bstack11llll_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡣࡱࡲࡴࡺࡡࡵࡧ࠽ࠤࢀ࠶ࡽࠣ᭛").format(e))
def bstack11l1lllll1l_opy_(test_name, error_message):
    try:
        bstack11l1llll1l1_opy_ = []
        bstack1ll111l11_opy_ = os.environ.get(bstack11llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ᭜"), bstack11llll_opy_ (u"ࠬ࠶ࠧ᭝"))
        bstack1llll1111_opy_ = {bstack11llll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ᭞"): test_name, bstack11llll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭᭟"): error_message, bstack11llll_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧ᭠"): bstack1ll111l11_opy_}
        bstack11l1lll11l1_opy_ = os.path.join(tempfile.gettempdir(), bstack11llll_opy_ (u"ࠩࡳࡻࡤࡶࡹࡵࡧࡶࡸࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧ᭡"))
        if os.path.exists(bstack11l1lll11l1_opy_):
            with open(bstack11l1lll11l1_opy_) as f:
                bstack11l1llll1l1_opy_ = json.load(f)
        bstack11l1llll1l1_opy_.append(bstack1llll1111_opy_)
        with open(bstack11l1lll11l1_opy_, bstack11llll_opy_ (u"ࠪࡻࠬ᭢")) as f:
            json.dump(bstack11l1llll1l1_opy_, f)
    except Exception as e:
        logger.debug(bstack11llll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡰࡦࡴࡶ࡭ࡸࡺࡩ࡯ࡩࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡱࡻࡷࡩࡸࡺࠠࡦࡴࡵࡳࡷࡹ࠺ࠡࠩ᭣") + str(e))
def bstack11l1ll1llll_opy_(item, report, summary, bstack11l1lll1ll1_opy_):
    if report.when in [bstack11llll_opy_ (u"ࠧࡹࡥࡵࡷࡳࠦ᭤"), bstack11llll_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࠣ᭥")]:
        return
    if (str(bstack11l1lll1ll1_opy_).lower() != bstack11llll_opy_ (u"ࠧࡵࡴࡸࡩࠬ᭦")):
        bstack1ll1lll1l1_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11llll_opy_ (u"ࠣࡹࡤࡷࡽ࡬ࡡࡪ࡮ࠥ᭧")))
    bstack11l11111l_opy_ = bstack11llll_opy_ (u"ࠤࠥ᭨")
    bstack1l1l1ll1111_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack11l11111l_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11llll_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤ࡫ࡧࡩ࡭ࡷࡵࡩࠥࡸࡥࡢࡵࡲࡲ࠿ࠦࡻ࠱ࡿࠥ᭩").format(e)
                )
        try:
            if passed:
                bstack11ll111lll_opy_(getattr(item, bstack11llll_opy_ (u"ࠫࡤࡶࡡࡨࡧࠪ᭪"), None), bstack11llll_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧ᭫"))
            else:
                error_message = bstack11llll_opy_ (u"᭬࠭ࠧ")
                if bstack11l11111l_opy_:
                    bstack1l11l1111_opy_(item._page, str(bstack11l11111l_opy_), bstack11llll_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨ᭭"))
                    bstack11ll111lll_opy_(getattr(item, bstack11llll_opy_ (u"ࠨࡡࡳࡥ࡬࡫ࠧ᭮"), None), bstack11llll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ᭯"), str(bstack11l11111l_opy_))
                    error_message = str(bstack11l11111l_opy_)
                else:
                    bstack11ll111lll_opy_(getattr(item, bstack11llll_opy_ (u"ࠪࡣࡵࡧࡧࡦࠩ᭰"), None), bstack11llll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ᭱"))
                bstack11l1lllll1l_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack11llll_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡹࡵࡪࡡࡵࡧࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࢁ࠰ࡾࠤ᭲").format(e))
try:
    from typing import Generator
    import pytest_playwright.pytest_playwright as p
    @pytest.fixture
    def page(context: BrowserContext, request: pytest.FixtureRequest) -> Generator[Page, None, None]:
        page = context.new_page()
        request.node._page = page
        yield page
except:
    pass
def pytest_addoption(parser):
    parser.addoption(bstack11llll_opy_ (u"ࠨ࠭࠮ࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ᭳"), default=bstack11llll_opy_ (u"ࠢࡇࡣ࡯ࡷࡪࠨ᭴"), help=bstack11llll_opy_ (u"ࠣࡃࡸࡸࡴࡳࡡࡵ࡫ࡦࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠢ᭵"))
    parser.addoption(bstack11llll_opy_ (u"ࠤ࠰࠱ࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣ᭶"), default=bstack11llll_opy_ (u"ࠥࡊࡦࡲࡳࡦࠤ᭷"), help=bstack11llll_opy_ (u"ࠦࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡩࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠥ᭸"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack11llll_opy_ (u"ࠧ࠳࠭ࡥࡴ࡬ࡺࡪࡸࠢ᭹"), action=bstack11llll_opy_ (u"ࠨࡳࡵࡱࡵࡩࠧ᭺"), default=bstack11llll_opy_ (u"ࠢࡤࡪࡵࡳࡲ࡫ࠢ᭻"),
                         help=bstack11llll_opy_ (u"ࠣࡆࡵ࡭ࡻ࡫ࡲࠡࡶࡲࠤࡷࡻ࡮ࠡࡶࡨࡷࡹࡹࠢ᭼"))
def bstack1ll11111_opy_(log):
    if not (log[bstack11llll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ᭽")] and log[bstack11llll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ᭾")].strip()):
        return
    active = bstack11lll11l_opy_()
    log = {
        bstack11llll_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ᭿"): log[bstack11llll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᮀ")],
        bstack11llll_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩᮁ"): bstack1l111l1l_opy_().isoformat() + bstack11llll_opy_ (u"࡛ࠧࠩᮂ"),
        bstack11llll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᮃ"): log[bstack11llll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᮄ")],
    }
    if active:
        if active[bstack11llll_opy_ (u"ࠪࡸࡾࡶࡥࠨᮅ")] == bstack11llll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩᮆ"):
            log[bstack11llll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᮇ")] = active[bstack11llll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᮈ")]
        elif active[bstack11llll_opy_ (u"ࠧࡵࡻࡳࡩࠬᮉ")] == bstack11llll_opy_ (u"ࠨࡶࡨࡷࡹ࠭ᮊ"):
            log[bstack11llll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᮋ")] = active[bstack11llll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᮌ")]
    bstack1lll11ll_opy_.bstack1ll1ll11_opy_([log])
def bstack11lll11l_opy_():
    if len(store[bstack11llll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᮍ")]) > 0 and store[bstack11llll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᮎ")][-1]:
        return {
            bstack11llll_opy_ (u"࠭ࡴࡺࡲࡨࠫᮏ"): bstack11llll_opy_ (u"ࠧࡩࡱࡲ࡯ࠬᮐ"),
            bstack11llll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᮑ"): store[bstack11llll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ᮒ")][-1]
        }
    if store.get(bstack11llll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᮓ"), None):
        return {
            bstack11llll_opy_ (u"ࠫࡹࡿࡰࡦࠩᮔ"): bstack11llll_opy_ (u"ࠬࡺࡥࡴࡶࠪᮕ"),
            bstack11llll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᮖ"): store[bstack11llll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫᮗ")]
        }
    return None
def pytest_runtest_logstart(nodeid, location):
    if cli.bstack1llll11l1l1_opy_(bstack1llll1llll1_opy_):
        cli.test_framework.track_event(cli_context, bstack1111l1lll1_opy_.bstack1ll1l11l1ll_opy_, bstack1111l11111_opy_.bstack111l1llll1_opy_, nodeid, location)
def pytest_runtest_logfinish(nodeid, location):
    if cli.bstack1llll11l1l1_opy_(bstack1llll1llll1_opy_):
        cli.test_framework.track_event(cli_context, bstack1111l1lll1_opy_.bstack1ll1l11l1ll_opy_, bstack1111l11111_opy_.bstack111lll1l11_opy_, nodeid, location)
def pytest_runtest_call(item):
    if cli.bstack1llll11l1l1_opy_(bstack1llll1llll1_opy_):
        cli.test_framework.track_event(cli_context, bstack1111l1lll1_opy_.TEST, bstack1111l11111_opy_.bstack111l1llll1_opy_, item)
        return # skip all existing bstack11l1ll1ll11_opy_
    bstack1lll1ll11l_opy_.invoke(bstack1111ll1lll_opy_.bstack1111llll11_opy_, item.nodeid)
    try:
        global CONFIG
        item._11ll1111l11_opy_ = True
        bstack1lllll1lll_opy_ = bstack11111l11_opy_.bstack11l1ll1ll1_opy_(bstack1l11lll1l1l_opy_(item.own_markers))
        if not cli.bstack1llll11l1l1_opy_(bstack1llll1llll1_opy_):
            item._a11y_test_case = bstack1lllll1lll_opy_
            if bstack1ll111l1_opy_(threading.current_thread(), bstack11llll_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧᮘ"), None):
                driver = getattr(item, bstack11llll_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪᮙ"), None)
                item._a11y_started = bstack11111l11_opy_.bstack1lllll11ll_opy_(driver, bstack1lllll1lll_opy_)
        if not bstack1lll11ll_opy_.on() or bstack11l1lll11ll_opy_ != bstack11llll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪᮚ"):
            return
        global current_test_uuid #, bstack1l111l11_opy_
        bstack1lll1lll_opy_ = {
            bstack11llll_opy_ (u"ࠫࡺࡻࡩࡥࠩᮛ"): uuid4().__str__(),
            bstack11llll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᮜ"): bstack1l111l1l_opy_().isoformat() + bstack11llll_opy_ (u"࡚࠭ࠨᮝ")
        }
        current_test_uuid = bstack1lll1lll_opy_[bstack11llll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᮞ")]
        store[bstack11llll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬᮟ")] = bstack1lll1lll_opy_[bstack11llll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᮠ")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _11llll11_opy_[item.nodeid] = {**_11llll11_opy_[item.nodeid], **bstack1lll1lll_opy_}
        bstack11l1llll1ll_opy_(item, _11llll11_opy_[item.nodeid], bstack11llll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᮡ"))
    except Exception as err:
        print(bstack11llll_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡶࡺࡴࡴࡦࡵࡷࡣࡨࡧ࡬࡭࠼ࠣࡿࢂ࠭ᮢ"), str(err))
def pytest_runtest_setup(item):
    if cli.bstack1llll11l1l1_opy_(bstack1llll1llll1_opy_):
        cli.test_framework.track_event(cli_context, bstack1111l1lll1_opy_.bstack1ll1l111l1l_opy_, bstack1111l11111_opy_.bstack111l1llll1_opy_, item)
        return # skip all existing bstack11l1ll1ll11_opy_
    global bstack11l1lll1111_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack1l11ll1l1ll_opy_():
        atexit.register(bstack11l11l1l1l_opy_)
        if not bstack11l1lll1111_opy_:
            try:
                bstack11ll1111lll_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack1l11l111l11_opy_():
                    bstack11ll1111lll_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack11ll1111lll_opy_:
                    signal.signal(s, bstack11l1lllll11_opy_)
                bstack11l1lll1111_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack11llll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡳࡧࡪ࡭ࡸࡺࡥࡳࠢࡶ࡭࡬ࡴࡡ࡭ࠢ࡫ࡥࡳࡪ࡬ࡦࡴࡶ࠾ࠥࠨᮣ") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack1l1l1ll1l11_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack11llll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᮤ")
    try:
        if not bstack1lll11ll_opy_.on():
            return
        uuid = uuid4().__str__()
        bstack1lll1lll_opy_ = {
            bstack11llll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᮥ"): uuid,
            bstack11llll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᮦ"): bstack1l111l1l_opy_().isoformat() + bstack11llll_opy_ (u"ࠩ࡝ࠫᮧ"),
            bstack11llll_opy_ (u"ࠪࡸࡾࡶࡥࠨᮨ"): bstack11llll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩᮩ"),
            bstack11llll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨ᮪"): bstack11llll_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋ᮫ࠫ"),
            bstack11llll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪᮬ"): bstack11llll_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧᮭ")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack11llll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭ᮮ")] = item
        store[bstack11llll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧᮯ")] = [uuid]
        if not _11llll11_opy_.get(item.nodeid, None):
            _11llll11_opy_[item.nodeid] = {bstack11llll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ᮰"): [], bstack11llll_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧ᮱"): []}
        _11llll11_opy_[item.nodeid][bstack11llll_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ᮲")].append(bstack1lll1lll_opy_[bstack11llll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ᮳")])
        _11llll11_opy_[item.nodeid + bstack11llll_opy_ (u"ࠨ࠯ࡶࡩࡹࡻࡰࠨ᮴")] = bstack1lll1lll_opy_
        bstack11l1lllllll_opy_(item, bstack1lll1lll_opy_, bstack11llll_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ᮵"))
    except Exception as err:
        print(bstack11llll_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡵࡹࡳࡺࡥࡴࡶࡢࡷࡪࡺࡵࡱ࠼ࠣࡿࢂ࠭᮶"), str(err))
def pytest_runtest_teardown(item):
    if cli.bstack1llll11l1l1_opy_(bstack1llll1llll1_opy_):
        cli.test_framework.track_event(cli_context, bstack1111l1lll1_opy_.TEST, bstack1111l11111_opy_.bstack111lll1l11_opy_, item)
        cli.test_framework.track_event(cli_context, bstack1111l1lll1_opy_.bstack1ll1l111l11_opy_, bstack1111l11111_opy_.bstack111l1llll1_opy_, item)
        return # skip all existing bstack11l1ll1ll11_opy_
    try:
        global bstack1l1lll1ll1_opy_
        bstack1ll111l11_opy_ = 0
        if bstack1l111l1l11_opy_ is True:
            bstack1ll111l11_opy_ = int(os.environ.get(bstack11llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ᮷")))
        if bstack1ll1lll1ll_opy_.bstack11ll11llll_opy_() == bstack11llll_opy_ (u"ࠧࡺࡲࡶࡧࠥ᮸"):
            if bstack1ll1lll1ll_opy_.bstack11111l1l1_opy_() == bstack11llll_opy_ (u"ࠨࡴࡦࡵࡷࡧࡦࡹࡥࠣ᮹"):
                bstack11l1ll1ll1l_opy_ = bstack1ll111l1_opy_(threading.current_thread(), bstack11llll_opy_ (u"ࠧࡱࡧࡵࡧࡾ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪᮺ"), None)
                bstack1l11lll1l_opy_ = bstack11l1ll1ll1l_opy_ + bstack11llll_opy_ (u"ࠣ࠯ࡷࡩࡸࡺࡣࡢࡵࡨࠦᮻ")
                driver = getattr(item, bstack11llll_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪᮼ"), None)
                bstack1ll11l11ll_opy_ = getattr(item, bstack11llll_opy_ (u"ࠪࡲࡦࡳࡥࠨᮽ"), None)
                bstack1ll1ll1ll_opy_ = getattr(item, bstack11llll_opy_ (u"ࠫࡺࡻࡩࡥࠩᮾ"), None)
                PercySDK.screenshot(driver, bstack1l11lll1l_opy_, bstack1ll11l11ll_opy_=bstack1ll11l11ll_opy_, bstack1ll1ll1ll_opy_=bstack1ll1ll1ll_opy_, bstack1l1ll11l1l_opy_=bstack1ll111l11_opy_)
        if not cli.bstack1llll11l1l1_opy_(bstack1llll1llll1_opy_):
            if getattr(item, bstack11llll_opy_ (u"ࠬࡥࡡ࠲࠳ࡼࡣࡸࡺࡡࡳࡶࡨࡨࠬᮿ"), False):
                bstack11l11l11_opy_.bstack111l1ll1_opy_(getattr(item, bstack11llll_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧᯀ"), None), bstack1l1lll1ll1_opy_, logger, item)
        if not bstack1lll11ll_opy_.on():
            return
        bstack1lll1lll_opy_ = {
            bstack11llll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᯁ"): uuid4().__str__(),
            bstack11llll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᯂ"): bstack1l111l1l_opy_().isoformat() + bstack11llll_opy_ (u"ࠩ࡝ࠫᯃ"),
            bstack11llll_opy_ (u"ࠪࡸࡾࡶࡥࠨᯄ"): bstack11llll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩᯅ"),
            bstack11llll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨᯆ"): bstack11llll_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪᯇ"),
            bstack11llll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪᯈ"): bstack11llll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪᯉ")
        }
        _11llll11_opy_[item.nodeid + bstack11llll_opy_ (u"ࠩ࠰ࡸࡪࡧࡲࡥࡱࡺࡲࠬᯊ")] = bstack1lll1lll_opy_
        bstack11l1lllllll_opy_(item, bstack1lll1lll_opy_, bstack11llll_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᯋ"))
    except Exception as err:
        print(bstack11llll_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡶࡺࡴࡴࡦࡵࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡀࠠࡼࡿࠪᯌ"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if not bstack1lll11ll_opy_.on():
        if cli.bstack1llll11l1l1_opy_(bstack1llll1llll1_opy_):
            cli.test_framework.track_event(cli_context, bstack1111l1lll1_opy_.bstack1lll1l11lll_opy_, bstack1111l11111_opy_.bstack111l1llll1_opy_, fixturedef, request)
        outcome = yield
        if cli.bstack1llll11l1l1_opy_(bstack1llll1llll1_opy_):
            cli.test_framework.track_event(cli_context, bstack1111l1lll1_opy_.bstack1lll1l11lll_opy_, bstack1111l11111_opy_.bstack111lll1l11_opy_, fixturedef, request, outcome)
        return # skip all existing bstack11l1ll1ll11_opy_
    start_time = datetime.datetime.now()
    if bstack1l1l1l1l1ll_opy_(fixturedef.argname):
        store[bstack11llll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥ࡭ࡰࡦࡸࡰࡪࡥࡩࡵࡧࡰࠫᯍ")] = request.node
    elif bstack1l1l1l1llll_opy_(fixturedef.argname):
        store[bstack11llll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡤ࡮ࡤࡷࡸࡥࡩࡵࡧࡰࠫᯎ")] = request.node
    if cli.bstack1llll11l1l1_opy_(bstack1llll1llll1_opy_):
        cli.test_framework.track_event(cli_context, bstack1111l1lll1_opy_.bstack1lll1l11lll_opy_, bstack1111l11111_opy_.bstack111l1llll1_opy_, fixturedef, request)
    outcome = yield
    if cli.bstack1llll11l1l1_opy_(bstack1llll1llll1_opy_):
        cli.test_framework.track_event(cli_context, bstack1111l1lll1_opy_.bstack1lll1l11lll_opy_, bstack1111l11111_opy_.bstack111lll1l11_opy_, fixturedef, request, outcome)
        return # skip all existing bstack11l1ll1ll11_opy_
    try:
        fixture = {
            bstack11llll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᯏ"): fixturedef.argname,
            bstack11llll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᯐ"): bstack1l111llll1l_opy_(outcome),
            bstack11llll_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫᯑ"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack11llll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧᯒ")]
        if not _11llll11_opy_.get(current_test_item.nodeid, None):
            _11llll11_opy_[current_test_item.nodeid] = {bstack11llll_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭ᯓ"): []}
        _11llll11_opy_[current_test_item.nodeid][bstack11llll_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧᯔ")].append(fixture)
    except Exception as err:
        logger.debug(bstack11llll_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡳࡦࡶࡸࡴ࠿ࠦࡻࡾࠩᯕ"), str(err))
if bstack1l1lll1l1l_opy_() and bstack1lll11ll_opy_.on():
    def pytest_bdd_before_step(request, step):
        try:
            _11llll11_opy_[request.node.nodeid][bstack11llll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᯖ")].bstack11ll11l1_opy_(id(step))
        except Exception as err:
            print(bstack11llll_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱ࠼ࠣࡿࢂ࠭ᯗ"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        try:
            _11llll11_opy_[request.node.nodeid][bstack11llll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᯘ")].bstack1l1l111l_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack11llll_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡳࡵࡧࡳࡣࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠧᯙ"), str(err))
    def pytest_bdd_after_step(request, step):
        try:
            bstack1l1l1lll_opy_: bstack1lll11l1_opy_ = _11llll11_opy_[request.node.nodeid][bstack11llll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᯚ")]
            bstack1l1l1lll_opy_.bstack1l1l111l_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack11llll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡵࡷࡩࡵࡥࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠩᯛ"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack11l1lll11ll_opy_
        try:
            if not bstack1lll11ll_opy_.on() or bstack11l1lll11ll_opy_ != bstack11llll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠪᯜ"):
                return
            driver = bstack1ll111l1_opy_(threading.current_thread(), bstack11llll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ᯝ"), None)
            if not _11llll11_opy_.get(request.node.nodeid, None):
                _11llll11_opy_[request.node.nodeid] = {}
            bstack1l1l1lll_opy_ = bstack1lll11l1_opy_.bstack1l11111111l_opy_(
                scenario, feature, request.node,
                name=bstack1l1l1l1lll1_opy_(request.node, scenario),
                started_at=bstack1l111ll1_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack11llll_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴ࠮ࡥࡸࡧࡺࡳࡢࡦࡴࠪᯞ"),
                tags=bstack1l1l1ll11l1_opy_(feature, scenario),
                bstack1ll1l111_opy_=bstack1lll11ll_opy_.bstack1l1ll111_opy_(driver) if driver and driver.session_id else {}
            )
            _11llll11_opy_[request.node.nodeid][bstack11llll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᯟ")] = bstack1l1l1lll_opy_
            bstack11l1llll111_opy_(bstack1l1l1lll_opy_.uuid)
            bstack1lll11ll_opy_.bstack1l1l11ll_opy_(bstack11llll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᯠ"), bstack1l1l1lll_opy_)
        except Exception as err:
            print(bstack11llll_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰ࠼ࠣࡿࢂ࠭ᯡ"), str(err))
def bstack11ll11111ll_opy_(bstack11ll11ll_opy_):
    if bstack11ll11ll_opy_ in store[bstack11llll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᯢ")]:
        store[bstack11llll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᯣ")].remove(bstack11ll11ll_opy_)
def bstack11l1llll111_opy_(bstack11ll1l11_opy_):
    store[bstack11llll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫᯤ")] = bstack11ll1l11_opy_
    threading.current_thread().current_test_uuid = bstack11ll1l11_opy_
@bstack1lll11ll_opy_.bstack11ll11ll1l1_opy_
def bstack11ll1111l1l_opy_(item, call, report):
    global bstack11l1lll11ll_opy_
    bstack111111l11_opy_ = bstack1l111ll1_opy_()
    if hasattr(report, bstack11llll_opy_ (u"ࠨࡵࡷࡳࡵ࠭ᯥ")):
        bstack111111l11_opy_ = bstack1l11lllll11_opy_(report.stop)
    elif hasattr(report, bstack11llll_opy_ (u"ࠩࡶࡸࡦࡸࡴࠨ᯦")):
        bstack111111l11_opy_ = bstack1l11lllll11_opy_(report.start)
    try:
        if getattr(report, bstack11llll_opy_ (u"ࠪࡻ࡭࡫࡮ࠨᯧ"), bstack11llll_opy_ (u"ࠫࠬᯨ")) == bstack11llll_opy_ (u"ࠬࡩࡡ࡭࡮ࠪᯩ"):
            if bstack11l1lll11ll_opy_ == bstack11llll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ᯪ"):
                _11llll11_opy_[item.nodeid][bstack11llll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᯫ")] = bstack111111l11_opy_
                bstack11l1llll1ll_opy_(item, _11llll11_opy_[item.nodeid], bstack11llll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᯬ"), report, call)
                store[bstack11llll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ᯭ")] = None
            elif bstack11l1lll11ll_opy_ == bstack11llll_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠢᯮ"):
                bstack1l1l1lll_opy_ = _11llll11_opy_[item.nodeid][bstack11llll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᯯ")]
                bstack1l1l1lll_opy_.set(hooks=_11llll11_opy_[item.nodeid].get(bstack11llll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᯰ"), []))
                exception, bstack1l1l11l1_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack1l1l11l1_opy_ = [call.excinfo.exconly(), getattr(report, bstack11llll_opy_ (u"࠭࡬ࡰࡰࡪࡶࡪࡶࡲࡵࡧࡻࡸࠬᯱ"), bstack11llll_opy_ (u"ࠧࠨ᯲"))]
                bstack1l1l1lll_opy_.stop(time=bstack111111l11_opy_, result=Result(result=getattr(report, bstack11llll_opy_ (u"ࠨࡱࡸࡸࡨࡵ࡭ࡦ᯳ࠩ"), bstack11llll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ᯴")), exception=exception, bstack1l1l11l1_opy_=bstack1l1l11l1_opy_))
                bstack1lll11ll_opy_.bstack1l1l11ll_opy_(bstack11llll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ᯵"), _11llll11_opy_[item.nodeid][bstack11llll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ᯶")])
        elif getattr(report, bstack11llll_opy_ (u"ࠬࡽࡨࡦࡰࠪ᯷"), bstack11llll_opy_ (u"࠭ࠧ᯸")) in [bstack11llll_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭᯹"), bstack11llll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪ᯺")]:
            bstack1l1111ll_opy_ = item.nodeid + bstack11llll_opy_ (u"ࠩ࠰ࠫ᯻") + getattr(report, bstack11llll_opy_ (u"ࠪࡻ࡭࡫࡮ࠨ᯼"), bstack11llll_opy_ (u"ࠫࠬ᯽"))
            if getattr(report, bstack11llll_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭᯾"), False):
                hook_type = bstack11llll_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫ᯿") if getattr(report, bstack11llll_opy_ (u"ࠧࡸࡪࡨࡲࠬᰀ"), bstack11llll_opy_ (u"ࠨࠩᰁ")) == bstack11llll_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨᰂ") else bstack11llll_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧᰃ")
                _11llll11_opy_[bstack1l1111ll_opy_] = {
                    bstack11llll_opy_ (u"ࠫࡺࡻࡩࡥࠩᰄ"): uuid4().__str__(),
                    bstack11llll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᰅ"): bstack111111l11_opy_,
                    bstack11llll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩᰆ"): hook_type
                }
            _11llll11_opy_[bstack1l1111ll_opy_][bstack11llll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᰇ")] = bstack111111l11_opy_
            bstack11ll11111ll_opy_(_11llll11_opy_[bstack1l1111ll_opy_][bstack11llll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᰈ")])
            bstack11l1lllllll_opy_(item, _11llll11_opy_[bstack1l1111ll_opy_], bstack11llll_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᰉ"), report, call)
            if getattr(report, bstack11llll_opy_ (u"ࠪࡻ࡭࡫࡮ࠨᰊ"), bstack11llll_opy_ (u"ࠫࠬᰋ")) == bstack11llll_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫᰌ"):
                if getattr(report, bstack11llll_opy_ (u"࠭࡯ࡶࡶࡦࡳࡲ࡫ࠧᰍ"), bstack11llll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᰎ")) == bstack11llll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᰏ"):
                    bstack1lll1lll_opy_ = {
                        bstack11llll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᰐ"): uuid4().__str__(),
                        bstack11llll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᰑ"): bstack1l111ll1_opy_(),
                        bstack11llll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᰒ"): bstack1l111ll1_opy_()
                    }
                    _11llll11_opy_[item.nodeid] = {**_11llll11_opy_[item.nodeid], **bstack1lll1lll_opy_}
                    bstack11l1llll1ll_opy_(item, _11llll11_opy_[item.nodeid], bstack11llll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ᰓ"))
                    bstack11l1llll1ll_opy_(item, _11llll11_opy_[item.nodeid], bstack11llll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᰔ"), report, call)
    except Exception as err:
        print(bstack11llll_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡢࡰࡧࡰࡪࡥ࡯࠲࠳ࡼࡣࡹ࡫ࡳࡵࡡࡨࡺࡪࡴࡴ࠻ࠢࡾࢁࠬᰕ"), str(err))
def bstack11l1ll1l1ll_opy_(test, bstack1lll1lll_opy_, result=None, call=None, bstack1lll111l1l_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack1l1l1lll_opy_ = {
        bstack11llll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᰖ"): bstack1lll1lll_opy_[bstack11llll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᰗ")],
        bstack11llll_opy_ (u"ࠪࡸࡾࡶࡥࠨᰘ"): bstack11llll_opy_ (u"ࠫࡹ࡫ࡳࡵࠩᰙ"),
        bstack11llll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᰚ"): test.name,
        bstack11llll_opy_ (u"࠭ࡢࡰࡦࡼࠫᰛ"): {
            bstack11llll_opy_ (u"ࠧ࡭ࡣࡱ࡫ࠬᰜ"): bstack11llll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨᰝ"),
            bstack11llll_opy_ (u"ࠩࡦࡳࡩ࡫ࠧᰞ"): inspect.getsource(test.obj)
        },
        bstack11llll_opy_ (u"ࠪ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᰟ"): test.name,
        bstack11llll_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࠪᰠ"): test.name,
        bstack11llll_opy_ (u"ࠬࡹࡣࡰࡲࡨࡷࠬᰡ"): bstack1lll1l11_opy_.bstack1ll111ll_opy_(test),
        bstack11llll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩᰢ"): file_path,
        bstack11llll_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠩᰣ"): file_path,
        bstack11llll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᰤ"): bstack11llll_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪᰥ"),
        bstack11llll_opy_ (u"ࠪࡺࡨࡥࡦࡪ࡮ࡨࡴࡦࡺࡨࠨᰦ"): file_path,
        bstack11llll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᰧ"): bstack1lll1lll_opy_[bstack11llll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᰨ")],
        bstack11llll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩᰩ"): bstack11llll_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺࠧᰪ"),
        bstack11llll_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡓࡧࡵࡹࡳࡖࡡࡳࡣࡰࠫᰫ"): {
            bstack11llll_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡠࡰࡤࡱࡪ࠭ᰬ"): test.nodeid
        },
        bstack11llll_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᰭ"): bstack1l11lll1l1l_opy_(test.own_markers)
    }
    if bstack1lll111l1l_opy_ in [bstack11llll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬᰮ"), bstack11llll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᰯ")]:
        bstack1l1l1lll_opy_[bstack11llll_opy_ (u"࠭࡭ࡦࡶࡤࠫᰰ")] = {
            bstack11llll_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩᰱ"): bstack1lll1lll_opy_.get(bstack11llll_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪᰲ"), [])
        }
    if bstack1lll111l1l_opy_ == bstack11llll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪᰳ"):
        bstack1l1l1lll_opy_[bstack11llll_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᰴ")] = bstack11llll_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬᰵ")
        bstack1l1l1lll_opy_[bstack11llll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᰶ")] = bstack1lll1lll_opy_[bstack11llll_opy_ (u"࠭ࡨࡰࡱ࡮ࡷ᰷ࠬ")]
        bstack1l1l1lll_opy_[bstack11llll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ᰸")] = bstack1lll1lll_opy_[bstack11llll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭᰹")]
    if result:
        bstack1l1l1lll_opy_[bstack11llll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ᰺")] = result.outcome
        bstack1l1l1lll_opy_[bstack11llll_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫ᰻")] = result.duration * 1000
        bstack1l1l1lll_opy_[bstack11llll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ᰼")] = bstack1lll1lll_opy_[bstack11llll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ᰽")]
        if result.failed:
            bstack1l1l1lll_opy_[bstack11llll_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬ᰾")] = bstack1lll11ll_opy_.bstack111llll11l_opy_(call.excinfo.typename)
            bstack1l1l1lll_opy_[bstack11llll_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨ᰿")] = bstack1lll11ll_opy_.bstack11ll11ll1ll_opy_(call.excinfo, result)
        bstack1l1l1lll_opy_[bstack11llll_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ᱀")] = bstack1lll1lll_opy_[bstack11llll_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ᱁")]
    if outcome:
        bstack1l1l1lll_opy_[bstack11llll_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ᱂")] = bstack1l111llll1l_opy_(outcome)
        bstack1l1l1lll_opy_[bstack11llll_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬ᱃")] = 0
        bstack1l1l1lll_opy_[bstack11llll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ᱄")] = bstack1lll1lll_opy_[bstack11llll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ᱅")]
        if bstack1l1l1lll_opy_[bstack11llll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ᱆")] == bstack11llll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ᱇"):
            bstack1l1l1lll_opy_[bstack11llll_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨ᱈")] = bstack11llll_opy_ (u"࡙ࠪࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠫ᱉")  # bstack11ll1111111_opy_
            bstack1l1l1lll_opy_[bstack11llll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬ᱊")] = [{bstack11llll_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨ᱋"): [bstack11llll_opy_ (u"࠭ࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠪ᱌")]}]
        bstack1l1l1lll_opy_[bstack11llll_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᱍ")] = bstack1lll1lll_opy_[bstack11llll_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᱎ")]
    return bstack1l1l1lll_opy_
def bstack11l1llllll1_opy_(test, bstack1l11l11l_opy_, bstack1lll111l1l_opy_, result, call, outcome, bstack11l1ll1lll1_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack1l11l11l_opy_[bstack11llll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬᱏ")]
    hook_name = bstack1l11l11l_opy_[bstack11llll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭᱐")]
    hook_data = {
        bstack11llll_opy_ (u"ࠫࡺࡻࡩࡥࠩ᱑"): bstack1l11l11l_opy_[bstack11llll_opy_ (u"ࠬࡻࡵࡪࡦࠪ᱒")],
        bstack11llll_opy_ (u"࠭ࡴࡺࡲࡨࠫ᱓"): bstack11llll_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ᱔"),
        bstack11llll_opy_ (u"ࠨࡰࡤࡱࡪ࠭᱕"): bstack11llll_opy_ (u"ࠩࡾࢁࠬ᱖").format(bstack1l1l1l1l11l_opy_(hook_name)),
        bstack11llll_opy_ (u"ࠪࡦࡴࡪࡹࠨ᱗"): {
            bstack11llll_opy_ (u"ࠫࡱࡧ࡮ࡨࠩ᱘"): bstack11llll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ᱙"),
            bstack11llll_opy_ (u"࠭ࡣࡰࡦࡨࠫᱚ"): None
        },
        bstack11llll_opy_ (u"ࠧࡴࡥࡲࡴࡪ࠭ᱛ"): test.name,
        bstack11llll_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࡳࠨᱜ"): bstack1lll1l11_opy_.bstack1ll111ll_opy_(test, hook_name),
        bstack11llll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬᱝ"): file_path,
        bstack11llll_opy_ (u"ࠪࡰࡴࡩࡡࡵ࡫ࡲࡲࠬᱞ"): file_path,
        bstack11llll_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᱟ"): bstack11llll_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭ᱠ"),
        bstack11llll_opy_ (u"࠭ࡶࡤࡡࡩ࡭ࡱ࡫ࡰࡢࡶ࡫ࠫᱡ"): file_path,
        bstack11llll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᱢ"): bstack1l11l11l_opy_[bstack11llll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᱣ")],
        bstack11llll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬᱤ"): bstack11llll_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶ࠰ࡧࡺࡩࡵ࡮ࡤࡨࡶࠬᱥ") if bstack11l1lll11ll_opy_ == bstack11llll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨᱦ") else bstack11llll_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸࠬᱧ"),
        bstack11llll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩᱨ"): hook_type
    }
    bstack1l111111l11_opy_ = bstack1l11ll1l_opy_(_11llll11_opy_.get(test.nodeid, None))
    if bstack1l111111l11_opy_:
        hook_data[bstack11llll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡ࡬ࡨࠬᱩ")] = bstack1l111111l11_opy_
    if result:
        hook_data[bstack11llll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᱪ")] = result.outcome
        hook_data[bstack11llll_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪᱫ")] = result.duration * 1000
        hook_data[bstack11llll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᱬ")] = bstack1l11l11l_opy_[bstack11llll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᱭ")]
        if result.failed:
            hook_data[bstack11llll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫᱮ")] = bstack1lll11ll_opy_.bstack111llll11l_opy_(call.excinfo.typename)
            hook_data[bstack11llll_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧᱯ")] = bstack1lll11ll_opy_.bstack11ll11ll1ll_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack11llll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᱰ")] = bstack1l111llll1l_opy_(outcome)
        hook_data[bstack11llll_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩᱱ")] = 100
        hook_data[bstack11llll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᱲ")] = bstack1l11l11l_opy_[bstack11llll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᱳ")]
        if hook_data[bstack11llll_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᱴ")] == bstack11llll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᱵ"):
            hook_data[bstack11llll_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬᱶ")] = bstack11llll_opy_ (u"ࠧࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠨᱷ")  # bstack11ll1111111_opy_
            hook_data[bstack11llll_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩᱸ")] = [{bstack11llll_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬᱹ"): [bstack11llll_opy_ (u"ࠪࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠧᱺ")]}]
    if bstack11l1ll1lll1_opy_:
        hook_data[bstack11llll_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᱻ")] = bstack11l1ll1lll1_opy_.result
        hook_data[bstack11llll_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭ᱼ")] = bstack1l11l1l11l1_opy_(bstack1l11l11l_opy_[bstack11llll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᱽ")], bstack1l11l11l_opy_[bstack11llll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ᱾")])
        hook_data[bstack11llll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭᱿")] = bstack1l11l11l_opy_[bstack11llll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᲀ")]
        if hook_data[bstack11llll_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᲁ")] == bstack11llll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᲂ"):
            hook_data[bstack11llll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫᲃ")] = bstack1lll11ll_opy_.bstack111llll11l_opy_(bstack11l1ll1lll1_opy_.exception_type)
            hook_data[bstack11llll_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧᲄ")] = [{bstack11llll_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪᲅ"): bstack1l111l11lll_opy_(bstack11l1ll1lll1_opy_.exception)}]
    return hook_data
def bstack11l1llll1ll_opy_(test, bstack1lll1lll_opy_, bstack1lll111l1l_opy_, result=None, call=None, outcome=None):
    bstack1l1l1lll_opy_ = bstack11l1ll1l1ll_opy_(test, bstack1lll1lll_opy_, result, call, bstack1lll111l1l_opy_, outcome)
    driver = getattr(test, bstack11llll_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩᲆ"), None)
    if bstack1lll111l1l_opy_ == bstack11llll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᲇ") and driver:
        bstack1l1l1lll_opy_[bstack11llll_opy_ (u"ࠪ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࡴࠩᲈ")] = bstack1lll11ll_opy_.bstack1l1ll111_opy_(driver)
    if bstack1lll111l1l_opy_ == bstack11llll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬᲉ"):
        bstack1lll111l1l_opy_ = bstack11llll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᲊ")
    bstack1lllll11_opy_ = {
        bstack11llll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ᲋"): bstack1lll111l1l_opy_,
        bstack11llll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩ᲌"): bstack1l1l1lll_opy_
    }
    bstack1lll11ll_opy_.bstack11ll1ll1_opy_(bstack1lllll11_opy_)
def bstack11l1lllllll_opy_(test, bstack1lll1lll_opy_, bstack1lll111l1l_opy_, result=None, call=None, outcome=None, bstack11l1ll1lll1_opy_=None):
    hook_data = bstack11l1llllll1_opy_(test, bstack1lll1lll_opy_, bstack1lll111l1l_opy_, result, call, outcome, bstack11l1ll1lll1_opy_)
    bstack1lllll11_opy_ = {
        bstack11llll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ᲍"): bstack1lll111l1l_opy_,
        bstack11llll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࠫ᲎"): hook_data
    }
    bstack1lll11ll_opy_.bstack11ll1ll1_opy_(bstack1lllll11_opy_)
def bstack1l11ll1l_opy_(bstack1lll1lll_opy_):
    if not bstack1lll1lll_opy_:
        return None
    if bstack1lll1lll_opy_.get(bstack11llll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭᲏"), None):
        return getattr(bstack1lll1lll_opy_[bstack11llll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᲐ")], bstack11llll_opy_ (u"ࠬࡻࡵࡪࡦࠪᲑ"), None)
    return bstack1lll1lll_opy_.get(bstack11llll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᲒ"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    if cli.bstack1llll11l1l1_opy_(bstack1llll1llll1_opy_):
        cli.test_framework.track_event(cli_context, bstack1111l1lll1_opy_.LOG, bstack1111l11111_opy_.bstack111l1llll1_opy_, request, caplog)
    yield
    if cli.bstack1llll11l1l1_opy_(bstack1llll1llll1_opy_):
        cli.test_framework.track_event(cli_context, bstack1111l1lll1_opy_.LOG, bstack1111l11111_opy_.bstack111lll1l11_opy_, request, caplog)
        return # skip all existing bstack11l1ll1ll11_opy_
    try:
        if not bstack1lll11ll_opy_.on():
            return
        places = [bstack11llll_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭Დ"), bstack11llll_opy_ (u"ࠨࡥࡤࡰࡱ࠭Ე"), bstack11llll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫᲕ")]
        bstack1ll11l11_opy_ = []
        for bstack11l1lll111l_opy_ in places:
            records = caplog.get_records(bstack11l1lll111l_opy_)
            bstack11l1lll1lll_opy_ = bstack11llll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᲖ") if bstack11l1lll111l_opy_ == bstack11llll_opy_ (u"ࠫࡨࡧ࡬࡭ࠩᲗ") else bstack11llll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᲘ")
            bstack11ll111111l_opy_ = request.node.nodeid + (bstack11llll_opy_ (u"࠭ࠧᲙ") if bstack11l1lll111l_opy_ == bstack11llll_opy_ (u"ࠧࡤࡣ࡯ࡰࠬᲚ") else bstack11llll_opy_ (u"ࠨ࠯ࠪᲛ") + bstack11l1lll111l_opy_)
            bstack11ll1l11_opy_ = bstack1l11ll1l_opy_(_11llll11_opy_.get(bstack11ll111111l_opy_, None))
            if not bstack11ll1l11_opy_:
                continue
            for record in records:
                if bstack1l11l1l11ll_opy_(record.message):
                    continue
                bstack1ll11l11_opy_.append({
                    bstack11llll_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬᲜ"): bstack1l11l1ll111_opy_(record.created).isoformat() + bstack11llll_opy_ (u"ࠪ࡞ࠬᲝ"),
                    bstack11llll_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪᲞ"): record.levelname,
                    bstack11llll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭Ჟ"): record.message,
                    bstack11l1lll1lll_opy_: bstack11ll1l11_opy_
                })
        if len(bstack1ll11l11_opy_) > 0:
            bstack1lll11ll_opy_.bstack1ll1ll11_opy_(bstack1ll11l11_opy_)
    except Exception as err:
        print(bstack11llll_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡥࡤࡱࡱࡨࡤ࡬ࡩࡹࡶࡸࡶࡪࡀࠠࡼࡿࠪᲠ"), str(err))
def bstack11l1lll111_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack1l1lll1ll_opy_
    bstack1llll1l11l_opy_ = bstack1ll111l1_opy_(threading.current_thread(), bstack11llll_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫᲡ"), None) and bstack1ll111l1_opy_(
            threading.current_thread(), bstack11llll_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧᲢ"), None)
    bstack1llllllll1_opy_ = getattr(driver, bstack11llll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩᲣ"), None) != None and getattr(driver, bstack11llll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪᲤ"), None) == True
    if sequence == bstack11llll_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫᲥ") and driver != None:
      if not bstack1l1lll1ll_opy_ and bstack1l111lll11l_opy_() and bstack11llll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᲦ") in CONFIG and CONFIG[bstack11llll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭Ყ")] == True and bstack11ll11l1l1_opy_.bstack1111l1ll1_opy_(driver_command) and (bstack1llllllll1_opy_ or bstack1llll1l11l_opy_) and not bstack1l11l11111_opy_(args):
        try:
          bstack1l1lll1ll_opy_ = True
          logger.debug(bstack11llll_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡩࡳࡷࠦࡻࡾࠩᲨ").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack11llll_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵ࡫ࡲࡧࡱࡵࡱࠥࡹࡣࡢࡰࠣࡿࢂ࠭Ჩ").format(str(err)))
        bstack1l1lll1ll_opy_ = False
    if sequence == bstack11llll_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨᲪ"):
        if driver_command == bstack11llll_opy_ (u"ࠪࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠧᲫ"):
            bstack1lll11ll_opy_.bstack1ll1lll11_opy_({
                bstack11llll_opy_ (u"ࠫ࡮ࡳࡡࡨࡧࠪᲬ"): response[bstack11llll_opy_ (u"ࠬࡼࡡ࡭ࡷࡨࠫᲭ")],
                bstack11llll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭Ხ"): store[bstack11llll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫᲯ")]
            })
def bstack11l11l1l1l_opy_():
    global bstack1ll1111111_opy_
    bstack1ll1l1l1l1_opy_.bstack111l1ll11_opy_()
    logging.shutdown()
    bstack1lll11ll_opy_.bstack1l11lll1_opy_()
    for driver in bstack1ll1111111_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack11l1lllll11_opy_(*args):
    global bstack1ll1111111_opy_
    bstack1lll11ll_opy_.bstack1l11lll1_opy_()
    for driver in bstack1ll1111111_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1l11l1l11_opy_(self, *args, **kwargs):
    bstack1l11l1l1l_opy_ = bstack11l1l1lll1_opy_(self, *args, **kwargs)
    bstack1lll11ll_opy_.bstack1ll1ll1l1_opy_(self)
    return bstack1l11l1l1l_opy_
def bstack1l11lll1ll_opy_(framework_name):
    from bstack_utils.config import Config
    bstack1111l1l1_opy_ = Config.bstack111ll1ll_opy_()
    if bstack1111l1l1_opy_.get_property(bstack11llll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠ࡯ࡲࡨࡤࡩࡡ࡭࡮ࡨࡨࠬᲰ")):
        return
    bstack1111l1l1_opy_.set_property(bstack11llll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡰࡳࡩࡥࡣࡢ࡮࡯ࡩࡩ࠭Ჱ"), True)
    global bstack1l1l11llll_opy_
    global bstack11111l11l_opy_
    bstack1l1l11llll_opy_ = framework_name
    logger.info(bstack11llll111l_opy_.format(bstack1l1l11llll_opy_.split(bstack11llll_opy_ (u"ࠪ࠱ࠬᲲ"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1l111lll11l_opy_():
            Service.start = bstack1ll1lllll1_opy_
            Service.stop = bstack11llllllll_opy_
            webdriver.Remote.get = bstack11l1111l11_opy_
            webdriver.Remote.__init__ = bstack1l111ll1l1_opy_
            if not isinstance(os.getenv(bstack11llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔ࡞࡚ࡅࡔࡖࡢࡔࡆࡘࡁࡍࡎࡈࡐࠬᲳ")), str):
                return
            WebDriver.close = bstack11l1ll11l1_opy_
            WebDriver.quit = bstack11lllll11l_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        elif bstack1lll11ll_opy_.on():
            webdriver.Remote.__init__ = bstack1l11l1l11_opy_
        bstack11111l11l_opy_ = True
    except Exception as e:
        pass
    bstack1ll1l11l11_opy_()
    if os.environ.get(bstack11llll_opy_ (u"࡙ࠬࡅࡍࡇࡑࡍ࡚ࡓ࡟ࡐࡔࡢࡔࡑࡇ࡙ࡘࡔࡌࡋࡍ࡚࡟ࡊࡐࡖࡘࡆࡒࡌࡆࡆࠪᲴ")):
        bstack11111l11l_opy_ = eval(os.environ.get(bstack11llll_opy_ (u"࠭ࡓࡆࡎࡈࡒࡎ࡛ࡍࡠࡑࡕࡣࡕࡒࡁ࡚࡙ࡕࡍࡌࡎࡔࡠࡋࡑࡗ࡙ࡇࡌࡍࡇࡇࠫᲵ")))
    if not bstack11111l11l_opy_:
        bstack1ll1l1llll_opy_(bstack11llll_opy_ (u"ࠢࡑࡣࡦ࡯ࡦ࡭ࡥࡴࠢࡱࡳࡹࠦࡩ࡯ࡵࡷࡥࡱࡲࡥࡥࠤᲶ"), bstack11ll111ll_opy_)
    if bstack1l1l1ll11l_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._1lll1l111l_opy_ = bstack1l11lllll_opy_
        except Exception as e:
            logger.error(bstack1lll1l111_opy_.format(str(e)))
    if bstack11llll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨᲷ") in str(framework_name).lower():
        if not bstack1l111lll11l_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack11111l111_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack111l111ll_opy_
            Config.getoption = bstack1l11ll11l_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack1ll1l11lll_opy_
        except Exception as e:
            pass
def bstack11lllll11l_opy_(self):
    global bstack1l1l11llll_opy_
    global bstack1l1l11111_opy_
    global bstack1lll11ll11_opy_
    try:
        if bstack11llll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩᲸ") in bstack1l1l11llll_opy_ and self.session_id != None and bstack1ll111l1_opy_(threading.current_thread(), bstack11llll_opy_ (u"ࠪࡸࡪࡹࡴࡔࡶࡤࡸࡺࡹࠧᲹ"), bstack11llll_opy_ (u"ࠫࠬᲺ")) != bstack11llll_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭᲻"):
            bstack1l1ll1l1l_opy_ = bstack11llll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭᲼") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack11llll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᲽ")
            bstack1ll1l111l1_opy_(logger, True)
            if self != None:
                bstack11l11l11ll_opy_(self, bstack1l1ll1l1l_opy_, bstack11llll_opy_ (u"ࠨ࠮ࠣࠫᲾ").join(threading.current_thread().bstackTestErrorMessages))
        if not cli.bstack1llll11l1l1_opy_(bstack1llll1llll1_opy_):
            item = store.get(bstack11llll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭Ჿ"), None)
            if item is not None and bstack1ll111l1_opy_(threading.current_thread(), bstack11llll_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ᳀"), None):
                bstack11l11l11_opy_.bstack111l1ll1_opy_(self, bstack1l1lll1ll1_opy_, logger, item)
        threading.current_thread().testStatus = bstack11llll_opy_ (u"ࠫࠬ᳁")
    except Exception as e:
        logger.debug(bstack11llll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡱࡦࡸ࡫ࡪࡰࡪࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࠨ᳂") + str(e))
    bstack1lll11ll11_opy_(self)
    self.session_id = None
def bstack1l111ll1l1_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1l1l11111_opy_
    global bstack1ll11ll11l_opy_
    global bstack1l111l1l11_opy_
    global bstack1l1l11llll_opy_
    global bstack11l1l1lll1_opy_
    global bstack1ll1111111_opy_
    global bstack111l11l11_opy_
    global bstack11ll1111l1_opy_
    global bstack1l1lll1ll1_opy_
    CONFIG[bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨ᳃")] = str(bstack1l1l11llll_opy_) + str(__version__)
    command_executor = bstack1lll1l1l1l_opy_(bstack111l11l11_opy_, CONFIG)
    logger.debug(bstack1l111l1l1_opy_.format(command_executor))
    proxy = bstack11l1111ll_opy_(CONFIG, proxy)
    bstack1ll111l11_opy_ = 0
    try:
        if bstack1l111l1l11_opy_ is True:
            bstack1ll111l11_opy_ = int(os.environ.get(bstack11llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧ᳄")))
    except:
        bstack1ll111l11_opy_ = 0
    bstack11lll11lll_opy_ = bstack11lll1ll1_opy_(CONFIG, bstack1ll111l11_opy_)
    logger.debug(bstack1l11lll11_opy_.format(str(bstack11lll11lll_opy_)))
    bstack1l1lll1ll1_opy_ = CONFIG.get(bstack11llll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ᳅"))[bstack1ll111l11_opy_]
    if bstack11llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭᳆") in CONFIG and CONFIG[bstack11llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ᳇")]:
        bstack111ll1lll_opy_(bstack11lll11lll_opy_, bstack11ll1111l1_opy_)
    if bstack11111l11_opy_.bstack1l1llll11_opy_(CONFIG, bstack1ll111l11_opy_) and bstack11111l11_opy_.bstack11ll11ll11_opy_(bstack11lll11lll_opy_, options, desired_capabilities):
        threading.current_thread().a11yPlatform = True
        if not cli.bstack1llll11l1l1_opy_(bstack1llll1llll1_opy_):
            bstack11111l11_opy_.set_capabilities(bstack11lll11lll_opy_, CONFIG)
    if desired_capabilities:
        bstack11l11l11l_opy_ = bstack11111llll_opy_(desired_capabilities)
        bstack11l11l11l_opy_[bstack11llll_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫ᳈")] = bstack1ll11l1111_opy_(CONFIG)
        bstack111llllll_opy_ = bstack11lll1ll1_opy_(bstack11l11l11l_opy_)
        if bstack111llllll_opy_:
            bstack11lll11lll_opy_ = update(bstack111llllll_opy_, bstack11lll11lll_opy_)
        desired_capabilities = None
    if options:
        bstack1ll1l1l1ll_opy_(options, bstack11lll11lll_opy_)
    if not options:
        options = bstack1llll1ll1_opy_(bstack11lll11lll_opy_)
    if proxy and bstack111l1111l_opy_() >= version.parse(bstack11llll_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬ᳉")):
        options.proxy(proxy)
    if options and bstack111l1111l_opy_() >= version.parse(bstack11llll_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬ᳊")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack111l1111l_opy_() < version.parse(bstack11llll_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭᳋")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack11lll11lll_opy_)
    logger.info(bstack11ll1l1l1l_opy_)
    if bstack111l1111l_opy_() >= version.parse(bstack11llll_opy_ (u"ࠨ࠶࠱࠵࠵࠴࠰ࠨ᳌")):
        bstack11l1l1lll1_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack111l1111l_opy_() >= version.parse(bstack11llll_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨ᳍")):
        bstack11l1l1lll1_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack111l1111l_opy_() >= version.parse(bstack11llll_opy_ (u"ࠪ࠶࠳࠻࠳࠯࠲ࠪ᳎")):
        bstack11l1l1lll1_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    else:
        bstack11l1l1lll1_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive)
    try:
        bstack11ll11l1l_opy_ = bstack11llll_opy_ (u"ࠫࠬ᳏")
        if bstack111l1111l_opy_() >= version.parse(bstack11llll_opy_ (u"ࠬ࠺࠮࠱࠰࠳ࡦ࠶࠭᳐")):
            bstack11ll11l1l_opy_ = self.caps.get(bstack11llll_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨ᳑"))
        else:
            bstack11ll11l1l_opy_ = self.capabilities.get(bstack11llll_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢ᳒"))
        if bstack11ll11l1l_opy_:
            bstack1l1l1l11l1_opy_(bstack11ll11l1l_opy_)
            if bstack111l1111l_opy_() <= version.parse(bstack11llll_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨ᳓")):
                self.command_executor._url = bstack11llll_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱᳔ࠥ") + bstack111l11l11_opy_ + bstack11llll_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨ᳕ࠢ")
            else:
                self.command_executor._url = bstack11llll_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨ᳖") + bstack11ll11l1l_opy_ + bstack11llll_opy_ (u"ࠧ࠵ࡷࡥ࠱࡫ࡹࡧࠨ᳗")
            logger.debug(bstack1lllll111_opy_.format(bstack11ll11l1l_opy_))
        else:
            logger.debug(bstack1l1llll1ll_opy_.format(bstack11llll_opy_ (u"ࠨࡏࡱࡶ࡬ࡱࡦࡲࠠࡉࡷࡥࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪ᳘ࠢ")))
    except Exception as e:
        logger.debug(bstack1l1llll1ll_opy_.format(e))
    bstack1l1l11111_opy_ = self.session_id
    if bstack11llll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ᳙ࠧ") in bstack1l1l11llll_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack11llll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬ᳚"), None)
        if item:
            bstack11l1ll1l1l1_opy_ = getattr(item, bstack11llll_opy_ (u"ࠩࡢࡸࡪࡹࡴࡠࡥࡤࡷࡪࡥࡳࡵࡣࡵࡸࡪࡪࠧ᳛"), False)
            if not getattr(item, bstack11llll_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵ᳜ࠫ"), None) and bstack11l1ll1l1l1_opy_:
                setattr(store[bstack11llll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨ᳝")], bstack11llll_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ᳞࠭"), self)
        bstack1lll11ll_opy_.bstack1ll1ll1l1_opy_(self)
    bstack1ll1111111_opy_.append(self)
    if bstack11llll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴ᳟ࠩ") in CONFIG and bstack11llll_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ᳠") in CONFIG[bstack11llll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ᳡")][bstack1ll111l11_opy_]:
        bstack1ll11ll11l_opy_ = CONFIG[bstack11llll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷ᳢ࠬ")][bstack1ll111l11_opy_][bstack11llll_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ᳣")]
    logger.debug(bstack111l1ll1l_opy_.format(bstack1l1l11111_opy_))
def bstack11l1111l11_opy_(self, url):
    global bstack1l11llll1l_opy_
    global CONFIG
    try:
        bstack11llll11l_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1lll111ll_opy_.format(str(err)))
    try:
        bstack1l11llll1l_opy_(self, url)
    except Exception as e:
        try:
            parsed_error = str(e)
            if any(err_msg in parsed_error for err_msg in bstack1ll11l1lll_opy_):
                bstack11llll11l_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1lll111ll_opy_.format(str(err)))
        raise e
def bstack1llllll11_opy_(item, when):
    global bstack1l1l1l1l1l_opy_
    try:
        bstack1l1l1l1l1l_opy_(item, when)
    except Exception as e:
        pass
def bstack1ll1l11lll_opy_(item, call, rep):
    global bstack11lll1l11_opy_
    global bstack1ll1111111_opy_
    name = bstack11llll_opy_ (u"᳤ࠫࠬ")
    try:
        if rep.when == bstack11llll_opy_ (u"ࠬࡩࡡ࡭࡮᳥ࠪ"):
            bstack1l1l11111_opy_ = threading.current_thread().bstackSessionId
            bstack11l1lll1ll1_opy_ = item.config.getoption(bstack11llll_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ᳦"))
            try:
                if (str(bstack11l1lll1ll1_opy_).lower() != bstack11llll_opy_ (u"ࠧࡵࡴࡸࡩ᳧ࠬ")):
                    name = str(rep.nodeid)
                    bstack11l1lllll1_opy_ = bstack1l111lll11_opy_(bstack11llll_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦ᳨ࠩ"), name, bstack11llll_opy_ (u"ࠩࠪᳩ"), bstack11llll_opy_ (u"ࠪࠫᳪ"), bstack11llll_opy_ (u"ࠫࠬᳫ"), bstack11llll_opy_ (u"ࠬ࠭ᳬ"))
                    os.environ[bstack11llll_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙ࡥࡔࡆࡕࡗࡣࡓࡇࡍࡆ᳭ࠩ")] = name
                    for driver in bstack1ll1111111_opy_:
                        if bstack1l1l11111_opy_ == driver.session_id:
                            driver.execute_script(bstack11l1lllll1_opy_)
            except Exception as e:
                logger.debug(bstack11llll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠡࡨࡲࡶࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡶࡩࡸࡹࡩࡰࡰ࠽ࠤࢀࢃࠧᳮ").format(str(e)))
            try:
                bstack1ll11llll_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack11llll_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᳯ"):
                    status = bstack11llll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᳰ") if rep.outcome.lower() == bstack11llll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᳱ") else bstack11llll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᳲ")
                    reason = bstack11llll_opy_ (u"ࠬ࠭ᳳ")
                    if status == bstack11llll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭᳴"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack11llll_opy_ (u"ࠧࡪࡰࡩࡳࠬᳵ") if status == bstack11llll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᳶ") else bstack11llll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ᳷")
                    data = name + bstack11llll_opy_ (u"ࠪࠤࡵࡧࡳࡴࡧࡧࠥࠬ᳸") if status == bstack11llll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ᳹") else name + bstack11llll_opy_ (u"ࠬࠦࡦࡢ࡫࡯ࡩࡩࠧࠠࠨᳺ") + reason
                    bstack1llll1lll1_opy_ = bstack1l111lll11_opy_(bstack11llll_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨ᳻"), bstack11llll_opy_ (u"ࠧࠨ᳼"), bstack11llll_opy_ (u"ࠨࠩ᳽"), bstack11llll_opy_ (u"ࠩࠪ᳾"), level, data)
                    for driver in bstack1ll1111111_opy_:
                        if bstack1l1l11111_opy_ == driver.session_id:
                            driver.execute_script(bstack1llll1lll1_opy_)
            except Exception as e:
                logger.debug(bstack11llll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡤࡱࡱࡸࡪࡾࡴࠡࡨࡲࡶࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡶࡩࡸࡹࡩࡰࡰ࠽ࠤࢀࢃࠧ᳿").format(str(e)))
    except Exception as e:
        logger.debug(bstack11llll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡶࡤࡸࡪࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡦࡵࡷࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࢁࡽࠨᴀ").format(str(e)))
    bstack11lll1l11_opy_(item, call, rep)
notset = Notset()
def bstack1l11ll11l_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack11lll1111_opy_
    if str(name).lower() == bstack11llll_opy_ (u"ࠬࡪࡲࡪࡸࡨࡶࠬᴁ"):
        return bstack11llll_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠧᴂ")
    else:
        return bstack11lll1111_opy_(self, name, default, skip)
def bstack1l11lllll_opy_(self):
    global CONFIG
    global bstack11l1ll111_opy_
    try:
        proxy = bstack11l1lll1l_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack11llll_opy_ (u"ࠧ࠯ࡲࡤࡧࠬᴃ")):
                proxies = bstack11l1ll1l11_opy_(proxy, bstack1lll1l1l1l_opy_())
                if len(proxies) > 0:
                    protocol, bstack111ll1l1l_opy_ = proxies.popitem()
                    if bstack11llll_opy_ (u"ࠣ࠼࠲࠳ࠧᴄ") in bstack111ll1l1l_opy_:
                        return bstack111ll1l1l_opy_
                    else:
                        return bstack11llll_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥᴅ") + bstack111ll1l1l_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack11llll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡰࡳࡱࡻࡽࠥࡻࡲ࡭ࠢ࠽ࠤࢀࢃࠢᴆ").format(str(e)))
    return bstack11l1ll111_opy_(self)
def bstack1l1l1ll11l_opy_():
    return (bstack11llll_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧᴇ") in CONFIG or bstack11llll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩᴈ") in CONFIG) and bstack1l1ll11ll_opy_() and bstack111l1111l_opy_() >= version.parse(
        bstack1ll11llll1_opy_)
def bstack1l111l1ll_opy_(self,
               executablePath=None,
               channel=None,
               args=None,
               ignoreDefaultArgs=None,
               handleSIGINT=None,
               handleSIGTERM=None,
               handleSIGHUP=None,
               timeout=None,
               env=None,
               headless=None,
               devtools=None,
               proxy=None,
               downloadsPath=None,
               slowMo=None,
               tracesDir=None,
               chromiumSandbox=None,
               firefoxUserPrefs=None
               ):
    global CONFIG
    global bstack1ll11ll11l_opy_
    global bstack1l111l1l11_opy_
    global bstack1l1l11llll_opy_
    CONFIG[bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨᴉ")] = str(bstack1l1l11llll_opy_) + str(__version__)
    bstack1ll111l11_opy_ = 0
    try:
        if bstack1l111l1l11_opy_ is True:
            bstack1ll111l11_opy_ = int(os.environ.get(bstack11llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᴊ")))
    except:
        bstack1ll111l11_opy_ = 0
    CONFIG[bstack11llll_opy_ (u"ࠣ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢᴋ")] = True
    bstack11lll11lll_opy_ = bstack11lll1ll1_opy_(CONFIG, bstack1ll111l11_opy_)
    logger.debug(bstack1l11lll11_opy_.format(str(bstack11lll11lll_opy_)))
    if CONFIG.get(bstack11llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ᴌ")):
        bstack111ll1lll_opy_(bstack11lll11lll_opy_, bstack11ll1111l1_opy_)
    if bstack11llll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᴍ") in CONFIG and bstack11llll_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩᴎ") in CONFIG[bstack11llll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᴏ")][bstack1ll111l11_opy_]:
        bstack1ll11ll11l_opy_ = CONFIG[bstack11llll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᴐ")][bstack1ll111l11_opy_][bstack11llll_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬᴑ")]
    import urllib
    import json
    if bstack11llll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬᴒ") in CONFIG and str(CONFIG[bstack11llll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ᴓ")]).lower() != bstack11llll_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩᴔ"):
        bstack1l11l11ll_opy_ = bstack1l1ll1l11_opy_()
        bstack1llll11ll_opy_ = bstack1l11l11ll_opy_ + urllib.parse.quote(json.dumps(bstack11lll11lll_opy_))
    else:
        bstack1llll11ll_opy_ = bstack11llll_opy_ (u"ࠫࡼࡹࡳ࠻࠱࠲ࡧࡩࡶ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠿ࡤࡣࡳࡷࡂ࠭ᴕ") + urllib.parse.quote(json.dumps(bstack11lll11lll_opy_))
    browser = self.connect(bstack1llll11ll_opy_)
    return browser
def bstack1ll1l11l11_opy_():
    global bstack11111l11l_opy_
    global bstack1l1l11llll_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1l11ll1ll_opy_
        if not bstack1l111lll11l_opy_():
            global bstack1lll11l1l1_opy_
            if not bstack1lll11l1l1_opy_:
                from bstack_utils.helper import bstack1l11l111l_opy_, bstack1l1l1111l1_opy_
                bstack1lll11l1l1_opy_ = bstack1l11l111l_opy_()
                bstack1l1l1111l1_opy_(bstack1l1l11llll_opy_)
            BrowserType.connect = bstack1l11ll1ll_opy_
            return
        BrowserType.launch = bstack1l111l1ll_opy_
        bstack11111l11l_opy_ = True
    except Exception as e:
        pass
def bstack11l1llll11l_opy_():
    global CONFIG
    global bstack11l111lll_opy_
    global bstack111l11l11_opy_
    global bstack11ll1111l1_opy_
    global bstack1l111l1l11_opy_
    global bstack1ll1l1ll1l_opy_
    CONFIG = json.loads(os.environ.get(bstack11llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࠫᴖ")))
    bstack11l111lll_opy_ = eval(os.environ.get(bstack11llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧᴗ")))
    bstack111l11l11_opy_ = os.environ.get(bstack11llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡈࡖࡄࡢ࡙ࡗࡒࠧᴘ"))
    bstack1lll11l11l_opy_(CONFIG, bstack11l111lll_opy_)
    bstack1ll1l1ll1l_opy_ = bstack1ll1l1l1l1_opy_.bstack1l1111111l_opy_(CONFIG, bstack1ll1l1ll1l_opy_)
    if cli.bstack11llllll1_opy_():
        bstack1lll1ll11l_opy_.invoke(Events.CONNECT, bstack11lllll11_opy_())
        cli_context.platform_index = int(os.environ.get(bstack11llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᴙ"), bstack11llll_opy_ (u"ࠩ࠳ࠫᴚ")))
        cli.bstack1lll1ll111l_opy_(bstack1lll1l1l1l_opy_(bstack111l11l11_opy_, CONFIG), cli_context.platform_index, bstack1llll1ll1_opy_)
        cli.bstack1lll1ll1ll1_opy_()
        logger.warning(bstack11llll_opy_ (u"ࠥࡇࡑࡏࠠࡪࡵࠣࡥࡨࡺࡩࡷࡧࠣࡪࡴࡸࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸ࠾ࠤᴛ") + str(cli_context.platform_index) + bstack11llll_opy_ (u"ࠦࠧᴜ"))
        return # skip all existing bstack11l1ll1ll11_opy_
    global bstack11l1l1lll1_opy_
    global bstack1lll11ll11_opy_
    global bstack111l11lll_opy_
    global bstack1ll1llll11_opy_
    global bstack1l1111lll_opy_
    global bstack11ll1l1l11_opy_
    global bstack1ll1111l1l_opy_
    global bstack1l11llll1l_opy_
    global bstack11l1ll111_opy_
    global bstack11lll1111_opy_
    global bstack1l1l1l1l1l_opy_
    global bstack11lll1l11_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack11l1l1lll1_opy_ = webdriver.Remote.__init__
        bstack1lll11ll11_opy_ = WebDriver.quit
        bstack1ll1111l1l_opy_ = WebDriver.close
        bstack1l11llll1l_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack11llll_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨᴝ") in CONFIG or bstack11llll_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪᴞ") in CONFIG) and bstack1l1ll11ll_opy_():
        if bstack111l1111l_opy_() < version.parse(bstack1ll11llll1_opy_):
            logger.error(bstack1ll1l1ll1_opy_.format(bstack111l1111l_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                bstack11l1ll111_opy_ = RemoteConnection._1lll1l111l_opy_
            except Exception as e:
                logger.error(bstack1lll1l111_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack11lll1111_opy_ = Config.getoption
        from _pytest import runner
        bstack1l1l1l1l1l_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack1111l11l_opy_)
    try:
        from pytest_bdd import reporting
        bstack11lll1l11_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack11llll_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺ࡯ࠡࡴࡸࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࡳࠨᴟ"))
    bstack11ll1111l1_opy_ = CONFIG.get(bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬᴠ"), {}).get(bstack11llll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᴡ"))
    bstack1l111l1l11_opy_ = True
    bstack1l11lll1ll_opy_(bstack11l1111l1_opy_)
if (bstack1l11ll1l1ll_opy_()):
    bstack11l1llll11l_opy_()
@bstack1l11llll_opy_(class_method=False)
def bstack11ll111l111_opy_(hook_name, event, bstack1l1llll1lll_opy_=None):
    if cli.bstack1llll11l1l1_opy_(bstack1llll1llll1_opy_):
        return # skip all existing bstack11l1ll1ll11_opy_
    if hook_name not in [bstack11llll_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࠫᴢ"), bstack11llll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨᴣ"), bstack11llll_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫᴤ"), bstack11llll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨᴥ"), bstack11llll_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬᴦ"), bstack11llll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩᴧ"), bstack11llll_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠨᴨ"), bstack11llll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬᴩ")]:
        return
    node = store[bstack11llll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨᴪ")]
    if hook_name in [bstack11llll_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫᴫ"), bstack11llll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨᴬ")]:
        node = store[bstack11llll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠ࡯ࡲࡨࡺࡲࡥࡠ࡫ࡷࡩࡲ࠭ᴭ")]
    elif hook_name in [bstack11llll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭ᴮ"), bstack11llll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠪᴯ")]:
        node = store[bstack11llll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡨࡲࡡࡴࡵࡢ࡭ࡹ࡫࡭ࠨᴰ")]
    if event == bstack11llll_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫᴱ"):
        hook_type = bstack1l1l1ll111l_opy_(hook_name)
        uuid = uuid4().__str__()
        bstack1l11l11l_opy_ = {
            bstack11llll_opy_ (u"ࠬࡻࡵࡪࡦࠪᴲ"): uuid,
            bstack11llll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᴳ"): bstack1l111ll1_opy_(),
            bstack11llll_opy_ (u"ࠧࡵࡻࡳࡩࠬᴴ"): bstack11llll_opy_ (u"ࠨࡪࡲࡳࡰ࠭ᴵ"),
            bstack11llll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬᴶ"): hook_type,
            bstack11llll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭ᴷ"): hook_name
        }
        store[bstack11llll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᴸ")].append(uuid)
        bstack11l1lll1l11_opy_ = node.nodeid
        if hook_type == bstack11llll_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪᴹ"):
            if not _11llll11_opy_.get(bstack11l1lll1l11_opy_, None):
                _11llll11_opy_[bstack11l1lll1l11_opy_] = {bstack11llll_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᴺ"): []}
            _11llll11_opy_[bstack11l1lll1l11_opy_][bstack11llll_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᴻ")].append(bstack1l11l11l_opy_[bstack11llll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᴼ")])
        _11llll11_opy_[bstack11l1lll1l11_opy_ + bstack11llll_opy_ (u"ࠩ࠰ࠫᴽ") + hook_name] = bstack1l11l11l_opy_
        bstack11l1lllllll_opy_(node, bstack1l11l11l_opy_, bstack11llll_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᴾ"))
    elif event == bstack11llll_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪᴿ"):
        bstack1l1111ll_opy_ = node.nodeid + bstack11llll_opy_ (u"ࠬ࠳ࠧᵀ") + hook_name
        _11llll11_opy_[bstack1l1111ll_opy_][bstack11llll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᵁ")] = bstack1l111ll1_opy_()
        bstack11ll11111ll_opy_(_11llll11_opy_[bstack1l1111ll_opy_][bstack11llll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᵂ")])
        bstack11l1lllllll_opy_(node, _11llll11_opy_[bstack1l1111ll_opy_], bstack11llll_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᵃ"), bstack11l1ll1lll1_opy_=bstack1l1llll1lll_opy_)
def bstack11ll1111ll1_opy_():
    global bstack11l1lll11ll_opy_
    if bstack1l1lll1l1l_opy_():
        bstack11l1lll11ll_opy_ = bstack11llll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭ᵄ")
    else:
        bstack11l1lll11ll_opy_ = bstack11llll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪᵅ")
@bstack1lll11ll_opy_.bstack11ll11ll1l1_opy_
def bstack11l1lll1l1l_opy_():
    if cli.bstack1llll11l1l1_opy_(bstack1llll1llll1_opy_):
        return # skip all existing bstack11l1ll1ll11_opy_
    bstack11ll1111ll1_opy_()
    if bstack1l1ll11ll_opy_():
        bstack1l1llll11l_opy_(bstack11l1lll111_opy_)
    try:
        bstack1l1ll1ll11l_opy_(bstack11ll111l111_opy_)
    except Exception as e:
        logger.debug(bstack11llll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡴࡵ࡫ࡴࠢࡳࡥࡹࡩࡨ࠻ࠢࡾࢁࠧᵆ").format(e))
bstack11l1lll1l1l_opy_()