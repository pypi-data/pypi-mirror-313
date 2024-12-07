import json
import typing

from .forms import InputData


def write_file(v: InputData, final):
    data = {"judge_result": final}
    with open(v.output, "w") as f:
        json.dump(data, f)


IntOrNone = typing.Union[int, None]
