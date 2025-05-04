# This file is placed in the Public Domain.


"read/write"


import datetime
import os
import pathlib
import threading


from .object import fqn


lock = threading.RLock()
p    = os.path.join


class Workdir:

    name = __file__.rsplit(os.sep, maxsplit=2)[-2]
    wdr  = ""


def long(name) -> str:
    split = name.split(".")[-1].lower()
    res = name
    for names in types():
        if split == names.split(".")[-1].lower():
            res = names
            break
    return res


def moddir():
    return p(Workdir.wdr, "mods")


def pidname(name) -> str:
    return p(Workdir.wdr, f"{name}.pid")


def skel() -> str:
    pth = pathlib.Path(store())
    pth.mkdir(parents=True, exist_ok=True)
    pth = pathlib.Path(moddir())
    pth.mkdir(parents=True, exist_ok=True)
    return pth


def setwd(pth):
    Workdir.wdr = pth


def store(pth="") -> str:
    return p(Workdir.wdr, "store", pth)


def strip(pth, nmr=2) -> str:
    return os.sep.join(pth.split(os.sep)[-nmr:])


def types() -> [str]:
    return os.listdir(store())


def wdr(pth):
    return p(Workdir.wdr, pth)


def __dir__():
    return (
        'Workdir',
        'long',
        'moddir',
        'pidname',
        'setwd',
        'skel',
        'store',
        'strip',
        'wdr'
    )
