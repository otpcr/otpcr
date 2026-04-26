# This file is placed in the Public Domain.


"main program"


import argparse


from .booting import Boot
from .command import Commands
from .configs import Main
from .handler import Console, Event
from .objects import Base, Methods, Object


class Arguments:

    args = None
    txt = None

    @classmethod
    def getargs(cls):
        "parse commandline arguments."
        parser = argparse.ArgumentParser(prog=Main.name, description=f"{Main.name.upper()}")
        parser.add_argument("-a", "--all", action="store_true", help="load all modules.")
        parser.add_argument("-c", "--console", action="store_true", help="start console.")
        parser.add_argument("-d", "--daemon", action="store_true", help="start background daemon.")
        parser.add_argument("-i", "--ignore", default="", help='modules to ignore.')
        parser.add_argument("-l", "--level", default=Main.level, help='set loglevel.')
        parser.add_argument("-m", "--mods", default="", help='modules to load.')
        parser.add_argument("-n", "--index", action="store", type=int, help="set index to use.")
        parser.add_argument("-r", "--read", action="store_true", help="read config on start.")
        parser.add_argument("-s", "--service", action="store_true", help="start service.")
        parser.add_argument("-v", "--verbose", action='store_true', help='enable verbose.')
        parser.add_argument("-w", "--wait", action='store_true', help='wait for services to start.')
        parser.add_argument("-u", "--user", action="store_true", help="use local mods directory.")
        parser.add_argument("-x", "--admin", action="store_true", help="enable admin mode.")
        parser.add_argument("--wdr", help='set working directory.')
        parser.add_argument("--nochdir", action="store_true", help='set working directory.')
        parser.add_argument("--noignore", action="store_true", help="disable ignore")
        cls.args, arguments = parser.parse_known_args()
        cls.txt = " ".join(arguments)
        Object.merge(Main, cls.args)
        parsed = Base()
        Methods.parse(parsed, cls.txt)
        Object.merge(Main, parsed)


class Line(Console):

    def raw(self, text):
        "write to console."
        print(text.encode('utf-8', 'replace').decode("utf-8"))


class CSL(Line):

    def poll(self):
        "poll for an event."
        evt = Event()
        evt.orig = repr(self)
        evt.text = input("> ")
        evt.kind = "command"
        return evt


class Scripts:

    @staticmethod
    def background():
        "background script."
        Boot.daemon(Main.verbose, Main.nochdir)
        Boot.privileges()
        Boot.configure(Main)
        Boot.pidfile(Main.name)
        Boot.scan(Main)
        Boot.init(Main)
        Boot.forever()

    @staticmethod
    def cmd(text):
        cli = Line()
        for txt in text.split(" ! "):
            evt = Event()
            evt.kind = "command"
            evt.orig = repr(cli)
            evt.text = txt
            Commands.command(evt)
            evt.wait()

    @staticmethod
    def console():
        "console script."
        import readline
        readline.redisplay()
        Boot.configure(Main)
        if Main.verbose:
            Boot.banner()
        Boot.scan(Main)
        Boot.init(Main)
        csl = CSL()
        csl.start(daemon=True)
        Boot.forever()

    @staticmethod
    def control():
        "cli script."
        if not Arguments.txt:
            return
        Main.all = True
        Boot.configure(Main)
        Boot.scan(Main)
        Scripts.cmd(Arguments.txt)

    @staticmethod
    def service():
        "service script."
        Boot.privileges()
        Boot.configure(Main)
        Boot.scan(Main)
        Boot.banner()
        Boot.pidfile(Main.name)
        Boot.init(Main)
        Boot.forever()


def main():
    "main"
    Arguments.getargs()
    Main.ignore = "mbx,rst,tmr,udp,web,wsd"
    if not Main.admin:
        Main.ignore += ",adm"
    if Main.daemon:
        Boot.wrap(Scripts.background)
    elif Main.console:
        Boot.wrap(Scripts.console)
    elif Main.service:
        Boot.wrap(Scripts.service)
    else:
        Boot.wrap(Scripts.control)
