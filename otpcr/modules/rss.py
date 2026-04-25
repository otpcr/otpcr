# This file is placed in the Public Domain.


"rich site syndicate"


import html
import html.parser
import http.client
import logging
import os
import queue
import re
import threading
import urllib
import urllib.parse
import urllib.request
import uuid
import _thread


from urllib.error import HTTPError, URLError
from urllib.parse import quote_plus, urlencode


from otpcr.configs import Configuration, Main
from otpcr.handler import Broker
from otpcr.objects import Base, Methods, Object
from otpcr.persist import Disk, Locate
from otpcr.threads import Repeater, Thread
from otpcr.utility import Utils


def configure():
    Disk.read(Config, "rss", "config")


def init():
    Runners.init(1, Runner)
    Run.fetcher.start()
    nrs = Locate.count("rss")
    txt = f"{nrs} feeds"
    if nrs == 1:
        txt = txt[:-1]
    logging.warning(txt)


def shutdown():
    Run.fetcher.stop()


class Config(Configuration):

    polltime = 300


class Feed(Base):

    link = ""
    skip = False


class Modified(Base):

    pass


class Urls(Base):

    pass


class Rss(Base):

    def __init__(self):
        super().__init__()
        self.display_list = "title,link,author"
        self.insertid = None
        self.name = ""
        self.rss = ""


class State:

    configfn = ""
    modified = Modified()
    modifiedfn = ""
    seenfn = ""
    seen = Urls()
    skipped = []


class Fetcher:

    def __init__(self):
        self.dosave = False
        self.runner = Runner()
        self.stopped = threading.Event()
        self.todo = queue.Queue()

    def run(self, silent=False):
        nrs = 0
        for fnm, feed in Locate.find(Methods.fqn(Rss)):
            if "skip" in feed and feed.skip:
                continue
            Runners.put((fnm, feed, silent))
            nrs += 1
        return nrs

    def start(self, repeat=True):
        State.seenfn = Locate.last(State.seen) or Methods.ident(State.seen)
        State.modifiedfn = Locate.last(State.modified) or Methods.ident(State.modified)
        if repeat:
            repeater = Repeater(Config.polltime, self.run)
            repeater.start()

    def stop(self):
        logging.debug("stopped fetcher")
        if State.modified:
            Disk.write(State.modified, State.modifiedfn)
        self.stopped.set()


class Runner:

    def __init__(self):
        self.dosave = False
        self.fetchlock = threading.RLock()
        self.queue = queue.Queue()
        self.running = threading.Event()
        self.todo = queue.Queue()

    def display(self, obj):
        displaylist = ""
        result = ""
        try:
            displaylist = obj.display_list or "title,link"
        except AttributeError:
            displaylist = "title,link,author"
        for key in displaylist.split(","):
            if not key:
                continue
            data = getattr(obj, key, None)
            if not data:
                continue
            result += Helpers.unescape(Helpers.striphtml(data.replace("\n", " ").rstrip()))
            result += " - "
        return result[:-2].rstrip()

    def loop(self):
        while self.running.is_set():
            job = self.queue.get()
            if job is None:
                break
            self.fetch(*job)

    def fetch(self, fnm, feed, silent=False):
        with Run.fetchlock:
            result = []
            see = getattr(State.seen, feed.rss, [])
            urls = []
            counter = 0
            for obj in Helpers.getfeed(fnm, feed, feed.display_list):
                if obj is None:
                    continue
                counter += 1
                fed = Feed()
                Object.update(fed, obj)
                Object.update(fed, feed)
                url = urllib.parse.urlparse(fed.link)
                if url.path and not url.path == "/":
                    uurl = f"{url.scheme}://{url.netloc}/{url.path}"
                else:
                    uurl = fed.link
                urls.append(uurl)
                if uurl in see:
                    continue
                if self.dosave:
                    Disk.write(fed)
                result.append(fed)
            if urls:
                setattr(State.seen, feed.rss, urls)
            if silent:
                return counter
            if not State.seenfn:
                State.seenfn = Methods.ident(State.seen)
            Disk.write(State.seen, State.seenfn)
        txt = ""
        feedname = getattr(feed, "name", None)
        if feedname:
            txt = f"[{feedname}] "
        for obj in result:
            Broker.announce(txt + self.display(obj))
        return counter

    def put(self, args):
        self.queue.put(args)

    def start(self, daemon=True):
        Thread.launch(self.loop, daemon=daemon)

    def stop(self):
        self.running.clear()
        self.queue.put(None)


