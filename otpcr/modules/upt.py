# This file is placed in the Public Domain.


"uptime"


import time


from ..command import Commands
from ..persist import laps
from ..runtime import STARTTIME


def upt(event):
    "show uptime"
    event.reply(laps(time.time()-STARTTIME))


Commands.add(upt)
