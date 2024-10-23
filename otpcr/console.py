# This file is placed in the Public Domain.
# pylint: disable=C,W0611,W0718


"console"


import readline
import sys
import termios
import time


from .main    import Client, Config, Event, forever, parse, scanner
from .modules import face
from .persist import NAME
from .runtime import Errors, later


cfg = Config()


class Console(Client):

    def callback(self, evt):
        Client.callback(self, evt)
        evt.wait()

    def poll(self):
        evt = Event()
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
    if "v" in cfg.opts:
        errors()


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


if __name__ == "__main__":
    wrapped()
