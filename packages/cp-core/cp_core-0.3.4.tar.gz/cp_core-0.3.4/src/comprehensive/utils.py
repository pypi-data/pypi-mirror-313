from pathlib import Path
from dataclasses import dataclass


@dataclass
class Response:
    data: dict
    msg: str = "success"

    def validate(self):
        assert self.data is not None
        assert self.msg is not None
