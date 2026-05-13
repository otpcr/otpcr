# This file is placed in the Public Domain.


"todo"


from otpcr.defines import Base, Disk, Locate


class Todo(Base):

    def __init__(self):
        super().__init__()
        self.txt = ''


def dne(event):
    if not event.args:
        event.reply("dne <txt>")
        return
    selector = {'txt': event.args[0]}
    nmr = 0
    for fnm, obj in Locate.find('todo', selector):
        nmr += 1
        obj.__deleted__ = True
        Disk.write(obj, fnm)
        event.reply("ok")
        break
    if not nmr:
        event.reply("nothing todo")


def tdo(event):
    if not event.rest:
        event.reply("tdo <txt>")
        return
    obj = Todo()
    obj.txt = event.rest
    Disk.write(obj)
    event.reply("ok")
