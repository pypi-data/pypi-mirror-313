import functools

from .errors import KeyMissingError


def check_value(name: str):
    def wrapper(func):
        @functools.wraps(func)
        def wrapper(data, values, interval_jihua, *args, **kwargs):
            if not values.get(name):
                raise KeyMissingError(f"values: {values} should have `{name}`")
            return func(data, values, interval_jihua, *args, **kwargs)

        return wrapper

    return wrapper
