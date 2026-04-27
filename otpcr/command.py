# This file is placed in the Public Domain.


"write your own commands"


import inspect


from .objects import Methods
from .package import Mods


class Commands:

    cmds = {}
    names = {}

    @classmethod
    def add(cls, *args):
        "add functions to commands."
        for func in args:
            name = func.__name__
            cls.cmds[name] = func
            modname = func.__module__.split(".")[-1]
            if "__" in modname:
                continue
            cls.names[name] = modname

    @classmethod
    def command(cls, evt):
        "command callback."
        Methods.parse(evt, evt.text)
        func = cls.get(evt.cmd)
        if not func:
            name = cls.names.get(evt.cmd)
            mod = None
            if name:
                mod = Mods.get(name)
            if mod:
                cls.scan(mod)
                func = cls.get(evt.cmd)
        if func:
            func(evt)
            evt.display()
        evt.ready()

    @classmethod
    def commands(cls, ignore=""):
        "list cpmmands available."
        return [x for x in cls.names if cls.names.get(x) not in ignore]

    @classmethod
    def get(cls, cmd):
        "get function for command."
        return cls.cmds.get(cmd, None)

    @classmethod
    def scan(cls, module):
        "scan a module for functions with event as argument."
        for key, cmdz in inspect.getmembers(module, inspect.isfunction):
            if 'event' in inspect.signature(cmdz).parameters:
                cls.add(cmdz)

    @classmethod
    def table(cls):
        "load names from table."
        mod = Mods.get("tbl")
        names = getattr(mod, "NAMES", None)
        if names:
            cls.names.update(names)


def __dir__():
    return (
        'Commands',
    )
