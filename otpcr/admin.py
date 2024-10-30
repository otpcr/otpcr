# This file is place in the Public Domain.
# pylint: disable=C,W0105


"administrator"


import os
import sys


from .command import NAME, Commands, command, parse
from .object  import Config, keys
from .persist import Workdir
from .runtime import Client, Event, errors, wrap


Workdir.wdr = os.path.expanduser(f"~/.{NAME}")


cfg = Config()


TXT = """[Unit]
Description=%s
After=network-online.target

[Service]
Type=simple
User=%s
Group=%s
ExecStart=/home/%s/.local/bin/%ss

[Install]
WantedBy=multi-user.target"""


class CLI(Client):

    def __init__(self):
        Client.__init__(self)
        self.register("command", command)

    def raw(self, txt):
        print(txt)


def cmd(event):
    event.reply(",".join(sorted(keys(Commands.cmds))))


def srv(event):
    import getpass
    name  = getpass.getuser()
    event.reply(TXT % (NAME.upper(), name, name, name, NAME))


def main():
    Commands.add(cmd)
    Commands.add(srv)
    parse(cfg, " ".join(sys.argv[1:]))
    evt = Event()
    evt.txt = cfg.txt
    evt.type = "command"
    csl = CLI()
    command(csl, evt)
    evt.wait()


showerrors = errors


def wrapped():
    wrap(main)
    for line in showerrors():
        print(line)


if __name__ == "__main__":
    wrapped()
