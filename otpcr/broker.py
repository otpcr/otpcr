# This file is placed in the Public Domain.
# pylint: disable=R.W0105,W0212,W0718


"client"


class Broker:

    "Broker"

    objs = {}

    @staticmethod
    def add(obj, key):
        "add object."
        Broker.objs[key] = obj

    @staticmethod
    def all(kind=None):
        "return all objects."
        if kind is not None:
            for key in [x for x in Broker.objs if kind in x]:
                yield Broker.get(key)
        return Broker.objs.values()

    @staticmethod
    def get(orig):
        "return object by matching repr."
        return Broker.objs.get(orig)


def __dir__():
    return (
        'Broker',
    )
