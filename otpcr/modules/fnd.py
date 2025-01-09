# This file is placed in the Public Domain.[B
# pylint: disable=W,C0116,E0402


"find"


import os
import pathlib
import time


from ..find import Workdir, find, fntime, format, laps, long, skel, types


def fnd(event):
    skel()
    if not event.rest:
        res = sorted([x.split('.')[-1].lower() for x in types()])
        if res:
            event.reply(",".join(res))
        return
    otype = event.args[0]
    clz = long(otype)
    nmr = 0
    for fnm, obj in find(clz, event.gets):
        event.reply(f"{nmr} {format(obj)} {laps(time.time()-fntime(fnm))}")
        nmr += 1
    if not nmr:
        event.reply("no result")
