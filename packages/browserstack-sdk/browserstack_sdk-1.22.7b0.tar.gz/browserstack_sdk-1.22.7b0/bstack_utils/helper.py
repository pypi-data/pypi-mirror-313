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
import datetime
import json
import os
import platform
import re
import subprocess
import traceback
import tempfile
import multiprocessing
import threading
import sys
import logging
from math import ceil
import urllib
from urllib.parse import urlparse
import copy
import zipfile
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import (bstack1l1ll111l1l_opy_, bstack11l1llll11_opy_, bstack11ll11lll_opy_, bstack1llll111ll_opy_,
                                    bstack1l1ll11l11l_opy_, bstack1l1ll111l11_opy_, bstack1l1ll11l1l1_opy_, bstack1l1ll11ll1l_opy_)
from bstack_utils.messages import bstack1lll1ll111_opy_, bstack1lll1l111_opy_
from bstack_utils.proxy import bstack1ll111111_opy_, bstack11l1lll1l_opy_
from bstack_utils.constants import *
from bstack_utils import bstack1ll1l1l1l1_opy_
from browserstack_sdk._version import __version__
bstack1111l1l1_opy_ = Config.bstack111ll1ll_opy_()
logger = bstack1ll1l1l1l1_opy_.get_logger(__name__, bstack1ll1l1l1l1_opy_.bstack1lllllll111_opy_())
def bstack1l11lll111l_opy_(config):
    return config[bstack11llll_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧᘖ")]
def bstack1l11llll1l1_opy_(config):
    return config[bstack11llll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩᘗ")]
def bstack1l111llll1_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack1l111l11ll1_opy_(obj):
    values = []
    bstack1l111l1lll1_opy_ = re.compile(bstack11llll_opy_ (u"ࡲࠣࡠࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࡜ࡥ࠭ࠧࠦᘘ"), re.I)
    for key in obj.keys():
        if bstack1l111l1lll1_opy_.match(key):
            values.append(obj[key])
    return values
def bstack1l111l1l11l_opy_(config):
    tags = []
    tags.extend(bstack1l111l11ll1_opy_(os.environ))
    tags.extend(bstack1l111l11ll1_opy_(config))
    return tags
def bstack1l11lll1l1l_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack1l111lll1l1_opy_(bstack1l11ll11l1l_opy_):
    if not bstack1l11ll11l1l_opy_:
        return bstack11llll_opy_ (u"ࠨࠩᘙ")
    return bstack11llll_opy_ (u"ࠤࡾࢁࠥ࠮ࡻࡾࠫࠥᘚ").format(bstack1l11ll11l1l_opy_.name, bstack1l11ll11l1l_opy_.email)
def bstack1l11ll1ll1l_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack1l11l11111l_opy_ = repo.common_dir
        info = {
            bstack11llll_opy_ (u"ࠥࡷ࡭ࡧࠢᘛ"): repo.head.commit.hexsha,
            bstack11llll_opy_ (u"ࠦࡸ࡮࡯ࡳࡶࡢࡷ࡭ࡧࠢᘜ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack11llll_opy_ (u"ࠧࡨࡲࡢࡰࡦ࡬ࠧᘝ"): repo.active_branch.name,
            bstack11llll_opy_ (u"ࠨࡴࡢࡩࠥᘞ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack11llll_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺࡴࡦࡴࠥᘟ"): bstack1l111lll1l1_opy_(repo.head.commit.committer),
            bstack11llll_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡵࡧࡵࡣࡩࡧࡴࡦࠤᘠ"): repo.head.commit.committed_datetime.isoformat(),
            bstack11llll_opy_ (u"ࠤࡤࡹࡹ࡮࡯ࡳࠤᘡ"): bstack1l111lll1l1_opy_(repo.head.commit.author),
            bstack11llll_opy_ (u"ࠥࡥࡺࡺࡨࡰࡴࡢࡨࡦࡺࡥࠣᘢ"): repo.head.commit.authored_datetime.isoformat(),
            bstack11llll_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡣࡲ࡫ࡳࡴࡣࡪࡩࠧᘣ"): repo.head.commit.message,
            bstack11llll_opy_ (u"ࠧࡸ࡯ࡰࡶࠥᘤ"): repo.git.rev_parse(bstack11llll_opy_ (u"ࠨ࠭࠮ࡵ࡫ࡳࡼ࠳ࡴࡰࡲ࡯ࡩࡻ࡫࡬ࠣᘥ")),
            bstack11llll_opy_ (u"ࠢࡤࡱࡰࡱࡴࡴ࡟ࡨ࡫ࡷࡣࡩ࡯ࡲࠣᘦ"): bstack1l11l11111l_opy_,
            bstack11llll_opy_ (u"ࠣࡹࡲࡶࡰࡺࡲࡦࡧࡢ࡫࡮ࡺ࡟ࡥ࡫ࡵࠦᘧ"): subprocess.check_output([bstack11llll_opy_ (u"ࠤࡪ࡭ࡹࠨᘨ"), bstack11llll_opy_ (u"ࠥࡶࡪࡼ࠭ࡱࡣࡵࡷࡪࠨᘩ"), bstack11llll_opy_ (u"ࠦ࠲࠳ࡧࡪࡶ࠰ࡧࡴࡳ࡭ࡰࡰ࠰ࡨ࡮ࡸࠢᘪ")]).strip().decode(
                bstack11llll_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫᘫ")),
            bstack11llll_opy_ (u"ࠨ࡬ࡢࡵࡷࡣࡹࡧࡧࠣᘬ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack11llll_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺࡳࡠࡵ࡬ࡲࡨ࡫࡟࡭ࡣࡶࡸࡤࡺࡡࡨࠤᘭ"): repo.git.rev_list(
                bstack11llll_opy_ (u"ࠣࡽࢀ࠲࠳ࢁࡽࠣᘮ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack1l11l1l1l1l_opy_ = []
        for remote in remotes:
            bstack1l11l1111l1_opy_ = {
                bstack11llll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᘯ"): remote.name,
                bstack11llll_opy_ (u"ࠥࡹࡷࡲࠢᘰ"): remote.url,
            }
            bstack1l11l1l1l1l_opy_.append(bstack1l11l1111l1_opy_)
        bstack1l111ll111l_opy_ = {
            bstack11llll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᘱ"): bstack11llll_opy_ (u"ࠧ࡭ࡩࡵࠤᘲ"),
            **info,
            bstack11llll_opy_ (u"ࠨࡲࡦ࡯ࡲࡸࡪࡹࠢᘳ"): bstack1l11l1l1l1l_opy_
        }
        bstack1l111ll111l_opy_ = bstack1l11ll1lll1_opy_(bstack1l111ll111l_opy_)
        return bstack1l111ll111l_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack11llll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡰࡲࡸࡰࡦࡺࡩ࡯ࡩࠣࡋ࡮ࡺࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡺ࡭ࡹ࡮ࠠࡦࡴࡵࡳࡷࡀࠠࡼࡿࠥᘴ").format(err))
        return {}
def bstack1l11ll1lll1_opy_(bstack1l111ll111l_opy_):
    bstack1l11l111l1l_opy_ = bstack1l11lllll1l_opy_(bstack1l111ll111l_opy_)
    if bstack1l11l111l1l_opy_ and bstack1l11l111l1l_opy_ > bstack1l1ll11l11l_opy_:
        bstack1l11l1111ll_opy_ = bstack1l11l111l1l_opy_ - bstack1l1ll11l11l_opy_
        bstack1l11l11l1ll_opy_ = bstack1l11l1l1ll1_opy_(bstack1l111ll111l_opy_[bstack11llll_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡠ࡯ࡨࡷࡸࡧࡧࡦࠤᘵ")], bstack1l11l1111ll_opy_)
        bstack1l111ll111l_opy_[bstack11llll_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡡࡰࡩࡸࡹࡡࡨࡧࠥᘶ")] = bstack1l11l11l1ll_opy_
        logger.info(bstack11llll_opy_ (u"ࠥࡘ࡭࡫ࠠࡤࡱࡰࡱ࡮ࡺࠠࡩࡣࡶࠤࡧ࡫ࡥ࡯ࠢࡷࡶࡺࡴࡣࡢࡶࡨࡨ࠳ࠦࡓࡪࡼࡨࠤࡴ࡬ࠠࡤࡱࡰࡱ࡮ࡺࠠࡢࡨࡷࡩࡷࠦࡴࡳࡷࡱࡧࡦࡺࡩࡰࡰࠣ࡭ࡸࠦࡻࡾࠢࡎࡆࠧᘷ")
                    .format(bstack1l11lllll1l_opy_(bstack1l111ll111l_opy_) / 1024))
    return bstack1l111ll111l_opy_
def bstack1l11lllll1l_opy_(json_data):
    try:
        if json_data:
            bstack1l11l111111_opy_ = json.dumps(json_data)
            bstack1l11lll1l11_opy_ = sys.getsizeof(bstack1l11l111111_opy_)
            return bstack1l11lll1l11_opy_
    except Exception as e:
        logger.debug(bstack11llll_opy_ (u"ࠦࡘࡵ࡭ࡦࡶ࡫࡭ࡳ࡭ࠠࡸࡧࡱࡸࠥࡽࡲࡰࡰࡪࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡦࡲࡣࡶ࡮ࡤࡸ࡮ࡴࡧࠡࡵ࡬ࡾࡪࠦ࡯ࡧࠢࡍࡗࡔࡔࠠࡰࡤ࡭ࡩࡨࡺ࠺ࠡࡽࢀࠦᘸ").format(e))
    return -1
def bstack1l11l1l1ll1_opy_(field, bstack1l11lll1lll_opy_):
    try:
        bstack1l111ll1l11_opy_ = len(bytes(bstack1l1ll111l11_opy_, bstack11llll_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫᘹ")))
        bstack1l111l1l1l1_opy_ = bytes(field, bstack11llll_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬᘺ"))
        bstack1l11l1l1l11_opy_ = len(bstack1l111l1l1l1_opy_)
        bstack1l111lll111_opy_ = ceil(bstack1l11l1l1l11_opy_ - bstack1l11lll1lll_opy_ - bstack1l111ll1l11_opy_)
        if bstack1l111lll111_opy_ > 0:
            bstack1l111l1llll_opy_ = bstack1l111l1l1l1_opy_[:bstack1l111lll111_opy_].decode(bstack11llll_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ᘻ"), errors=bstack11llll_opy_ (u"ࠨ࡫ࡪࡲࡴࡸࡥࠨᘼ")) + bstack1l1ll111l11_opy_
            return bstack1l111l1llll_opy_
    except Exception as e:
        logger.debug(bstack11llll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡵࡴࡸࡲࡨࡧࡴࡪࡰࡪࠤ࡫࡯ࡥ࡭ࡦ࠯ࠤࡳࡵࡴࡩ࡫ࡱ࡫ࠥࡽࡡࡴࠢࡷࡶࡺࡴࡣࡢࡶࡨࡨࠥ࡮ࡥࡳࡧ࠽ࠤࢀࢃࠢᘽ").format(e))
    return field
def bstack1l1111ll1l_opy_():
    env = os.environ
    if (bstack11llll_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣ࡚ࡘࡌࠣᘾ") in env and len(env[bstack11llll_opy_ (u"ࠦࡏࡋࡎࡌࡋࡑࡗࡤ࡛ࡒࡍࠤᘿ")]) > 0) or (
            bstack11llll_opy_ (u"ࠧࡐࡅࡏࡍࡌࡒࡘࡥࡈࡐࡏࡈࠦᙀ") in env and len(env[bstack11llll_opy_ (u"ࠨࡊࡆࡐࡎࡍࡓ࡙࡟ࡉࡑࡐࡉࠧᙁ")]) > 0):
        return {
            bstack11llll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᙂ"): bstack11llll_opy_ (u"ࠣࡌࡨࡲࡰ࡯࡮ࡴࠤᙃ"),
            bstack11llll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᙄ"): env.get(bstack11llll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨᙅ")),
            bstack11llll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᙆ"): env.get(bstack11llll_opy_ (u"ࠧࡐࡏࡃࡡࡑࡅࡒࡋࠢᙇ")),
            bstack11llll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᙈ"): env.get(bstack11llll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨᙉ"))
        }
    if env.get(bstack11llll_opy_ (u"ࠣࡅࡌࠦᙊ")) == bstack11llll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢᙋ") and bstack1lll1lll11_opy_(env.get(bstack11llll_opy_ (u"ࠥࡇࡎࡘࡃࡍࡇࡆࡍࠧᙌ"))):
        return {
            bstack11llll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᙍ"): bstack11llll_opy_ (u"ࠧࡉࡩࡳࡥ࡯ࡩࡈࡏࠢᙎ"),
            bstack11llll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᙏ"): env.get(bstack11llll_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥᙐ")),
            bstack11llll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᙑ"): env.get(bstack11llll_opy_ (u"ࠤࡆࡍࡗࡉࡌࡆࡡࡍࡓࡇࠨᙒ")),
            bstack11llll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᙓ"): env.get(bstack11llll_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࠢᙔ"))
        }
    if env.get(bstack11llll_opy_ (u"ࠧࡉࡉࠣᙕ")) == bstack11llll_opy_ (u"ࠨࡴࡳࡷࡨࠦᙖ") and bstack1lll1lll11_opy_(env.get(bstack11llll_opy_ (u"ࠢࡕࡔࡄ࡚ࡎ࡙ࠢᙗ"))):
        return {
            bstack11llll_opy_ (u"ࠣࡰࡤࡱࡪࠨᙘ"): bstack11llll_opy_ (u"ࠤࡗࡶࡦࡼࡩࡴࠢࡆࡍࠧᙙ"),
            bstack11llll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᙚ"): env.get(bstack11llll_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࡣࡇ࡛ࡉࡍࡆࡢ࡛ࡊࡈ࡟ࡖࡔࡏࠦᙛ")),
            bstack11llll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᙜ"): env.get(bstack11llll_opy_ (u"ࠨࡔࡓࡃ࡙ࡍࡘࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣᙝ")),
            bstack11llll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᙞ"): env.get(bstack11llll_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᙟ"))
        }
    if env.get(bstack11llll_opy_ (u"ࠤࡆࡍࠧᙠ")) == bstack11llll_opy_ (u"ࠥࡸࡷࡻࡥࠣᙡ") and env.get(bstack11llll_opy_ (u"ࠦࡈࡏ࡟ࡏࡃࡐࡉࠧᙢ")) == bstack11llll_opy_ (u"ࠧࡩ࡯ࡥࡧࡶ࡬࡮ࡶࠢᙣ"):
        return {
            bstack11llll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᙤ"): bstack11llll_opy_ (u"ࠢࡄࡱࡧࡩࡸ࡮ࡩࡱࠤᙥ"),
            bstack11llll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᙦ"): None,
            bstack11llll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᙧ"): None,
            bstack11llll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᙨ"): None
        }
    if env.get(bstack11llll_opy_ (u"ࠦࡇࡏࡔࡃࡗࡆࡏࡊ࡚࡟ࡃࡔࡄࡒࡈࡎࠢᙩ")) and env.get(bstack11llll_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡅࡒࡑࡒࡏࡔࠣᙪ")):
        return {
            bstack11llll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᙫ"): bstack11llll_opy_ (u"ࠢࡃ࡫ࡷࡦࡺࡩ࡫ࡦࡶࠥᙬ"),
            bstack11llll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᙭"): env.get(bstack11llll_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡍࡉࡕࡡࡋࡘ࡙ࡖ࡟ࡐࡔࡌࡋࡎࡔࠢ᙮")),
            bstack11llll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᙯ"): None,
            bstack11llll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᙰ"): env.get(bstack11llll_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᙱ"))
        }
    if env.get(bstack11llll_opy_ (u"ࠨࡃࡊࠤᙲ")) == bstack11llll_opy_ (u"ࠢࡵࡴࡸࡩࠧᙳ") and bstack1lll1lll11_opy_(env.get(bstack11llll_opy_ (u"ࠣࡆࡕࡓࡓࡋࠢᙴ"))):
        return {
            bstack11llll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᙵ"): bstack11llll_opy_ (u"ࠥࡈࡷࡵ࡮ࡦࠤᙶ"),
            bstack11llll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᙷ"): env.get(bstack11llll_opy_ (u"ࠧࡊࡒࡐࡐࡈࡣࡇ࡛ࡉࡍࡆࡢࡐࡎࡔࡋࠣᙸ")),
            bstack11llll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᙹ"): None,
            bstack11llll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᙺ"): env.get(bstack11llll_opy_ (u"ࠣࡆࡕࡓࡓࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨᙻ"))
        }
    if env.get(bstack11llll_opy_ (u"ࠤࡆࡍࠧᙼ")) == bstack11llll_opy_ (u"ࠥࡸࡷࡻࡥࠣᙽ") and bstack1lll1lll11_opy_(env.get(bstack11llll_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋࠢᙾ"))):
        return {
            bstack11llll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᙿ"): bstack11llll_opy_ (u"ࠨࡓࡦ࡯ࡤࡴ࡭ࡵࡲࡦࠤ "),
            bstack11llll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᚁ"): env.get(bstack11llll_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࡣࡔࡘࡇࡂࡐࡌ࡞ࡆ࡚ࡉࡐࡐࡢ࡙ࡗࡒࠢᚂ")),
            bstack11llll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᚃ"): env.get(bstack11llll_opy_ (u"ࠥࡗࡊࡓࡁࡑࡊࡒࡖࡊࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣᚄ")),
            bstack11llll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᚅ"): env.get(bstack11llll_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࡠࡌࡒࡆࡤࡏࡄࠣᚆ"))
        }
    if env.get(bstack11llll_opy_ (u"ࠨࡃࡊࠤᚇ")) == bstack11llll_opy_ (u"ࠢࡵࡴࡸࡩࠧᚈ") and bstack1lll1lll11_opy_(env.get(bstack11llll_opy_ (u"ࠣࡉࡌࡘࡑࡇࡂࡠࡅࡌࠦᚉ"))):
        return {
            bstack11llll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᚊ"): bstack11llll_opy_ (u"ࠥࡋ࡮ࡺࡌࡢࡤࠥᚋ"),
            bstack11llll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᚌ"): env.get(bstack11llll_opy_ (u"ࠧࡉࡉࡠࡌࡒࡆࡤ࡛ࡒࡍࠤᚍ")),
            bstack11llll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᚎ"): env.get(bstack11llll_opy_ (u"ࠢࡄࡋࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᚏ")),
            bstack11llll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᚐ"): env.get(bstack11llll_opy_ (u"ࠤࡆࡍࡤࡐࡏࡃࡡࡌࡈࠧᚑ"))
        }
    if env.get(bstack11llll_opy_ (u"ࠥࡇࡎࠨᚒ")) == bstack11llll_opy_ (u"ࠦࡹࡸࡵࡦࠤᚓ") and bstack1lll1lll11_opy_(env.get(bstack11llll_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࠣᚔ"))):
        return {
            bstack11llll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᚕ"): bstack11llll_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡱࡩࡵࡧࠥᚖ"),
            bstack11llll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᚗ"): env.get(bstack11llll_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣᚘ")),
            bstack11llll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᚙ"): env.get(bstack11llll_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡍࡃࡅࡉࡑࠨᚚ")) or env.get(bstack11llll_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡒࡆࡓࡅࠣ᚛")),
            bstack11llll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ᚜"): env.get(bstack11llll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤ᚝"))
        }
    if bstack1lll1lll11_opy_(env.get(bstack11llll_opy_ (u"ࠣࡖࡉࡣࡇ࡛ࡉࡍࡆࠥ᚞"))):
        return {
            bstack11llll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᚟"): bstack11llll_opy_ (u"࡚ࠥ࡮ࡹࡵࡢ࡮ࠣࡗࡹࡻࡤࡪࡱࠣࡘࡪࡧ࡭ࠡࡕࡨࡶࡻ࡯ࡣࡦࡵࠥᚠ"),
            bstack11llll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᚡ"): bstack11llll_opy_ (u"ࠧࢁࡽࡼࡿࠥᚢ").format(env.get(bstack11llll_opy_ (u"࠭ࡓ࡚ࡕࡗࡉࡒࡥࡔࡆࡃࡐࡊࡔ࡛ࡎࡅࡃࡗࡍࡔࡔࡓࡆࡔ࡙ࡉࡗ࡛ࡒࡊࠩᚣ")), env.get(bstack11llll_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡕࡘࡏࡋࡇࡆࡘࡎࡊࠧᚤ"))),
            bstack11llll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᚥ"): env.get(bstack11llll_opy_ (u"ࠤࡖ࡝ࡘ࡚ࡅࡎࡡࡇࡉࡋࡏࡎࡊࡖࡌࡓࡓࡏࡄࠣᚦ")),
            bstack11llll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᚧ"): env.get(bstack11llll_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠦᚨ"))
        }
    if bstack1lll1lll11_opy_(env.get(bstack11llll_opy_ (u"ࠧࡇࡐࡑࡘࡈ࡝ࡔࡘࠢᚩ"))):
        return {
            bstack11llll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᚪ"): bstack11llll_opy_ (u"ࠢࡂࡲࡳࡺࡪࡿ࡯ࡳࠤᚫ"),
            bstack11llll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᚬ"): bstack11llll_opy_ (u"ࠤࡾࢁ࠴ࡶࡲࡰ࡬ࡨࡧࡹ࠵ࡻࡾ࠱ࡾࢁ࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽࠣᚭ").format(env.get(bstack11llll_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤ࡛ࡒࡍࠩᚮ")), env.get(bstack11llll_opy_ (u"ࠫࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡁࡄࡅࡒ࡙ࡓ࡚࡟ࡏࡃࡐࡉࠬᚯ")), env.get(bstack11llll_opy_ (u"ࠬࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡑࡔࡒࡎࡊࡉࡔࡠࡕࡏ࡙ࡌ࠭ᚰ")), env.get(bstack11llll_opy_ (u"࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪᚱ"))),
            bstack11llll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᚲ"): env.get(bstack11llll_opy_ (u"ࠣࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᚳ")),
            bstack11llll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᚴ"): env.get(bstack11llll_opy_ (u"ࠥࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᚵ"))
        }
    if env.get(bstack11llll_opy_ (u"ࠦࡆࡠࡕࡓࡇࡢࡌ࡙࡚ࡐࡠࡗࡖࡉࡗࡥࡁࡈࡇࡑࡘࠧᚶ")) and env.get(bstack11llll_opy_ (u"࡚ࠧࡆࡠࡄࡘࡍࡑࡊࠢᚷ")):
        return {
            bstack11llll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᚸ"): bstack11llll_opy_ (u"ࠢࡂࡼࡸࡶࡪࠦࡃࡊࠤᚹ"),
            bstack11llll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᚺ"): bstack11llll_opy_ (u"ࠤࡾࢁࢀࢃ࠯ࡠࡤࡸ࡭ࡱࡪ࠯ࡳࡧࡶࡹࡱࡺࡳࡀࡤࡸ࡭ࡱࡪࡉࡥ࠿ࡾࢁࠧᚻ").format(env.get(bstack11llll_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡇࡑࡘࡒࡉࡇࡔࡊࡑࡑࡗࡊࡘࡖࡆࡔࡘࡖࡎ࠭ᚼ")), env.get(bstack11llll_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡒࡕࡓࡏࡋࡃࡕࠩᚽ")), env.get(bstack11llll_opy_ (u"ࠬࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠬᚾ"))),
            bstack11llll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᚿ"): env.get(bstack11llll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠢᛀ")),
            bstack11llll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᛁ"): env.get(bstack11llll_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠤᛂ"))
        }
    if any([env.get(bstack11llll_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣᛃ")), env.get(bstack11llll_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡓࡇࡖࡓࡑ࡜ࡅࡅࡡࡖࡓ࡚ࡘࡃࡆࡡ࡙ࡉࡗ࡙ࡉࡐࡐࠥᛄ")), env.get(bstack11llll_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡕࡒ࡙ࡗࡉࡅࡠࡘࡈࡖࡘࡏࡏࡏࠤᛅ"))]):
        return {
            bstack11llll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᛆ"): bstack11llll_opy_ (u"ࠢࡂ࡙ࡖࠤࡈࡵࡤࡦࡄࡸ࡭ࡱࡪࠢᛇ"),
            bstack11llll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᛈ"): env.get(bstack11llll_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡖࡕࡃࡎࡌࡇࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣᛉ")),
            bstack11llll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᛊ"): env.get(bstack11llll_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤᛋ")),
            bstack11llll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᛌ"): env.get(bstack11llll_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦᛍ"))
        }
    if env.get(bstack11llll_opy_ (u"ࠢࡣࡣࡰࡦࡴࡵ࡟ࡣࡷ࡬ࡰࡩࡔࡵ࡮ࡤࡨࡶࠧᛎ")):
        return {
            bstack11llll_opy_ (u"ࠣࡰࡤࡱࡪࠨᛏ"): bstack11llll_opy_ (u"ࠤࡅࡥࡲࡨ࡯ࡰࠤᛐ"),
            bstack11llll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᛑ"): env.get(bstack11llll_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡧࡻࡩ࡭ࡦࡕࡩࡸࡻ࡬ࡵࡵࡘࡶࡱࠨᛒ")),
            bstack11llll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᛓ"): env.get(bstack11llll_opy_ (u"ࠨࡢࡢ࡯ࡥࡳࡴࡥࡳࡩࡱࡵࡸࡏࡵࡢࡏࡣࡰࡩࠧᛔ")),
            bstack11llll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᛕ"): env.get(bstack11llll_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡤࡸ࡭ࡱࡪࡎࡶ࡯ࡥࡩࡷࠨᛖ"))
        }
    if env.get(bstack11llll_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࠥᛗ")) or env.get(bstack11llll_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡒࡇࡉࡏࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡘ࡚ࡁࡓࡖࡈࡈࠧᛘ")):
        return {
            bstack11llll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᛙ"): bstack11llll_opy_ (u"ࠧ࡝ࡥࡳࡥ࡮ࡩࡷࠨᛚ"),
            bstack11llll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᛛ"): env.get(bstack11llll_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦᛜ")),
            bstack11llll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᛝ"): bstack11llll_opy_ (u"ࠤࡐࡥ࡮ࡴࠠࡑ࡫ࡳࡩࡱ࡯࡮ࡦࠤᛞ") if env.get(bstack11llll_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡒࡇࡉࡏࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡘ࡚ࡁࡓࡖࡈࡈࠧᛟ")) else None,
            bstack11llll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᛠ"): env.get(bstack11llll_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࡥࡇࡊࡖࡢࡇࡔࡓࡍࡊࡖࠥᛡ"))
        }
    if any([env.get(bstack11llll_opy_ (u"ࠨࡇࡄࡒࡢࡔࡗࡕࡊࡆࡅࡗࠦᛢ")), env.get(bstack11llll_opy_ (u"ࠢࡈࡅࡏࡓ࡚ࡊ࡟ࡑࡔࡒࡎࡊࡉࡔࠣᛣ")), env.get(bstack11llll_opy_ (u"ࠣࡉࡒࡓࡌࡒࡅࡠࡅࡏࡓ࡚ࡊ࡟ࡑࡔࡒࡎࡊࡉࡔࠣᛤ"))]):
        return {
            bstack11llll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᛥ"): bstack11llll_opy_ (u"ࠥࡋࡴࡵࡧ࡭ࡧࠣࡇࡱࡵࡵࡥࠤᛦ"),
            bstack11llll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᛧ"): None,
            bstack11llll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᛨ"): env.get(bstack11llll_opy_ (u"ࠨࡐࡓࡑࡍࡉࡈ࡚࡟ࡊࡆࠥᛩ")),
            bstack11llll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᛪ"): env.get(bstack11llll_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡊࡆࠥ᛫"))
        }
    if env.get(bstack11llll_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࠧ᛬")):
        return {
            bstack11llll_opy_ (u"ࠥࡲࡦࡳࡥࠣ᛭"): bstack11llll_opy_ (u"ࠦࡘ࡮ࡩࡱࡲࡤࡦࡱ࡫ࠢᛮ"),
            bstack11llll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᛯ"): env.get(bstack11llll_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧᛰ")),
            bstack11llll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᛱ"): bstack11llll_opy_ (u"ࠣࡌࡲࡦࠥࠩࡻࡾࠤᛲ").format(env.get(bstack11llll_opy_ (u"ࠩࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡐࡏࡃࡡࡌࡈࠬᛳ"))) if env.get(bstack11llll_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡊࡐࡄࡢࡍࡉࠨᛴ")) else None,
            bstack11llll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᛵ"): env.get(bstack11llll_opy_ (u"࡙ࠧࡈࡊࡒࡓࡅࡇࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᛶ"))
        }
    if bstack1lll1lll11_opy_(env.get(bstack11llll_opy_ (u"ࠨࡎࡆࡖࡏࡍࡋ࡟ࠢᛷ"))):
        return {
            bstack11llll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᛸ"): bstack11llll_opy_ (u"ࠣࡐࡨࡸࡱ࡯ࡦࡺࠤ᛹"),
            bstack11llll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᛺"): env.get(bstack11llll_opy_ (u"ࠥࡈࡊࡖࡌࡐ࡛ࡢ࡙ࡗࡒࠢ᛻")),
            bstack11llll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᛼"): env.get(bstack11llll_opy_ (u"࡙ࠧࡉࡕࡇࡢࡒࡆࡓࡅࠣ᛽")),
            bstack11llll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ᛾"): env.get(bstack11llll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡉࡅࠤ᛿"))
        }
    if bstack1lll1lll11_opy_(env.get(bstack11llll_opy_ (u"ࠣࡉࡌࡘࡍ࡛ࡂࡠࡃࡆࡘࡎࡕࡎࡔࠤᜀ"))):
        return {
            bstack11llll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᜁ"): bstack11llll_opy_ (u"ࠥࡋ࡮ࡺࡈࡶࡤࠣࡅࡨࡺࡩࡰࡰࡶࠦᜂ"),
            bstack11llll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᜃ"): bstack11llll_opy_ (u"ࠧࢁࡽ࠰ࡽࢀ࠳ࡦࡩࡴࡪࡱࡱࡷ࠴ࡸࡵ࡯ࡵ࠲ࡿࢂࠨᜄ").format(env.get(bstack11llll_opy_ (u"࠭ࡇࡊࡖࡋ࡙ࡇࡥࡓࡆࡔ࡙ࡉࡗࡥࡕࡓࡎࠪᜅ")), env.get(bstack11llll_opy_ (u"ࠧࡈࡋࡗࡌ࡚ࡈ࡟ࡓࡇࡓࡓࡘࡏࡔࡐࡔ࡜ࠫᜆ")), env.get(bstack11llll_opy_ (u"ࠨࡉࡌࡘࡍ࡛ࡂࡠࡔࡘࡒࡤࡏࡄࠨᜇ"))),
            bstack11llll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᜈ"): env.get(bstack11llll_opy_ (u"ࠥࡋࡎ࡚ࡈࡖࡄࡢ࡛ࡔࡘࡋࡇࡎࡒ࡛ࠧᜉ")),
            bstack11llll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᜊ"): env.get(bstack11llll_opy_ (u"ࠧࡍࡉࡕࡊࡘࡆࡤࡘࡕࡏࡡࡌࡈࠧᜋ"))
        }
    if env.get(bstack11llll_opy_ (u"ࠨࡃࡊࠤᜌ")) == bstack11llll_opy_ (u"ࠢࡵࡴࡸࡩࠧᜍ") and env.get(bstack11llll_opy_ (u"ࠣࡘࡈࡖࡈࡋࡌࠣᜎ")) == bstack11llll_opy_ (u"ࠤ࠴ࠦᜏ"):
        return {
            bstack11llll_opy_ (u"ࠥࡲࡦࡳࡥࠣᜐ"): bstack11llll_opy_ (u"࡛ࠦ࡫ࡲࡤࡧ࡯ࠦᜑ"),
            bstack11llll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᜒ"): bstack11llll_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࡻࡾࠤᜓ").format(env.get(bstack11llll_opy_ (u"ࠧࡗࡇࡕࡇࡊࡒ࡟ࡖࡔࡏ᜔ࠫ"))),
            bstack11llll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧ᜕ࠥ"): None,
            bstack11llll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ᜖"): None,
        }
    if env.get(bstack11llll_opy_ (u"ࠥࡘࡊࡇࡍࡄࡋࡗ࡝ࡤ࡜ࡅࡓࡕࡌࡓࡓࠨ᜗")):
        return {
            bstack11llll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᜘"): bstack11llll_opy_ (u"࡚ࠧࡥࡢ࡯ࡦ࡭ࡹࡿࠢ᜙"),
            bstack11llll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᜚"): None,
            bstack11llll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ᜛"): env.get(bstack11llll_opy_ (u"ࠣࡖࡈࡅࡒࡉࡉࡕ࡛ࡢࡔࡗࡕࡊࡆࡅࡗࡣࡓࡇࡍࡆࠤ᜜")),
            bstack11llll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ᜝"): env.get(bstack11llll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤ᜞"))
        }
    if any([env.get(bstack11llll_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋࠢᜟ")), env.get(bstack11llll_opy_ (u"ࠧࡉࡏࡏࡅࡒ࡙ࡗ࡙ࡅࡠࡗࡕࡐࠧᜠ")), env.get(bstack11llll_opy_ (u"ࠨࡃࡐࡐࡆࡓ࡚ࡘࡓࡆࡡࡘࡗࡊࡘࡎࡂࡏࡈࠦᜡ")), env.get(bstack11llll_opy_ (u"ࠢࡄࡑࡑࡇࡔ࡛ࡒࡔࡇࡢࡘࡊࡇࡍࠣᜢ"))]):
        return {
            bstack11llll_opy_ (u"ࠣࡰࡤࡱࡪࠨᜣ"): bstack11llll_opy_ (u"ࠤࡆࡳࡳࡩ࡯ࡶࡴࡶࡩࠧᜤ"),
            bstack11llll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᜥ"): None,
            bstack11llll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᜦ"): env.get(bstack11llll_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨᜧ")) or None,
            bstack11llll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᜨ"): env.get(bstack11llll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡉࡅࠤᜩ"), 0)
        }
    if env.get(bstack11llll_opy_ (u"ࠣࡉࡒࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨᜪ")):
        return {
            bstack11llll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᜫ"): bstack11llll_opy_ (u"ࠥࡋࡴࡉࡄࠣᜬ"),
            bstack11llll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᜭ"): None,
            bstack11llll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᜮ"): env.get(bstack11llll_opy_ (u"ࠨࡇࡐࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦᜯ")),
            bstack11llll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᜰ"): env.get(bstack11llll_opy_ (u"ࠣࡉࡒࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡃࡐࡗࡑࡘࡊࡘࠢᜱ"))
        }
    if env.get(bstack11llll_opy_ (u"ࠤࡆࡊࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢᜲ")):
        return {
            bstack11llll_opy_ (u"ࠥࡲࡦࡳࡥࠣᜳ"): bstack11llll_opy_ (u"ࠦࡈࡵࡤࡦࡈࡵࡩࡸ࡮᜴ࠢ"),
            bstack11llll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ᜵"): env.get(bstack11llll_opy_ (u"ࠨࡃࡇࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧ᜶")),
            bstack11llll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ᜷"): env.get(bstack11llll_opy_ (u"ࠣࡅࡉࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡎࡂࡏࡈࠦ᜸")),
            bstack11llll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ᜹"): env.get(bstack11llll_opy_ (u"ࠥࡇࡋࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣ᜺"))
        }
    return {bstack11llll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᜻"): None}
def get_host_info():
    return {
        bstack11llll_opy_ (u"ࠧ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠢ᜼"): platform.node(),
        bstack11llll_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠣ᜽"): platform.system(),
        bstack11llll_opy_ (u"ࠢࡵࡻࡳࡩࠧ᜾"): platform.machine(),
        bstack11llll_opy_ (u"ࠣࡸࡨࡶࡸ࡯࡯࡯ࠤ᜿"): platform.version(),
        bstack11llll_opy_ (u"ࠤࡤࡶࡨ࡮ࠢᝀ"): platform.architecture()[0]
    }
def bstack1l1ll11ll_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack1l1l1111111_opy_():
    if bstack1111l1l1_opy_.get_property(bstack11llll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫᝁ")):
        return bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᝂ")
    return bstack11llll_opy_ (u"ࠬࡻ࡮࡬ࡰࡲࡻࡳࡥࡧࡳ࡫ࡧࠫᝃ")
def bstack1l11l11l111_opy_(driver):
    info = {
        bstack11llll_opy_ (u"࠭ࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᝄ"): driver.capabilities,
        bstack11llll_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠫᝅ"): driver.session_id,
        bstack11llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩᝆ"): driver.capabilities.get(bstack11llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧᝇ"), None),
        bstack11llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᝈ"): driver.capabilities.get(bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᝉ"), None),
        bstack11llll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࠧᝊ"): driver.capabilities.get(bstack11llll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠬᝋ"), None),
    }
    if bstack1l1l1111111_opy_() == bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ᝌ"):
        if bstack11lllllll_opy_():
            info[bstack11llll_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࠩᝍ")] = bstack11llll_opy_ (u"ࠩࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥࠨᝎ")
        elif driver.capabilities.get(bstack11llll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᝏ"), {}).get(bstack11llll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨᝐ"), False):
            info[bstack11llll_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭ᝑ")] = bstack11llll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪᝒ")
        else:
            info[bstack11llll_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࠨᝓ")] = bstack11llll_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪ᝔")
    return info
