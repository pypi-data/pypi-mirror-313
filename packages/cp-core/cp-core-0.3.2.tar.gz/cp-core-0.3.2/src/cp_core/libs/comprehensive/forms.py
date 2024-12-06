import typing as t

from pydantic import BaseModel


class InputData(BaseModel):
    corrosive: t.Literal[-1, 0, 1]
    detect: t.Literal[0, 1]
    is_protect: t.Literal[-1, 0, 1]
    jiaoliu: t.Literal[-1, 0, 1]
    zhiliu: t.Literal[-1, 0, 1]
    output: str
