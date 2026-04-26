#  This file is placed in the Public Domain.


"administrator"


import time


from otpcr.command import Commands
from otpcr.configs import Main
from otpcr.package import Mods
from otpcr.utility import Time, Utils


STARTTIME = time.time()


def cmd(event):
    "list available commands."
    event.reply(",".join(sorted(Commands.commands(Main.ignore))))


def mod(event):
    "list available modules."
    mods = Mods.list()
    if not mods:
        event.reply("no modules available")
        return
    event.reply(mods)


def upt(event):
    "show uptiome."
    event.reply(Time.elapsed(time.time()-STARTTIME))


def ver(event):
    "show verson."
    event.reply(f"{Main.name.upper()} {Utils.md5sum(Mods.path('tbl') or '')[:7]}")
