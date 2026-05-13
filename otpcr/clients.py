# This file is placed in the Public Domain.


"clients"


import logging
import queue
import threading
import _thread


from .command import Commands
from .handler import Client
from .message import Message
from .threads import Thread


class Poller(Client):

    def loop(self):
        "polling loop."
        while not self.stopped.is_set():
            event = self.poll()
            if event is None:
                break
            if not event.text:
                event.ready()
                continue
            self.working.append(event)
            event.orig = repr(self)
            self.callback(event)
        self.done.set()

    def poll(self):
        return self.queue.get()


class Buffered(Poller):

    def __init__(self):
        super().__init__()
        self.oqueue = queue.Queue()
        self.ostopped = threading.Event()

    def output(self):
        "output loop."
        while not self.ostopped.is_set():
            try:
                event = self.oqueue.get()
            except (KeyboardInterrupt, EOFError):
                _thread.interrupt_main()
            if event is None:
                self.oqueue.task_done()
                break
            self.display(event)
            self.oqueue.task_done()

    def start(self, daemon=True):
        "start output loop."
        super().start(daemon=daemon)
        self.ostopped.clear()
        Thread.launch(self.output, daemon=daemon)

    def stop(self):
        "stop output loop."
        super().stop()
        self.ostopped.set()
        self.oqueue.put(None)

    def wait(self):
        "wait for output to finish."
        try:
            super().wait()
            self.oqueue.join()
        except Exception as ex:
            logging.exception(ex)
            _thread.interrupt_main()


class Waiter(Client):

    def loop(self):
        "polling loop."
        while not self.stopped.is_set():
            event = self.poll()
            if event is None:
                break
            if not event.text:
                event.ready()
                continue
            self.working.append(event)
            event.orig = repr(self)
            self.callback(event)
            event.wait()
        self.done.set()


class Console(Waiter):

    def __init__(self):
        super().__init__()
        self.register("command", Commands.command)

    def poll(self):
        "return event."
        evt = Message()
        evt.orig = repr(self)
        evt.text = input("> ")
        evt.kind = "command"
        return evt


def __dir__():
    return (
        'Buffered',
        'Console',
        'Poller',
        'Waiter'
    )
