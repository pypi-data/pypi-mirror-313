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
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack1l1ll1l1l11_opy_
from browserstack_sdk.bstack1111l1ll_opy_ import bstack11l11l11_opy_
def _1l1ll1l1ll1_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack1l1ll1ll11l_opy_:
    def __init__(self, handler):
        self._1l1ll1ll1l1_opy_ = {}
        self._1l1lll11l11_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack11l11l11_opy_.version()
        if bstack1l1ll1l1l11_opy_(pytest_version, bstack11llll_opy_ (u"ࠦ࠽࠴࠱࠯࠳ࠥኣ")) >= 0:
            self._1l1ll1ll1l1_opy_[bstack11llll_opy_ (u"ࠬ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨኤ")] = Module._register_setup_function_fixture
            self._1l1ll1ll1l1_opy_[bstack11llll_opy_ (u"࠭࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧእ")] = Module._register_setup_module_fixture
            self._1l1ll1ll1l1_opy_[bstack11llll_opy_ (u"ࠧࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫ࠧኦ")] = Class._register_setup_class_fixture
            self._1l1ll1ll1l1_opy_[bstack11llll_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠩኧ")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack1l1ll1ll1ll_opy_(bstack11llll_opy_ (u"ࠩࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬከ"))
            Module._register_setup_module_fixture = self.bstack1l1ll1ll1ll_opy_(bstack11llll_opy_ (u"ࠪࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫኩ"))
            Class._register_setup_class_fixture = self.bstack1l1ll1ll1ll_opy_(bstack11llll_opy_ (u"ࠫࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠫኪ"))
            Class._register_setup_method_fixture = self.bstack1l1ll1ll1ll_opy_(bstack11llll_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ካ"))
        else:
            self._1l1ll1ll1l1_opy_[bstack11llll_opy_ (u"࠭ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩኬ")] = Module._inject_setup_function_fixture
            self._1l1ll1ll1l1_opy_[bstack11llll_opy_ (u"ࠧ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨክ")] = Module._inject_setup_module_fixture
            self._1l1ll1ll1l1_opy_[bstack11llll_opy_ (u"ࠨࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨኮ")] = Class._inject_setup_class_fixture
            self._1l1ll1ll1l1_opy_[bstack11llll_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠪኯ")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack1l1ll1ll1ll_opy_(bstack11llll_opy_ (u"ࠪࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ኰ"))
            Module._inject_setup_module_fixture = self.bstack1l1ll1ll1ll_opy_(bstack11llll_opy_ (u"ࠫࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ኱"))
            Class._inject_setup_class_fixture = self.bstack1l1ll1ll1ll_opy_(bstack11llll_opy_ (u"ࠬࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࠬኲ"))
            Class._inject_setup_method_fixture = self.bstack1l1ll1ll1ll_opy_(bstack11llll_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠧኳ"))
    def bstack1l1ll1llll1_opy_(self, bstack1l1ll1lll1l_opy_, hook_type):
        bstack1l1lll1111l_opy_ = id(bstack1l1ll1lll1l_opy_.__class__)
        if (bstack1l1lll1111l_opy_, hook_type) in self._1l1lll11l11_opy_:
            return
        meth = getattr(bstack1l1ll1lll1l_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._1l1lll11l11_opy_[(bstack1l1lll1111l_opy_, hook_type)] = meth
            setattr(bstack1l1ll1lll1l_opy_, hook_type, self.bstack1l1lll11111_opy_(hook_type, bstack1l1lll1111l_opy_))
    def bstack1l1ll1l1l1l_opy_(self, instance, bstack1l1ll1lllll_opy_):
        if bstack1l1ll1lllll_opy_ == bstack11llll_opy_ (u"ࠢࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠥኴ"):
            self.bstack1l1ll1llll1_opy_(instance.obj, bstack11llll_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠤኵ"))
            self.bstack1l1ll1llll1_opy_(instance.obj, bstack11llll_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠨ኶"))
        if bstack1l1ll1lllll_opy_ == bstack11llll_opy_ (u"ࠥࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠦ኷"):
            self.bstack1l1ll1llll1_opy_(instance.obj, bstack11llll_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠥኸ"))
            self.bstack1l1ll1llll1_opy_(instance.obj, bstack11llll_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠢኹ"))
        if bstack1l1ll1lllll_opy_ == bstack11llll_opy_ (u"ࠨࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪࠨኺ"):
            self.bstack1l1ll1llll1_opy_(instance.obj, bstack11llll_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠧኻ"))
            self.bstack1l1ll1llll1_opy_(instance.obj, bstack11llll_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠤኼ"))
        if bstack1l1ll1lllll_opy_ == bstack11llll_opy_ (u"ࠤࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠥኽ"):
            self.bstack1l1ll1llll1_opy_(instance.obj, bstack11llll_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠤኾ"))
            self.bstack1l1ll1llll1_opy_(instance.obj, bstack11llll_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩࠨ኿"))
    @staticmethod
    def bstack1l1ll1ll111_opy_(hook_type, func, args):
        if hook_type in [bstack11llll_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠫዀ"), bstack11llll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠨ዁")]:
            _1l1ll1l1ll1_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack1l1lll11111_opy_(self, hook_type, bstack1l1lll1111l_opy_):
        def bstack1l1ll1l1lll_opy_(arg=None):
            self.handler(hook_type, bstack11llll_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫ࠧዂ"))
            result = None
            try:
                bstack1ll11l1llll_opy_ = self._1l1lll11l11_opy_[(bstack1l1lll1111l_opy_, hook_type)]
                self.bstack1l1ll1ll111_opy_(hook_type, bstack1ll11l1llll_opy_, (arg,))
                result = Result(result=bstack11llll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨዃ"))
            except Exception as e:
                result = Result(result=bstack11llll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩዄ"), exception=e)
                self.handler(hook_type, bstack11llll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩዅ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11llll_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪ዆"), result)
        def bstack1l1lll111ll_opy_(this, arg=None):
            self.handler(hook_type, bstack11llll_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࠬ዇"))
            result = None
            exception = None
            try:
                self.bstack1l1ll1ll111_opy_(hook_type, self._1l1lll11l11_opy_[hook_type], (this, arg))
                result = Result(result=bstack11llll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ወ"))
            except Exception as e:
                result = Result(result=bstack11llll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧዉ"), exception=e)
                self.handler(hook_type, bstack11llll_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧዊ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11llll_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨዋ"), result)
        if hook_type in [bstack11llll_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠩዌ"), bstack11llll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ው")]:
            return bstack1l1lll111ll_opy_
        return bstack1l1ll1l1lll_opy_
    def bstack1l1ll1ll1ll_opy_(self, bstack1l1ll1lllll_opy_):
        def bstack1l1lll111l1_opy_(this, *args, **kwargs):
            self.bstack1l1ll1l1l1l_opy_(this, bstack1l1ll1lllll_opy_)
            self._1l1ll1ll1l1_opy_[bstack1l1ll1lllll_opy_](this, *args, **kwargs)
        return bstack1l1lll111l1_opy_