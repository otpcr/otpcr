# This file is placed in the Public Domain.
# pylint: disable=R


"command"


import inspect


from .object   import Default
from .utils  import spl


class Event(Default):

    "Event"

    def __init__(self):
        Default.__init__(self)
        self._thr   = None
        self.orig   = ""
        self.result = []
        self.txt    = ""
        self.type = "event"

    def reply(self, txt):
        "add text to the result."
        self.result.append(txt)


class Commands:

    "Commands"

    cmds     = {}
    modnames = {}

    @staticmethod
    def add(func):
        "add command."
        Commands.cmds[func.__name__] = func
        if func.__module__ != "__main__":
            Commands.modnames[func.__name__] = func.__module__


def command(bot, evt, txt=""):
    "check for and run a command."
    parse(evt, txt or evt.txt)
    func = Commands.cmds.get(evt.cmd, None)
    if func:
        func(evt)
        bot.display(evt)


def parse(obj, txt):
    "parse a string for a command."
    if txt is None:
        txt = ""
    args = []
    obj.args    = []
    obj.cmd     = ""
    obj.gets    = Default()
    obj.hasmods = False
    obj.index   = None
    obj.mod     = ""
    obj.opts    = ""
    obj.result  = []
    obj.sets    = Default()
    obj.txt     = txt
    obj.otxt    = txt
    _nr = -1
    for spli in obj.otxt.split():
        if spli.startswith("-"):
            try:
                obj.index = int(spli[1:])
            except ValueError:
                obj.opts += spli[1:]
            continue
        if "==" in spli:
            key, value = spli.split("==", maxsplit=1)
            val = getattr(obj.gets, key, None)
            if val:
                value = val + "," + value
                setattr(obj.gets, key, value)
            continue
        if "=" in spli:
            key, value = spli.split("=", maxsplit=1)
            if key == "mod":
                obj.hasmods = True
                if obj.mod:
                    obj.mod += f",{value}"
                else:
                    obj.mod = value
                continue
            setattr(obj.sets, key, value)
            continue
        _nr += 1
        if _nr == 0:
            obj.cmd = spli
            continue
        args.append(spli)
    if args:
        obj.args = args
        obj.txt  = obj.cmd or ""
        obj.rest = " ".join(obj.args)
        obj.txt  = obj.cmd + " " + obj.rest
    else:
        obj.txt = obj.cmd or ""
    return obj


def scan(mod):
    "Scan module for commands."
    for key, cmnd in inspect.getmembers(mod, inspect.isfunction):
        if key.startswith('cb'):
            continue
        names = cmnd.__code__.co_varnames
        if 'event' in names:
            Commands.add(cmnd)


def scanner(modstr, *pkgs, disable=None):
    "scan modules for commands and classes"
    mods = []
    for mod in spl(modstr):
        if disable and mod in spl(disable):
            continue
        for pkg in pkgs:
            modi = getattr(pkg, mod, None)
            if not modi:
                continue
            scan(modi)
            mods.append(modi)
            break
    return mods


def __dir__():
    return (
        'Commands',
        'EVent',
        'command',
        'scan'
    )