def bstack11lllllll_opy_():
    if bstack1111l1l1_opy_.get_property(bstack11llll_opy_ (u"ࠩࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠨ᝕")):
        return True
    if bstack1lll1lll11_opy_(os.environ.get(bstack11llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫ᝖"), None)):
        return True
    return False
def bstack1l1111l1l_opy_(bstack1l11l1l1111_opy_, url, data, config):
    headers = config.get(bstack11llll_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬ᝗"), None)
    proxies = bstack1ll111111_opy_(config, url)
    auth = config.get(bstack11llll_opy_ (u"ࠬࡧࡵࡵࡪࠪ᝘"), None)
    response = requests.request(
            bstack1l11l1l1111_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack1l11llllll_opy_(bstack1lll1ll1ll_opy_, size):
    bstack1l1lll11l1_opy_ = []
    while len(bstack1lll1ll1ll_opy_) > size:
        bstack11l1l11l11_opy_ = bstack1lll1ll1ll_opy_[:size]
        bstack1l1lll11l1_opy_.append(bstack11l1l11l11_opy_)
        bstack1lll1ll1ll_opy_ = bstack1lll1ll1ll_opy_[size:]
    bstack1l1lll11l1_opy_.append(bstack1lll1ll1ll_opy_)
    return bstack1l1lll11l1_opy_
def bstack1l11ll11ll1_opy_(message, bstack1l1l1111ll1_opy_=False):
    os.write(1, bytes(message, bstack11llll_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬ᝙")))
    os.write(1, bytes(bstack11llll_opy_ (u"ࠧ࡝ࡰࠪ᝚"), bstack11llll_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧ᝛")))
    if bstack1l1l1111ll1_opy_:
        with open(bstack11llll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠯ࡲ࠵࠶ࡿ࠭ࠨ᝜") + os.environ[bstack11llll_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩ᝝")] + bstack11llll_opy_ (u"ࠫ࠳ࡲ࡯ࡨࠩ᝞"), bstack11llll_opy_ (u"ࠬࡧࠧ᝟")) as f:
            f.write(message + bstack11llll_opy_ (u"࠭࡜࡯ࠩᝠ"))
def bstack1l111lll11l_opy_():
    return os.environ[bstack11llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪᝡ")].lower() == bstack11llll_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᝢ")
def bstack11l1ll11l_opy_(bstack1l11l1lll1l_opy_):
    return bstack11llll_opy_ (u"ࠩࡾࢁ࠴ࢁࡽࠨᝣ").format(bstack1l1ll111l1l_opy_, bstack1l11l1lll1l_opy_)
def bstack1l111ll1_opy_():
    return bstack1l111l1l_opy_().replace(tzinfo=None).isoformat() + bstack11llll_opy_ (u"ࠪ࡞ࠬᝤ")
def bstack1l11l1l11l1_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack11llll_opy_ (u"ࠫ࡟࠭ᝥ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack11llll_opy_ (u"ࠬࡠࠧᝦ")))).total_seconds() * 1000
def bstack1l11lllll11_opy_(timestamp):
    return bstack1l11l1ll111_opy_(timestamp).isoformat() + bstack11llll_opy_ (u"࡚࠭ࠨᝧ")
def bstack1l1l1111l11_opy_(bstack1l11l11l1l1_opy_):
    date_format = bstack11llll_opy_ (u"࡛ࠧࠦࠨࡱࠪࡪࠠࠦࡊ࠽ࠩࡒࡀࠥࡔ࠰ࠨࡪࠬᝨ")
    bstack1l111llllll_opy_ = datetime.datetime.strptime(bstack1l11l11l1l1_opy_, date_format)
    return bstack1l111llllll_opy_.isoformat() + bstack11llll_opy_ (u"ࠨ࡜ࠪᝩ")
def bstack1l111llll1l_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack11llll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᝪ")
    else:
        return bstack11llll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᝫ")
def bstack1lll1lll11_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack11llll_opy_ (u"ࠫࡹࡸࡵࡦࠩᝬ")
def bstack1l111ll1111_opy_(val):
    return val.__str__().lower() == bstack11llll_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ᝭")
def bstack1l11llll_opy_(bstack1l11ll1llll_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack1l11ll1llll_opy_ as e:
                print(bstack11llll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡼࡿࠣ࠱ࡃࠦࡻࡾ࠼ࠣࡿࢂࠨᝮ").format(func.__name__, bstack1l11ll1llll_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack1l11l11l11l_opy_(bstack1l111llll11_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack1l111llll11_opy_(cls, *args, **kwargs)
            except bstack1l11ll1llll_opy_ as e:
                print(bstack11llll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࡽࢀࠤ࠲ࡄࠠࡼࡿ࠽ࠤࢀࢃࠢᝯ").format(bstack1l111llll11_opy_.__name__, bstack1l11ll1llll_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack1l11l11l11l_opy_
    else:
        return decorator
def bstack11ll11111_opy_(bstack111lll1l_opy_):
    if bstack11llll_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᝰ") in bstack111lll1l_opy_ and bstack1l111ll1111_opy_(bstack111lll1l_opy_[bstack11llll_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭᝱")]):
        return False
    if bstack11llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᝲ") in bstack111lll1l_opy_ and bstack1l111ll1111_opy_(bstack111lll1l_opy_[bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᝳ")]):
        return False
    return True
def bstack1l1lll1l1l_opy_():
    try:
        from pytest_bdd import reporting
        return True
    except Exception as e:
        return False
def bstack1lll1l1l1l_opy_(hub_url, CONFIG):
    if bstack111l1111l_opy_() <= version.parse(bstack11llll_opy_ (u"ࠬ࠹࠮࠲࠵࠱࠴ࠬ᝴")):
        if hub_url:
            return bstack11llll_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢ᝵") + hub_url + bstack11llll_opy_ (u"ࠢ࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠦ᝶")
        return bstack11ll11lll_opy_
    if hub_url:
        return bstack11llll_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥ᝷") + hub_url + bstack11llll_opy_ (u"ࠤ࠲ࡻࡩ࠵ࡨࡶࡤࠥ᝸")
    return bstack1llll111ll_opy_
def bstack1l11ll1l1ll_opy_():
    return isinstance(os.getenv(bstack11llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓ࡝࡙ࡋࡓࡕࡡࡓࡐ࡚ࡍࡉࡏࠩ᝹")), str)
def bstack11l1l111l_opy_(url):
    return urlparse(url).hostname
def bstack1l1111ll11_opy_(hostname):
    for bstack1l1l111lll_opy_ in bstack11l1llll11_opy_:
        regex = re.compile(bstack1l1l111lll_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack1l1lll1lll1_opy_(bstack1l111ll1l1l_opy_, file_name, logger):
    bstack11ll1ll11l_opy_ = os.path.join(os.path.expanduser(bstack11llll_opy_ (u"ࠫࢃ࠭᝺")), bstack1l111ll1l1l_opy_)
    try:
        if not os.path.exists(bstack11ll1ll11l_opy_):
            os.makedirs(bstack11ll1ll11l_opy_)
        file_path = os.path.join(os.path.expanduser(bstack11llll_opy_ (u"ࠬࢄࠧ᝻")), bstack1l111ll1l1l_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack11llll_opy_ (u"࠭ࡷࠨ᝼")):
                pass
            with open(file_path, bstack11llll_opy_ (u"ࠢࡸ࠭ࠥ᝽")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1lll1ll111_opy_.format(str(e)))
def bstack1l1lll1llll_opy_(file_name, key, value, logger):
    file_path = bstack1l1lll1lll1_opy_(bstack11llll_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ᝾"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1l1lll1111_opy_ = json.load(open(file_path, bstack11llll_opy_ (u"ࠩࡵࡦࠬ᝿")))
        else:
            bstack1l1lll1111_opy_ = {}
        bstack1l1lll1111_opy_[key] = value
        with open(file_path, bstack11llll_opy_ (u"ࠥࡻ࠰ࠨក")) as outfile:
            json.dump(bstack1l1lll1111_opy_, outfile)
def bstack1ll111111l_opy_(file_name, logger):
    file_path = bstack1l1lll1lll1_opy_(bstack11llll_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫខ"), file_name, logger)
    bstack1l1lll1111_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack11llll_opy_ (u"ࠬࡸࠧគ")) as bstack11ll111l1l_opy_:
            bstack1l1lll1111_opy_ = json.load(bstack11ll111l1l_opy_)
    return bstack1l1lll1111_opy_
def bstack1llll1l1l1_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack11llll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡦࡨࡰࡪࡺࡩ࡯ࡩࠣࡪ࡮ࡲࡥ࠻ࠢࠪឃ") + file_path + bstack11llll_opy_ (u"ࠧࠡࠩង") + str(e))
def bstack111l1111l_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack11llll_opy_ (u"ࠣ࠾ࡑࡓ࡙࡙ࡅࡕࡀࠥច")
def bstack1ll11l1111_opy_(config):
    if bstack11llll_opy_ (u"ࠩ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨឆ") in config:
        del (config[bstack11llll_opy_ (u"ࠪ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩជ")])
        return False
    if bstack111l1111l_opy_() < version.parse(bstack11llll_opy_ (u"ࠫ࠸࠴࠴࠯࠲ࠪឈ")):
        return False
    if bstack111l1111l_opy_() >= version.parse(bstack11llll_opy_ (u"ࠬ࠺࠮࠲࠰࠸ࠫញ")):
        return True
    if bstack11llll_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ដ") in config and config[bstack11llll_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧឋ")] is False:
        return False
    else:
        return True
def bstack1ll1ll11ll_opy_(args_list, bstack1l111ll1ll1_opy_):
    index = -1
    for value in bstack1l111ll1ll1_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack1l1l11l1_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack1l1l11l1_opy_ = bstack1l1l11l1_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack11llll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨឌ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack11llll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩឍ"), exception=exception)
    def bstack111llll11l_opy_(self):
        if self.result != bstack11llll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪណ"):
            return None
        if isinstance(self.exception_type, str) and bstack11llll_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢត") in self.exception_type:
            return bstack11llll_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࡆࡴࡵࡳࡷࠨថ")
        return bstack11llll_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢទ")
    def bstack1l11l1ll11l_opy_(self):
        if self.result != bstack11llll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧធ"):
            return None
        if self.bstack1l1l11l1_opy_:
            return self.bstack1l1l11l1_opy_
        return bstack1l111l11lll_opy_(self.exception)
def bstack1l111l11lll_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack1l11l1l11ll_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1ll111l1_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1l11l1ll11_opy_(config, logger):
    try:
        import playwright
        bstack1l11l1ll1l1_opy_ = playwright.__file__
        bstack1l11lll1111_opy_ = os.path.split(bstack1l11l1ll1l1_opy_)
        bstack1l11l111ll1_opy_ = bstack1l11lll1111_opy_[0] + bstack11llll_opy_ (u"ࠨ࠱ࡧࡶ࡮ࡼࡥࡳ࠱ࡳࡥࡨࡱࡡࡨࡧ࠲ࡰ࡮ࡨ࠯ࡤ࡮࡬࠳ࡨࡲࡩ࠯࡬ࡶࠫន")
        os.environ[bstack11llll_opy_ (u"ࠩࡊࡐࡔࡈࡁࡍࡡࡄࡋࡊࡔࡔࡠࡊࡗࡘࡕࡥࡐࡓࡑ࡛࡝ࠬប")] = bstack11l1lll1l_opy_(config)
        with open(bstack1l11l111ll1_opy_, bstack11llll_opy_ (u"ࠪࡶࠬផ")) as f:
            file_content = f.read()
            bstack1l111lllll1_opy_ = bstack11llll_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯࠱ࡦ࡭ࡥ࡯ࡶࠪព")
            bstack1l1l111l111_opy_ = file_content.find(bstack1l111lllll1_opy_)
            if bstack1l1l111l111_opy_ == -1:
              process = subprocess.Popen(bstack11llll_opy_ (u"ࠧࡴࡰ࡮ࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣ࡫ࡱࡵࡢࡢ࡮࠰ࡥ࡬࡫࡮ࡵࠤភ"), shell=True, cwd=bstack1l11lll1111_opy_[0])
              process.wait()
              bstack1l11ll1111l_opy_ = bstack11llll_opy_ (u"࠭ࠢࡶࡵࡨࠤࡸࡺࡲࡪࡥࡷࠦࡀ࠭ម")
              bstack1l1l1111lll_opy_ = bstack11llll_opy_ (u"ࠢࠣࠤࠣࡠࠧࡻࡳࡦࠢࡶࡸࡷ࡯ࡣࡵ࡞ࠥ࠿ࠥࡩ࡯࡯ࡵࡷࠤࢀࠦࡢࡰࡱࡷࡷࡹࡸࡡࡱࠢࢀࠤࡂࠦࡲࡦࡳࡸ࡭ࡷ࡫ࠨࠨࡩ࡯ࡳࡧࡧ࡬࠮ࡣࡪࡩࡳࡺࠧࠪ࠽ࠣ࡭࡫ࠦࠨࡱࡴࡲࡧࡪࡹࡳ࠯ࡧࡱࡺ࠳ࡍࡌࡐࡄࡄࡐࡤࡇࡇࡆࡐࡗࡣࡍ࡚ࡔࡑࡡࡓࡖࡔ࡞࡙ࠪࠢࡥࡳࡴࡺࡳࡵࡴࡤࡴ࠭࠯࠻ࠡࠤࠥࠦយ")
              bstack1l111ll11l1_opy_ = file_content.replace(bstack1l11ll1111l_opy_, bstack1l1l1111lll_opy_)
              with open(bstack1l11l111ll1_opy_, bstack11llll_opy_ (u"ࠨࡹࠪរ")) as f:
                f.write(bstack1l111ll11l1_opy_)
    except Exception as e:
        logger.error(bstack1lll1l111_opy_.format(str(e)))
def bstack1ll1lll11l_opy_():
  try:
    bstack1l11l1l111l_opy_ = os.path.join(tempfile.gettempdir(), bstack11llll_opy_ (u"ࠩࡲࡴࡹ࡯࡭ࡢ࡮ࡢ࡬ࡺࡨ࡟ࡶࡴ࡯࠲࡯ࡹ࡯࡯ࠩល"))
    bstack1l11lll11ll_opy_ = []
    if os.path.exists(bstack1l11l1l111l_opy_):
      with open(bstack1l11l1l111l_opy_) as f:
        bstack1l11lll11ll_opy_ = json.load(f)
      os.remove(bstack1l11l1l111l_opy_)
    return bstack1l11lll11ll_opy_
  except:
    pass
  return []
def bstack1l1l1l11l1_opy_(bstack11ll11l1l_opy_):
  try:
    bstack1l11lll11ll_opy_ = []
    bstack1l11l1l111l_opy_ = os.path.join(tempfile.gettempdir(), bstack11llll_opy_ (u"ࠪࡳࡵࡺࡩ࡮ࡣ࡯ࡣ࡭ࡻࡢࡠࡷࡵࡰ࠳ࡰࡳࡰࡰࠪវ"))
    if os.path.exists(bstack1l11l1l111l_opy_):
      with open(bstack1l11l1l111l_opy_) as f:
        bstack1l11lll11ll_opy_ = json.load(f)
    bstack1l11lll11ll_opy_.append(bstack11ll11l1l_opy_)
    with open(bstack1l11l1l111l_opy_, bstack11llll_opy_ (u"ࠫࡼ࠭ឝ")) as f:
        json.dump(bstack1l11lll11ll_opy_, f)
  except:
    pass
def bstack1ll1l111l1_opy_(logger, bstack1l11ll11lll_opy_ = False):
  try:
    test_name = os.environ.get(bstack11llll_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࡤ࡚ࡅࡔࡖࡢࡒࡆࡓࡅࠨឞ"), bstack11llll_opy_ (u"࠭ࠧស"))
    if test_name == bstack11llll_opy_ (u"ࠧࠨហ"):
        test_name = threading.current_thread().__dict__.get(bstack11llll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡃࡦࡧࡣࡹ࡫ࡳࡵࡡࡱࡥࡲ࡫ࠧឡ"), bstack11llll_opy_ (u"ࠩࠪអ"))
    bstack1l11l1l1lll_opy_ = bstack11llll_opy_ (u"ࠪ࠰ࠥ࠭ឣ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack1l11ll11lll_opy_:
        bstack1ll111l11_opy_ = os.environ.get(bstack11llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫឤ"), bstack11llll_opy_ (u"ࠬ࠶ࠧឥ"))
        bstack1llll1111_opy_ = {bstack11llll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫឦ"): test_name, bstack11llll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ឧ"): bstack1l11l1l1lll_opy_, bstack11llll_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧឨ"): bstack1ll111l11_opy_}
        bstack1l11lllllll_opy_ = []
        bstack1l11ll11l11_opy_ = os.path.join(tempfile.gettempdir(), bstack11llll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡳࡴࡵࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨឩ"))
        if os.path.exists(bstack1l11ll11l11_opy_):
            with open(bstack1l11ll11l11_opy_) as f:
                bstack1l11lllllll_opy_ = json.load(f)
        bstack1l11lllllll_opy_.append(bstack1llll1111_opy_)
        with open(bstack1l11ll11l11_opy_, bstack11llll_opy_ (u"ࠪࡻࠬឪ")) as f:
            json.dump(bstack1l11lllllll_opy_, f)
    else:
        bstack1llll1111_opy_ = {bstack11llll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩឫ"): test_name, bstack11llll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫឬ"): bstack1l11l1l1lll_opy_, bstack11llll_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬឭ"): str(multiprocessing.current_process().name)}
        if bstack11llll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷࠫឮ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1llll1111_opy_)
  except Exception as e:
      logger.warn(bstack11llll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡴࡾࡺࡥࡴࡶࠣࡪࡺࡴ࡮ࡦ࡮ࠣࡨࡦࡺࡡ࠻ࠢࡾࢁࠧឯ").format(e))
def bstack1l1111ll1_opy_(error_message, test_name, index, logger):
  try:
    bstack1l11ll1l11l_opy_ = []
    bstack1llll1111_opy_ = {bstack11llll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧឰ"): test_name, bstack11llll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩឱ"): error_message, bstack11llll_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪឲ"): index}
    bstack1l111lll1ll_opy_ = os.path.join(tempfile.gettempdir(), bstack11llll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭ឳ"))
    if os.path.exists(bstack1l111lll1ll_opy_):
        with open(bstack1l111lll1ll_opy_) as f:
            bstack1l11ll1l11l_opy_ = json.load(f)
    bstack1l11ll1l11l_opy_.append(bstack1llll1111_opy_)
    with open(bstack1l111lll1ll_opy_, bstack11llll_opy_ (u"࠭ࡷࠨ឴")) as f:
        json.dump(bstack1l11ll1l11l_opy_, f)
  except Exception as e:
    logger.warn(bstack11llll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡵࡲࡦࠢࡵࡳࡧࡵࡴࠡࡨࡸࡲࡳ࡫࡬ࠡࡦࡤࡸࡦࡀࠠࡼࡿࠥ឵").format(e))
def bstack1l11111lll_opy_(bstack111ll1l11_opy_, name, logger):
  try:
    bstack1llll1111_opy_ = {bstack11llll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ា"): name, bstack11llll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨិ"): bstack111ll1l11_opy_, bstack11llll_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩី"): str(threading.current_thread()._name)}
    return bstack1llll1111_opy_
  except Exception as e:
    logger.warn(bstack11llll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡲࡶࡪࠦࡢࡦࡪࡤࡺࡪࠦࡦࡶࡰࡱࡩࡱࠦࡤࡢࡶࡤ࠾ࠥࢁࡽࠣឹ").format(e))
  return
def bstack1l11l111l11_opy_():
    return platform.system() == bstack11llll_opy_ (u"ࠬ࡝ࡩ࡯ࡦࡲࡻࡸ࠭ឺ")
def bstack1l1lllll1l_opy_(bstack1l11llll11l_opy_, config, logger):
    bstack1l11ll1ll11_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack1l11llll11l_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack11llll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡩ࡭ࡱࡺࡥࡳࠢࡦࡳࡳ࡬ࡩࡨࠢ࡮ࡩࡾࡹࠠࡣࡻࠣࡶࡪ࡭ࡥࡹࠢࡰࡥࡹࡩࡨ࠻ࠢࡾࢁࠧុ").format(e))
    return bstack1l11ll1ll11_opy_
def bstack1l1ll1l1l11_opy_(bstack1l111ll1lll_opy_, bstack1l11lll11l1_opy_):
    bstack1l111l1ll1l_opy_ = version.parse(bstack1l111ll1lll_opy_)
    bstack1l11ll1l1l1_opy_ = version.parse(bstack1l11lll11l1_opy_)
    if bstack1l111l1ll1l_opy_ > bstack1l11ll1l1l1_opy_:
        return 1
    elif bstack1l111l1ll1l_opy_ < bstack1l11ll1l1l1_opy_:
        return -1
    else:
        return 0
def bstack1l111l1l_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack1l11l1ll111_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack1l1l11111l1_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack1l111ll11_opy_(options, framework):
    if options is None:
        return
    if getattr(options, bstack11llll_opy_ (u"ࠧࡨࡧࡷࠫូ"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack1ll1l11ll1_opy_ = caps.get(bstack11llll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩួ"))
    bstack1l11l1lllll_opy_ = True
    if bstack1l111ll1111_opy_(caps.get(bstack11llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩ࡜࠹ࡃࠨើ"))) or bstack1l111ll1111_opy_(caps.get(bstack11llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡥࡷ࠴ࡥࠪឿ"))):
        bstack1l11l1lllll_opy_ = False
    if bstack1ll11l1111_opy_({bstack11llll_opy_ (u"ࠦࡺࡹࡥࡘ࠵ࡆࠦៀ"): bstack1l11l1lllll_opy_}):
        bstack1ll1l11ll1_opy_ = bstack1ll1l11ll1_opy_ or {}
        bstack1ll1l11ll1_opy_[bstack11llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧេ")] = bstack1l1l11111l1_opy_(framework)
        bstack1ll1l11ll1_opy_[bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨែ")] = bstack1l111lll11l_opy_()
        if getattr(options, bstack11llll_opy_ (u"ࠧࡴࡧࡷࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡹࠨៃ"), None):
            options.set_capability(bstack11llll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩោ"), bstack1ll1l11ll1_opy_)
        else:
            options[bstack11llll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪៅ")] = bstack1ll1l11ll1_opy_
    else:
        if getattr(options, bstack11llll_opy_ (u"ࠪࡷࡪࡺ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶࡼࠫំ"), None):
            options.set_capability(bstack11llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬះ"), bstack1l1l11111l1_opy_(framework))
            options.set_capability(bstack11llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ៈ"), bstack1l111lll11l_opy_())
        else:
            options[bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ៉")] = bstack1l1l11111l1_opy_(framework)
            options[bstack11llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ៊")] = bstack1l111lll11l_opy_()
    return options
def bstack1l11l11llll_opy_(ws_endpoint, framework):
    if ws_endpoint and len(ws_endpoint.split(bstack11llll_opy_ (u"ࠨࡥࡤࡴࡸࡃࠧ់"))) > 1:
        ws_url = ws_endpoint.split(bstack11llll_opy_ (u"ࠩࡦࡥࡵࡹ࠽ࠨ៌"))[0]
        if bstack11llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭៍") in ws_url:
            from browserstack_sdk._version import __version__
            bstack1l1l1111l1l_opy_ = json.loads(urllib.parse.unquote(ws_endpoint.split(bstack11llll_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪ៎"))[1]))
            bstack1l1l1111l1l_opy_ = bstack1l1l1111l1l_opy_ or {}
            bstack1l1l1111l1l_opy_[bstack11llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭៏")] = str(framework) + str(__version__)
            bstack1l1l1111l1l_opy_[bstack11llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧ័")] = bstack1l111lll11l_opy_()
            ws_endpoint = ws_endpoint.split(bstack11llll_opy_ (u"ࠧࡤࡣࡳࡷࡂ࠭៑"))[0] + bstack11llll_opy_ (u"ࠨࡥࡤࡴࡸࡃ្ࠧ") + urllib.parse.quote(json.dumps(bstack1l1l1111l1l_opy_))
    return ws_endpoint
def bstack1l11l111l_opy_():
    global bstack1lll11l1l1_opy_
    from playwright._impl._browser_type import BrowserType
    bstack1lll11l1l1_opy_ = BrowserType.connect
    return bstack1lll11l1l1_opy_
def bstack1l1l1111l1_opy_(framework_name):
    global bstack1l1l11llll_opy_
    bstack1l1l11llll_opy_ = framework_name
    return framework_name
def bstack1l11ll1ll_opy_(self, *args, **kwargs):
    global bstack1lll11l1l1_opy_
    try:
        global bstack1l1l11llll_opy_
        if bstack11llll_opy_ (u"ࠩࡺࡷࡊࡴࡤࡱࡱ࡬ࡲࡹ࠭៓") in kwargs:
            kwargs[bstack11llll_opy_ (u"ࠪࡻࡸࡋ࡮ࡥࡲࡲ࡭ࡳࡺࠧ។")] = bstack1l11l11llll_opy_(
                kwargs.get(bstack11llll_opy_ (u"ࠫࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴࠨ៕"), None),
                bstack1l1l11llll_opy_
            )
    except Exception as e:
        logger.error(bstack11llll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡥ࡯ࠢࡳࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡓࡅࡍࠣࡧࡦࡶࡳ࠻ࠢࡾࢁࠧ៖").format(str(e)))
    return bstack1lll11l1l1_opy_(self, *args, **kwargs)
def bstack1l11l1llll1_opy_(bstack111l1l11l1_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack1ll111111_opy_(bstack111l1l11l1_opy_, bstack11llll_opy_ (u"ࠨࠢៗ"))
        if proxies and proxies.get(bstack11llll_opy_ (u"ࠢࡩࡶࡷࡴࡸࠨ៘")):
            parsed_url = urlparse(proxies.get(bstack11llll_opy_ (u"ࠣࡪࡷࡸࡵࡹࠢ៙")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack11llll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡉࡱࡶࡸࠬ៚")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack11llll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡲࡶࡹ࠭៛")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack11llll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡘࡷࡪࡸࠧៜ")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack11llll_opy_ (u"ࠬࡶࡲࡰࡺࡼࡔࡦࡹࡳࠨ៝")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack11l111l11l_opy_(bstack111l1l11l1_opy_):
    bstack1l1l111111l_opy_ = {
        bstack1l1ll11ll1l_opy_[bstack1l11ll1l111_opy_]: bstack111l1l11l1_opy_[bstack1l11ll1l111_opy_]
        for bstack1l11ll1l111_opy_ in bstack111l1l11l1_opy_
        if bstack1l11ll1l111_opy_ in bstack1l1ll11ll1l_opy_
    }
    bstack1l1l111111l_opy_[bstack11llll_opy_ (u"ࠨࡰࡳࡱࡻࡽࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸࠨ៞")] = bstack1l11l1llll1_opy_(bstack111l1l11l1_opy_, bstack1111l1l1_opy_.get_property(bstack11llll_opy_ (u"ࠢࡱࡴࡲࡼࡾ࡙ࡥࡵࡶ࡬ࡲ࡬ࡹࠢ៟")))
    bstack1l11llll1ll_opy_ = [element.lower() for element in bstack1l1ll11l1l1_opy_]
    bstack1l11llllll1_opy_(bstack1l1l111111l_opy_, bstack1l11llll1ll_opy_)
    return bstack1l1l111111l_opy_
def bstack1l11llllll1_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack11llll_opy_ (u"ࠣࠬ࠭࠮࠯ࠨ០")
    for value in d.values():
        if isinstance(value, dict):
            bstack1l11llllll1_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack1l11llllll1_opy_(item, keys)
def bstack1l11l1lll11_opy_():
    bstack1l111l1l111_opy_ = [os.environ.get(bstack11llll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡌࡐࡊ࡙࡟ࡅࡋࡕࠦ១")), os.path.join(os.path.expanduser(bstack11llll_opy_ (u"ࠥࢂࠧ២")), bstack11llll_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ៣")), os.path.join(bstack11llll_opy_ (u"ࠬ࠵ࡴ࡮ࡲࠪ៤"), bstack11llll_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭៥"))]
    for path in bstack1l111l1l111_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack11llll_opy_ (u"ࠢࡇ࡫࡯ࡩࠥ࠭ࠢ៦") + str(path) + bstack11llll_opy_ (u"ࠣࠩࠣࡩࡽ࡯ࡳࡵࡵ࠱ࠦ៧"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack11llll_opy_ (u"ࠤࡊ࡭ࡻ࡯࡮ࡨࠢࡳࡩࡷࡳࡩࡴࡵ࡬ࡳࡳࡹࠠࡧࡱࡵࠤࠬࠨ៨") + str(path) + bstack11llll_opy_ (u"ࠥࠫࠧ៩"))
                    os.chmod(path, 0o755)
                else:
                    logger.debug(bstack11llll_opy_ (u"ࠦࡋ࡯࡬ࡦࠢࠪࠦ៪") + str(path) + bstack11llll_opy_ (u"ࠧ࠭ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡪࡤࡷࠥࡺࡨࡦࠢࡵࡩࡶࡻࡩࡳࡧࡧࠤࡵ࡫ࡲ࡮࡫ࡶࡷ࡮ࡵ࡮ࡴ࠰ࠥ៫"))
            else:
                logger.debug(bstack11llll_opy_ (u"ࠨࡃࡳࡧࡤࡸ࡮ࡴࡧࠡࡨ࡬ࡰࡪࠦࠧࠣ៬") + str(path) + bstack11llll_opy_ (u"ࠢࠨࠢࡺ࡭ࡹ࡮ࠠࡸࡴ࡬ࡸࡪࠦࡰࡦࡴࡰ࡭ࡸࡹࡩࡰࡰ࠱ࠦ៭"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o755)
            logger.debug(bstack11llll_opy_ (u"ࠣࡑࡳࡩࡷࡧࡴࡪࡱࡱࠤࡸࡻࡣࡤࡧࡨࡨࡪࡪࠠࡧࡱࡵࠤࠬࠨ៮") + str(path) + bstack11llll_opy_ (u"ࠤࠪ࠲ࠧ៯"))
            return path
        except Exception as e:
            logger.debug(bstack11llll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡹࡵࠦࡦࡪ࡮ࡨࠤࠬࢁࡰࡢࡶ࡫ࢁࠬࡀࠠࠣ៰") + str(e) + bstack11llll_opy_ (u"ࠦࠧ៱"))
    logger.debug(bstack11llll_opy_ (u"ࠧࡇ࡬࡭ࠢࡳࡥࡹ࡮ࡳࠡࡨࡤ࡭ࡱ࡫ࡤ࠯ࠤ៲"))
    return None
def bstack1lllll11ll1_opy_(binary_path, bstack1lllll1l1ll_opy_, bs_config):
    logger.debug(bstack11llll_opy_ (u"ࠨࡃࡶࡴࡵࡩࡳࡺࠠࡄࡎࡌࠤࡕࡧࡴࡩࠢࡩࡳࡺࡴࡤ࠻ࠢࡾࢁࠧ៳").format(binary_path))
    bstack1l11l111lll_opy_ = bstack11llll_opy_ (u"ࠧࠨ៴")
    bstack1l11lll1ll1_opy_ = {
        bstack11llll_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭៵"): __version__,
        bstack11llll_opy_ (u"ࠤࡲࡷࠧ៶"): platform.system(),
        bstack11llll_opy_ (u"ࠥࡳࡸࡥࡡࡳࡥ࡫ࠦ៷"): platform.machine(),
        bstack11llll_opy_ (u"ࠦࡨࡲࡩࡠࡸࡨࡶࡸ࡯࡯࡯ࠤ៸"): bstack11llll_opy_ (u"ࠬ࠶ࠧ៹"),
        bstack11llll_opy_ (u"ࠨࡳࡥ࡭ࡢࡰࡦࡴࡧࡶࡣࡪࡩࠧ៺"): bstack11llll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ៻")
    }
    try:
        if binary_path:
            bstack1l11lll1ll1_opy_[bstack11llll_opy_ (u"ࠨࡥ࡯࡭ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭៼")] = subprocess.check_output([binary_path, bstack11llll_opy_ (u"ࠤࡹࡩࡷࡹࡩࡰࡰࠥ៽")]).strip().decode(bstack11llll_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩ៾"))
        response = requests.request(
            bstack11llll_opy_ (u"ࠫࡌࡋࡔࠨ៿"),
            url=bstack11l1ll11l_opy_(bstack1l1ll1l111l_opy_),
            headers=None,
            auth=(bs_config[bstack11llll_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ᠀")], bs_config[bstack11llll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ᠁")]),
            json=None,
            params=bstack1l11lll1ll1_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack11llll_opy_ (u"ࠧࡶࡴ࡯ࠫ᠂") in data.keys() and bstack11llll_opy_ (u"ࠨࡷࡳࡨࡦࡺࡥࡥࡡࡦࡰ࡮ࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ᠃") in data.keys():
            logger.debug(bstack11llll_opy_ (u"ࠤࡑࡩࡪࡪࠠࡵࡱࠣࡹࡵࡪࡡࡵࡧࠣࡦ࡮ࡴࡡࡳࡻ࠯ࠤࡨࡻࡲࡳࡧࡱࡸࠥࡨࡩ࡯ࡣࡵࡽࠥࡼࡥࡳࡵ࡬ࡳࡳࡀࠠࡼࡿࠥ᠄").format(bstack1l11lll1ll1_opy_[bstack11llll_opy_ (u"ࠪࡧࡱ࡯࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ᠅")]))
            bstack1l11l11lll1_opy_ = bstack1l11ll111ll_opy_(data[bstack11llll_opy_ (u"ࠫࡺࡸ࡬ࠨ᠆")], bstack1lllll1l1ll_opy_)
            bstack1l11l111lll_opy_ = os.path.join(bstack1lllll1l1ll_opy_, bstack1l11l11lll1_opy_)
            os.chmod(bstack1l11l111lll_opy_, 0o755) # bstack1l11l1ll1ll_opy_ permission
            return bstack1l11l111lll_opy_
    except Exception as e:
        logger.debug(bstack11llll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡨࡴࡽ࡮࡭ࡱࡤࡨ࡮ࡴࡧࠡࡰࡨࡻ࡙ࠥࡄࡌࠢࡾࢁࠧ᠇").format(e))
    return binary_path
def bstack1l11ll111ll_opy_(bstack1l111l1l1ll_opy_, bstack1l11l11ll11_opy_):
    logger.debug(bstack11llll_opy_ (u"ࠨࡄࡰࡹࡱࡰࡴࡧࡤࡪࡰࡪࠤࡘࡊࡋࠡࡤ࡬ࡲࡦࡸࡹࠡࡨࡵࡳࡲࡀࠠࠣ᠈") + str(bstack1l111l1l1ll_opy_) + bstack11llll_opy_ (u"ࠢࠣ᠉"))
    zip_path = os.path.join(bstack1l11l11ll11_opy_, bstack11llll_opy_ (u"ࠣࡦࡲࡻࡳࡲ࡯ࡢࡦࡨࡨࡤ࡬ࡩ࡭ࡧ࠱ࡾ࡮ࡶࠢ᠊"))
    bstack1l11l11lll1_opy_ = bstack11llll_opy_ (u"ࠩࠪ᠋")
    with requests.get(bstack1l111l1l1ll_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack11llll_opy_ (u"ࠥࡻࡧࠨ᠌")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack11llll_opy_ (u"ࠦࡋ࡯࡬ࡦࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࡩࡩࠦࡳࡶࡥࡦࡩࡸࡹࡦࡶ࡮࡯ࡽ࠳ࠨ᠍"))
    with zipfile.ZipFile(zip_path, bstack11llll_opy_ (u"ࠬࡸࠧ᠎")) as zip_ref:
        bstack1l11ll111l1_opy_ = zip_ref.namelist()
        if len(bstack1l11ll111l1_opy_) > 0:
            bstack1l11l11lll1_opy_ = bstack1l11ll111l1_opy_[0] # bstack1l11l11ll1l_opy_ bstack1l11llll111_opy_ will be bstack1l111l1ll11_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack1l11l11ll11_opy_)
        logger.debug(bstack11llll_opy_ (u"ࠨࡆࡪ࡮ࡨࡷࠥࡹࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭࡮ࡼࠤࡪࡾࡴࡳࡣࡦࡸࡪࡪࠠࡵࡱࠣࠫࠧ᠏") + str(bstack1l11l11ll11_opy_) + bstack11llll_opy_ (u"ࠢࠨࠤ᠐"))
    os.remove(zip_path)
    return bstack1l11l11lll1_opy_
def bstack1llllll1l1l_opy_():
    bstack1l1l11111ll_opy_ = bstack1l11l1lll11_opy_()
    if bstack1l1l11111ll_opy_:
        bstack1lllll1l1ll_opy_ = os.path.join(bstack1l1l11111ll_opy_, bstack11llll_opy_ (u"ࠣࡥ࡯࡭ࠧ᠑"))
        if not os.path.exists(bstack1lllll1l1ll_opy_):
            os.makedirs(bstack1lllll1l1ll_opy_, exist_ok=True)
        return bstack1lllll1l1ll_opy_
    else:
        raise FileNotFoundError(bstack11llll_opy_ (u"ࠤࡑࡳࠥࡽࡲࡪࡶࡤࡦࡱ࡫ࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡔࡆࡎࠤࡧ࡯࡮ࡢࡴࡼ࠲ࠧ᠒"))
def bstack1llllll1l11_opy_(bstack1lllll1l1ll_opy_):
    bstack11llll_opy_ (u"ࠥࠦࠧࡍࡥࡵࠢࡷ࡬ࡪࠦࡰࡢࡶ࡫ࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡘࡊࡋࠡࡤ࡬ࡲࡦࡸࡹࠡ࡫ࡱࠤࡦࠦࡷࡳ࡫ࡷࡥࡧࡲࡥࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼ࠲ࠧࠨࠢ᠓")
    bstack1l111ll11ll_opy_ = [
        os.path.join(bstack1lllll1l1ll_opy_, f)
        for f in os.listdir(bstack1lllll1l1ll_opy_)
        if os.path.isfile(os.path.join(bstack1lllll1l1ll_opy_, f)) and f.startswith(bstack11llll_opy_ (u"ࠦࡧ࡯࡮ࡢࡴࡼ࠱ࠧ᠔"))
    ]
    if len(bstack1l111ll11ll_opy_) > 0:
        return max(bstack1l111ll11ll_opy_, key=os.path.getmtime) # get bstack1l11ll11111_opy_ binary
    return bstack11llll_opy_ (u"ࠧࠨ᠕")