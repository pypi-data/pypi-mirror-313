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
from uuid import uuid4
from bstack_utils.helper import bstack1l111ll1_opy_, bstack1l11l1l11l1_opy_
from bstack_utils.bstack1lll11ll1_opy_ import bstack1l1l1ll11ll_opy_
class bstack11lll1ll_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack1l11111llll_opy_=None, bstack1l11111ll1l_opy_=True, bstack1l1111l11l1_opy_=None, bstack1lll111l1l_opy_=None, result=None, duration=None, bstack1l1llll1_opy_=None, meta={}):
        self.bstack1l1llll1_opy_ = bstack1l1llll1_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1l11111ll1l_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1l11111llll_opy_ = bstack1l11111llll_opy_
        self.bstack1l1111l11l1_opy_ = bstack1l1111l11l1_opy_
        self.bstack1lll111l1l_opy_ = bstack1lll111l1l_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack1l1l1l11_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack11l1l1l1_opy_(self, meta):
        self.meta = meta
    def bstack11l1l1ll_opy_(self, hooks):
        self.hooks = hooks
    def bstack1l11111lll1_opy_(self):
        bstack1l11111l11l_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack11llll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨᢌ"): bstack1l11111l11l_opy_,
            bstack11llll_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠨᢍ"): bstack1l11111l11l_opy_,
            bstack11llll_opy_ (u"ࠧࡷࡥࡢࡪ࡮ࡲࡥࡱࡣࡷ࡬ࠬᢎ"): bstack1l11111l11l_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack11llll_opy_ (u"ࠣࡗࡱࡩࡽࡶࡥࡤࡶࡨࡨࠥࡧࡲࡨࡷࡰࡩࡳࡺ࠺ࠡࠤᢏ") + key)
            setattr(self, key, val)
    def bstack1l11111l111_opy_(self):
        return {
            bstack11llll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᢐ"): self.name,
            bstack11llll_opy_ (u"ࠪࡦࡴࡪࡹࠨᢑ"): {
                bstack11llll_opy_ (u"ࠫࡱࡧ࡮ࡨࠩᢒ"): bstack11llll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬᢓ"),
                bstack11llll_opy_ (u"࠭ࡣࡰࡦࡨࠫᢔ"): self.code
            },
            bstack11llll_opy_ (u"ࠧࡴࡥࡲࡴࡪࡹࠧᢕ"): self.scope,
            bstack11llll_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ᢖ"): self.tags,
            bstack11llll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬᢗ"): self.framework,
            bstack11llll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᢘ"): self.started_at
        }
    def bstack1l11111l1l1_opy_(self):
        return {
         bstack11llll_opy_ (u"ࠫࡲ࡫ࡴࡢࠩᢙ"): self.meta
        }
    def bstack1l1111111l1_opy_(self):
        return {
            bstack11llll_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡗ࡫ࡲࡶࡰࡓࡥࡷࡧ࡭ࠨᢚ"): {
                bstack11llll_opy_ (u"࠭ࡲࡦࡴࡸࡲࡤࡴࡡ࡮ࡧࠪᢛ"): self.bstack1l11111llll_opy_
            }
        }
    def bstack1l1111l111l_opy_(self, bstack1l1111l1111_opy_, details):
        step = next(filter(lambda st: st[bstack11llll_opy_ (u"ࠧࡪࡦࠪᢜ")] == bstack1l1111l1111_opy_, self.meta[bstack11llll_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᢝ")]), None)
        step.update(details)
    def bstack11ll11l1_opy_(self, bstack1l1111l1111_opy_):
        step = next(filter(lambda st: st[bstack11llll_opy_ (u"ࠩ࡬ࡨࠬᢞ")] == bstack1l1111l1111_opy_, self.meta[bstack11llll_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᢟ")]), None)
        step.update({
            bstack11llll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᢠ"): bstack1l111ll1_opy_()
        })
    def bstack1l1l111l_opy_(self, bstack1l1111l1111_opy_, result, duration=None):
        bstack1l1111l11l1_opy_ = bstack1l111ll1_opy_()
        if bstack1l1111l1111_opy_ is not None and self.meta.get(bstack11llll_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᢡ")):
            step = next(filter(lambda st: st[bstack11llll_opy_ (u"࠭ࡩࡥࠩᢢ")] == bstack1l1111l1111_opy_, self.meta[bstack11llll_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᢣ")]), None)
            step.update({
                bstack11llll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᢤ"): bstack1l1111l11l1_opy_,
                bstack11llll_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫᢥ"): duration if duration else bstack1l11l1l11l1_opy_(step[bstack11llll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᢦ")], bstack1l1111l11l1_opy_),
                bstack11llll_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᢧ"): result.result,
                bstack11llll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ᢨ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1l11111ll11_opy_):
        if self.meta.get(bstack11llll_opy_ (u"࠭ࡳࡵࡧࡳࡷᢩࠬ")):
            self.meta[bstack11llll_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᢪ")].append(bstack1l11111ll11_opy_)
        else:
            self.meta[bstack11llll_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ᢫")] = [ bstack1l11111ll11_opy_ ]
    def bstack1l11111l1ll_opy_(self):
        return {
            bstack11llll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ᢬"): self.bstack1l1l1l11_opy_(),
            **self.bstack1l11111l111_opy_(),
            **self.bstack1l11111lll1_opy_(),
            **self.bstack1l11111l1l1_opy_()
        }
    def bstack1l111111l1l_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack11llll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ᢭"): self.bstack1l1111l11l1_opy_,
            bstack11llll_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬ᢮"): self.duration,
            bstack11llll_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ᢯"): self.result.result
        }
        if data[bstack11llll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᢰ")] == bstack11llll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᢱ"):
            data[bstack11llll_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧᢲ")] = self.result.bstack111llll11l_opy_()
            data[bstack11llll_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪᢳ")] = [{bstack11llll_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ᢴ"): self.result.bstack1l11l1ll11l_opy_()}]
        return data
    def bstack1l111111111_opy_(self):
        return {
            bstack11llll_opy_ (u"ࠫࡺࡻࡩࡥࠩᢵ"): self.bstack1l1l1l11_opy_(),
            **self.bstack1l11111l111_opy_(),
            **self.bstack1l11111lll1_opy_(),
            **self.bstack1l111111l1l_opy_(),
            **self.bstack1l11111l1l1_opy_()
        }
    def bstack1lll1l1l_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack11llll_opy_ (u"࡙ࠬࡴࡢࡴࡷࡩࡩ࠭ᢶ") in event:
            return self.bstack1l11111l1ll_opy_()
        elif bstack11llll_opy_ (u"࠭ࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᢷ") in event:
            return self.bstack1l111111111_opy_()
    def bstack1l1lll1l_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1l1111l11l1_opy_ = time if time else bstack1l111ll1_opy_()
        self.duration = duration if duration else bstack1l11l1l11l1_opy_(self.started_at, self.bstack1l1111l11l1_opy_)
        if result:
            self.result = result
class bstack1lll11l1_opy_(bstack11lll1ll_opy_):
    def __init__(self, hooks=[], bstack1ll1l111_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack1ll1l111_opy_ = bstack1ll1l111_opy_
        super().__init__(*args, **kwargs, bstack1lll111l1l_opy_=bstack11llll_opy_ (u"ࠧࡵࡧࡶࡸࠬᢸ"))
    @classmethod
    def bstack1l11111111l_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack11llll_opy_ (u"ࠨ࡫ࡧࠫᢹ"): id(step),
                bstack11llll_opy_ (u"ࠩࡷࡩࡽࡺࠧᢺ"): step.name,
                bstack11llll_opy_ (u"ࠪ࡯ࡪࡿࡷࡰࡴࡧࠫᢻ"): step.keyword,
            })
        return bstack1lll11l1_opy_(
            **kwargs,
            meta={
                bstack11llll_opy_ (u"ࠫ࡫࡫ࡡࡵࡷࡵࡩࠬᢼ"): {
                    bstack11llll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᢽ"): feature.name,
                    bstack11llll_opy_ (u"࠭ࡰࡢࡶ࡫ࠫᢾ"): feature.filename,
                    bstack11llll_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬᢿ"): feature.description
                },
                bstack11llll_opy_ (u"ࠨࡵࡦࡩࡳࡧࡲࡪࡱࠪᣀ"): {
                    bstack11llll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᣁ"): scenario.name
                },
                bstack11llll_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᣂ"): steps,
                bstack11llll_opy_ (u"ࠫࡪࡾࡡ࡮ࡲ࡯ࡩࡸ࠭ᣃ"): bstack1l1l1ll11ll_opy_(test)
            }
        )
    def bstack1l1111111ll_opy_(self):
        return {
            bstack11llll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᣄ"): self.hooks
        }
    def bstack1l111111ll1_opy_(self):
        if self.bstack1ll1l111_opy_:
            return {
                bstack11llll_opy_ (u"࠭ࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠬᣅ"): self.bstack1ll1l111_opy_
            }
        return {}
    def bstack1l111111111_opy_(self):
        return {
            **super().bstack1l111111111_opy_(),
            **self.bstack1l1111111ll_opy_()
        }
    def bstack1l11111l1ll_opy_(self):
        return {
            **super().bstack1l11111l1ll_opy_(),
            **self.bstack1l111111ll1_opy_()
        }
    def bstack1l1lll1l_opy_(self):
        return bstack11llll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩᣆ")
class bstack1l1l1ll1_opy_(bstack11lll1ll_opy_):
    def __init__(self, hook_type, *args,bstack1ll1l111_opy_={}, **kwargs):
        self.hook_type = hook_type
        self.bstack1l111111l11_opy_ = None
        self.bstack1ll1l111_opy_ = bstack1ll1l111_opy_
        super().__init__(*args, **kwargs, bstack1lll111l1l_opy_=bstack11llll_opy_ (u"ࠨࡪࡲࡳࡰ࠭ᣇ"))
    def bstack1lll1111_opy_(self):
        return self.hook_type
    def bstack1l111111lll_opy_(self):
        return {
            bstack11llll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬᣈ"): self.hook_type
        }
    def bstack1l111111111_opy_(self):
        return {
            **super().bstack1l111111111_opy_(),
            **self.bstack1l111111lll_opy_()
        }
    def bstack1l11111l1ll_opy_(self):
        return {
            **super().bstack1l11111l1ll_opy_(),
            bstack11llll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤ࡯ࡤࠨᣉ"): self.bstack1l111111l11_opy_,
            **self.bstack1l111111lll_opy_()
        }
    def bstack1l1lll1l_opy_(self):
        return bstack11llll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳ࠭ᣊ")
    def bstack11l11ll1_opy_(self, bstack1l111111l11_opy_):
        self.bstack1l111111l11_opy_ = bstack1l111111l11_opy_