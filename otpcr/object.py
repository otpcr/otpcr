# This file is placed in the Public Domain.


"a clean namespace"


class Object:

    def __contains__(self, key):
        return key in dir(self)

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __str__(self):
        return str(self.__dict__)


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


def fqn(obj) -> str:
    kin = str(type(obj)).split()[-1][1:-2]
    if kin == "type":
        kin = f"{obj.__module__}.{obj.__name__}"
    return kin


def items(obj) -> []:
    if isinstance(obj,type({})):
        return obj.items()
    return obj.__dict__.items()


def keys(obj) -> [str]:
    if isinstance(obj, type({})):
        return obj.keys()
    return list(obj.__dict__.keys())


def update(obj, data) -> None:
    if not isinstance(data, type({})):
        obj.__dict__.update(vars(data))
    else:
        obj.__dict__.update(data)


def values(obj) -> []:
    return obj.__dict__.values()


def __dir__():
    return (
        'Object',
        'construct',
        'fqn',
        'items',
        'keys',
        'update',
        'values'
    )
