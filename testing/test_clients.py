# This file is placed in the Public Domain.


"engine"


import unittest


from otpcr.clients import Poller
from otpcr.handler import Client
from otpcr.message import Message


buffer = []


class MyClient(Client):

    def raw(self, text):
        buffer.append(text)


def hello(event):
    event.reply(event.text)
    event.ready()


def output(self, txt):
    buffer.append(txt)


class TestInput(unittest.TestCase):

    def setUp(self):
        self.clt = MyClient()
        self.clt.silent = False
        self.clt.register("hello", hello)
        self.clt.start()

    def shutDown(self):
        self.clt.stop()

    def test_announce(self):
        self.clt.announce("hello")
        self.assertTrue("hello" in buffer)

    def test_display(self):
        evt = Message()
        evt.reply("test1")
        evt.reply("test2")
        self.clt.display(evt)
        self.assertTrue("test1" in buffer)
        self.assertTrue("test2" in buffer)
        self.assertTrue(buffer.index("test1") < buffer.index("test2"))

    def test_dosay(self):
        self.clt.dosay("#channel", "yo!")
        self.assertTrue("yo!" in buffer)

    def test_poll(self):
        clt = Poller()
        evt = Message()
        evt.text = "okdan"
        clt.queue.put(evt)
        event = clt.poll()
        self.assertTrue(event is evt)

    def test_put(self):
        evt = Message()
        evt.kind = "hello"
        self.clt.put(evt)
