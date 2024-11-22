# This file is placed in the Public Domain.
# pylint: disable=C,W0212


"daemon"


import os
import sys


from .control import NAME
from .persist import Workdir, pidfile, pidname
from .runtime import errors, forever, scan, wrap


Workdir.wdr = os.path.expanduser(f"~/.{NAME}")


def daemon(verbose=False):
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


def privileges():
    import getpass
    import pwd
    pwnam2 = pwd.getpwnam(getpass.getuser())
    os.setgid(pwnam2.pw_gid)
    os.setuid(pwnam2.pw_uid)


def service():
    privileges()
    pidfile(pidname(NAME))
    from .modules import face
    scan(face, init=True)
    forever()


def wrapped():
    wrap(service)
    for line in errors():
        print(line)


def main():
    daemon(True)
    service()


if __name__ == "__main__":
    wrapped()
