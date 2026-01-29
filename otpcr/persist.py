# This file is placed in the Public Domain.


"persistence through storage"


import datetime
import json
import os
import pathlib
import threading
import time


from .encoder import dump, load
from .methods import fqn
from .objects import Object, items, keys, update


lock = threading.RLock()


class Cache:

    paths = {}


def addpath(path, obj):
    "put object into cache."
    Cache.paths[path] = obj


def getpath(path):
    "get object from cache."
    return Cache.paths.get(path, None)


def syncpath(path, obj):
    "update cached object."
    try:
        update(Cache.paths[path], obj)
    except KeyError:
        addpath(path, obj)


"workdir"


class Workdir:

    wdr = ""


def setwd(path):
    "enable writing to disk."
    Workdir.wdr = path
    skel()


def kinds():
    "show kind on objects in cache."
    return os.listdir(os.path.join(Workdir.wdr, "store"))


def long(name):
    "expand to fqn."
    split = name.split(".")[-1].lower()
    res = name
    for names in kinds():
        if split == names.split(".")[-1].lower():
            res = names
            break
    return res


def pidfile(name):
    "write pidfile."
    filename = os.path.join(Workdir.wdr, f"{name}.pid")
    if os.path.exists(filename):
        os.unlink(filename)
    path2 = pathlib.Path(filename)
    path2.parent.mkdir(parents=True, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as fds:
        fds.write(str(os.getpid()))


def skel():
    "create directories."
    if not Workdir.wdr:
        return
    path = os.path.abspath(Workdir.wdr)
    workpath = os.path.join(path, "store")
    pth = pathlib.Path(workpath)
    pth.mkdir(parents=True, exist_ok=True)
    modpath = os.path.join(path, "mods")
    pth = pathlib.Path(modpath)
    pth.mkdir(parents=True, exist_ok=True)


def workdir():
    "return workdir."
    return Workdir.wdr


"disk"


def read(obj, path):
    "read object from path."
    with lock:
        pth = os.path.join(Workdir.wdr, "store", path)
        with open(pth, "r", encoding="utf-8") as fpt:
            try:
                update(obj, load(fpt))
            except json.decoder.JSONDecodeError as ex:
                ex.add_note(path)
                raise ex



def write(obj, path=""):
    "write object to disk."
    with lock:
        if path == "":
            path = ident(obj)
        pth = os.path.join(Workdir.wdr, "store", path)
        cdir(pth)
        with open(pth, "w", encoding="utf-8") as fpt:
            dump(obj, fpt, indent=4)
        syncpath(path, obj)
        return path


"locate"


def attrs(kind):
    "show attributes for kind of objects."
    pth, obj = find(kind, nritems=1)
    if obj:
        return list(keys(obj))
    return []


def find(kind, selector={}, removed=False, matching=False, nritems=None):
    "locate objects by matching atributes."
    nrs = 0
    res = []
    for pth in fns(long(kind)):
        obj = getpath(pth)
        if not obj:
            obj = Object()
            read(obj, pth)
            addpath(pth, obj)
        if not removed and deleted(obj):
            continue
        if selector and not search(obj, selector, matching):
            continue
        if nritems and nrs >= nritems:
            break
        nrs += 1
        res.append((pth, obj))
    return res


def fns(kind):
    "file names by kind of object."
    path = os.path.join(Workdir.wdr, "store", kind)
    for rootdir, dirs, _files in os.walk(path, topdown=True):
        for dname in dirs:
            if dname.count("-") != 2:
                continue
            ddd = os.path.join(rootdir, dname)
            for fll in os.listdir(ddd):
                yield strip(os.path.join(ddd, fll))


def last(obj, selector={}):
    "last saved version."
    result = sorted(
                    find(fqn(obj), selector),
                    key=lambda x: fntime(x[0])
                   )
    res = ""
    if result:
        inp = result[-1]
        update(obj, inp[-1])
        res = inp[0]
    return res


"utilities"


def cdir(path):
    "create directory."
    pth = pathlib.Path(path)
    pth.parent.mkdir(parents=True, exist_ok=True)


def deleted(obj):
    "check whether obj had deleted flag set."
    return "__deleted__" in dir(obj) and obj.__deleted__


def fntime(daystr):
    "time from path."
    datestr = " ".join(daystr.split(os.sep)[-2:])
    datestr = datestr.replace("_", " ")
    if "." in datestr:
        datestr, rest = datestr.rsplit(".", 1)
    else:
        rest = ""
    timd = time.mktime(time.strptime(datestr, "%Y-%m-%d %H:%M:%S"))
    if rest:
        timd += float("." + rest)
    return float(timd)


def ident(obj):
    "return ident string for object."
    return os.path.join(fqn(obj), *str(datetime.datetime.now()).split())


def search(obj, selector={}, matching=False):
    "check whether object matches search criteria."
    res = False
    for key, value in items(selector):
        val = getattr(obj, key, None)
        if not val:
            res = False
            break
        if matching and value != val:
            res = False
            break
        if str(value).lower() not in str(val).lower():
            res = False
            break
        res = True
    return res


def strip(path):
    "strip filename from path."
    return path.split('store')[-1][1:]


"interface"


def __dir__():
    return (
        'Cache',
        'Workdir',
        'addpath',
        'find',
        'getpath',
        'kinds',
        'last',
        'pidfile',
        'read',
        'setwd',
        'skel',
        'strip',
        'syncpath',
        'workdir',
        'write'
    )
