# This file is placed in the Public Domain.


"usefulness"


import datetime
import inspect
import logging
import os
import time


from .objects import Base


class NoDate(Exception):

    pass


class Time:

    @staticmethod
    def date(daystr):
        "date from string."
        daystr = daystr.encode('utf-8', 'replace').decode("utf-8")
        for fmat in TIMES:
            try:
                return time.mktime(time.strptime(daystr, fmat))
            except ValueError:
                pass

    @staticmethod
    def elapsed(seconds, short=True):
        "seconds to string."
        txt = ""
        nsec = float(seconds)
        if nsec < 1:
            return f"{nsec:.2f}s"
        yea = 365 * 24 * 60 * 60
        week = 7 * 24 * 60 * 60
        nday = 24 * 60 * 60
        hou = 60 * 60
        minute = 60
        yeas = int(nsec / yea)
        nsec -= yeas * yea
        weeks = int(nsec / week)
        nsec -= weeks * week
        nrdays = int(nsec / nday)
        nsec -= nrdays * nday
        hours = int(nsec / hou)
        nsec -= hours * hou
        minutes = int(nsec / minute)
        nsec -= minutes * minute
        sec = int(nsec / 1)
        nsec -= nsec - sec
        if yeas:
            txt += f"{yeas}y"
        if weeks:
            nrdays += weeks * 7
        if nrdays:
            txt += f"{nrdays}d"
        if hours:
            txt += f"{hours}h"
        if short and txt:
            return txt.strip()
        if minutes:
            txt += f"{minutes}m"
        if sec:
            txt += f"{sec}s"
        txt = txt.strip()
        return txt

    @staticmethod
    def extract(daystr):
        "extract date/time from string."
        daystr = str(daystr)
        res = None
        for word in daystr.split():
            if word.startswith("+"):
                try:
                    return int(word[1:]) + time.time()
                except (ValueError, IndexError):
                    continue
            res = Time.date(word.strip())
            if not res:
                date = datetime.date.fromtimestamp(time.time())
                word = f"{date.year}-{date.month}-{date.day}" + " " + word
                res = Time.date(word.strip())
            if res:
                break
        return res

    @staticmethod
    def fntime(daystr):
        "time from path."
        datestr = " ".join(daystr.split(os.sep)[-2:])
        datestr = datestr.replace("_", " ")
        if "." in datestr:
            datestr, rest = datestr.rsplit(".", 1)
        else:
            rest = ""
        timd = time.mktime(time.strptime(datestr, "%Y-%m-%d %H:%M:%S"))
        if rest:
            timd += float("." + rest)
        return float(timd)

    @staticmethod
    def today():
        "start of the day."
        return str(datetime.datetime.today()).split()[0]


class Utils:

    @staticmethod
    def clsname(obj):
        return obj.__class__.__name__

    @staticmethod
    def md5dir(path):
        md5s = {}
        for fnm in os.listdir(path):
            if not fnm.endswith(".py"):
                continue
            name = fnm[:-3]
            mpath = os.path.join(path, fnm)
            md5s[name] = Utils.md5sum(mpath)
        return md5s

    @staticmethod
    def md5sum(path):
        "return md5 of a file."
        import hashlib
        if not os.path.exists(path):
            return ""
        with open(path, "r", encoding="utf-8") as file:
            txt = file.read().encode("utf-8")
            return hashlib.md5(txt, usedforsecurity=False).hexdigest()  # pylint: disable=E1123

    @staticmethod
    def modname(obj):
        "return package name of an object."
        return obj.__module__.split(".")[-1]

    @staticmethod
    def pkgname(obj):
        "return package name of an object."
        return obj.__module__.split(".", maxsplit=1)[0]

    @staticmethod
    def pipxdir(name):
        "return examples directory."
        return f"~/.local/share/pipx/venvs/{name}/share/{name}/"

    @staticmethod
    def spl(txt):
        "list from comma seperated string."
        try:
            result = txt.split(",")
        except (TypeError, ValueError):
            result = []
        return [x for x in result if x]

    @staticmethod
    def where(obj):
        "path where object is defined."
        return os.path.dirname(inspect.getfile(obj))

    @staticmethod
    def wrapped(func):
        "wrap function in a try/except, silence ctrl-c/ctrl-d."
        try:
            func()
        except (KeyboardInterrupt, EOFError):
            pass


class Format(logging.Formatter):

    disable = False
    size = 3

    def format(self, record):
        if not Format.disable:
            record.module = record.module.upper()
            record.module = record.module[:Format.size]
        return logging.Formatter.format(self, record)


class Log:

    datefmt = "%H:%M:%S"
    format = "%(module)-3s %(message)s"

    @staticmethod
    def size(nr):
        "set text size."
        index = Log.format.find("-")+1
        newformat = Log.format[:index]
        newformat += str(nr)
        newformat += Log.format[index+1:]
        Log.format = newformat
        Format.size = nr

    @staticmethod
    def level(loglevel):
        "set log level."
        formatter = Format(Log.format, Log.datefmt)
        stream = logging.StreamHandler()
        stream.setFormatter(formatter)
        logging.basicConfig(
            level=loglevel.upper(),
            handlers=[stream,],
            force=True
        )


LEVELS = Base({
    "notset": logging.NOTSET,
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
    "fatal": logging.FATAL
})


TIMES = [
    "%a, %d %b %Y %H:%M:%S %z",
    "%a, %d %b %Y %H:%M:%S",
    "%a, %d %b %Y %T %z",
    "%a, %d %b %Y %T",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d %H:%M",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d",
    "%d-%m-%Y",
    "%d-%m",
    "%m-%d"
]


def __dir__():
    return (
        'COLORS',
        'LEVELS',
        'TIMES',
        'Log',
        'Time',
        'Utils'
    )
