# This file is placed in the Public Domain.
# pylint: disable=C,R0903,E0402


"client"


from .command import command
from .output  import Output
from .reactor import Reactor


class Client(Reactor):

    def __init__(self):
        Reactor.__init__(self)
        self.register("command", command)

    def display(self, evt):
        for txt in evt.result:
            self.raw(txt)

    def raw(self, txt):
        raise NotImplementedError("raw")


class Buffered(Output, Client):

    def __init__(self):
        Output.__init__(self)
        Client.__init__(self)

    def raw(self, txt):
        raise NotImplementedError("raw")

    def stop(self):
        Output.stop(self)
        Client.stop(self)
    
    def start(self):
        Output.start(self)
        Client.start(self)

    def wait(self):
        Output.wait(self)
        Client.wait(self)


def __dir__():
    return (
        'Buffered',
        'Client'
    )
