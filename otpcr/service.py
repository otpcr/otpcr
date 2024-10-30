# This file is placed in the Public Domain.
# pylint: disable=C


"service"


import os


from .command import NAME, scanner
from .modules import face
from .persist import Workdir, pidfile, pidname
from .runtime import errors, forever, privileges, wrap


Workdir.wdr = os.path.expanduser(f"~/.{NAME}")


scan = scanner


def main():
    privileges()
    pidfile(pidname(NAME))
    scan(face, init=True)
    forever()


def wrapped():
    wrap(main)


if __name__ == "__main__":
    wrapped()
    for line in errors():
        print(line)
