# This file is placed in the Public Domain.


from otpcr.brokers import Broker
from otpcr.objects import Methods


def flt(event):
    clts = list(Broker.objs("announce"))
    if event.args:
        index = int(event.args[0])
        if index < len(clts):
            event.reply(str(clts[index]))
        else:
            event.reply("no matching client in fleet.")
        return
    event.reply(' | '.join([Methods.fqn(o).split(".")[-1] for o in clts]))
