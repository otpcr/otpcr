# This file is placed in the Public Domain.
# pylint: disable=C,R,W0105,W0719,E1101


"persist to disk"


import datetime
import json
import os
import pathlib
import time
import _thread


from .object import Object, dump, load, search, update


"defines"


cachelock = _thread.allocate_lock()
disklock  = _thread.allocate_lock()
lock      = _thread.allocate_lock()
p         = os.path.join


"workdir"


class Workdir:

    fqns = []
    wdr = ''


def long(name) -> str:
    split = name.split(".")[-1].lower()
    res = name
    for names in types():
        if split == names.split(".")[-1].lower():
            res = names
            break
    return res


def modname() -> str:
    return p(Workdir.wdr, "mods")


def pidname(name) -> str:
    return p(Workdir.wdr, f"{name}.pid")


def store(pth="") -> str:
    stor = p(Workdir.wdr, "store", "")
    if not os.path.exists(stor):
        skel()
    return p(Workdir.wdr, "store", pth)


def whitelist(clz) -> None:
    Workdir.fqns.append(fqn(clz))


"cache"


class Cache:

    objs = {}

    @staticmethod
    def add(path, obj) -> None:
        with cachelock:
            Cache.objs[path] = obj

    @staticmethod
    def get(path) -> Object:
        with cachelock:
            return Cache.objs.get(path)

    @staticmethod
    def typed(match) -> list:
        with cachelock:
            for key in Cache.objs:
                if match not in key:
                    continue
                yield Cache.objs.get(key)


"utilities"


def cdir(pth) -> str:
    path = pathlib.Path(pth)
    path.parent.mkdir(parents=True, exist_ok=True)


def find(mtc, selector=None, index=None, deleted=False, matching=False) -> list:
    clz = long(mtc)
    nrs = -1
    for fnm in sorted(fns(clz), key=fntime):
        obj = Cache.get(fnm)
        if obj:
            yield (fnm, obj)
            continue
        obj = Object()
        read(obj, fnm)
        Cache.add(fnm, obj)
        if not deleted and '__deleted__' in dir(obj) and obj.__deleted__:
            continue
        if selector and not search(obj, selector, matching):
            continue
        nrs += 1
        if index is not None and nrs != int(index):
            continue
        yield (fnm, obj)


def fns(mtc="") -> list:
    dname = ''
    pth = store(mtc)
    for rootdir, dirs, _files in os.walk(pth, topdown=False):
        if dirs:
            for dname in sorted(dirs):
                if dname.count('-') == 2:
                    ddd = p(rootdir, dname)
                    for fll in os.scandir(ddd):
                        yield strip(p(ddd, fll))


def fntime(daystr) -> str:
    daystr = daystr.replace('_', ':')
    datestr = ' '.join(daystr.split(os.sep)[-2:])
    if '.' in datestr:
        datestr, rest = datestr.rsplit('.', 1)
    else:
        rest = ''
    timed = time.mktime(time.strptime(datestr, '%Y-%m-%d %H:%M:%S'))
    if rest:
        timed += float('.' + rest)
    return timed


def pidfile(filename) -> str:
    if os.path.exists(filename):
        os.unlink(filename)
    path2 = pathlib.Path(filename)
    path2.parent.mkdir(parents=True, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as fds:
        fds.write(str(os.getpid()))

def skel() -> str:
    stor = p(Workdir.wdr, "store", "")
    path = pathlib.Path(stor)
    path.mkdir(parents=True, exist_ok=True)


def strip(pth, nmr=3) -> str:
    return os.sep.join(pth.split(os.sep)[-nmr:])


def types() -> list:
    return os.listdir(store())


"methods"

def read(obj, pth) -> None:
    with disklock:
        fetch(obj, store(pth))


def fqn(obj) -> str:
    kin = str(type(obj)).split()[-1][1:-2]
    if kin == "type":
        kin = f"{obj.__module__}.{obj.__name__}"
    return kin


def ident(obj) -> str:
    return p(fqn(obj), *str(datetime.datetime.now()).split())


def last(obj, selector=None) -> Object:
    if selector is None:
        selector = {}
    result = sorted(
                    find(fqn(obj), selector),
                    key=lambda x: fntime(x[0])
                   )
    res = None
    if result:
        inp = result[-1]
        update(obj, inp[-1])
        res = inp[0]
    return res


def fetch(obj, pth) -> None:
    with lock:
        with open(pth, 'r', encoding='utf-8') as ofile:
            try:
                update(obj, load(ofile))
            except json.decoder.JSONDecodeError as ex:
                raise Exception(pth) from ex


def write(obj, pth) -> str:
    with disklock:
        sync(obj, store(pth))


def sync(obj, pth) -> None:
    with lock:
        cdir(pth)
        with open(pth, 'w', encoding='utf-8') as ofile:
            dump(obj, ofile, indent=4)


"interface"


def __dir__():
    return (
        'Workdir',
        'find',
        'fetch',
        'last',
        'read',
        'sync',
        'write'
    )
