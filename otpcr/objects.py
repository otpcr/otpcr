# This file is placed in the Public Domain.


"a clean namespace"


import types


class Reserved(Exception):

    pass


class Object:

    def __contains__(self, key):
        return key in dir(self)

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __str__(self):
        return str(self.__dict__)


def clear(obj):
    "remove all items from the object."
    obj.__dict__.clear()


def construct(obj, *args, **kwargs):
    "object contructor."
    if args:
        val = args[0]
        if isinstance(val, zip):
            update(obj, dict(val))
        elif isinstance(val, dict):
            update(obj, val)
        else:
            update(obj, vars(val))
    if kwargs:
        update(obj, kwargs)


def copy(obj):
    "return shallow copy of the object."
    oobj = type(obj)()
    update(oobj, obj.__dict__.copy())
    return oobj


def fromkeys(obj, keyz, value=None):
    "create a new object with keys from iterable and values set to value/"
    return obj.__dict__.fromkeys(keyz, value)


def get(obj, key, default=None):
    "return value for key if key is in the object, otherwise return default."
    return obj.__dict__.get(key, default)


def items(obj):
    "object's key,value pairs."
    if isinstance(obj, dict):
        return obj.items()
    if isinstance(obj, types.MappingProxyType):
        return obj.items()
    return obj.__dict__.items()


def keys(obj):
    "object's keys."
    if isinstance(obj, dict):
        return obj.keys()
    if isinstance(obj, types.MappingProxyType):
        return obj.keys()
    return obj.__dict__.keys()


def pop(obj, key, default=None):
    "remove key from object and return it's value. return default or KeyError."
    return obj.__dict__.pop(key, default)


def popitem(obj):
    "remove and return (key, value) pair."
    return obj.__dict__.popitem()


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


"default"


class Default(Object):

    def __getattr__(self, key):
        return self.__dict__.get(key, "")


"interface"


def __dir__():
    return (
        'Default',
        'Object',
        'clear',
        'construct',
        'copy',
        'fromkeys',
        'get',
        'items',
        'keys',
        'pop',
        'popitem',
        'setdefault',
        'update',
        'values'
    )
