# This file is placed in the Public Domain.


"threads"


import queue
import threading
import time
import typing


from .excepts import later


STARTTIME = time.time()


lock = threading.RLock()


class Thread(threading.Thread):

    """ Thread """

    def __init__(self, func, thrname, *args, daemon=True, **kwargs):
        super().__init__(None, self.run, name, (), {}, daemon=daemon)
        self.name = thrname
        self.queue = queue.Queue()
        self.result = None
        self.starttime = time.time()
        self.stopped = threading.Event()
        self.queue.put((func, args))

    def run(self) -> None:
        """ code tu run in thread. """
        func, args = self.queue.get()
        try:
            self.result = func(*args)
        except Exception as ex:
            later(ex)
            if args and "ready" in dir(args[0]):
                args[0].ready()

    def join(self, timeout=None) -> typing.Any:
        """ join thread for result. """
        super().join(timeout)
        return self.result


def launch(func, *args, **kwargs) -> Thread:
    """ launch a thread. """
    nme = kwargs.get("name", name(func))
    thread = Thread(func, nme, *args, **kwargs)
    thread.start()
    return thread


def name(obj) -> str:
    """ return name of an object. """
    typ = type(obj)
    if '__builtins__' in dir(typ):
        return obj.__name__
    if '__self__' in dir(obj):
        return f'{obj.__self__.__class__.__name__}.{obj.__name__}'
    if '__class__' in dir(obj) and '__name__' in dir(obj):
        return f'{obj.__class__.__name__}.{obj.__name__}'
    if '__class__' in dir(obj):
        return f"{obj.__class__.__module__}.{obj.__class__.__name__}"
    if '__name__' in dir(obj):
        return f'{obj.__class__.__name__}.{obj.__name__}'
    return None


class Timer:

    """ Timer """

    def __init__(self, sleep, func, *args, thrname=None, **kwargs):
        self.args   = args
        self.func   = func
        self.kwargs = kwargs
        self.sleep  = sleep
        self.name   = thrname or kwargs.get("name", name(func))
        self.state  = {}
        self.timer  = None

    def run(self) -> None:
        """ run timer function. """
        self.state["latest"] = time.time()
        launch(self.func, *self.args)

    def start(self) -> None:
        """ start the timer. """
        timer = threading.Timer(self.sleep, self.run)
        timer.name   = self.name
        timer.sleep  = self.sleep
        timer.state  = self.state
        timer.func   = self.func
        timer.state["starttime"] = time.time()
        timer.state["latest"]    = time.time()
        timer.start()
        self.timer   = timer

    def stop(self) -> None:
        """ stop theme timer. """
        if self.timer:
            self.timer.cancel()


class Repeater(Timer):


    """ Repeater """

    def run(self) -> None:
        """ start the repeater. """
        launch(self.start)
        super().run()


def __dir__():
    return (
        'Repeater',
        'Thread',
        'Timer',
        'errors',
        'later',
        'launch',
        'name'
    )
