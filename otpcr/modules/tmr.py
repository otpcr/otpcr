# This file is placed in the Public Domain.


"timers"


import logging
import random
import threading
import time


from otpcr.defines import Base, Broker, Disk, Locate, Object, Thread, Time


rand = random.SystemRandom()


def init():
    TimerLoop.start()
    logging.warning("%s timers" , len(TimerLoop.timers))


def shutdown():
    TimerLoop.stop()


class Timers(Base):

    pass


class TimerLoop:

    dosave = False
    lock = threading.RLock()
    path = ""
    running = threading.Event()
    timers = Timers()

    @classmethod
    def add(cls, tme, orig, channel,  txt):
        with cls.lock:
            setattr(cls.timers, str(tme), (orig, channel, txt))

    @classmethod
    def delete(cls, tme):
        with cls.lock:
            delattr(cls.timers, str(tme))

    @classmethod
    def loop(cls):
        while cls.running.is_set():
            time.sleep(1.0)
            timed = time.time()
            remove = []
            for tme, args in Object.items(cls.timers):
                if float(tme) < timed:
                    Thread.launch(cls.run, args)
                    remove.append(tme)
            for tme in remove:
                cls.dosave = True
                cls.delete(tme)

    @classmethod
    def run(cls, args):
        orig, channel, txt = args
        for origin, bot in Broker.like(orig):
            if not origin or not bot:
                continue
            bot.say(channel, txt)

    @classmethod
    def start(cls):
        cls.path = Locate.first(cls.timers) or Object.ident(cls.timers)
        cls.running.set()
        Thread.launch(cls.loop, name="Timers.loop")

    @classmethod
    def stop(cls):
        cls.running.clear()
        if cls.timers or cls.dosave:
            Disk.write(cls.timers, cls.path)


def tmr(event):
    if not event.rest:
        event.reply("tmr <date> <txt>")
        return
    todo = Time.extract(event.rest)
    if not todo:
        event.reply("can't determine time")
        return
    todo += rand.random()
    if not todo or time.time() > todo:
        event.reply("already passed given time.")
        return
    diff = todo - time.time()
    txt = " ".join(event.args[1:])
    bot = Broker.get(event.orig)
    TimerLoop.add(todo, Object.fqn(bot), event.channel, txt)
    event.ok(Time.elapsed(diff))
