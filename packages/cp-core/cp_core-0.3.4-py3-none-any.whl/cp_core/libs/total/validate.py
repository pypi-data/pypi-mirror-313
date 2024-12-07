import functools

from cp_core.libs.result import ComputeResult


def validate_files(file_result: ComputeResult):
    if len(file_result.data) != 3:
        raise ValueError(
            f"file_result.data should be 3, but got {len(file_result.data)}"
        )


def validate(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        res, df = func(*args, **kwargs)
        if kwargs.get("is_write"):
            validate_files(res)
        return res, df

    return wrapper
