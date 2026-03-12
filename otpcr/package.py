# This file is placed in the Public Domain.


"module management"


import importlib.util
import logging
import os


from .utility import Utils


class Mods:

    dirs = {}
    modules = {}

    @staticmethod
    def add(name, path):
        "add modules directory."
        if os.path.exists(path):
            Mods.dirs[name] = path

    @staticmethod
    def get(modname):
        "return module."
        result = list(Mods.iter(modname))
        if result:
            return result[0][-1]

    @staticmethod
    def has(attr):
        "return list of modules containing an attribute."
        result = []
        for mod in Mods.modules.values():
            if getattr(mod, attr, False):
                result.append(mod.__name__.split(".")[-1])
        return ",".join(result)

    @staticmethod
    def iter(modlist, ignore=""):
        "loop over modules."
        for pkgname, path in Mods.dirs.items():
            if not os.path.exists(path):
                continue
            for fnm in os.listdir(path):
                if fnm.startswith("__"):
                    continue
                if not fnm.endswith(".py"):
                    continue
                name = fnm[:-3]
                if not name:
                    continue
                if name not in Utils.spl(modlist):
                    continue
                if ignore and name in Utils.spl(ignore):
                    continue
                modname = f"{pkgname}.{name}"
                mod = Mods.modules.get(modname, None)
                if not mod:
                    pth = os.path.join(path, fnm)
                    if not os.path.exists(pth):
                        continue
                    mod = Mods.importer(modname, pth)
                if mod:
                    yield name, mod

    @staticmethod
    def list(ignore=""):
        "comma seperated list of available modules."
        mods = []
        for pkgname, path in Mods.dirs.items():
            mods.extend([
                x[:-3] for x in os.listdir(path)
                if x.endswith(".py") and
                not x.startswith("__") and
                x[:-3] not in Utils.spl(ignore)
            ])
        return ",".join(sorted(mods))

    @staticmethod
    def importer(name, pth=""):
        "import module by path."
        if pth and os.path.exists(pth):
            spec = importlib.util.spec_from_file_location(name, pth)
        else:
            spec = importlib.util.find_spec(name)
        if not spec or not spec.loader:
            logging.debug("missing spec or loader for %s", name)
            return None
        mod = importlib.util.module_from_spec(spec)
        if not mod:
            logging.debug("can't load %s module from spec", name)
            return None
        Mods.modules[name] = mod
        spec.loader.exec_module(mod)
        return mod

    @staticmethod
    def pkg(package):
        return Mods.add(package.__name__, package.__path__[0])


def __dir__():
    return (
        'Mods',
    )
