# This file is placed in the Public Domain.
# pylint: disable=R0903,W0613


"clients"


import os
import queue
import threading


from .default import Default
from .reactor import Fleet, Reactor
from .threads import launch


class Config(Default):

    """ Config """

    init    = ""
    name    = __file__.rsplit(os.sep, maxsplit=2)[-2]
    opts    = Default()
    version = 170


class Client(Reactor):

    """ Client """

    def __init__(self):
        Reactor.__init__(self)
        Fleet.add(self)

    def raw(self, txt) -> None:
        """ text to screen. """
        raise NotImplementedError("raw")

    def say(self, channel, txt) -> None:
        """ text to channel. """
        self.raw(txt)


class Output:

    """ Output """

    def __init__(self):
        self.oqueue   = queue.Queue()
        self.running = threading.Event()

    def loop(self) -> None:
        """ output loop. """
        self.running.set()
        while self.running.is_set():
            evt = self.oqueue.get()
            if evt is None:
                self.oqueue.task_done()
                break
            Fleet.display(evt)
            self.oqueue.task_done()

    def oput(self,evt) -> None:
        """ put event into output queue. """
        if not self.running.is_set():
            Fleet.display(evt)
        self.oqueue.put(evt)

    def start(self) -> None:
        """ start output loop. """
        if not self.running.is_set():
            self.running.set()
            launch(self.loop)

    def stop(self) -> None:
        """ stop output loop. """
        self.running.clear()
        self.oqueue.put(None)

    def wait(self) -> None:
        """ wait for loop to finish, """
        self.oqueue.join()
        self.running.wait()


class Buffered(Client, Output):

    """ Buffered """

    def __init__(self):
        Client.__init__(self)
        Output.__init__(self)

    def raw(self, txt) -> None:
        """ text to screen. """
        raise NotImplementedError("raw")

    def start(self) -> None:
        """ start client. """
        Output.start(self)
        Client.start(self)

    def stop(self) -> None:
        """ stop client. """
        Output.stop(self)
        Client.stop(self)

    def wait(self) -> None:
        """ wait for client to finish. """
        Output.wait(self)
        Client.wait(self)


def debug(txt) -> None:
    """ text to screen if verbose is enabled. """
    if "v" in Config.opts:
        output(txt)


def output(txt) -> None:
    """ text to screen. """


def __dir__():
    return (
        'Default',
        'Client',
        'Fleet',
        'debug'
    )
