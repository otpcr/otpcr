# This file is placed in the Public Domain.


"persistence cache"


import json
import logging
import os
import pathlib
import threading


from .configs import Main
from .encoder import Json
from .objects import Base, Object
from .utility import Time, Utils, e, j


class Cache:

    paths = {}

    @classmethod
    def add(cls, path, obj):
        "put object into cache."
        cls.paths[path] = obj

    @classmethod
    def get(cls, path):
        "get object from cache."
        return cls.paths.get(path, None)

    @classmethod
    def sync(cls, path, obj):
        "update cached object."
        try:
            Object.update(cls.paths[path], obj)
        except KeyError:
            cls.add(path, obj)


class Disk:

    lock = threading.RLock()

    @classmethod
    def read(cls, obj, path, base="store", error=True):
        "read object from path."
        with cls.lock:
            pth = j(Workdir.wdr, base, path)
            if not e(pth):
                return False
            with open(pth, "r", encoding="utf-8") as fpt:
                try:
                    Object.update(obj, Json.load(fpt))
                except json.decoder.JSONDecodeError as ex:
                    logging.error("failed read at %s: %s", pth, str(ex))
                    if error:
                        raise
                    return False
            return True

    @classmethod
    def write(cls, obj, path="", base="store", skip=False):
        "write object to disk."
        with cls.lock:
            if path == "":
                path = Object.ident(obj)
            pth = j(Workdir.wdr, base, path)
            if not e(pth):
                Workdir.skel()
            Utils.cdir(pth)
            with open(pth, "w", encoding="utf-8") as fpt:
                Json.dump(obj, fpt, indent=4)
            Cache.sync(path, obj)
            return path


class Locate:

    lock = threading.RLock()

    @classmethod
    def attrs(cls, kind):
        "show attributes for kind of objects."
        result = []
        for pth, obj in cls.find(kind, nritems=1):
            result.extend(Object.keys(obj))
        return set(result)

    @classmethod
    def count(cls, kind):
        "count kinds of objects."
        return len(list(cls.find(kind)))

    @classmethod
    def find(cls, kind, selector={}, removed=False, matching=False, nritems=None):
        "locate objects by matching atributes."
        with cls.lock:
            nrs = 0
            for pth in cls.fns(Workdir.long(kind)):
                obj = Cache.get(pth)
                if obj is None:
                    obj = Base()
                    Disk.read(obj, pth)
                    Cache.add(pth, obj)
                if not removed and Object.deleted(obj):
                    continue
                if selector and not Object.search(obj, selector, matching):
                    continue
                if nritems and nrs >= nritems:
                    break
                nrs += 1
                yield pth, obj
            else:
                return None, None

    @classmethod
    def first(cls, obj, selector={}):
        "return first object of a kind."
        result = sorted(
                        cls.find(Object.fqn(obj), selector),
                        key=lambda x: Time.fntime(x[0])
                       )
        res = ""
        if result:
            inp = result[0]
            Object.update(obj, inp[-1])
            res = inp[0]
        return res

    @classmethod
    def fns(cls, kind):
        "file names by kind of object."
        path = j(Workdir.wdr, "store", kind)
        for rootdir, dirs, _files in os.walk(path, topdown=True):
            for dname in dirs:
                if dname.count("-") != 2:
                    continue
                ddd = j(rootdir, dname)
                for fll in os.listdir(ddd):
                    yield cls.strip(j(ddd, fll))

    @classmethod
    def last(cls, obj, selector={}):
        "last saved version."
        result = sorted(
                        cls.find(Object.fqn(obj), selector),
                        key=lambda x: Time.fntime(x[0])
                       )
        res = ""
        if result:
            inp = result[-1]
            Object.update(obj, inp[-1])
            res = inp[0]
        return res

    @classmethod
    def strip(cls, path):
        "strip filename from path."
        return path.split('store')[-1][1:]


class Workdir:

    wdr = f".{Main.name}"

    @classmethod
    def kinds(cls):
        "show kind on objects in cache."
        path = j(cls.wdr, "store")
        if not e(path):
            cls.skel()
        return os.listdir(path)

    @classmethod
    def long(cls, name):
        "expand to fqn."
        if "." in name:
            return name
        split = name.split(".")[-1].lower()
        res = name
        for names in cls.kinds():
            if split == names.split(".")[-1].lower():
                res = names
                break
        return res

    @classmethod
    def skel(cls):
        "create directories."
        if not cls.wdr:
            return
        if not e(cls.wdr):
            Utils.cdir(cls.wdr)
        path = os.path.abspath(cls.wdr)
        for wpth in ["config", "mods", "store"]:
            pth = pathlib.Path(j(path, wpth))
            pth.mkdir(parents=True, exist_ok=True)

    @classmethod
    def workdir(cls, path=""):
        "return workdir."
        return j(cls.wdr, path)


def __dir__():
    return (
        'Cache',
        'Disk',
        'Locate',
        'Workdir'
    )
