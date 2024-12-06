import typing as t

import pandas as pd


class ProcessData(t.Protocol):
    def __call__(
        self, files: tuple[str, ...], values: t.Any, interval_jihua: bool
    ) -> pd.DataFrame: ...
