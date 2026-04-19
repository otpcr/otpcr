# This file is placed in the Public Domain.


"show fields on objects"


from otpcr.persist import Locate, Workdir


def fie(event):
    if not event.rest:
        result = sorted({y.split('.')[-1].lower() for y in Workdir.kinds()})
        if result:
            event.reply(",".join(result))
        else:
            event.reply("no fields")
        return
    itms = Locate.attrs(event.args[0])
    if not itms:
        event.reply("no fields")
    else:
        event.reply(",".join(itms))
