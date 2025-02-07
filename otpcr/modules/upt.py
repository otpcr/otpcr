# This file is placed in the Public Domain.


"uptime"


import time


from ..clients import Config
from ..threads import STARTTIME
from ..utility import elapsed


def upt(event):
    """ show uptime. """
    event.reply(elapsed(time.time()-STARTTIME))


def ver(event):
    """ show version. """
    event.reply(f"{Config.name.upper()} {Config.version}")
