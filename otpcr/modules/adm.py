#  This file is placed in the Public Domain.


"administrator"


from otpcr.booting import Boot
from otpcr.command import Commands
from otpcr.configs import Main
from otpcr.encoder import Json
from otpcr.package import Mods
from otpcr.persist import Workdir


def srv(event):
    "generate systemd service file."
    import getpass
    name = getpass.getuser()
    event.reply(SYSTEMD % (Main.name.upper(), name, name, name, Main.name))


def tbl(event):
    "create table."
    Boot.md5 = {}
    Commands.names = {}
    Mods.md5 = {}
    for name, module in Mods.all():
        Commands.scan(module)
    Boot.md5s()
    Mods.md5s()
    event.reply("# This file is placed in the Pubic Domain.\n\n")
    event.reply('"tables"\n\n')
    event.reply(f"CORE = {Json.dumps(Boot.md5, indent=4, sort_keys=True)}\n\n")
    event.reply(f"NAMES = {Json.dumps(Commands.names, indent=4, sort_keys=True)}\n\n")
    event.reply(f"MD5 = {Json.dumps(Mods.md5, indent=4, sort_keys=True)}")


def wdr(event):
    "show working directory."
    event.reply(Workdir.workdir())


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
