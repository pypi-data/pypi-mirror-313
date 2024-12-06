import functools

from cp_core.config import DEBUG
from cp_core.libs.result import Result, Status

from .judge import comprehensive


def debug_func(func):
    if DEBUG:

        @functools.wraps(func)
        def wrapper(values, write=True):
            final = comprehensive(values, write=write)
            return Result(status=Status.success, msg="success", value=final)

        return wrapper
    else:
        return func


@debug_func
def comprehensive_controller(values: dict, write: bool = True) -> Result:
    try:
        final = comprehensive(values, write=write)
        return Result(status=Status.success, msg="success", value=final)
    except Exception as e:
        return Result(status=Status.failed, msg="Unknown error: " + str(e))
