# This file is placed in the Public Domain.
# pylint: disable=C0413,W0105


"service"


import getpass
import os
import pwd
import sys


sys.path.insert(0, os.getcwd())


from nixt.persist import pidfile, pidname
from nixt.runtime import Errors


from .command import forever, init, wrap
from .modules import face as faced


def errors():
    "print errors."
    for err in Errors.errors:
        for line in err:
            print(line)


def privileges(username):
    "privileges."
    pwnam2 = pwd.getpwnam(username)
    os.setgid(pwnam2.pw_gid)
    os.setuid(pwnam2.pw_uid)


def main():
    "main"
    privileges(getpass.getuser())
    pidfile(pidname())
    init(faced)
    forever()


if __name__ == "__main__":
    wrap(main)
    errors()
