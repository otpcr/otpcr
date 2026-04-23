# This file is placed in the Public Domain.


"web server"


import logging
import os
import sys
import time


from http.server import HTTPServer, BaseHTTPRequestHandler


from otpcr.configs import Configuration, Main
from otpcr.objects import Base
from otpcr.threads import Thread
from otpcr.utility import Utils


def init():
    path = Utils.pkgname(Base)
    if not os.path.exists(os.path.join(path, "network", 'index.html')):
        logging.warning("no index.html")
        return
    try:
        server = HTTP((Config.hostname, int(Config.port)), HTTPHandler)
        server.start()
        logging.warning("http://%s:%s", Config.hostname, Config.port)
        return server
    except OSError as ex:
        logging.warning("%s", str(ex))


class Config(Configuration):

    hostname = "localhost"
    path = ""
    port = 8000


class HTTP(HTTPServer, Base):

    daemon_thread = True
    allow_reuse_address = True

    def __init__(self, *args, **kwargs):
        HTTPServer.__init__(self, *args, **kwargs)
        Base.__init__(self)
        self.host = args[0]
        self._starttime = time.time()
        self._last = time.time()
        self._status = "start"

    def exit(self):
        time.sleep(0.2)
        self._status = ""
        self.shutdown()

    def start(self):
        Thread.launch(self.serve_forever)
        self._status = "ok"

    def request(self):
        self._last = time.time()

    def error(self, _request, _addr):
        exctype, excvalue, _trb = sys.exc_info()
        exc = exctype(excvalue)
        logging.exception(exc)


class HTTPHandler(BaseHTTPRequestHandler):

    def setup(self):
        BaseHTTPRequestHandler.setup(self)
        self._path = os.path.join(Utils.where(Base), "network")
        self._size = 0
        self._ip = self.client_address[0]

    def raw(self, data):
        self.wfile.write(data)

    def send(self, txt):
        self.wfile.write(bytes(txt, encoding="utf-8"))
        self.wfile.flush()

    def write_header(self, htype='text/plain', size=None):
        self.send_response(200)
        self.send_header('Content-type: ', '%s' % htype)
        if size is not None:
            self.send_header('Content-length', size)
        self.send_header('Server', "1")
        self.end_headers()

    def log(self, code):
        pass

    def do_GET(self):
        if "favicon" in self.path:
            return
        if Main.debug:
            return
        if self.path == "/":
            self.path = "index.html"
        path = self._path + os.sep + self.path
        ext = path[-3]
        if not os.path.exists(path):
            self.write_header("text/html")
            self.send_response(404)
            self.end_headers()
            return
        if "_images" in path:
            try:
                with open(path, "rb") as file:
                    img = file.read()
                    file.close()
                self.write_header(f"image/{ext}", len(img))
                self.raw(img)
            except (TypeError, FileNotFoundError, IsADirectoryError):
                self.send_response(404)
                self.end_headers()
            return
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as file:
                txt = file.read()
                file.close()
            if ext == "css":
                self.write_header("text/css")
            else:
                self.write_header("text/html")
            self.send(txt)
        except (TypeError, FileNotFoundError, IsADirectoryError):
            self.send_response(404)
            self.end_headers()


def html2(txt):
    return """<!doctype html>
<html>
   %s
</html>
""" % txt
