# This file is placed in the Public Domain.


"make it non-blocking"


import inspect
import logging
import queue
import threading
import time
import _thread


class Task(threading.Thread):

    last = time.time()

    def __init__(self, func, *args, daemon=True, **kwargs):
        super().__init__(None, self.run, None, (), daemon=daemon)
        self.event = None
        self.name = kwargs.get("name", Thread.name(func))
        self.queue = queue.Queue()
        self.result = None
        self.starttime = time.time()
        self.stopped = threading.Event()
        self.queue.put((func, args))

    def __iter__(self):
        return self

    def __next__(self):
        yield from dir(self)

    def join(self, timeout=0.0):
        "join thread and return result."
        try:
            super().join(timeout or None)
            return self.result
        except (KeyboardInterrupt, EOFError) as ex:
            if self.event and self.event.ready:
                self.event.ready()
            raise ex

    def run(self):
        "run function."
        if time.time() - Task.last < 0.01:
            time.sleep(0.01)
        Task.last = time.time()
        func, args = self.queue.get()
        if args and hasattr(args[0], "ready"):
            self.event = args[0]
        try:
            self.result = func(*args)
            return self.result
        except (KeyboardInterrupt, EOFError):
            pass
        except Exception as ex:
            logging.exception(ex)
        if self.event:
            self.event.ready()
        _thread.interrupt_main()


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
        self.kwargs["name"] = self.name
        timer = Timy(self.sleep, self.run, *self.args, **self.kwargs)
        timer.start()
        self.timer = timer

    def stop(self):
        "stop timer."
        if self.timer:
            self.timer.cancel()


class Repeater(Timed):

    def run(self):
        "run function and launch timer for next run."
        Thread.launch(super().run)
        Thread.launch(self.start)


class Thread:

    lock = threading.RLock()

    @staticmethod
    def launch(func, *args, **kwargs):
        "run function in a thread."
        with Thread.lock:
            try:
                task = Task(func, *args, **kwargs)
                task.start()
                return task
            except (KeyboardInterrupt, EOFError):
                _thread.interrupt_main()

    @staticmethod
    def name(obj):
        "string of function/method."
        if inspect.ismethod(obj):
            return f"{obj.__self__.__class__.__name__}.{obj.__name__}"
        if inspect.isfunction(obj):
            return repr(obj).split()[1]
        return repr(obj)


def __dir__():
    return (
        'Repeater',
        'Thread',
        'Timed'
    )
