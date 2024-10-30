# This file is placed in the Public Domain.
# pylint: disable=C,W0611,W0718


"console"


import os
import readline
import sys
import termios
import time


from .command import NAME, command, parse, scanner
from .modules import face
from .object  import Config
from .persist import Workdir
from .runtime import Client, Errors, Event, errors, forever, later


Workdir.wdr = os.path.expanduser(f"~/.{NAME}")


cfg  = Config()


class Console(Client):

    def __init__(self):
        Client.__init__(self)
        self.register("command", command)

    def callback(self, evt):
        Client.callback(self, evt)
        evt.wait()

    def poll(self):
        evt = Event()
        evt.txt = input("> ")
        evt.type = "command"
        return evt

    def raw(self, txt):
        print(txt)


def banner():
    tme = time.ctime(time.time()).replace("  ", " ")
    print(f"{NAME.upper()} since {tme}")


def main():
    parse(cfg, " ".join(sys.argv[1:]))
    if "v" in cfg.opts:
        banner()
    for mod, thr in scanner(face, init="i" in cfg.opts, disable=cfg.sets.dis):
        if "v" in cfg.opts and "output" in dir(mod):
            mod.output = print
        if thr and "w" in cfg.opts:
            thr.join()
    csl = Console()
    csl.start()
    forever()


def wrap(func):
    old = None
    try:
        old = termios.tcgetattr(sys.stdin.fileno())
    except termios.error:
        pass
    try:
        func()
    except (KeyboardInterrupt, EOFError):
        print("")
    except Exception as ex:
        later(ex)
    finally:
        if old:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old)


def wrapped():
    wrap(main)
    for line in errors():
        print(line)



if __name__ == "__main__":
    wrapped()
