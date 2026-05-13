# This file is placed in the Public Domain.


"if it repeats it's important"


import threading
import time


from .threads import Thread


class Timy(threading.Timer):

    def __init__(self, sleep, func, *args, **kwargs):
        super().__init__(sleep, func)
        self.name = kwargs.get("name", Thread.name(func))
        self.sleep = sleep
        self.state = {}
        self.status = "none"
        self.state["latest"] = time.time()
        self.state["starttime"] = time.time()
        self.starttime = time.time()

    def stop(self):
        self.cancel()


class Timed:

    def __init__(self, sleep, func, *args, thrname="", **kwargs):
        self.args = args
        self.func = func
        self.kwargs = kwargs
        self.sleep = sleep
        self.name = thrname or kwargs.get("name", Thread.name(func))
        self.target = time.time() + self.sleep
        self.timer = None

    def run(self):
        "run timed function."
        self.timer.latest = time.time()
        self.timer.status = "wait"
        self.func(*self.args)
        self.timer.status = "idle"

    def start(self):
        "start timer."
        self.kwargs["daemon"] = True
        self.kwargs["name"] = self.name
        timer = Timy(self.sleep, self.run, *self.args, **self.kwargs)
        timer.start()
        self.timer = timer

    def stop(self):
        "stop timer."
        if self.timer:
            self.timer.cancel()
            self.timer = None


class Repeater(Timed):

    def run(self):
        "run function and launch timer for next run."
        Thread.launch(super().run)
        Thread.launch(self.start)


def __dir__():
    return (
        'Repeater',
        'Timed'
    )
