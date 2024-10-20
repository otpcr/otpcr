# This file is placed in the Public Domain.
# pylint: disable=C,W0611,W0718


"cli"


import os
import sys
import threading
import time
import _thread


from .main    import NAME, Client, Command, Config, command, scanner
from .modules import face
from .object  import Object, parse
from .persist import Workdir, modname
from .runtime import Errors, Reactor, later


cfg = Config()
cfg.txt = ""


class CLI(Client):

    def raw(self, txt):
        print(txt)


def errors():
    for error in Errors.errors:
        for line in error:
            print(line)


def main():
    parse(cfg, " ".join(sys.argv[1:]))
    scanner(face)
    cli = CLI()
    evt = Command()
    evt.txt = cfg.txt
    command(cli, evt)
    evt.wait()


def wrapped():
    main()
    errors()


if __name__ == "__main__":
    wrapped()
