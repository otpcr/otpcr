# This file is placed in the Public Domain.


"configurations"


from .objects import Object
from .utility import Utils


class MainConfig(type):

    def __getattr__(cls, key):
        if key in dir(cls):
            return cls.__getattribute__(cls, key)
        return ""

    def __str__(cls):
        return str(Object.skip(cls.__dict__))


class Main(metaclass=MainConfig):

    name = Utils.pkgname(Object)


def __dir__():
    return (
        'Main',
    )
