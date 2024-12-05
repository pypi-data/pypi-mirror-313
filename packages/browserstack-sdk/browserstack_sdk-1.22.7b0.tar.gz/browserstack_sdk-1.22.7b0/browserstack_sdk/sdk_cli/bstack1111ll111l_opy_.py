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
import threading
import os
from typing import Dict, Any
from dataclasses import dataclass
from collections import defaultdict
from datetime import timedelta
@dataclass
class bstack1111l1l11l_opy_:
    id: str
    hash: str
    thread_id: int
    process_id: int
    type: str
class bstack1111l1llll_opy_:
    bstack11111l11ll_opy_ = bstack11llll_opy_ (u"ࠢࡣࡧࡱࡧ࡭ࡳࡡࡳ࡭ࠥ࿪")
    context: bstack1111l1l11l_opy_
    data: Dict[str, Any]
    platform_index: int
    def __init__(self, context: bstack1111l1l11l_opy_):
        self.context = context
        self.data = dict({bstack1111l1llll_opy_.bstack11111l11ll_opy_: defaultdict(lambda: timedelta(microseconds=0))})
        self.platform_index = int(os.environ.get(bstack11llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ࿫"), bstack11llll_opy_ (u"ࠩ࠳ࠫ࿬")))
    def ref(self) -> str:
        return str(self.context.id)
    def bstack11111l1l11_opy_(self, target: object):
        return bstack1111l1llll_opy_.create_context(target) == self.context
    def bstack11111ll1ll_opy_(self, context: bstack1111l1l11l_opy_):
        return context and context.thread_id == self.context.thread_id and context.process_id == self.context.process_id
    def bstack1ll1l1l11l_opy_(self, key: str, value: timedelta):
        self.data[bstack1111l1llll_opy_.bstack11111l11ll_opy_][key] += value
    def bstack11111l1l1l_opy_(self) -> dict:
        return self.data[bstack1111l1llll_opy_.bstack11111l11ll_opy_]
    @staticmethod
    def create_context(
        target: object,
        thread_id=threading.get_ident(),
        process_id=os.getpid(),
    ):
        return bstack1111l1l11l_opy_(
            id=id(target),
            hash=hash(target),
            thread_id=thread_id,
            process_id=process_id,
            type=type(target),
        )