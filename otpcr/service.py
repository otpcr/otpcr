#!/usr/bin/env python3
# This file is placed in the Public Domain.
# pylint: disable=C,W0212,W0718


"service"


import getpass
import os
import pwd
import sys


from .main    import NAME, forever, privileges, scanner, wrap
from .modules import face
from .persist import modname, pidfile, pidname
from .runtime import Errors


def errors():
    for errr in Errors.errors:
        for line in errr:
            print(line)


def main():
    privileges()
    pidfile(pidname(NAME))
    scanner(face, init=True)
    forever()


def wrapped():
    wrap(main)
    errors()


if __name__ == "__main__":
    wrapped()
