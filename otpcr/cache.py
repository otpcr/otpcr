# This file is placed in the Public Domain.
# pylint: disable=C


"cache"


import _thread


lock = _thread.allocate_lock()


class Cache:

    objs = {}

    @staticmethod
    def add(path, obj):
        with lock:
            Cache.objs[path] = obj

    @staticmethod
    def get(path):
        with lock:
            return Cache.objs.get(path)

    @staticmethod
    def typed(matcher):
        with lock:
            for key in Cache.objs:
                if matcher not in key:
                    continue
                yield Cache.objs.get(key)


def __dir__():
    return (
        'Cache',
    )
