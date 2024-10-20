# This file is placed in the Public Domain.
# pylint: disable=C,W0212,W0718


"console"


import os
import readline
import sys
import termios
import time


from .main    import NAME, Client, Command, Config, forever, scanner
from .modules import face
from .object  import Object, parse
from .persist import modname
from .runtime import Errors, later


Cfg = Config()


class Console(Client):

    def callback(self, evt):
        Client.callback(self, evt)
        evt.wait()

    def poll(self):
        evt = Command()
        evt.txt = input("> ")
        return evt

    def raw(self, txt):
        print(txt)


def banner():
    tme = time.ctime(time.time()).replace("  ", " ")
    print(f"{NAME.upper()} since {tme}")


def errors():
    for error in Errors.errors:
        for line in error:
            print(line)


def wrap(func):
    old2 = None
    try:
        old2 = termios.tcgetattr(sys.stdin.fileno())
    except termios.error:
        pass
    try:
        func()
    except (KeyboardInterrupt, EOFError):
        print("")
    except Exception as ex:
        later(ex)
    finally:
        if old2:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old2)


def main():
    parse(Cfg, " ".join(sys.argv[1:]))
    if "v" in Cfg.opts:
        readline.redisplay()
        banner()
    for mod, thr in scanner(face, init="i" in Cfg.opts):
        if "v" in Cfg.opts and "output" in dir(mod):
            mod.output = print
        if "w" in Cfg.opts and thr:
            thr.join()
    csl = Console()
    csl.start()
    forever()


def wrapped():
    wrap(main)
    errors()


if __name__ == "__main__":
    wrapped()
