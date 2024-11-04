# This file is placed in the Public Domain.
# pylint: disable=C,R,W0105,W0622


"a clean namespace"


import json


"classes"


class Object:

    def __contains__(self, key):
        return key in dir(self)

    def __getstate__(self) -> None:
        pass

    def __iter__(self) -> list:
        return iter(self.__dict__)

    def __len__(self) -> int:
        return len(self.__dict__)

    def __str__(self) -> str:
        return str(self.__dict__)


class Obj(Object):

    def __getattr__(self, key):
        return self.__dict__.get(key, "")


"methods"


def construct(obj, *args, **kwargs) -> None:
    if args:
        val = args[0]
        if isinstance(val, zip):
            update(obj, dict(val))
        elif isinstance(val, dict):
            update(obj, val)
        elif isinstance(val, Object):
            update(obj, vars(val))
    if kwargs:
        update(obj, kwargs)


def edit(obj, setter, skip=False) -> None:
    for key, val in items(setter):
        if skip and val == "":
            continue
        try:
            setattr(obj, key, int(val))
            continue
        except ValueError:
            pass
        try:
            setattr(obj, key, float(val))
            continue
        except ValueError:
            pass
        if val in ["True", "true"]:
            setattr(obj, key, True)
        elif val in ["False", "false"]:
            setattr(obj, key, False)
        else:
            setattr(obj, key, val)


def format(obj, args=None, skip=None, plain=False) -> str:
    if args is None:
        args = keys(obj)
    if skip is None:
        skip = []
    txt = ""
    for key in args:
        if key.startswith("__"):
            continue
        if key in skip:
            continue
        value = getattr(obj, key, None)
        if value is None:
            continue
        if plain:
            txt += f"{value} "
        elif isinstance(value, str) and len(value.split()) >= 2:
            txt += f'{key}="{value}" '
        else:
            txt += f'{key}={value} '
    return txt.strip()



def items(obj) -> dict:
    if isinstance(obj,type({})):
        return obj.items()
    else:
        return obj.__dict__.items()


def keys(obj) -> list:
    if isinstance(obj, type({})):
        return obj.keys()
    return list(obj.__dict__.keys())


def match(obj, txt) -> list:
    for key in keys(obj):
        if txt in key:
            yield key


def search(obj, selector, matching=None) -> bool:
    res = False
    if not selector:
        return res
    for key, value in items(selector):
        val = getattr(obj, key, None)
        if not val:
            continue
        if matching and value == val:
            res = True
        elif str(value).lower() in str(val).lower():
            res = True
        else:
            res = False
            break
    return res


def update(obj, data) -> None:
    if isinstance(data, type({})):
        obj.__dict__.update(data)
    else:
        obj.__dict__.update(vars(data))


def values(obj) -> list:
    return obj.__dict__.values()


"decoder"


class ObjectDecoder(json.JSONDecoder):

    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, *args, **kwargs)

    def decode(self, s, _w=None) -> Object:
        val = json.JSONDecoder.decode(self, s)
        if not val:
            val = {}
        return hook(val)

    def raw_decode(self, s, idx=0) -> Object:
        return json.JSONDecoder.raw_decode(self, s, idx)


def hook(objdict) -> Object:
    obj = Object()
    construct(obj, objdict)
    return obj


def load(fpt, *args, **kw) -> Object:
    kw["cls"] = ObjectDecoder
    kw["object_hook"] = hook
    return json.load(fpt, *args, **kw)


def loads(string, *args, **kw) -> Object:
    kw["cls"] = ObjectDecoder
    kw["object_hook"] = hook
    return json.loads(string, *args, **kw)


"encoder"


class ObjectEncoder(json.JSONEncoder):

    def __init__(self, *args, **kwargs):
        json.JSONEncoder.__init__(self, *args, **kwargs)

    def default(self, o):
        if isinstance(o, dict):
            return o.items()
        if isinstance(o, Object):
            return vars(o)
        if isinstance(o, list):
            return iter(o)
        if isinstance(o, (type(str), type(True), type(False), type(int), type(float))):
            return o
        try:
            return json.JSONEncoder.default(self, o)
        except TypeError:
            try:
                return o.__dict__
            except AttributeError:
                return repr(o)

    def encode(self, o) -> str:
        return json.JSONEncoder.encode(self, o)

    def iterencode(self, o, _one_shot=False) -> str:
        return json.JSONEncoder.iterencode(self, o, _one_shot)


def dump(*args, **kw) -> str:
    kw["cls"] = ObjectEncoder
    return json.dump(*args, **kw)


def dumps(*args, **kw) -> str:
    kw["cls"] = ObjectEncoder
    return json.dumps(*args, **kw)


"interface"


def __dir__():
    return (
        'Object',
        'construct',
        'dumps',
        'edit',
        'keys',
        'loads',
        'items',
        'match',
        'search',
        'update',
        'values',
    )
