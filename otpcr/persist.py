# This file is placed in the Public Domain.


"persistence"


import datetime
import os
import json
import pathlib
import threading


from .caching import Cache
from .decoder import loads
from .encoder import dumps
from .objects import fqn, update
from .workdir import store


p    = os.path.join
lock = threading.RLock()


class DecodeError(Exception):

    """ DecodeError """


def cdir(pth) -> None:
    """ create directory. """
    path = pathlib.Path(pth)
    path.parent.mkdir(parents=True, exist_ok=True)


def ident(obj) -> str:
    """ return path to save object to. """
    return p(fqn(obj),*str(datetime.datetime.now()).split())


def read(obj, pth):
    """ read object fron path. """
    with lock:
        with open(pth, 'r', encoding='utf-8') as ofile:
            try:
                obj2 = loads(ofile.read())
                update(obj, obj2)
            except json.decoder.JSONDecodeError as ex:
                raise DecodeError(pth) from ex
    return pth


def write(obj, pth=None):
    """ write object to provided path or freshly created one. """
    with lock:
        if pth is None:
            pth = store(ident(obj))
        cdir(pth)
        txt = dumps(obj, indent=4)
        Cache.objs[pth] = obj
        with open(pth, 'w', encoding='utf-8') as ofile:
            ofile.write(txt)
    return pth


def __dir__():
    return (
        'cdir',
        'ident',
        'read',
        'write'
    )
