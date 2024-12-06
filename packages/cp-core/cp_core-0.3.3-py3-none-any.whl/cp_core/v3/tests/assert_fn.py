import pandas as pd


# avoid to use this function, not clear.
def assert_keys(df: pd.DataFrame, keys: list[str]):
    for key in keys:
        if key not in df.keys():
            return False
    return True
