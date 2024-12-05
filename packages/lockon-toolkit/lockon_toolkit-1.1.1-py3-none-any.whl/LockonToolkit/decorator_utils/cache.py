#!/opt/homebrew/anaconda3/envs/quantfin/bin/ python
# -*- coding: utf-8 -*-
# @Time    : 2024/9/25 下午5:03
# @Author  : @Zhenxi Zhang
# @File    : cache.py
# @Software: PyCharm

from threading import RLock

_MISSING = object()


PREV, NEXT, KEY, VALUE = range(4)  # names for the link fields
DEFAULT_MAX_SIZE = 128


class _HashedKey(list):
    __slots__ = "hash_value"

    def __init__(self, key):
        self[:] = key
        self.hash_value = hash(tuple(key))

    def __hash__(self):
        return self.hash_value

    def __repr__(self):
        return f"{self.__class__.__name__}({list.__repr__(self)})"


def make_cache_key(
    args,
    kwargs,
    typed=False,
    kwarg_mark=object(),
    fast_types=frozenset([int, str, frozenset, type(None)]),
):
    key = list(args)
    if kwargs:
        sorted_items = sorted(kwargs.items())
        key.append(kwarg_mark)
        key.extend(sorted_items)
    if typed:
        key.extend([type(v) for v in args])
        if kwargs:
            sorted_items = sorted(kwargs.items())
            key.extend([type(v) for k, v in sorted_items])
    elif len(key) == 1 and type(key[0]) in fast_types:
        return key[0]
    return _HashedKey(key)


# for backwards compatibility in case someone was importing it
_make_cache_key = make_cache_key


class CachedFunction:
    def __init__(self, func, cache, scoped=True, typed=False, key=None):
        self.func = func
        if callable(cache):
            self.get_cache = cache
        elif not (
            callable(getattr(cache, "__getitem__", None))
            and callable(getattr(cache, "__setitem__", None))
        ):
            raise TypeError(
                "expected cache to be a dict-like object,"
                " or callable returning a dict-like object, not %r" % cache
            )
        else:

            def _get_cache():
                return cache

            self.get_cache = _get_cache
        self.scoped = scoped
        self.typed = typed
        self.key_func = key or make_cache_key

    def __call__(self, *args, **kwargs):
        cache = self.get_cache()
        key = self.key_func(args, kwargs, typed=self.typed)
        try:
            ret = cache[key]
        except KeyError:
            ret = cache[key] = self.func(*args, **kwargs)
        return ret

    def __repr__(self):
        cn = self.__class__.__name__
        if self.typed or not self.scoped:
            return "%s(func=%r, scoped=%r, typed=%r)" % (
                cn,
                self.func,
                self.scoped,
                self.typed,
            )
        return f"{cn}(func={self.func!r})"


