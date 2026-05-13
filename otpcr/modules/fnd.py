# This file is placed in the Public Domain.


"locate objects"


import time


from otpcr.defines import Locate, Object, Time, Workdir


def fie(event):
    if not event.rest:
        res = sorted({x.split('.')[-1].lower() for x in Workdir.kinds()})
        if res:
            event.reply(",".join(res))
        else:
            event.reply("no types")
        return
    itms = Locate.attrs(event.args[0])
    if not itms:
        event.reply("no attributes")
    else:
        event.reply(",".join(itms))


def fnd(event):
    if not event.rest:
        res = sorted([x.split('.')[-1].lower() for x in Workdir.kinds()])
        if res:
            event.reply(",".join(res))
        else:
            event.reply("no data.")
        return
    otype = event.args[0]
    nmr = 0
    for fnm, obj in sorted(
                           Locate.find(otype, event.gets),
                           key=lambda x: Time.fntime(x[0])
                          ):
        diff = time.time()-Time.fntime(fnm)
        event.reply(f"{nmr} {Object.fmt(obj)} {Time.elapsed(diff)}")
        nmr += 1
    if not nmr:
        event.reply("no result")
