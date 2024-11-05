# This file is placed in the Public Domain.
# pylint: disable=C


"uptime"


import time


from ..command import STARTTIME, laps


def upt(event):
    event.reply(laps(time.time()-STARTTIME))
