# This file is placed in the Public Domain.


"persistence through storage"


import json.decoder
import logging
import os
import pathlib
import threading


from .configs import Main
from .encoder import Json
from .objects import Base, Methods, Object
from .utility import Time, Utils


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


class Cfg:

    @classmethod
    def load(cls, obj, name=""):
        if not name:
            name = Utils.modname(obj)
        return Disk.read(obj, name, "config")

    @classmethod
    def save(cls, obj, name=""):
        return Disk.write(obj, name, "config")


class Disk:

    lock = threading.RLock()

    @classmethod
    def cdir(cls, path):
        "create directory."
        if os.path.exists(path):
            return
        pth = pathlib.Path(path)
        if not os.path.exists(pth.parent):
            pth.parent.mkdir(parents=True, exist_ok=True)

    @classmethod
    def read(cls, obj, path, base="store", error=False):
        "read object from path."
        with cls.lock:
            pth = os.path.join(Main.wdr, base, path)
            if not os.path.exists(pth):
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
                path = Methods.ident(obj)
            pth = os.path.join(Main.wdr, base, path)
            Disk.cdir(pth)
            with open(pth, "w", encoding="utf-8") as fpt:
                Json.dump(obj, fpt, indent=4)
            Cache.sync(path, obj)
            return path


class Locate:

    @classmethod
    def attrs(cls, kind):
        "show attributes for kind of objects."
        result = []
        for pth, obj in Locate.find(kind, nritems=1):
            result.extend(Object.keys(obj))
        return set(result)

    @classmethod
    def count(cls, kind):
        "count kinds of objects."
        return len(list(Locate.find(kind)))

    @classmethod
    def find(cls, kind, selector={}, removed=False, matching=False, nritems=None):
        "locate objects by matching atributes."
        nrs = 0
        Workdir.skel()
        for pth in Locate.fns(Workdir.long(kind)):
            obj = Cache.get(pth)
            if obj is None:
                obj = Base()
                Disk.read(obj, pth)
                Cache.add(pth, obj)
            if not removed and Methods.deleted(obj):
                continue
            if selector and not Methods.search(obj, selector, matching):
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
                        Locate.find(Methods.fqn(obj), selector),
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
        path = os.path.join(Main.wdr, "store", kind)
        for rootdir, dirs, _files in os.walk(path, topdown=True):
            for dname in dirs:
                if dname.count("-") != 2:
                    continue
                ddd = os.path.join(rootdir, dname)
                for fll in os.listdir(ddd):
                    yield cls.strip(os.path.join(ddd, fll))

    @classmethod
    def last(cls, obj, selector={}):
        "last saved version."
        result = sorted(
                        cls.find(Methods.fqn(obj), selector),
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


class Table:

    @classmethod
    def load(cls, obj, name=""):
        return Disk.read(obj, name or Utils.modname(obj), "tables")

    @classmethod
    def save(cls, obj, name=""):
        return Disk.write(obj, name or Utils.modname(obj), "tables")


class Workdir:

    @staticmethod
    def kinds():
        "show kind on objects in cache."
        path = os.path.join(Main.wdr, "store")
        if os.path.exists(path):
            return os.listdir(path)

    @staticmethod
    def long(name):
        "expand to fqn."
        if "." in name:
            return name
        split = name.split(".")[-1].lower()
        res = name
        for names in Workdir.kinds():
            if split == names.split(".")[-1].lower():
                res = names
                break
        return res

    @staticmethod
    def skel():
        "create directories."
        if not Main.wdr:
            return
        if not os.path.exists(Main.wdr):
            Disk.cdir(Main.wdr)
        path = os.path.abspath(Main.wdr)
        for wpth in ["config", "mods", "store"]:
            pth = pathlib.Path(os.path.join(path, wpth))
            pth.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def workdir(path=""):
        "return workdir."
        return os.path.join(Main.wdr, path)


def __dir__():
    return (
        'Cfg',
        'Disk',
        'Locate',
        'Yable',
        'Workdir',
        'd',
        'e',
        'j'
    )
