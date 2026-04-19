# This file is placed in the Public Domain.


"runtime"


import argparse


from .booting import Boot
from .command import Commands
from .configs import Main
from .encoder import Json
from .handler import Console, Event
from .objects import Object
from .package import Mods


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
        parser.add_argument("-p", "--prune", action="store_true", help="prune directories.")
        parser.add_argument("-r", "--read", action="store_true", help="read modules on start.")
        parser.add_argument("-s", "--service", action="store_true", help="start service.")
        parser.add_argument("-t", "--threaded", action="store_true", help="use threads.")
        parser.add_argument("-v", "--verbose", action='store_true', help='enable verbose.')
        parser.add_argument("-w", "--wait", action='store_true', help='wait for services to start.')
        parser.add_argument("-u", "--user", action="store_true", help="use local mods directory.")
        parser.add_argument("-x", "--admin", action="store_true", help="enable admin mode.")
        parser.add_argument("--wdr", help='set working directory.')
        parser.add_argument("--nochdir", action="store_true", help='set working directory.')
        cls.args, arguments = parser.parse_known_args()
        cls.txt = " ".join(arguments)
        Object.merge(Main, cls.args)


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


class Run:

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


class Scripts:

    @staticmethod
    def background():
        "background script."
        Boot.daemon(Main.verbose, Main.nochdir)
        Boot.privileges()
        Boot.configure()
        Boot.pidfile(Main.name)
        Boot.scan()
        Boot.init()
        Boot.forever()

    @staticmethod
    def console():
        "console script."
        import readline
        readline.redisplay()
        Boot.configure()
        if Main.verbose:
            Boot.banner()
        Boot.scan()
        Boot.init()
        csl = CSL()
        csl.start()
        Boot.forever()

    @staticmethod
    def control():
        "cli script."
        if not Arguments.txt:
            return
        Main.all = True
        Boot.configure()
        Boot.scan()
        if Main.admin:
            Commands.add(Cmd.srv, Cmd.tbl)
        Run.cmd(Arguments.txt)

    @staticmethod
    def service():
        "service script."
        Boot.privileges()
        Boot.configure()
        Boot.scan()
        Boot.banner()
        Boot.pidfile(Main.name)
        Boot.init()
        Boot.forever()


class Cmd:

    @staticmethod
    def srv(event):
        "generate systemd service file."
        import getpass
        name = getpass.getuser()
        event.reply(SYSTEMD % (Main.name.upper(), name, name, name, Main.name))

    @staticmethod
    def tbl(event):
        "create table."
        # Mods.md5s = {}
        for name, module in Mods.all():
            Commands.scan(module)
        event.reply("# This file is placed in the Pubic Domain.\n\n")
        event.reply('"tables"\n\n')
        event.reply(f"CORE = {Json.dumps(Boot.md5s, indent=4)}\n\n")
        event.reply(f"NAMES = {Json.dumps(Commands.names, indent=4)}\n\n")
        event.reply(f"MD5 = {Json.dumps(Mods.md5s, indent=4)}\n\n")
        event.reply(f"SKIPS = {Json.dumps(Commands.skips, indent=4)}")


SYSTEMD = """[Unit]
Description=%s
After=multi-user.target

[Service]
Type=simple
User=%s
Group=%s
ExecStart=/home/%s/.local/bin/%s -s

[Install]
WantedBy=multi-user.target"""


def main():
    "main"
    Arguments.getargs()
    if Main.daemon:
        Scripts.background()
    elif Main.console:
        Boot.wrap(Scripts.console)
    elif Main.service:
        Boot.wrap(Scripts.service)
    else:
        Boot.wrap(Scripts.control)
    Boot.shutdown()