class Runners:

    runners = []
    lock = threading.RLock()
    nrcpu = 1
    nrlast = 0

    @staticmethod
    def add(client):
        Runners.runners.append(client)

    @staticmethod
    def init(nrcpu, cls):
        Runners.nrcpu = nrcpu
        for _x in range(Runners.nrcpu):
            clt = cls()
            clt.start()
            Runners.add(clt)

    @staticmethod
    def put(*args):
        if not Runners.runners:
            Runners.init(Runners.nrcpu, Runner)
        with Runners.lock:
            if Runners.nrlast >= Runners.nrcpu-1:
                Runners.nrlast = 0
            clt = Runners.runners[Runners.nrlast]
            clt.put(*args)
            Runners.nrlast += 1


class Parser:

    @staticmethod
    def getitem(line, item):
        lne = ""
        index1 = line.find(f"<{item}>")
        if index1 == -1:
            return lne
        index1 += len(item) + 2
        index2 = line.find(f"</{item}>", index1)
        if index2 == -1:
            return lne
        return Helpers.cdata(line[index1:index2]).strip()

    @staticmethod
    def getitems(text, token, nrs=None):
        index = 0
        end = len(text)
        stop = False
        nrx = -1
        while not stop:
            nrx += 1
            if nrs and nrx >= nrs:
                break
            index1 = text.rfind(f"<{token}", index, end)
            if index1 == -1:
                break
            end = index1
            index1 += len(token) + 2
            index2 = text.rfind(f"</{token}>", index1)
            if index2 == -1:
                break
            yield text[index1:index2]

    @staticmethod
    def parse(txt, toke="item", items="title,link"):
        for line in Parser.getitems(txt, toke):
            line = line.strip()
            obj = {}
            for itm in Utils.spl(items):
                val = Parser.getitem(line, itm)
                if val:
                    obj[itm] = Helpers.striphtml(Helpers.unescape(val.strip())).replace("\n", "")
            yield obj


class OPML:

    @staticmethod
    def getnames(line):
        return [x.split('="')[0] for x in line.split()]

    @staticmethod
    def getvalue(line, attr):
        lne = ""
        index1 = line.find(f'{attr}="')
        if index1 == -1:
            return lne
        index1 += len(attr) + 2
        index2 = line.find('"', index1)
        if index2 == -1:
            index2 = line.find("/>", index1)
        if index2 == -1:
            return lne
        return Helpers.cdata(line[index1:index2])

    @staticmethod
    def getattrs(line, token):
        index = 0
        result = []
        stop = False
        while not stop:
            index1 = line.find(f"<{token} ", index)
            if index1 == -1:
                return result
            index1 += len(token) + 2
            index2 = line.find("/>", index1)
            if index2 == -1:
                return result
            result.append(line[index1:index2])
            index = index2
        return result

    @staticmethod
    def parse(txt, toke="outline", itemz=None):
        if itemz is None:
            itemz = ",".join(OPML.getnames(txt))
        for attrz in OPML.getattrs(txt, toke):
            if not attrz:
                continue
            obj = {}
            for itm in Utils.spl(itemz):
                if itm == "link":
                    itm = "href"
                obj[itm] = OPML.getvalue(attrz, itm)
            yield obj


