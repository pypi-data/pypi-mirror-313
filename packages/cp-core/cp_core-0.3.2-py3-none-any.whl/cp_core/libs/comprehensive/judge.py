"""
comprehensive judge
"""

from .utils import write_file
from .validate import parse_external


def comprehensive(values: dict, write: bool) -> int:
    """
    v for values
    """
    v = parse_external(values)

    high, mid, low = 1, 0, -1
    final = None

    if v.detect == 0:
        final = low

    if v.detect == 1:
        if v.zhiliu == low and v.jiaoliu == low and (v.is_protect >= 0):
            final = low

        if v.zhiliu == high or v.jiaoliu == high:
            final = high

        if v.zhiliu == low or v.jiaoliu == low:
            if v.is_protect == low and v.corrosive == high:
                final = high

    if final is None:
        final = mid

    if write:
        write_file(v, final)
    return final
