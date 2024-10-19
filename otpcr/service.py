# This file is placed in the Public Domain.
# pylint: disable=C0413,W0105


"service"


import getpass
import os
import pwd
import sys


from .command import forever, init, wrap
from .modules import face as faced
from .persist import pidfile, pidname
from .runtime import Errors


def errors():
    for err in Errors.errors:
        for line in err:
            print(line)


def privileges(username):
    pwnam2 = pwd.getpwnam(username)
    os.setgid(pwnam2.pw_gid)
    os.setuid(pwnam2.pw_uid)


def main():
    privileges(getpass.getuser())
    pidfile(pidname())
    init(faced)
    forever()


def wrapped():
    wrap(main)
    errors()


if __name__ == "__main__":
    wrapped()
