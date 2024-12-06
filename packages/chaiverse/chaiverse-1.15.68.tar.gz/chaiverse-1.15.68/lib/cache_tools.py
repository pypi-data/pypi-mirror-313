import functools
import threading


def thread_safe_lru_cache(maxsize=128, typed=False):
    def decorator(func):
        func = functools.lru_cache(maxsize=maxsize, typed=typed)(func)
        lock = threading.Lock()

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with lock:
                return func(*args, **kwargs)

        def cache_info():
            with lock:
                return func.cache_info()

        def cache_clear():
            with lock:
                func.cache_clear()

        wrapper.cache_info = cache_info
        wrapper.cache_clear = cache_clear

        return wrapper

    return decorator
