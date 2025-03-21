# This file is placed in the Public Domain.


"timers"


import time


from ..disk    import write
from ..find    import find, ident
from ..fleet   import Fleet
from ..object  import update
from ..thread  import launch
from ..timer   import Timer
from ..utils   import NoDate, elapsed, get_day, get_hour, to_day, today
from ..workdir import store


def init():
    for fnm, obj in find("timer"):
        diff = float(obj.time) - time.time()
        if diff > 0:
            timer = Timer(diff, Fleet.announce, obj.rest)
            timer.start()
        else:
            obj.__deleted__ = True
            write(obj, fnm)


def tmr(event):
    result = ""
    if not event.rest:
        nmr = 0
        for _fn, obj in find('timer'):
            lap = float(obj.time) - time.time()
            if lap > 0:
                event.reply(f'{nmr} {obj.txt} {elapsed(lap)}')
                nmr += 1
        if not nmr:
            event.reply("no timers.")
        return result
    seconds = 0
    line = ""
    for word in event.args:
        if word.startswith("+"):
            try:
                seconds = int(word[1:])
            except (ValueError, IndexError):
                event.reply(f"{seconds} is not an integer")
                return result
        else:
            line += word + " "
    if seconds:
        target = time.time() + seconds
    else:
        try:
            target = get_day(event.rest)
        except NoDate:
            target = to_day(today())
        hour =  get_hour(event.rest)
        if hour:
            target += hour
    if not target or time.time() > target:
        event.reply("already passed given time.")
        return result
    event.time = target
    diff = target - time.time()
    event.reply("ok " +  elapsed(diff))
    del event.args
    event.reply(event.rest)
    timer = Timer(diff, event.display)
    update(timer, event)
    write(timer, store(ident(timer)))
    launch(timer.start)
    return result
