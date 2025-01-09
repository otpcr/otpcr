# This file is placed in the Public Domain.
# pylint: disable=C,W0719,E0402


"read/write"


import datetime
import json
import os
import pathlib
import _thread


from .object import dumps, loads, update


lock = _thread.allocate_lock()
p    = os.path.join


def cdir(pth):
    path = pathlib.Path(pth)
    path.parent.mkdir(parents=True, exist_ok=True)


def doskel(pth):
    path = pathlib.Path(pth)
    path.mkdir(parents=True, exist_ok=True)
    return path


def ident(obj):
    return p(fqn(obj),*str(datetime.datetime.now()).split())


def fqn(obj):
    kin = str(type(obj)).split()[-1][1:-2]
    if kin == "type":
        kin = f"{obj.__module__}.{obj.__name__}"
    return kin


def read(obj, pth):
    with lock:
        with open(pth, 'r', encoding='utf-8') as ofile:
            try:
                obj2 = loads(ofile.read())
                update(obj, obj2)
            except json.decoder.JSONDecodeError as ex:
                raise Exception(pth) from ex
        return os.sep.join(pth.split(os.sep)[-3:])


def write(obj, pth):
    with lock:
        cdir(pth)
        txt = dumps(obj, indent=4)
        with open(pth, 'w', encoding='utf-8') as ofile:
            ofile.write(txt)
        return pth


def __dir__():
    return (
        'cdir',
        'doskel',
        'fqn',
        'ident',
        'read',
        'write'
    )
    