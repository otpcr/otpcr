# This file is placed in the Public Domain.


"show running clients"


from otpcr.defines import Broker, Object


def flt(event):
    clts = list(Broker.objs("announce"))
    if not clts:
        event.reply("no bots")
        return
    if event.args:
        index = int(event.args[0])
        if index < len(clts):
            event.reply(str(clts[index]))
        else:
            event.reply("no matching client.")
        return
    event.reply(' | '.join([Object.fqn(o).split(".")[-1] for o in clts]))
