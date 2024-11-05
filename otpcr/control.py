# This file is placed in the Public Domain.
# pylint: disable=C,W0105,W0611,W0718


"console"


import os
import readline
import sys
import termios
import time


from .command import NAME, Commands, Config
from .command import command, forever, parse, scanner, wrap
from .defines import TXT
from .modules import face
from .runtime import Client, Errors, Event, errors, later


cfg  = Config()


class CLI(Client):

    def __init__(self):
        Client.__init__(self)
        self.register("command", command)

    def raw(self, txt):
        print(txt)


def srv(event):
    import getpass
    name  = getpass.getuser()
    event.reply(TXT % (NAME.upper(), name, name, name, NAME))


def wrapped():
    wrap(main)
    for line in errors():
        print(line)

def main():
    Commands.add(srv)
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
