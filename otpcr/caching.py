# This file is placed in the Public Domain.


"caching"


import typing


class Cache:

    """ Cache """

    objs = {}

    @staticmethod
    def add(path, obj) -> None:
        """ add object with path. """
        Cache.objs[path] = obj

    @staticmethod
    def get(path) -> typing.Any:
        """ get object by path. """
        return Cache.objs.get(path, None)

    @staticmethod
    def typed(matcher) -> [typing.Any]:
        """ get objects by type. """
        for key in Cache.objs:
            if matcher not in key:
                continue
            yield Cache.objs.get(key)


def __dir__():
    return (
        'Cache',
    )
