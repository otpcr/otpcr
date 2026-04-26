# This file is placed in the Public Domain.


"timers"


import logging
import random
import threading
import time


from otpcr.brokers import Broker
from otpcr.objects import Base, Object, Methods
from otpcr.persist import Disk, Locate
from otpcr.threads import Timed
from otpcr.utility import Time


rand = random.SystemRandom()


def init():
    Timers.path = Locate.last(Timers.timers) or Methods.ident(Timers.timers)
    remove = []
    for tme, args in Object.items(Timers.timers):
        if not args:
            continue
        orig, channel, txt = args
        for origin, bot in Broker.like(orig):
            if not origin or not bot:
                continue
            diff = float(tme) - time.time()
            if diff > 0:
                timer = Timed(diff, bot.say, channel, txt)
                timer.start()
            else:
                remove.append(tme)
    for tme in remove:
        Timers.delete(tme)
    if Timers.timers:
        Disk.write(Timers.timers, Timers.path)
    logging.warning("%s timers", len(Timers.timers))


def shutdown():
    for timer in Timers.timers:
        print(timer)
        timer.stop()


class Timer(Base):

    pass


class Timers(Base):

    path = ""
    timers = Timer()
    lock = threading.RLock()

    @staticmethod
    def add(tme, orig, channel,  txt):
        with Timers.lock:
            setattr(Timers.timers, str(tme), (orig, channel, txt))

    @staticmethod
    def delete(tme):
        with Timers.lock:
            delattr(Timers.timers, str(tme))


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
    Timers.add(todo, event.orig, event.channel, txt)
    with Timers.lock:
        Disk.write(Timers.timers, Timers.path or Methods.ident(Timers.timers))
    bot = Broker.get(event.orig)
    if not bot:
        event.reply("no bot")
        return
    timer = Timed(diff, bot.say, event.channel, txt)
    timer.start()
    event.reply("ok " + Time.elapsed(diff))
