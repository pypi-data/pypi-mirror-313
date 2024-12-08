import time
from functools import wraps

__all__ = [
    "remaining_time",
    "sleep_until",
    "unix_timestamp",
    "timely_cls_property",
    "timely_property",
]


def remaining_time(string: str | int) -> None | int:
    """
    Parses a time string and returns the remaining time in seconds until the specified time.

    The function supports the following time string formats:
    - 10:25pm / 3:25am
    - 21:24
    - 555 (interpreted as seconds)

    If the specified time has already passed, the function returns `None`. Otherwise, it returns the remaining time in seconds.
    """

    if isinstance(string, int):
        return string

    if string.isdigit():
        return int(string)

    current_time = time.localtime()
    current_seconds = (
        current_time.tm_hour * 3600 + current_time.tm_min * 60 + current_time.tm_sec
    )

    if "am" in string or "pm" in string:
        time_struct = time.strptime(string, "%I:%M%p")
    elif ":" in string:
        time_struct = time.strptime(string, "%H:%M")
    else:
        total_seconds = int(string)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        time_struct = time.struct_time((0, 0, 0, hours, minutes, seconds, 0, 0, 0))

    target_seconds = (
        time_struct.tm_hour * 3600 + time_struct.tm_min * 60 + time_struct.tm_sec
    )
    remaining_seconds = target_seconds - current_seconds

    if remaining_seconds < 0:
        return None

    return remaining_seconds


def sleep_until(string: str | int):
    """
    sleeps until time
    supports
    10:25pm / 3:25am
    21:24
    555
    """
    remaining = remaining_time(string)
    if remaining is None:
        raise ValueError("time has already passed")
    print(f"sleeping for {remaining} seconds till {string}")
    time.sleep(remaining)


def unix_timestamp():
    return int(time.time() * 1000)


def timely_property(expiration_seconds):
    """
    A decorator that creates a property that caches the result of a function call for a specified expiration time.

    The `timely_property` decorator takes an `expiration_seconds` argument, which specifies the number of seconds to cache the result of the decorated function. If `expiration_seconds` is 0, the cache is disabled and the function is called every time the property is accessed.

    When the property is accessed, the decorator checks if the cached value is still valid (i.e., the expiration time has not been reached). If the cached value is valid, it is returned. Otherwise, the function is called, the result is cached, and the new value is returned.

    The decorator uses private attributes on the object to store the cached value and the timestamp of the last update. These attributes are named `__<function_name>_value` and `__<function_name>_timestamp`, respectively.

    The `timely_property` decorator can be used on any instance method of a class.
    """
    if expiration_seconds < 0:
        raise ValueError("expiration_seconds must be greater than 0")

    def decorator(func):
        @wraps(func)
        def wrapper(self):
            if not hasattr(self, f"__{func.__name__}_value"):
                setattr(self, f"__{func.__name__}_value", None)
                setattr(self, f"__{func.__name__}_timestamp", 0)

            current_time = time.time()
            if (
                expiration_seconds == 0
                or current_time - getattr(self, f"__{func.__name__}_timestamp")
                >= expiration_seconds
            ):
                value = func(self)
                setattr(self, f"__{func.__name__}_value", value)
                setattr(self, f"__{func.__name__}_timestamp", current_time)

            return getattr(self, f"__{func.__name__}_value")

        return property(wrapper)

    return decorator


class TimelyClsProperty:
    """
    A class that provides a class-level property that caches the result of a function call for a specified expiration time.

    The `TimelyClsProperty` class is a descriptor that can be used to create a class-level property. When the property is accessed, the descriptor checks if the cached value is still valid (i.e., the expiration time has not been reached). If the cached value is valid, it is returned. Otherwise, the function is called, the result is cached, and the new value is returned.

    The class uses a dictionary `self.cache` to store the cached values, where the key is the class object and the value is a dictionary containing the cached value and the expiration time.

    """

    def __init__(self, func, expiration_seconds):
        self.func = func
        self.expiration_seconds = expiration_seconds
        self.cache = {}

    def __get__(self, instance, owner):
        current_time = time.time()
        cache_entry = self.cache.get(owner)

        if cache_entry and (current_time < cache_entry["expire_time"]):
            return cache_entry["value"]

        value = self.func(owner)
        self.cache[owner] = {
            "value": value,
            "expire_time": current_time + self.expiration_seconds,
        }
        return value


def timely_cls_property(expiration_seconds):
    def decorator(func):
        prop = TimelyClsProperty(func, expiration_seconds)
        return prop

    return decorator
