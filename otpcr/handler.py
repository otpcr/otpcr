# This file is placed in the Public Domain.


"callback engine"


import logging
import queue
import threading
import time
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
        self.result = {}
        self.text = ""

    def display(self):
        bot = Broker.get(self.orig)
        if bot:
            bot.display(self)

    def ok(self, txt=""):
        self.reply(f"ok {txt}".strip())

    def ready(self):
        "flag message as ready."
        self._ready.set()

    def reply(self, text):
        "add text to result."
        self.result[time.time()] = text

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
            if not event:
                break
            event.orig = repr(self)
            self.callback(event)

    def put(self, event):
        "put event on queue."
        self.queue.put(event)

    def register(self, kind, callback):
        "register callback."
        self.cbs[kind] = callback

    def start(self):
        "start event handler loop."
        self.running.set()
        Thread.launch(self.loop)

    def stop(self):
        "stop event handler loop."
        self.running.clear()
        self.queue.put(None)


class Client(Handler):

    def __init__(self):
        Handler.__init__(self)
        self.iqueue = queue.Queue()
        self.olock = threading.RLock()
        self.silent = True
        self.stopped = threading.Event()
        Broker.add(self)

    def announce(self, text):
        "announce text to all channels."
        if not self.silent:
            self.raw(text)

    def display(self, event):
        "display event results."
        with self.olock:
            for tme in event.result:
                self.dosay(event.channel, event.result.get(tme))

    def dosay(self, channel, text):
        "say called by display."
        self.say(channel, text)

    def loop(self):
        "input loop."
        while True:
            event = self.poll()
            if not event or self.stopped.is_set():
                break
            event.orig = repr(self)
            self.callback(event)

    def poll(self):
        "return event."
        return self.iqueue.get()

    def put(self, event):
        self.iqueue.put(event)

    def raw(self, text):
        "raw output."

    def say(self, channel, text):
        "say text in channel."
        self.raw(text)


class Console(Client):

    def __init__(self):
        super().__init__()
        self.register("command", Commands.command)

    def loop(self):
        "input loop."
        while True:
            event = self.poll()
            if not event or self.stopped.is_set():
                break
            if not event.text:
                event.ready()
                continue
            event.orig = repr(self)
            self.callback(event)
            event.wait()
            time.sleep(0.001)

    def poll(self):
        "return event."
        return self.iqueue.get()


class Output(Client):

    def __init__(self):
        super().__init__()
        self.oqueue = queue.Queue()

    def output(self):
        "output loop."
        while True:
            event = self.oqueue.get()
            if event is None:
                self.oqueue.task_done()
                break
            self.display(event)
            self.oqueue.task_done()
            time.sleep(0.001)

    def start(self):
        "start output loop."
        super().start()
        Thread.launch(self.output)

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
