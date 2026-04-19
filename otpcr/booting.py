# This file is placed in the Public Domain.


"in the beginning"


import logging
import os
import pathlib
import sys
import time
import _thread


from .brokers import Broker
from .command import Commands
from .configs import Main
from .package import Mods
from .persist import Disk, Workdir
from .threads import Thread
from .utility import Log, Utils


class Boot:

    configured = False
    inits = []
    md5s = {}
    path = os.path.dirname(__spec__.loader.path)

    @classmethod
    def banner(cls):
        "hello."
        tme = time.ctime(time.time()).replace("  ", " ")
        print("%s since %s %s (%s)" % (
            Main.name.upper(),
            tme,
            Main.level.upper() or "INFO",
            Utils.md5sum(Mods.path("tbl") or "")[:7],
        ))
        sys.stdout.flush()

    @classmethod
    def configure(cls, name=""):
        "in the beginning."
        if cls.configured:
            logging.warning("already configured")
            return
        Main.name = name or Main.name or Utils.pkgname(Boot)
        if Main.read:
            Disk.read(Main, "main", "config")
        if Main.wdr == f".{Main.name}":
            Main.wdr = os.path.expanduser(f"~/.{Main.name}")
        cls.md5s.update(Utils.md5dir(cls.path))
        Workdir.skel()
        Log.size(len(Main.name))
        Log.level(Main.level or "info")
        Mods.add(
                 f"{Utils.pkgname(Main)}.modules",
                 os.path.join(os.path.dirname(__spec__.loader.path), "modules")
                ) 
        if Main.user:
            Mods.add(os.path.join(Main.wdr, "mods"), "modules")
            Mods.add('mods', 'mods')
        if Main.all:
            Main.mods = Mods.list()
        cls.configured = True

    @classmethod
    def daemon(cls, verbose=False, nochdir=False):
        "run in the background."
        pid = os.fork()
        if pid != 0:
            os._exit(0)
        os.setsid()
        pid2 = os.fork()
        if pid2 != 0:
            os._exit(0)
        if not verbose:
            with open('/dev/null', 'r', encoding="utf-8") as sis:
                os.dup2(sis.fileno(), sys.stdin.fileno())
            with open('/dev/null', 'a+', encoding="utf-8") as sos:
                os.dup2(sos.fileno(), sys.stdout.fileno())
            with open('/dev/null', 'a+', encoding="utf-8") as ses:
                os.dup2(ses.fileno(), sys.stderr.fileno())
        os.umask(0)
        if not nochdir:
            os.chdir("/")
        os.nice(10)

    @classmethod
    def forever(cls):
        "run forever until ctrl-c."
        while True:
            try:
                time.sleep(0.1)
            except (KeyboardInterrupt, EOFError):
                _thread.interrupt_main()

    @classmethod
    def init(cls):
        "scan named modules for commands."
        thrs = []
        for name, mod in Mods.iter():
            if "init" in dir(mod):
                thrs.append((name, Thread.launch(mod.init)))
                cls.inits.append(name)
        if Main.wait:
            for name, thr in thrs:
                thr.join()

    @staticmethod
    def pidfile(name):
        "write pidfile."
        filename = os.path.join(Main.wdr, f"{name}.pid")
        if os.path.exists(filename):
            os.unlink(filename)
        path2 = pathlib.Path(filename)
        path2.parent.mkdir(parents=True, exist_ok=True)
        with open(filename, "w", encoding="utf-8") as fds:
            fds.write(str(os.getpid()))

    @classmethod
    def privileges(cls):
        "drop privileges."
        import getpass
        import pwd
        pwnam2 = pwd.getpwnam(getpass.getuser())
        os.setgid(pwnam2.pw_gid)
        os.setuid(pwnam2.pw_uid)

    @classmethod
    def scan(cls):
        if Main.read:
            cls.scanner()
        else:
            Commands.table()
            Mods.sums()
        if not Commands.names:
            cls.scanner()

    @classmethod
    def scanner(cls):
        "scan named modules for commands."
        res = []
        for name, mod in Mods.iter():
            Commands.scan(mod)
            if "configure" in dir(mod):
                mod.configure()
            res.append((name, mod))
        return res

    @classmethod
    def shutdown(cls):
        "call shutdown on modules."
        for name in cls.inits:
            mod = Mods.get(name)
            if "shutdown" in dir(mod):
                try:
                    mod.shutdown()
                except Exception as ex:
                    logging.exception(ex)
        Broker.stop()

    @classmethod
    def wrap(cls, func, *args):
        "restore console."
        import termios
        old = None
        try:
            old = termios.tcgetattr(sys.stdin.fileno())
        except termios.error:
            pass
        try:
            func(*args)
        except (KeyboardInterrupt, EOFError):
            pass
        except Exception as ex:
            logging.exception(ex)
        if old:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old)


def __dir__():
    return (
        "Boot",
    )
