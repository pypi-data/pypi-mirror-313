import functools


class MemberCaches:
    def __init__(self):
        self._cache = {}

    def cache(self, key: str):
        def actual_decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                if key not in self._cache:
                    self._cache[key] = func(*args, **kwargs)
                return self._cache[key]

            return wrapper

        return actual_decorator

    def clear(self, key: str = None):
        if key is None:
            self._cache.clear()
        elif key in self._cache:
            del self._cache[key]

    def __getitem__(self, item):
        return self._cache[item]

    def __setitem__(self, key, value):
        self._cache[key] = value

    def __delitem__(self, key):
        del self._cache[key]

    def __len__(self):
        return len(self._cache)

    def __iter__(self):
        return self._cache.__iter__()
