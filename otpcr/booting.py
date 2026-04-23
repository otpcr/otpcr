# This file is placed in the Public Domain.


"runtime"


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
    def check(cls, opts):
        "check for command line options."
        for arg in sys.argv:
            if not arg.startswith("-"):
                continue
            for opt in opts:
                if opt in arg:
                    return True
        return False

    @classmethod
    def configure(cls, cfg):
        "in the beginning."
        Main.name = cfg.name or Main.name or Utils.pkgname(Boot)
        if cfg.read:
            Disk.read(Main, "main", "config")
        Workdir.configure(cfg)
        Log.configure(cfg)
        Mods.configure(cfg)
        if Main.all:
            Main.mods = Mods.list()
        if Main.noignore:
            Main.ignore = ""

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
                break

    @classmethod
    def init(cls, cfg):
        "scan named modules for commands."
        thrs = []
        for name, mod in Mods.iter(cfg.mods, cfg.ignore):
            if "init" in dir(mod):
                thrs.append((name, Thread.launch(mod.init)))
                cls.inits.append(name)
        if cfg.wait:
            for name, thr in thrs:
                thr.join()

    @staticmethod
    def pidfile(name):
        "write pidfile."
        filename = os.path.join(Workdir.wdr, f"{name}.pid")
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
    def scan(cls, cfg):
        "load tables or scan directories."
        if cfg.read:
            cls.scanner(cfg)
        else:
            Commands.table()
            Mods.sums()
        if not Commands.names:
            cls.scanner(cfg)

    @classmethod
    def scanner(cls, cfg):
        "scan named modules for commands."
        res = []
        for name, mod in Mods.iter(cfg.mods, cfg.ignore):
            Commands.scan(mod)
            if "configure" in dir(mod):
                mod.configure()
            res.append((name, mod))
        return res

    @classmethod
    def setmd5s(cls):
        "set md5 sums."
        cls.md5s.update(Utils.md5dir(cls.path))

    @classmethod
    def shutdown(cls):
        "call shutdown on modules."
        for name in cls.inits:
            mod = Mods.get(name)
            if "shutdown" in dir(mod):
                logging.info("shutdown %s", name)
                try:
                    mod.shutdown()
                except (KeyboardInterrupt, EOFError):
                    _thread.interrupt_main()
                except Exception as ex:
                    logging.exception(ex)
                    return
        for obj in Broker.objs("stop"):
            if "wait" in dir(obj):
                try:
                    obj.wait()
                    obj.stop()
                except (KeyboardInterrupt, EOFError):
                    _thread.interrupt_main()
                except Exception as ex:
                    logging.exception(ex)
                    return

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
            cls.shutdown()
        except (KeyboardInterrupt, EOFError):
            os._exit(0)
        except Exception as ex:
            logging.exception(ex)
        if old:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old)


def __dir__():
    return (
        "Boot",
    )
