# This file is placed in the Public Domain.
# pylint: disable=R.W0105,W0212,W0718


"client"


from .broker  import Broker
from .command import command
from .runtime import Reactor


class Client(Reactor):

    "Client"

    def __init__(self):
        Reactor.__init__(self)
        Broker.add(self, repr(self))
        self.register("command", command)

    def display(self, evt):
        "show results into a channel."
        for txt in evt.result:
            self.say(evt.channel, txt)

    def say(self, _channel, txt):
        "echo on verbose."
        self.raw(txt)

    def raw(self, txt):
        "print to screen."
        raise NotImplementedError


def __dir__():
    return (
        'Client',
    )
