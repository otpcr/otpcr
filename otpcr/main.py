# This file is placed in the Public Domain.
# pylint: disable=C,R,W0105,W0212,W0718


"program helpers"


import getpass
import inspect
import os
import pwd
import threading
import time
import _thread


from .object  import Object, parse
from .persist import Workdir
from .runtime import Reactor, later, launch


NAME = Reactor.__module__.split(".", maxsplit=2)[-2]
STARTTIME = time.time()


Workdir.wdr = os.path.expanduser(f"~/.{NAME}")


class Config(Object):

    pass


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


def forever():
    while True:
        try:
            time.sleep(1.0)
        except (KeyboardInterrupt, EOFError):
            _thread.interrupt_main()


def modloop(*pkgs):
    for pkg in pkgs:
        for modname in dir(pkg):
            if modname.startswith("__"):
                continue
            yield getattr(pkg, modname)


def privileges():
    pwnam2 = pwd.getpwnam(getpass.getuser())
    os.setgid(pwnam2.pw_gid)
    os.setuid(pwnam2.pw_uid)
            

def scanner(*pkgs, init=False):
    result = []
    for mod in modloop(*pkgs):
        Commands.scan(mod)
        thr = None
        if init and "init" in dir(mod):
            thr = launch(mod.init, "init")
        result.append((mod, thr))
    return result
            

def wrap(func):
    try:
        func()
    except (KeyboardInterrupt, EOFError):
        pass
    except Exception as ex:
        later(ex)


def __dir__():
    return (
        'NAME',
        'STARTTIME',
        'Commands',
        'Config',
        'Event',
        'forever',
        'privileges',
        'scan',
        'wrap'
    )
