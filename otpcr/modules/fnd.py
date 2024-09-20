# This file is placed in the Public Domain.


"find"


import time


from ..client  import Commands, laps
from ..object  import fmt
from ..persist import find, fntime, long, skel, store


def fnd(event):
    "locate objects."
    skel()
    if not event.rest:
        res = sorted([x.split('.')[-1].lower() for x in store()])
        if res:
            event.reply(",".join(res))
        return
    otype = event.args[0]
    clz = long(otype)
    if "." not in clz:
        for fnm in store():
            claz = fnm.split(".")[-1]
            if otype == claz.lower():
                clz = fnm
    nmr = 0
    for fnm, obj in find(clz, event.gets):
        event.reply(f"{nmr} {fmt(obj)} {laps(time.time()-fntime(fnm))}")
        nmr += 1
    if not nmr:
        event.reply("no result")


fnd.target = "cli"


Commands.add(fnd)
