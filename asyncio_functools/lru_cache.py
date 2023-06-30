from functools import lru_cache, wraps


class _CachedAwaitable:
    """Cached Awaitable"""

    def __init__(self, func, *args, **kwargs):
        wraps(func)(self)
        self._func = func
        self._args = args
        self._kwargs = kwargs
        self._coro = func(*args, **kwargs)
        self._result = None
        self._result_given = False

    def __repr__(self):
        coro = self._func(*self._args, **self._kwargs)
        result = repr(coro)
        coro.close()
        del coro
        return result

    def __str__(self):
        coro = self._func(*self._args, **self._kwargs)
        result = str(coro)
        coro.close()
        del coro
        return result

    def __del__(self):
        self._coro.close()
        del self._coro
        self._coro = None

    def __await__(self):
        async def iterator():
            if not self._result_given:
                self._result = await self._func(*self._args, **self._kwargs)
                self._result_given = True

            return self._result

        return iterator().__await__()


def async_lru_cache(*args, **kwargs):
    """As functools.lru_cache, but for async coroutines

    Example:

        @async_lru_cache(100)
        async def cached_function(arg1, args2=None):
            ...
    """

    def decorator(func):
        @wraps(func)
        @lru_cache(*args, **kwargs)
        def wrapper(*f_args, **f_kwargs):
            return _CachedAwaitable(func, *f_args, **f_kwargs)

        return wrapper

    return decorator
