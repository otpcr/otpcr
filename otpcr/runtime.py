# This file is placed in the Public Domain.


"main program"


import argparse
import os
import sys
import time


from otpcr.defines import Boot, Commands, Console, Disk, Log, Main, Message
from otpcr.defines import Mods, Object, Parse, Utils, Workdir


class Arguments:

    @classmethod
    def getargs(cls):
        "parse commandline arguments."
        Main.name = Main.name or Utils.pkgname(Main)
        theparser = argparse.ArgumentParser(
                                         prog=Main.name,
                                         description=f'{Main.name.upper()}',
                                         epilog='use "%(prog)s cmd" for a list of commands.',
                                         formatter_class=argparse.RawDescriptionHelpFormatter,
                                         usage='''%(prog)s [-c|d|h|s] [-a] [-v] [-u] [-l level] [-m m1,m2] [-w] [--wdr]\n       %(prog)s [cmd] [arg=val] [arg==val]'''
                                        )
        group = theparser.add_mutually_exclusive_group()
        group.add_argument("-c", "--console", action="store_true", help="run as console.")
        group.add_argument("-d", "--daemon", action="store_true", help="run as background daemon.")
        group.add_argument("-s", "--service", action="store_true", help="run as service.")
        parser = theparser.add_argument_group()
        parser.add_argument("-a", "--all", action="store_true", help="load all modules.")
        parser.add_argument("-l", "--level", default=Main.level, help='set loglevel.', metavar="level")
        parser.add_argument("-m", "--mods", default="", help='modules to load.', metavar="m1,m2")
        parser.add_argument("-v", "--verbose", action='store_true', help='enable verbose.')
        parser.add_argument("-w", "--wait", action='store_true', help='wait for services to start.')
        parser.add_argument("-u", "--user", action="store_true", help="use local mods directory.")
        optparser = theparser.add_argument_group()
        optparser.add_argument("--check", action="store_false", help=argparse.SUPPRESS)
        optparser.add_argument("--read", action="store_true", help=argparse.SUPPRESS)
        optparser.add_argument("--default", default="irc,rss", help="use default values.")
        optparser.add_argument("--nochdir", action="store_true", help=argparse.SUPPRESS)
        optparser.add_argument("--wdr", default="", help='set working directory.', metavar="wdr")
        args, arguments = theparser.parse_known_args()
        Main.otxt = txt = " ".join(arguments)
        Object.update(Main, args)
        Parse.parse(Main, txt)


class CSL(Console):

    @staticmethod
    def cmd(text):
        "do a command."
        cli = CSL()
        for txt in text.split(" ! "):
            evt = Message()
            evt.kind = "command"
            evt.orig = repr(cli)
            evt.text = txt
            Commands.command(evt)
            evt.wait()

    def raw(self, text):
        "write to console."
        print(text.encode('utf-8', 'replace').decode("utf-8"))


class Runs:

    @classmethod
    def banner(cls, cfg):
        "hello."
        tme = time.ctime(time.time()).replace("  ", " ")
        txt = "%s %s since %s %s (%s)" % (
            cfg.name.upper(),
            cfg.version,
            tme,
            cfg.level.upper() or "INFO",
            Utils.md5core()
        )
        print(txt.replace("  ", " "))
        sys.stdout.flush()

    @classmethod
    def boot(cls, cfg):
        Workdir.wdr = os.path.expanduser(f"~/.{Main.name}")
        Mods.add("modules", Utils.moddir())
        if cfg.user:
            Mods.add("mods", "mods")
            Mods.add("other", "other")
        Log.size(len(Main.name))
        Log.level(cfg.level or "info")
        if cfg.read:
            Disk.read(Main, 'main', "config")
        if cfg.all:
            cfg.mods = Mods.list()
        if cfg.verbose:
            Runs.banner(cfg)
        if not Commands.table():
            Boot.scanner()
        Boot.table()
        Mods.table()
        if cfg.check and cfg.verbose:
            Boot.check()


class Scripts:

    @staticmethod
    def background():
        "background script."
        Boot.daemon(Main.verbose, Main.nochdir)
        Boot.privileges()
        Runs.boot(Main)
        Boot.pidfile(Main.name)
        Boot.init(Main.mods or Main.default)
        Boot.forever()

    @staticmethod
    def console():
        "console script."
        import readline
        readline.redisplay()
        Runs.boot(Main)
        if not Boot.init(Main.mods, Main.wait):
            return
        csl = CSL()
        csl.start()
        Boot.forever()

    @staticmethod
    def control():
        "cli script."
        Runs.boot(Main)
        Main.check = False
        CSL.cmd(Main.otxt)

    @staticmethod
    def service():
        "service script."
        Boot.privileges()
        Runs.boot(Main)
        Boot.pidfile(Main.name)
        Boot.init(Main.mods or Main.default)
        Boot.forever()


def main():
    "main"
    Arguments.getargs()
    if Main.daemon:
        Boot.wrap(Scripts.background)
    elif Main.console:
        Boot.wrap(Scripts.console)
    elif Main.service:
        Boot.wrap(Scripts.service)
    else:
        Boot.wrap(Scripts.control)


if __name__ == "__main__":
    main()
