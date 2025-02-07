# This file is placed in the Public Domain.


"encoder"


import json


from .objects import Object


class ObjectEncoder(json.JSONEncoder):

    """ ObjectEncoder """

    def __init__(self, *args, **kwargs):
        json.JSONEncoder.__init__(self, *args, **kwargs)

    def default(self, o) -> str:
        """ return representable string of an object. """
        if isinstance(o, dict):
            return o.items()
        if issubclass(type(o), Object):
            return vars(o)
        if isinstance(o, list):
            return iter(o)
        try:
            return json.JSONEncoder.default(self, o)
        except TypeError:
            try:
                return vars(o)
            except TypeError:
                return repr(o)


def dumps(*args, **kw):
    """ dumps object to string. """
    kw["cls"] = ObjectEncoder
    return json.dumps(*args, **kw)


def __dir__():
    return (
        'ObjectEncoder',
        'dumps'
    )
