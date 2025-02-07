# This file is placed in the Public Domain.


"reactor"


import queue
import threading
import time
import _thread


from .default import Default
from .excepts import later
from .threads import launch


cblock = threading.RLock()
lock   = threading.RLock()


class Event(Default):

    "Event"

    def __init__(self):
        Default.__init__(self)
        self._ready = threading.Event()
        self._thr   = None
        self.ctime  = time.time()
        self.result = {}
        self.type   = "event"
        self.txt    = ""

    def display(self) -> None:
        """ display result to channel """
        Fleet.display(self)

    def done(self) -> None:
        """ echo ok """
        self.reply("ok")

    def ready(self) -> None:
        """ flag ready """
        self._ready.set()

    def reply(self, txt) -> None:
        """ add to result. """
        self.result[time.time()] = txt

    def wait(self) -> None:
        """ wait for completion. """
        self._ready.wait()
        if self._thr:
            self._thr.join()


class Reactor:

    """ Reactor """

    def __init__(self):
        self.cbs     = {}
        self.queue   = queue.Queue()
        self.ready   = threading.Event()
        self.stopped = threading.Event()

    def callback(self, evt) -> None:
        """ run callback in it'w own thread. """
        with cblock:
            func = self.cbs.get(evt.type, None)
            if func:
                try:
                    evt._thr = launch(func, evt, name=evt.cmd or evt.txt)
                except Exception as ex:
                    later(ex)
                    evt.ready()

    def loop(self) -> None:
        """ event handling loop. """
        evt = None
        while not self.stopped.is_set():
            try:
                evt = self.poll()
                if evt is None:
                    break
                evt.orig = repr(self)
                self.callback(evt)
            except (KeyboardInterrupt, EOFError):
                if evt:
                    evt.ready()
                _thread.interrupt_main()
        self.ready.set()

    def poll(self) -> Event:
        """ return event to be processed. """
        return self.queue.get()

    def put(self, evt) -> None:
        """ put event in queue. """
        self.queue.put(evt)

    def register(self, typ, cbs) -> None:
        """ register callback. """
        self.cbs[typ] = cbs

    def start(self) -> None:
        """ start event handler. """
        self.stopped.clear()
        self.ready.clear()
        launch(self.loop)

    def stop(self) -> None:
        """ stop event handler. """
        self.stopped.set()
        self.queue.put(None)

    def wait(self) -> None:
        """ wait for ready. """
        self.ready.wait()


class Fleet:

    """ Fleet """

    bots = {}

    @staticmethod
    def add(bot) -> None:
        """ add bot to fleet. """
        Fleet.bots[repr(bot)] = bot

    @staticmethod
    def announce(txt) -> None:
        """ announce on all bots. """
        for bot in Fleet.bots.values():
            bot.announce(txt)

    @staticmethod
    def display(evt) -> None:
        """ display event on orignating bot. """
        with lock:
            for tme in sorted(evt.result):
                text = evt.result[tme]
                Fleet.say(evt.orig, evt.channel, text)
            evt.ready()

    @staticmethod
    def first() -> None:
        """ return first bot in fleet. """
        bots =  list(Fleet.bots.values())
        res = None
        if bots:
            res = bots[0]
        return res

    @staticmethod
    def get(orig) -> None:
        """ return bot by origin. """
        return Fleet.bots.get(orig, None)

    @staticmethod
    def say(orig, channel, txt) -> None:
        """ say text in channel. """
        bot = Fleet.get(orig)
        if bot:
            bot.say(channel, txt)

    @staticmethod
    def wait():
        """ call wait on all bots. """
        for bot in Fleet.bots.values():
            if "wait" in dir(bot):
                bot.wait()


def __dir__():
    return (
        'Event',
        'Fleet',
        'Reactor'
    )
