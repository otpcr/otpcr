# This file is placed in the Public Domain.


from otpcr.persist import attrs, kinds


def atr(event):
    if not event.rest:
        res = sorted({x.split('.')[-1].lower() for x in kinds()})
        if res:
            event.reply(",".join(res))
        else:
            event.reply("no types")
        return
    itms = attrs(event.args[0])
    if not itms:
        event.reply("no attributes")
    else:
        event.reply(",".join(itms))
