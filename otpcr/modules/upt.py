# This file is placed in the Public Domain.


"uptime"


import time


from ..command import Commands
from ..runtime import STARTTIME
from ..utils   import laps


def upt(event):
    "show uptime"
    event.reply(laps(time.time()-STARTTIME))


Commands.add(upt)
