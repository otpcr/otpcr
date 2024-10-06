# This file is placed in the Public Domain.
# pylint: disable=C0413,W0105,W0611


"cli"


import getpass
import os
import sys


sys.path.insert(0, os.getcwd())


from nixt.runtime import Event


from .command import NAME, CLI, Commands, command
from .modules import face


class CLIS(CLI):

    "CLI"

    def raw(self, txt):
        "print text."
        print(txt)


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


def srv(event):
    "create service file (pipx)."
    name  = getpass.getuser()
    event.reply(TXT % (NAME.upper(), name, name, name, NAME))


Commands.add(srv)


def main():
    "main"
    cli = CLIS()
    evt = Event()
    evt.txt = " ".join(sys.argv[1:])
    command(cli, evt)
    evt.wait()


if __name__ == "__main__":
    main()
