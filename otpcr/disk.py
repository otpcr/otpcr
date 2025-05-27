# This file is placed in the Public Domain.


"persistence"


import datetime
import json.decoder
import os
import pathlib
import threading


from .json   import dump, load
from .object import fqn, update
from .store  import store


lock = threading.RLock()
j    = os.path.join


class Error(Exception):

    pass


class Cache:

    objs = {}

    @staticmethod
    def add(path, obj):
        Cache.objs[path] = obj

    @staticmethod
    def get(path):
        return Cache.objs.get(path, None)

    @staticmethod
    def typed(matcher):
        for key in Cache.objs:
            if matcher not in key:
                continue
            yield Cache.objs.get(key)


def cdir(path):
    pth = pathlib.Path(path)
    pth.parent.mkdir(parents=True, exist_ok=True)


def getpath(obj):
    return j(store(ident(obj)))


def ident(obj):
    return j(fqn(obj),*str(datetime.datetime.now()).split())


def read(obj, path):
    with lock:
        with open(path, "r", encoding="utf-8") as fpt:
            try:
                update(obj, load(fpt))
            except json.decoder.JSONDecodeError as ex:
                raise Error(path) from ex


def write(obj, path=""):
    with lock:
        if path == "":
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
