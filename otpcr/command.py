# This file is placed in the Public Domain.


"write your own commands"


import inspect


from .objects import Methods
from .package import Mods
from .utility import Utils


class Commands:

    cmds = {}
    names = {}
    skips = {}

    @classmethod
    def add(cls, *args):
        "add functions to commands."
        for func in args:
            name = func.__name__
            cls.cmds[name] = func
            modname = func.__module__.split(".")[-1]
            if "__" in modname or name in ["tbl", "srv"]:
                continue
            cls.names[name] = modname
            if "skip" in dir(func):
                cls.skips[name] = func.skip

    @classmethod
    def command(cls, evt):
        "command callback."
        Methods.parse(evt, evt.text)
        if cls.skip(evt.orig, cls.skips.get(evt.cmd, "")):
            evt.ready()
            return
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
    def commands(cls, orig):
        "list cpmmands available."
        res = []
        for nme in cls.names:
            skp = cls.skips.get(nme, False)
            if skp and cls.skip(orig, skp):
                continue
            res.append(nme)
        return res

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
    def scanner(cls):
        "scan named modules for commands."
        for name, mod in Mods.iter(Mods.list()):
            cls.scan(mod)

    @classmethod
    def skip(cls, orig, skips):
        for skp in Utils.spl(skips):
            if skp.lower() in orig.lower():
                return True
        return False

    @classmethod
    def table(cls):
        mod = Mods.get("tbl")
        names = getattr(mod, "NAMES", None)
        if names:
            cls.names.update(names)
        skips = getattr(mod, "SKIPS", None)
        if skips:
            cls.skips.update(skips)


def __dir__():
    return (
        'Commands',
    )