def cached(scoped=True, typed=False, key=None):
    """
    装饰器：创建一个带有 LRU 缓存机制的函数。

    此装饰器可以应用于任何函数，以提供带有 LRU（最近最少使用）策略的缓存，
    当缓存达到最大容量时，将自动移除最久未使用的条目。

    参数:
      scoped (bool): 是否使用作用域缓存。默认为 True。
      typed (bool): 是否区分类型。如果为 True，则不同类型的相同值将视为不同的键。
      key (callable): 用于生成缓存键的自定义函数。默认为 None，使用内置的 make_cache_key 函数。

    返回:
      Callable: 装饰后的函数。

    示例:
      >>> @cached()
      ... def fibonacci(n):
      ...     if n <= 1:
      ...         return n
      ...     return fibonacci(n - 1) + fibonacci(n - 2)
      ...
      >>> fibonacci(30)  # 第一次计算可能会较慢
      832040
      >>> fibonacci(30)  # 第二次调用会从缓存中获取结果，非常快
      832040
    """

    class LRU(dict):
        def __init__(self, max_size=DEFAULT_MAX_SIZE, values=None, on_miss=None):
            if max_size <= 0:
                raise ValueError("expected max_size > 0, not %r" % max_size)
            self.hit_count = self.miss_count = self.soft_miss_count = 0
            self.max_size = max_size
            self._lock = RLock()
            self._init_ll()

            if on_miss is not None and not callable(on_miss):
                raise TypeError(
                    "expected on_miss to be a callable" " (or None), not %r" % on_miss
                )
            self.on_miss = on_miss

            if values:
                self.update(values)

        def _init_ll(self):
            anchor = []
            anchor[:] = [anchor, anchor, _MISSING, _MISSING]
            # a link lookup table for finding linked list links in O(1)
            # time.
            self._link_lookup = {}
            self._anchor = anchor

        def _print_ll(self):
            print("***")
            for _key, val in self._get_flattened_ll():
                print(_key, val)
            print("***")

        def _get_flattened_ll(self):
            flattened_list = []
            link = self._anchor
            while True:
                flattened_list.append((link[KEY], link[VALUE]))
                link = link[NEXT]
                if link is self._anchor:
                    break
            return flattened_list

        def _get_link_and_move_to_front_of_ll(self, _key):
            # find what will become the newest link. this may raise a
            # KeyError, which is useful to __getitem__ and __setitem__
            newest = self._link_lookup[_key]

            # splice out what will become the newest link.
            newest[PREV][NEXT] = newest[NEXT]
            newest[NEXT][PREV] = newest[PREV]

            # move what will become the newest link immediately before
            # anchor (invariant 2)
            anchor = self._anchor
            second_newest = anchor[PREV]
            second_newest[NEXT] = anchor[PREV] = newest
            newest[PREV] = second_newest
            newest[NEXT] = anchor
            return newest

        def _set_key_and_add_to_front_of_ll(self, _key, value):
            # create a new link and place it immediately before anchor
            # (invariant 2).
            anchor = self._anchor
            second_newest = anchor[PREV]
            newest = [second_newest, anchor, _key, value]
            second_newest[NEXT] = anchor[PREV] = newest
            self._link_lookup[_key] = newest

        def _set_key_and_evict_last_in_ll(self, _key, value):
            # the link after anchor is the oldest in the linked list
            # (invariant 3).  the current anchor becomes a link that holds
            # the newest key, and the oldest link becomes the new anchor
            # (invariant 1).  now the newest link comes before anchor
            # (invariant 2).  no links are moved; only their keys
            # and values are changed.
            oldanchor = self._anchor
            oldanchor[KEY] = _key
            oldanchor[VALUE] = value

            self._anchor = anchor = oldanchor[NEXT]
            evicted = anchor[KEY]
            anchor[KEY] = anchor[VALUE] = _MISSING
            del self._link_lookup[evicted]
            self._link_lookup[_key] = oldanchor
            return evicted

        def _remove_from_ll(self, _key):
            # splice a link out of the list and drop it from our lookup
            # table.
            link = self._link_lookup.pop(_key)
            link[PREV][NEXT] = link[NEXT]
            link[NEXT][PREV] = link[PREV]

        def __setitem__(self, _key, value):
            with self._lock:
                try:
                    link = self._get_link_and_move_to_front_of_ll(_key)
                except KeyError:
                    if len(self) < self.max_size:
                        self._set_key_and_add_to_front_of_ll(_key, value)
                    else:
                        evicted = self._set_key_and_evict_last_in_ll(_key, value)
                        super().__delitem__(evicted)
                else:
                    link[VALUE] = value
                super().__setitem__(_key, value)

        def __getitem__(self, _key):
            with self._lock:
                try:
                    link = self._get_link_and_move_to_front_of_ll(_key)
                except KeyError:
                    self.miss_count += 1
                    if not self.on_miss:
                        raise
                    ret = self[_key] = self.on_miss(_key)
                    return ret

                self.hit_count += 1
                return link[VALUE]

        def get(self, _key, default=None):
            try:
                return self[_key]
            except KeyError:
                self.soft_miss_count += 1
                return default

        def __delitem__(self, _key):
            with self._lock:
                super().__delitem__(_key)
                self._remove_from_ll(_key)

        def pop(self, _key, default=_MISSING):
            # NB: hit/miss counts are bypassed for pop()
            with self._lock:
                try:
                    ret = super().pop(_key)
                except KeyError:
                    if default is _MISSING:
                        raise
                    ret = default
                else:
                    self._remove_from_ll(_key)
                return ret

        def popitem(self):
            with self._lock:
                item = super().popitem()
                self._remove_from_ll(item[0])
                return item

        def clear(self):
            with self._lock:
                super().clear()
                self._init_ll()

        def copy(self):
            return self.__class__(max_size=self.max_size, values=self)

        def setdefault(self, _key, default=None):
            with self._lock:
                try:
                    return self[_key]
                except KeyError:
                    self.soft_miss_count += 1
                    self[_key] = default
                    return default

        def update(self, e, **f):
            # E and F are throwback names to the dict() __doc__
            with self._lock:
                if e is self:
                    return
                setitem = self.__setitem__
                if callable(getattr(e, "keys", None)):
                    for k in e.keys():
                        setitem(k, e[k])
                else:
                    for k, v in e:
                        setitem(k, v)
                for k in f:
                    setitem(k, f[k])

        def __eq__(self, other):
            with self._lock:
                if self is other:
                    return True
                if len(other) != len(self):
                    return False
                if not isinstance(other, LRU):
                    return other == self
                return super().__eq__(other)

        def __ne__(self, other):
            return not (self == other)

        def __repr__(self):
            cn = self.__class__.__name__
            val_map = super().__repr__()
            return "%s(max_size=%r, on_miss=%r, values=%s)" % (
                cn,
                self.max_size,
                self.on_miss,
                val_map,
            )

    def cached_func_decorator(func):
        return CachedFunction(func, LRU(), scoped=scoped, typed=typed, key=key)

    return cached_func_decorator
