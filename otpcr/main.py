# This file is placed in the Public Domain.
# pylint: disable=W0212,W0718


"main"


import pathlib
import pwd
import os
import sys
import termios
import time
import _thread


from .config  import Config
from .runtime import later, launch
from .utils   import spl


def banner(outer):
    "show banner."
    tme = time.ctime(time.time()).replace("  ", " ")
    outer(f"{Config.name.upper()} since {tme}")


def daemon(verbose=False):
    "switch to background."
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
    os.chdir("/")
    os.nice(10)


def forever():
    "it doesn't stop, until ctrl-c"
    while True:
        try:
            time.sleep(1.0)
        except (KeyboardInterrupt, EOFError):
            _thread.interrupt_main()


def initter(modstr, *pkgs, disable=None):
    "scan modules for commands and classes"
    thrs = []
    for mod in spl(modstr):
        if disable and mod in spl(disable):
            continue
        for pkg in pkgs:
            modi = getattr(pkg, mod, None)
            if not modi:
                continue
            if "init" in dir(modi):
                thrs.append(launch(modi.init))
            break
    return thrs


def modnames(*args):
    "return module names."
    res = []
    for arg in args:
        res.extend([x for x in dir(arg) if not x.startswith("__")])
    return sorted(res)


def pidfile(pid):
    "write the pid to a file."
    if os.path.exists(pid):
        os.unlink(pid)
    path = pathlib.Path(pid)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(pid, "w", encoding="utf-8") as fds:
        fds.write(str(os.getpid()))


def privileges(username):
    "drop privileges."
    pwnam = pwd.getpwnam(username)
    os.setgid(pwnam.pw_gid)
    os.setuid(pwnam.pw_uid)


def wrap(func, outer):
    "reset console."
    old3 = None
    try:
        old3 = termios.tcgetattr(sys.stdin.fileno())
    except termios.error:
        pass
    try:
        func()
    except (KeyboardInterrupt, EOFError):
        outer("")
    except Exception as ex:
        later(ex)
    finally:
        if old3:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old3)


def __dir__():
    return (
        'banner',
        'daemon',
        'forever',
        'initter',
        'laps',
        'modnames',
        'pidfile',
        'privileges',
        'scanner',
        'spl',
        'wrap'
    )
