from azaka.commands import VNCondition as VNC
from azaka.commands.proxy import _BoolOProxy


def test_cdns() -> None:
    expr = '(((id >= 0) and (search ~ "*")) or (id = [1, 2, 3]))'
    proxy = ((VNC.ID >= 0) & (VNC.SEARCH % "*")) | (VNC.ID_ARRAY == [1, 2, 3])
    assert isinstance(proxy, _BoolOProxy)
    assert proxy.expression == expr
