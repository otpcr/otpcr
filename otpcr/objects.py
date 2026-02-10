# This file is placed in the Public Domain.


"a clean namespace"


import datetime
import os
import types


"exceptions"


class Reserved(Exception):

    pass


"object"


class Object:

    def __contains__(self, key):
        return key in dir(self)

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __str__(self):
        return str(self.__dict__)


class Default(Object):

    def __getattr__(self, key):
        return self.__dict__.get(key, "")


class Config(Default):

    def __init__(self, *args, **kwargs):
        super().__init__()
        if args:
           Dict.update(self, args[0])
        if kwargs:
           Dict.update(self, kwargs)


"dict"


class Dict:

    @staticmethod
    def clear(obj):
        "remove all items from the object."
        obj.__dict__.clear()


    @staticmethod
    def construct(obj, *args, **kwargs):
        "object contructor."
        if args:
            val = args[0]
            if isinstance(val, zip):
                Dict.update(obj, dict(val))
            elif isinstance(val, dict):
                Dict.update(obj, val)
            else:
                Dict.update(obj, vars(val))
        if kwargs:
            Dict.update(obj, kwargs)

    @staticmethod
    def copy(obj):
        "return shallow copy of the object."
        oobj = type(obj)()
        Dict.update(oobj, obj.__dict__.copy())
        return oobj

    @staticmethod
    def fromkeys(obj, keyz, value=None):
        "create a new object with keys from iterable and values set to value/"
        return obj.__dict__.fromkeys(keyz, value)

    @staticmethod
    def get(obj, key, default=None):
        "return value for key if key is in the object, otherwise return default."
        return obj.__dict__.get(key, default)

    @staticmethod
    def items(obj):
        "object's key,value pairs."
        if isinstance(obj, dict):
            return obj.items()
        if isinstance(obj, types.MappingProxyType):
            return obj.items()
        return obj.__dict__.items()

    @staticmethod
    def keys(obj):
        "object's keys."
        if isinstance(obj, dict):
            return obj.keys()
        if isinstance(obj, types.MappingProxyType):
            return obj.keys()
        return obj.__dict__.keys()

    @staticmethod
    def pop(obj, key, default=None):
        "remove key from object and return it's value. return default or KeyError."
        return obj.__dict__.pop(key, default)

    @staticmethod
    def popitem(obj):
        "remove and return (key, value) pair."
        return obj.__dict__.popitem()

    @staticmethod
    def update(obj, data, empty=True):
        "update object,"
        if isinstance(obj, dict):
            obj.update(data)
        elif isinstance(obj.__dict__, types.MappingProxyType):
            for key, value in data.items():
                setattr(obj, key, value)
        elif isinstance(data, dict):
            obj.__dict__.update(data)
        else:
            obj.__dict__.update(data.__dict__)

    @staticmethod
    def values(obj):
        "object's values."
        if isinstance(obj, dict):
            return obj.values()
        elif isinstance(obj.__dict__, types.MappingProxyType):
            res = []
            for key in obj.__dict__:
                res.append(obj[key])
            return res
        return obj.__dict__.values()


"methods"


class Methods:

    @staticmethod
    def deleted(obj):
        "check whether obj had deleted flag set."
        return "__deleted__" in dir(obj) and obj.__deleted__

    @staticmethod
    def edit(obj, setter={}, skip=False):
        "update object with dict."
        for key, val in Dict.items(setter):
            if skip and val == "":
                continue
            Methods.typed(obj, key, val)

    @staticmethod
    def fmt(obj, args=[], skip=[], plain=False, empty=False):
        "format object info printable string."
        if args == []:
            args = list(obj.__dict__.keys())
        txt = ""
        for key in args:
            if key.startswith("__"):
                continue
            if key in skip:
                continue
            value = getattr(obj, key, None)
            if value is None:
                continue
            if not empty and not value:
                continue
            if plain:
                txt += f"{value} "
            elif isinstance(value, (int, float, dict, bool, list)):
                txt += f"{key}={value} "
            elif isinstance(value, str):
                txt += f'{key}="{value}" '
            else:
                txt += f"{key}={Methods.fqn(value)}((value))"
        if txt == "":
            txt = "{}"
        return txt.strip()

    @staticmethod
    def fqn(obj):
        "full qualified name."
        kin = str(type(obj)).split()[-1][1:-2]
        if kin == "type":
            kin = f"{obj.__module__}.{obj.__name__}"
        return kin

    @staticmethod
    def ident(obj):
        "return ident string for object."
        return os.path.join(Methods.fqn(obj), *str(datetime.datetime.now()).split())

    @staticmethod
    def parse(obj, text):
        "parse text for command."
        data = {
            "args": [],
            "cmd": "",
            "gets": Default(),
            "index": None,
            "init": "",
            "opts": "",
            "otxt": text,
            "rest": "",
            "silent": Default(),
            "sets": Default(),
            "text": text
        }
        for k, v in data.items():
            setattr(obj, k, getattr(obj, k, v) or v)
        args = []
        nr = -1
        for spli in text.split():
            if spli.startswith("-"):
                try:
                    obj.index = int(spli[1:])
                except ValueError:
                    obj.opts += spli[1:]
                continue
            if "-=" in spli:
                key, value = spli.split("-=", maxsplit=1)
                Methods.typed(obj.silent, key, value)
                Methods.typed(obj.gets, key, value)
                continue
            if "==" in spli:
                key, value = spli.split("==", maxsplit=1)
                Methods.typed(obj.gets, key, value)
                continue
            if "=" in spli:
                key, value = spli.split("=", maxsplit=1)
                Methods.typed(obj.sets, key, value)
                continue
            nr += 1
            if nr == 0:
                obj.cmd = spli
                continue
            args.append(spli)
        if args:
            obj.args = args
            obj.text  = obj.cmd or ""
            obj.rest = " ".join(obj.args)
            obj.text  = obj.cmd + " " + obj.rest
        else:
            obj.text = obj.cmd or ""

    @staticmethod
    def search(obj, selector={}, matching=False):
        "check whether object matches search criteria."
        res = False
        for key, value in Dict.items(selector):
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

    @staticmethod
    def skip(obj, chars="_"):
        "skip keys containing chars."
        res = {}
        for key, value in Dict.items(obj):
            next = False
            for char in chars:
                if char in key:
                    next = True
            if next:
                continue
            res[key] = value
        return res

    @staticmethod
    def typed(obj, key, val):
        "assign proper types."
        try:
            setattr(obj, key, int(val))
            return
        except ValueError:
            pass
        try:
            setattr(obj, key, float(val))
            return
        except ValueError:
           pass
        if val in ["True", "true", True]:
            setattr(obj, key, True)
        elif val in ["False", "false", False]:
            setattr(obj, key, False)
        else:
            setattr(obj, key, val)


"interface"


def __dir__():
    return (
        'Config',
        'Default',
        'Dict',
        'Methods',
        'Object'
    )
