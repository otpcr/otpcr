# This file is placed in the Public Domain.


"mailbox"


import mailbox
import os
import time


from ..disk    import write
from ..find    import find, ident
from ..object  import Object, fmt, keys, update
from ..utils   import elapsed, extract_date
from ..workdir import store


class Email(Object):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = ""


def todate(date):
    date = date.replace("_", ":")
    res = date.split()
    ddd = ""
    try:
        if "+" in res[3]:
            raise ValueError
        if "-" in res[3]:
            raise ValueError
        int(res[3])
        ddd = "{:4}-{:#02}-{:#02} {:6}".format(res[3], MONTH[res[2]], int(res[1]), res[4])
    except (IndexError, KeyError, ValueError) as ex:
        try:
            if "+" in res[4]:
                raise ValueError from ex
            if "-" in res[4]:
                raise ValueError from ex
            int(res[4])
            ddd = "{:4}-{:#02}-{:02} {:6}".format(res[4], MONTH[res[1]], int(res[2]), res[3])
        except (IndexError, KeyError, ValueError):
            try:
                ddd = "{:4}-{:#02}-{:02} {:6}".format(res[2], MONTH[res[1]], int(res[0]), res[3])
            except (IndexError, KeyError):
                try:
                    ddd = "{:4}-{:#02}-{:02}".format(res[2], MONTH[res[1]], int(res[0]))
                except (IndexError, KeyError):
                    try:
                        ddd = "{:4}-{:#02}".format(res[2], MONTH[res[1]])
                    except (IndexError, KeyError):
                        try:
                            ddd = "{:4}".format(res[2])
                        except (IndexError, KeyError):
                            ddd = ""
    return ddd


"commands"


def eml(event):
    nrs = -1
    args = ["From", "Subject"]
    if len(event.args) > 1:
        args.extend(event.args[1:])
    if event.gets:
        args.extend(keys(event.gets))
    for key in keys(event.silent):
        if key in args:
            args.remove(key)
    args = set(args)        
    result = sorted(find("email", event.gets), key=lambda x: extract_date(todate(getattr(x[1], "Date", ""))))
    if event.index:
        o = result[event.index][1]
        tme = getattr(o, "Date", "")
        event.reply(f'{event.index} {fmt(o, args, plain=True)} {elapsed(time.time() - extract_date(todate(tme)))}')
    else:
        for fnm, o in result:
            nrs += 1
            tme = getattr(o, "Date", "")
            event.reply(f'{nrs} {fmt(o, args, plain=True)} {elapsed(time.time() - extract_date(todate(tme)))}')
    if not result:
        event.reply("no emails found.")


def mbx(event):
    if not event.args:
        event.reply("mbx <path>")
        return
    fn = os.path.expanduser(event.args[0])
    event.reply("reading from %s" % fn)
    nr = 0
    if os.path.isdir(fn):
        thing = mailbox.Maildir(fn, create=False)
    elif os.path.isfile(fn):
        thing = mailbox.mbox(fn, create=False)
    else:
        return
    try:
        thing.lock()
    except FileNotFoundError:
        pass
    for m in thing:
        o = Email()
        update(o, dict(m._headers))
        o.text = ""
        for payload in m.walk():
            if payload.get_content_type() == 'text/plain':
                o.text += payload.get_payload()
        o.text = o.text.replace("\\n", "\n")
        write(o, store(ident(o)))
        nr += 1
    if nr:
        event.reply("ok %s" % nr)


MONTH = {
    'Jan': 1,
    'Feb': 2,
    'Mar': 3,
    'Apr': 4,
    'May': 5,
    'Jun': 6,
    'Jul': 7,
    'Aug': 8,
    'Sep': 9,
    'Oct': 10,
    'Nov': 11,
    'Dec': 12
}
