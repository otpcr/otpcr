# This file is placed in the Public Domain.


"log text"


from otpcr.objects import Base
from otpcr.persist import Disk


class Log(Base):

    def __init__(self):
        super().__init__()
        self.txt = ''


def log(event):
    if not event.rest:
        event.reply("log <txt>")
        return
    obj = Log()
    obj.txt = event.rest
    Disk.write(obj)
    event.reply("ok")
