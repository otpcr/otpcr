#!/usr/bin/env python3
# This file is placed in the Public Domain.
# pylint: disable=R,W0105,C0413,W0223,W0611,W0718


"command"


import time
import _thread


from .object  import Obj
from .runtime import Client, later, launch


NAME = __file__.rsplit("/", maxsplit=2)[-2]
STARTTIME = time.time()


class Config(Obj):

    "Config"


class Broker:

    "Broker"

    objs = {}

    @staticmethod
    def add(obj):
        "add object."
        Broker.objs[repr(obj)] = obj

    @staticmethod
    def announce(txt, kind=None):
        "announce text on brokered objects."
        for obj in Broker.all(kind):
            if "announce" in dir(obj):
                obj.announce(txt)

    @staticmethod
    def all(kind=None):
        "return all objects."
        result = []
        if kind is not None:
            for key in [x for x in Broker.objs if kind in x]:
                result.append(Broker.get(key))
        else:
            result.extend(list(Broker.objs.values()))
        return result

    @staticmethod
    def get(orig):
        "return object by matching repr."
        return Broker.objs.get(orig)



class CLI(Client):

    "CLI"

    def __init__(self):
        Client.__init__(self)
        Broker.add(self)
        self.register("event", command)


class Commands:

    "Commands"

    cmds = {}

    @staticmethod
    def add(func):
        "add command."
        Commands.cmds[func.__name__] = func


def command(bot, evt):
    "check for and run a command."
    parse(evt, evt.txt)
    evt.orig = repr(bot)
    func = Commands.cmds.get(evt.cmd, None)
    if func:
        try:
            func(evt)
            bot.display(evt)
        except Exception as ex:
            later(ex)
    evt.ready()


def parse(obj, txt=None):
    "parse a string for a command."
    if txt is None:
        txt = ""
    args = []
    obj.args    = []
    obj.cmd     = ""
    obj.gets    = Obj()
    obj.hasmods = False
    obj.index   = None
    obj.mod     = ""
    obj.opts    = ""
    obj.result  = []
    obj.sets    = Obj()
    obj.txt     = txt or ""
    obj.otxt    = obj.txt
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



def forever():
    "it doesn't stop, until ctrl-c"
    while True:
        try:
            time.sleep(1.0)
        except (KeyboardInterrupt, EOFError):
            _thread.interrupt_main()


def init(*pkgs):
    "run the init function in modules."
    mods = []
    for pkg in pkgs:
        for modname in dir(pkg):
            if modname.startswith("__"):
                continue
            modi = getattr(pkg, modname)
            if "init" not in dir(modi):
                continue
            thr = launch(modi.init)
            mods.append((modi, thr))
    return mods


def wrap(func):
    "reset console."
    try:
        func()
    except (KeyboardInterrupt, EOFError):
        pass
    except Exception as ex:
        later(ex)


def __dir__():
    return (
        'CLI',
        'Broker',
        'Commands',
        'Config',
        'command',
        'forever',
        'init',
        'parse',
        'wrap'
    )
