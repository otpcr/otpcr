# This file is placed in the Public Domain.
# pylint: disable=C,E0402


"event"


import threading
import time


from .default import Default


class Event(Default):

    def __init__(self):
        Default.__init__(self)
        self._ex    = None
        self._ready = threading.Event()
        self._thr   = None
        self.ctime  = time.time()
        self.result = []
        self.type   = "event"
        self.txt    = ""

    def ready(self):
        self._ready.set()

    def reply(self, txt):
        self.result.append(txt)

    def wait(self):
        self._ready.wait()
        if self._thr:
            self._thr.join()


def __dir__():
    return (
        'Event',
    )
