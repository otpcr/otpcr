# This file is placed in the Public Domain.
# pylint: disable=C,R,W0105,W0212,W0718


"program helpers"


import inspect
import os
import threading
import time
import _thread


from .object  import Object, keys
from .persist import NAME, Workdir
from .runtime import Reactor, later, launch


Workdir.wdr = os.path.expanduser(f"~/.{NAME}")


"defaults"


class Default(Object):

    def __getattr__(self, key):
        return self.__dict__.get(key, "")


class Config(Default):

    pass


"commands"


class Commands:

    cmds = {}

    @staticmethod
    def add(func):
        Commands.cmds[func.__name__] = func

    @staticmethod
    def scan(mod):
        for key, cmdz in inspect.getmembers(mod, inspect.isfunction):
            if key.startswith("cb"):
                continue
            if 'event' in cmdz.__code__.co_varnames:
                Commands.add(cmdz)


def command(bot, evt):
    parse(evt, evt.txt)
    if "ident" in dir(bot):
        evt.orig = bot.ident
    funct = Commands.cmds.get(evt.cmd, None)
    if funct:
        try:
            funct(evt)
            bot.display(evt)
        except Exception as ex:
            later(ex)
    evt.ready()


def modloop(*pkgs, disable=""):
    for pkg in pkgs:
        for modname in dir(pkg):
            if modname in spl(disable):
                continue
            if modname.startswith("__"):
                continue
            yield getattr(pkg, modname)


def scanner(*pkgs, init=False, disable=""):
    result = []
    for mod in modloop(*pkgs, disable=disable):
        Commands.scan(mod)
        thr = None
        if init and "init" in dir(mod):
            thr = launch(mod.init)
        result.append((mod, thr))
    return result


"client"


class Client(Reactor):

    def __init__(self):
        Reactor.__init__(self)
        self.register("event", command)

    def display(self, evt):
        for txt in evt.result:
            self.raw(txt)

    def raw(self, txt):
        raise NotImplementedError


class Event:

    def __init__(self):
        self._ready  = threading.Event()
        self._thr    = None
        self.result  = []
        self.type    = "event"
        self.txt     = ""

    def __getattr__(self, key):
        return self.__dict__.get(key, "")

    def __str__(self):
        return str(self.__dict__)

    def ready(self):
        self._ready.set()

    def reply(self, txt):
        self.result.append(txt)

    def wait(self):
        self._ready.wait()
        if self._thr:
            self._thr.join()


"utilities"


def forever():
    while True:
        try:
            time.sleep(1.0)
        except (KeyboardInterrupt, EOFError):
            _thread.interrupt_main()


def privileges():
    import getpass
    import pwd
    pwnam2 = pwd.getpwnam(getpass.getuser())
    os.setgid(pwnam2.pw_gid)
    os.setuid(pwnam2.pw_uid)


def spl(txt):
    try:
        result = txt.split(',')
    except (TypeError, ValueError):
        result = txt
    return [x for x in result if x]


def wrap(func):
    try:
        func()
    except (KeyboardInterrupt, EOFError):
        pass
    except Exception as ex:
        later(ex)


"methods"


def fmt(obj, args=None, skip=None, plain=False):
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


def parse(obj, txt=None):
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


"interface"


def __dir__():
    return (
        'Commands',
        'Config',
        'Event',
        'fmt',
        'forever',
        'parse',
        'privileges',
        'scan',
        'spl',
        'wrap'
    )
