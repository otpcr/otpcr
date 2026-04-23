# This file is placed in the Public Domain.


"mailbox"


import mailbox
import os
import time


from otpcr.objects import Base, Methods, Object
from otpcr.persist import Disk, Locate
from otpcr.utility import Time


class Email(Base):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = ""


def timed(datestr):
    if not datestr:
        return time.time()
    tme = Time.date(datestr)
    if not tme:
        tme = time.time()
    return tme


def eml(event):
    nrs = -1
    args = ["From", "Subject"]
    args.extend(event.args)
    if event.gets:
        args.extend(Object.keys(event.gets))
    for key in event.silent:
        if key in args:
            args.remove(key)
    args = set(args)
    result = sorted(
                    Locate.find("email", event.gets),
                    key=lambda x: timed(x[1].Date)
                   )
    if event.index:
        obj = result[event.index]
        if obj:
            obj = obj[-1]
            tme = getattr(obj, "Date", "")
            event.reply(f'{event.index} {Methods.fmt(obj, args, plain=True)} {Time.elapsed(time.time() - timed(tme))}')
    else:
        for _fn, obj in result:
            nrs += 1
            tme = getattr(obj, "Date", "")
            event.reply(f'{nrs} {Methods.fmt(obj, args, plain=True)} {Time.elapsed(time.time() - timed(tme))}')
    if not result:
        event.reply("no emails found.")


def mbx(event):
    if not event.args:
        event.reply("mbx <path>")
        return
    fnm = os.path.expanduser(event.args[0])
    event.reply("reading from %s" % fnm)
    if os.path.isdir(fnm):
        thing = mailbox.Maildir(fnm, create=False)
    elif os.path.isfile(fnm):
        thing = mailbox.mbox(fnm, create=False)
    else:
        return
    try:
        thing.lock()
    except FileNotFoundError:
        pass
    nrs = 0
    for mail in thing:
        obj = Email()
        Object.update(obj, dict(mail._headers))
        obj.text = ""
        for payload in mail.walk():
            if payload.get_content_type() == 'text/plain':
                obj.text += payload.get_payload()
        obj.text = obj.text.replace("\\n", "\n")
        Disk.write(obj)
        nrs += 1
    if nrs:
        event.reply("ok %s" % nrs)
