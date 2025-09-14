# This file is placed in the Public Domain.


"commands"


import hashlib
import importlib
import importlib.util
import inspect
import logging
import os
import sys
import threading
import _thread


from .methods import j, rlog, spl
from .handler import Fleet


lock = threading.RLock()


class Commands:

    cmds = {}
    debug = False
    md5s = {}
    mod = j(os.path.dirname(__file__), "modules")
    package = __name__.split(".")[0] + "." + "modules"
    names = {}

    @staticmethod
    def add(func) -> None:
        name = func.__name__
        modname = func.__module__.split(".")[-1]
        Commands.cmds[name] = func
        Commands.names[name] = modname

    @staticmethod
    def get(cmd):
        func = Commands.cmds.get(cmd, None)
        if func:
            return func
        name = Commands.names.get(cmd, None)
        if not name:
            return
        module = getmod(name)
        if not module:
            return
        scan(module)
        if Commands.debug:
            module.DEBUG = True
        return Commands.cmds.get(cmd, None)


def command(evt):
    parse(evt)
    func = Commands.get(evt.cmd)
    if func:
        func(evt)
        Fleet.display(evt)
    evt.ready()


"modules"


def getmod(name, path=None):
    with lock:
        mname = Commands.package + "." +  name
        module = sys.modules.get(mname, None)
        if module:
            return module
        if not path:
            path = Commands.mod
        pth = j(path, f"{name}.py")
        if not os.path.exists(pth):
            return
        if name != "tbl" and md5sum(pth) != Commands.md5s.get(name, None):
            rlog("warn", f"md5 error on {pth.split(os.sep)[-1]}")
        return importer(mname, pth) 


def modules():
    if not os.path.exists(Commands.mod):
        return {}
    return {
            x[:-3] for x in os.listdir(Commands.mod)
            if x.endswith(".py") and not x.startswith("__")
           }


def scan(module):
    for key, cmdz in inspect.getmembers(module, inspect.isfunction):
        if key.startswith("cb"):
            continue
        if 'event' in inspect.signature(cmdz).parameters:
            Commands.add(cmdz)


def scanner(names=None):
    res = []
    for nme in sorted(modules()):
        if names and nme not in spl(names):
            continue
        module = getmod(nme)
        if not module:
            continue
        scan(module)
        res.append(module)
    return res


def table(checksum=""):
    pth = j(Commands.mod, "tbl.py")
    if os.path.exists(pth):
        if checksum and md5sum(pth) != checksum:
            rlog("warn", "table checksum error.")
    tbl = getmod("tbl")
    if tbl:
        if "NAMES" in dir(tbl):
            Commands.names.update(tbl.NAMES)
        if "MD5" in dir(tbl):
            Commands.md5s.update(tbl.MD5)
    else:
        scanner()


"utilities"


def importer(name, pth):
    try:
        spec = importlib.util.spec_from_file_location(name, pth)
        if not spec:
            rlog("info", f"misiing {pth}")
            return 
        module = importlib.util.module_from_spec(spec)
        if not module:
            rlog("info", f"{pth} not importable")
            return
        sys.modules[name] = module
        spec.loader.exec_module(module)
        rlog("info", f"load {pth}")
        return module
    except Exception as ex:
        logging.exception(ex)
        _thread.interrupt_main()


def md5sum(path):
    with open(path, "r", encoding="utf-8") as file:
        txt = file.read().encode("utf-8")
        return hashlib.md5(txt).hexdigest()


def parse(obj, txt=None):
    if txt is None:
        if "txt" in dir(obj):
            txt = obj.txt
        else:
            txt = ""
    args = []
    obj.args   = getattr(obj, "args", [])
    obj.cmd    = getattr(obj, "cmd", "")
    obj.gets   = getattr(obj, "gets", "")
    obj.index  = getattr(obj, "index", None)
    obj.inits  = getattr(obj, "inits", "")
    obj.mod    = getattr(obj, "mod", "")
    obj.opts   = getattr(obj, "opts", "")
    obj.result = getattr(obj, "result", "")
    obj.sets   = getattr(obj, "sets", {})
    obj.silent = getattr(obj, "silent", "")
    obj.txt    = txt or getattr(obj, "txt", "")
    obj.otxt   = obj.txt or getattr(obj, "otxt", "")
    _nr = -1
    for spli in obj.otxt.split():
        if spli.startswith("-"):
            try:
                obj.index = int(spli[1:])
            except ValueError:
                obj.opts += spli[1:]
            continue
        if "-=" in spli:
            key, value = spli.split("-=", maxsplit=1)
            obj.silent[key] = value
            obj.gets[key] = value
            continue
        if "==" in spli:
            key, value = spli.split("==", maxsplit=1)
            obj.gets[key] = value
            continue
        if "=" in spli:
            key, value = spli.split("=", maxsplit=1)
            if key == "mod":
                if obj.mod:
                    obj.mod += f",{value}"
                else:
                    obj.mod = value
                continue
            obj.sets[key] = value
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


"interface"


def __dir__():
    return (
        'Commands',
        'command',
        'getmod',
        'importer',
        'md5sum',
        'modules',
        'parse',
        'scan',
        'scanner',
        'table'
    )
