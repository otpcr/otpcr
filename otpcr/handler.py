# This file is placed in the Public Domain.


"event handling"


import collections
import logging
import queue
import threading
import _thread


from .brokers import Broker
from .command import Commands
from .objects import Base
from .threads import Thread


class Event(Base):

    def __init__(self):
        Base.__init__(self)
        self._ready = threading.Event()
        self._thr = None
        self.args = []
        self.channel = ""
        self.index = 0
        self.kind = "event"
        self.orig = ""
        self.result = collections.deque()
        self.text = ""

    def display(self):
        "print results."
        bot = Broker.get(self.orig)
        if bot:
            bot.display(self)

    def ok(self, txt=""):
        "print ok response."
        if not txt:
            txt = self.text
        self.reply(f"ok {txt}".strip())

    def ready(self):
        "flag message as ready."
        self._ready.set()

    def reply(self, text):
        "add text to result."
        self.result.append(text)

    def wait(self, timeout=0.0):
        "wait for completion."
        if self._thr:
            self._thr.join(timeout or None)
        self._ready.wait(timeout or None)


class Handler:

    def __init__(self):
        self.cbs = {}
        self.queue = queue.Queue()
        self.running = threading.Event()

    def callback(self, event):
        "run callback function with event."
        func = self.cbs.get(event.kind, None)
        if not func:
            event.ready()
            return
        name = event.text and event.text.split()[0]
        event._thr = Thread.launch(func, event, name=name)

    def loop(self):
        "event loop."
        while self.running.is_set():
            event = self.queue.get()
            if event is None:
                break
            event.orig = repr(self)
            self.callback(event)

    def put(self, event):
        "put event on queue."
        self.queue.put(event)

    def register(self, kind, callback):
        "register callback."
        self.cbs[kind] = callback

    def start(self, daemon=False):
        "start event handler loop."
        self.running.set()
        Thread.launch(self.loop, daemon=daemon)

    def stop(self):
        "stop event handler loop."
        self.running.clear()
        self.queue.put(None)

    def wait(self):
        pass


class Client(Handler):

    def __init__(self):
        Handler.__init__(self)
        self.iqueue = queue.Queue()
        self.olock = threading.RLock()
        self.silent = False
        self.stopped = threading.Event()
        Broker.add(self)

    def announce(self, text):
        "announce text to all channels."
        if not self.silent:
            self.raw(text)

    def display(self, event):
        "display event results."
        with self.olock:
            for txt in event.result:
                self.dosay(event.channel, txt)

    def dosay(self, channel, text):
        "say called by display."
        self.say(channel, text)

    def loop(self):
        "input loop."
        while self.running.is_set():
            event = self.iqueue.get()
            if not event:
                break
            event.orig = repr(self)
            self.callback(event)

    def put(self, event):
        "put event into queue."
        self.iqueue.put(event)

    def raw(self, text):
        "raw output."

    def say(self, channel, text):
        "say text in channel."
        self.raw(text)

    def stop(self):
        "stop client."
        super().stop()
        self.running.clear()
        self.iqueue.put(None)


class Polled(Client):

    def loop(self):
        "polling loop."
        while self.running.is_set():
            event = self.poll()
            if event is None:
                break
            if not event.text:
                event.ready()
                continue
            event.orig = repr(self)
            self.callback(event)

    def poll(self):
        "return event."
        return self.iqueue.get()

    def start(self, daemon=True):
        super().start(daemon=daemon)


class Console(Polled):

    def __init__(self):
        super().__init__()
        self.register("command", Commands.command)

    def loop(self):
        "input loop."
        while self.running.is_set():
            event = self.poll()
            if event is None:
                break
            if not event.text:
                event.ready()
                continue
            event.orig = repr(self)
            self.callback(event)
            event.wait()


class Output(Polled):

    def __init__(self):
        super().__init__()
        self.oqueue = queue.Queue()

    def output(self):
        "output loop."
        while self.running.is_set():
            event = self.oqueue.get()
            if event is None:
                self.oqueue.task_done()
                break
            self.display(event)
            self.oqueue.task_done()

    def start(self, daemon=False):
        "start output loop."
        super().start(daemon=daemon)
        Thread.launch(self.output, daemon=daemon)

    def stop(self):
        "stop output loop."
        super().stop()
        self.oqueue.put(None)

    def wait(self):
        "wait for output to finish."
        try:
            self.oqueue.join()
        except Exception as ex:
            logging.exception(ex)
            _thread.interrupt_main()


def __dir__():
    return (
        'Client',
        'Console',
        'Event',
        'Handler',
        'Output'
    )
