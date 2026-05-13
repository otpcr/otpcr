# This file is placed in the Public Domain.


"event handling"


import threading


from .brokers import Broker
from .objects import Base


class Message(Base):

    def __init__(self):
        super().__init__()
        self._ready = threading.Event()
        self._thr = None
        self.args = []
        self.channel = ""
        self.cmd = ""
        self.index = 0
        self.kind = "event"
        self.orig = ""
        self.result = []
        self.text = ""

    def display(self):
        "print results."
        Broker.display(self)

    def ok(self, txt=""):
        "print ok response."
        self.reply(f"ok {txt}".strip())

    def ready(self):
        "flag message as ready."
        self._ready.set()

    def reply(self, text):
        "add text to result."
        self.result.append(text)

    def wait(self, timeout=0.0):
        "wait for completion."
        self._ready.wait(timeout or None)
        if self._thr:
            self._thr.join(timeout or None)


def __dir__():
    return (
        'Message'
    )