class Helpers:

    skip = [
        '403',
        '404',
        '410',
        '500',
        '503',
        'not valid',
        'not known',
        'failed'
    ]

    @staticmethod
    def attrs(obj, txt):
        "parse attribute into an object."
        Object.update(obj, *list(OPML.parse(txt)))

    @staticmethod
    def cdata(line):
        "scrape CDATA block."
        if "CDATA" in line:
            lne = line.replace("![CDATA[", "")
            lne = lne.replace("]]", "")
            lne = lne[1:-1]
            return lne
        return line

    @staticmethod
    def doskip(errors):
        for error in Helpers.skip:
            if error in errors:
                return True
        return False

    @staticmethod
    def getfeed(fnm, feed, items):
        "fetch a feed."
        result = [None,]
        try:
            response = Helpers.geturl(feed.rss)
            if not response.data:
                return result
            if "link" not in items:
                items += ",link"
            if feed.rss.endswith("atom"):
                yield from Parser.parse(str(response.data, "utf-8", errors='ignore'), "entry", items) or []
            else:
                yield from Parser.parse(str(response.data, "utf-8", errors='ignore'), "item", items) or []
        except TimeoutError:
            return result
        except (
                urllib.error.URLError,
                http.client.HTTPException,
                ValueError,
                HTTPError,
                URLError,
                UnicodeDecodeError,
                ConnectionResetError
        ) as ex:
            if '304' in str(ex):
                return result
            feed.error = str(ex)
            logging.debug("%s %s", feed.rss, feed.error)
            if Helpers.doskip(feed.error):
                feed.skip = True
                Disk.write(feed, fnm)
                logging.error("removed %s %s", feed.rss, ex)
        return result

    @staticmethod
    def gettinyurl(url):
        "query tinyurl for a link."
        postarray = [
            ("submit", "submit"),
            ("url", url),
        ]
        postdata = urlencode(postarray, quote_via=quote_plus)
        req = urllib.request.Request(
            "http://tinyurl.com/create.php", data=bytes(postdata, "UTF-8")
        )
        req.add_header("User-agent", Helpers.useragent("rss fetcher"))
        with urllib.request.urlopen(req) as htm:  # nosec
            for txt in htm.readlines():
                line = txt.decode("UTF-8").strip()
                i = re.search('data-clipboard-text="(.*?)"', line, re.M)
                if i:
                    return i.groups()
        return []

    @staticmethod
    def geturl(url, force=False):
        "fetch an url."
        url = urllib.parse.urlunparse(urllib.parse.urlparse(url))
        req = urllib.request.Request(str(url))
        req.add_header("User-Agent", Helpers.useragent("RSS Fetcher"))
        if not force:
            since = getattr(State.modified, url, "")
            if since:
                req.add_header('If-Modified-Since', since)
        logging.debug("fetching %s %s", url, req.headers)
        with urllib.request.urlopen(req, timeout=5.0) as response:  # nosec
            modi = response.headers.get('Last-Modified', "")
            if modi:
                setattr(State.modified, url, modi)
            response.data = response.read()
            return response

    @staticmethod
    def shortid():
        "return a shortid."
        return str(uuid.uuid4())[:8]

    @staticmethod
    def striphtml(text):
        "strip html."
        clean = re.compile("<.*?>")
        return re.sub(clean, "", text)

    @staticmethod
    def unescape(text):
        "unescape html."
        txt = re.sub(r"\s+", " ", text)
        return html.unescape(txt)

    @staticmethod
    def unquote(url):
        return urllib.parse.unquote(url, errors='ignore')

    @staticmethod
    def useragent(txt):
        "produce useragent string."
        return "Mozilla/5.0 (X11; Linux x86_64) " + txt


class Run:

    fetcher = Fetcher()
    fetchlock = _thread.allocate_lock()
    importlock = _thread.allocate_lock()


def atr(event):
    if not event.rest:
        event.reply("atr <stringinurl>")
        return
    for _fnm, obj in Locate.find(Methods.fqn(Rss), {'rss': event.rest}):
        try:
            request = Helpers.geturl(obj.rss, True)
        except Exception as ex:
            event.reply(ex)
            return
        if obj.rss.endswith('atom'):
            result = list(Parser.getitems(str(request.data, 'utf-8', errors='ignore'), 'entry', 1))
        else:
            result = list(Parser.getitems(str(request.data, 'utf-8', errors='ignore'), 'item', 1))
        resulting = []
        for x in re.findall('<.*?>', result[0]):
            if x[1] == '/' and len(x) > 4:
                resulting.append(x[2:-1])
        event.reply(','.join(resulting))


def dpl(event):
    if len(event.args) < 2:
        event.reply("dpl <stringinurl> <item1,item2>")
        return
    setter = {"display_list": event.args[1]}
    for fnm, feed in Locate.find(Methods.fqn(Rss), {"rss": event.args[0]}):
        if feed:
            Object.update(feed, setter)
            Disk.write(feed, fnm)
    event.reply("ok")


