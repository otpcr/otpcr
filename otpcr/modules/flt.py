# This file is placed in the Public Domain.


"fleet"


from ..objects import fmt
from ..threads import name
from ..clients import Fleet


def flt(event):
    """ show bots in fleet. """
    bots = Fleet.bots.values()
    try:
        event.reply(fmt(list(Fleet.bots.values())[int(event.args[0])]))
    except (KeyError, IndexError, ValueError):
        event.reply(",".join([name(x).split(".")[-1] for x in bots]))
