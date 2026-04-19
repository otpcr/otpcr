# This file is placed in the Public Domain.


"show bots in fleet"


from otpcr.brokers import Broker
from otpcr.objects import Methods


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
            event.reply("no matching client in fleet.")
        return
    event.reply(' | '.join([Methods.fqn(o).split(".")[-1] for o in clts]))
