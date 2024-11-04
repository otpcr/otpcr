# This file is placed in the Public Domain.
# pylint: disable=C,W0105,W0611,W0718


"console"


import os
import readline
import sys
import termios
import time


sys.path.insert(0, os.getcwd())


from .command import NAME, Config, command, forever, parse, scanner, wrap
from .modules import face
from .runtime import Client, Errors, Event, errors, later


cfg  = Config()


class CLI(Client):

    def __init__(self):
        Client.__init__(self)
        self.register("command", command)

    def raw(self, txt):
        print(txt)


def wrapped():
    wrap(main)


def main():
    parse(cfg, " ".join(sys.argv[1:]))
    scanner(face)
    evt = Event()
    evt.txt = cfg.txt
    evt.type = "command"
    csl = CLI()
    command(csl, evt)
    evt.wait()
    

if __name__ == "__main__":
    wrapped()