def err(event):
    nre = 0
    nrs = 0
    for fnm, obj in Locate.find(Methods.fqn(Rss), event.gets):
        if "error" not in obj:
            continue
        if not obj.error:
            continue
        if event.rest and event.rest in obj.error:
            nre += 1
            feed = Rss()
            Object.update(feed, obj)
            feed.__deleted__ = False
            feed.error = ""
            Disk.write(feed, fnm)
            continue
        if not event.rest:
            nrs += 1
            event.reply(f"{nrs} {Methods.fmt(obj)}")
    if not nrs:
        event.reply("no feed errors.")
    else:
        event.reply(f'{nre} feeds reset.')


def exp(event):
    with Run.importlock:
        event.reply(TEMPLATE)
        nrs = 0
        for _fn, ooo in Locate.find(Methods.fqn(Rss)):
            nrs += 1
            obj = Rss()
            Object.update(obj, ooo)
            name = f"url{nrs}"
            txt = f'<outline name="{name}" display_list="{obj.display_list}" xmlUrl="{obj.rss}"/>'
            event.reply(" " * 12 + txt)
        event.reply(" " * 8 + "</outline>")
        event.reply("    <body>")
        event.reply("</opml>")


def imp(event):
    if not event.args:
        event.reply("imp <filename>")
        return
    fnm = event.args[0]
    if not os.path.exists(fnm):
        event.reply(f"no {fnm} file found.")
        return
    with Run.importlock:
        with open(fnm, "r", encoding="utf-8") as file:
            txt = file.read()
        prs = OPML()
        nrs = 0
        nrskip = 0
        insertid = Helpers.shortid()
        for obj in prs.parse(txt, "outline", "name,xmlUrl"):
            url = obj["xmlUrl"]
            if url in State.skipped:
                continue
            if not url.startswith("http"):
                continue
            has = list(Locate.find(Methods.fqn(Rss), {"rss": url}, matching=True))
            if has:
                State.skipped.append(url)
                nrskip += 1
                continue
            feed = Rss()
            feed.rss = obj["xmlUrl"]
            del obj["xmlUrl"]
            Object.update(feed, obj)
            uri = urllib.parse.urlparse(feed.rss)
            if uri.netloc.count(".") >= 2:
                feed.name = ".".join(uri.netloc.split('.')[1:-1])
            else:
                feed.name = '.'.join(uri.netloc.split('.')[:-1])
            feed.insertid = insertid
            Disk.write(feed)
            nrs += 1
    if nrskip:
        event.reply(f"skipped {nrskip} urls.")
    if nrs:
        event.reply(f"added {nrs} urls.")


def nme(event):
    if len(event.args) != 2:
        event.reply("nme <stringinurl> <name>")
        return
    selector = {"rss": event.args[0]}
    for fnm, fed in Locate.find(Methods.fqn(Rss), selector):
        feed = Rss()
        Object.update(feed, fed)
        if feed:
            feed.name = str(event.args[1])
            Disk.write(feed, fnm)
    event.reply("ok")


def rem(event):
    if len(event.args) != 1:
        event.reply("rem <stringinurl>")
        return
    for fnm, fed in Locate.find(Methods.fqn(Rss)):
        feed = Rss()
        Object.update(feed, fed)
        if event.args[0] not in feed.rss:
            continue
        if feed:
            feed.__deleted__ = True
            Disk.write(feed, fnm)
            event.reply("ok")
            break


def res(event):
    if len(event.args) != 1:
        event.reply("res <stringinurl>")
        return
    nrs = 0
    for fnm, fed in Locate.find(Methods.fqn(Rss), removed=True):
        feed = Rss()
        Object.update(feed, fed)
        if event.args[0] not in feed.rss:
            continue
        nrs += 1
        feed.__deleted__ = False
        Disk.write(feed, fnm)
    event.reply(f"{nrs} feeds restored.")


def rss(event):
    if not event.rest:
        event.reply("rss <url>")
        return
    url = event.args[0]
    if "http://" not in url and "https://" not in url:
        event.reply("i need an url")
        return
    for fnm, result in Locate.find(Methods.fqn(Rss), {"rss": url}):
        if result:
            event.reply(f"{url} is known")
            return
    feed = Rss()
    feed.rss = event.args[0]
    Disk.write(feed)
    event.reply("ok")


def syn(event):
    if Main.debug:
        return
    fetcher = Fetcher()
    fetcher.start(False)
    nrs = fetcher.run(True)
    event.reply(f"{nrs} feeds synced")


TEMPLATE = """<opml version="1.0">
    <head>
        <title>OPML</title>
    </head>
    <body>
        <outline title="opml" text="rss feeds">"""
