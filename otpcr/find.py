# This file is placed in the Public Domain.
# pylint: disable=C,R,W0105,W0719,W0622,E1101,E0402


"locate objects"


import os
import time


from .cache   import Cache
from .default import Default
from .disk    import read, doskel, fqn
from .object  import Object, items, keys, update


p = os.path.join


class Workdir(Default):

    name = Default.__module__.split(".")[0]
    wdr  = ""

    def __init__(self):
        Default.__init__(self)
        self.name = Workdir.name
        self.wdr  = self.wdr or os.path.expanduser(f"~/.{Workdir.name}")


"path"


def long(name):
    split = name.split(".")[-1].lower()
    res = name
    for names in types():
        if split == names.split(".")[-1].lower():
            res = names
            break
    return res


def skel():
    return doskel(p(Workdir.wdr, "store", ""))


def store(pth=""):
    return p(Workdir.wdr, "store", pth)


def types():
    return os.listdir(store())


"find"


def fns(clz):
    dname = ''
    pth = store(clz)
    res = []
    for rootdir, dirs, _files in os.walk(pth, topdown=False):
        if dirs:
            for dname in sorted(dirs):
                if dname.count('-') == 2:
                    ddd = p(rootdir, dname)
                    for fll in os.listdir(ddd):
                        res.append(p(ddd, fll))
    return res


def find(clz, selector=None, index=None, deleted=False, matching=False):
    skel()
    nrs = -1
    pth = long(clz)
    res = []
    for fnm in fns(pth):
        obj = Cache.get(fnm)
        if not obj:
            obj = Object()
            read(obj, fnm)
            Cache.add(fnm, obj)
        if not deleted and '__deleted__' in dir(obj) and obj.__deleted__:
            continue
        if selector and not search(obj, selector, matching):
            continue
        nrs += 1
        if index is not None and nrs != int(index):
            continue
        res.append((fnm, obj))
    return sorted(res, key=lambda x: fntime(x[0]))


"methods"


def format(obj, args=None, skip=None, plain=False):
    if args is None:
        args = keys(obj)
    if skip is None:
        skip = []
    txt = ""
    for key in args:
        if key.startswith("__"):
            continue
        if key in skip:
            continue
        value = getattr(obj, key, None)
        if value is None:
            continue
        if plain:
            txt += f"{value} "
        elif isinstance(value, str) and len(value.split()) >= 2:
            txt += f'{key}="{value}" '
        else:
            txt += f'{key}={value} '
    return txt.strip()


def last(obj, selector=None):
    if selector is None:
        selector = {}
    result = sorted(
                    find(fqn(obj), selector),
                    key=lambda x: fntime(x[0])
                   )
    res = None
    if result:
        inp = result[-1]
        update(obj, inp[-1])
        res = inp[0]
    return res


def match(obj, txt):
    for key in keys(obj):
        if txt in key:
            yield key


def search(obj, selector, matching=None):
    res = False
    if not selector:
        return res
    for key, value in items(selector):
        val = getattr(obj, key, None)
        if not val:
            continue
        if matching and value == val:
            res = True
        elif str(value).lower() in str(val).lower():
            res = True
        else:
            res = False
            break
    return res


"utility"


def fntime(daystr):
    daystr = daystr.replace('_', ':')
    datestr = ' '.join(daystr.split(os.sep)[-2:])
    if '.' in datestr:
        datestr, rest = datestr.rsplit('.', 1)
    else:
        rest = ''
    timed = time.mktime(time.strptime(datestr, '%Y-%m-%d %H:%M:%S'))
    if rest:
        timed += float('.' + rest)
    return timed


def laps(seconds, short=True):
    txt = ""
    nsec = float(seconds)
    if nsec < 1:
        return f"{nsec:.2f}s"
    yea = 365*24*60*60
    week = 7*24*60*60
    nday = 24*60*60
    hour = 60*60
    minute = 60
    yeas = int(nsec/yea)
    nsec -= yeas*yea
    weeks = int(nsec/week)
    nsec -= weeks*week
    nrdays = int(nsec/nday)
    nsec -= nrdays*nday
    hours = int(nsec/hour)
    nsec -= hours*hour
    minutes = int(nsec/minute)
    nsec -= int(minute*minutes)
    sec = int(nsec)
    if yeas:
        txt += f"{yeas}y"
    if weeks:
        nrdays += weeks * 7
    if nrdays:
        txt += f"{nrdays}d"
    if short and txt:
        return txt.strip()
    if hours:
        txt += f"{hours}h"
    if minutes:
        txt += f"{minutes}m"
    if sec:
        txt += f"{sec}s"
    txt = txt.strip()
    return txt


def strip(pth, nmr=3):
    return os.sep.join(pth.split(os.sep)[-nmr:])


"interface"


def __dir__():
    return (
        'Workdir',
        'find',
        'format',
        'laps',
        'last',
        'skel'
    )
    