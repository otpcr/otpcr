# This file is placed in the Public Domain.


"disk"


import datetime
import json
import os
import pathlib
import threading


from .json   import dump, load
from .object import fqn, update
from .store  import store


lock = threading.RLock()
p    = os.path.join


class Error(Exception):

    pass


class Cache:

    objs = {}

    @staticmethod
    def add(path, obj) -> None:
        Cache.objs[path] = obj

    @staticmethod
    def get(path):
        return Cache.objs.get(path, None)

    @staticmethod
    def typed(matcher) -> []:
        for key in Cache.objs:
            if matcher not in key:
                continue
            yield Cache.objs.get(key)



def cdir(path) -> None:
    pth = pathlib.Path(path)
    pth.parent.mkdir(parents=True, exist_ok=True)


def getpath(obj):
    return p(store(ident(obj)))


def ident(obj) -> str:
    return p(fqn(obj),*str(datetime.datetime.now()).split())


def read(obj, path) -> str:
    with lock:
        with open(path, "r", encoding="utf-8") as fpt:
            try:
                update(obj, load(fpt))
            except json.decoder.JSONDecodeError as ex:
                raise Error(path) from ex
    return path


def write(obj, path=None) -> str:
    with lock:
        if path is None:
            path = getpath(obj)
        cdir(path)
        with open(path, "w", encoding="utf-8") as fpt:
            dump(obj, fpt, indent=4)
        return path


def __dir__():
    return (
        'Cache',
        'Error',
        'cdir',
        'getpath',
        'ident',
        'read',
        'write'
    )
