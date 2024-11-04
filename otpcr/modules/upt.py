# This file is placed in the Public Domain.
# pylint: disable=C,W0105


"uptime"


import time


from ..command import laps


"defines"


STARTTIME = time.time()


"commands"


def upt(event):
    event.reply(laps(time.time()-STARTTIME))
