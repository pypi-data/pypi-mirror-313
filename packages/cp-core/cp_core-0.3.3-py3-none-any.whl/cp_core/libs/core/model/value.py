from typing import Tuple


def gen_minmax_from_name(name) -> Tuple[str, str, str]:
    res = (
        name + "_max",
        name + "_min",
        name + "_average",
    )
    return res
