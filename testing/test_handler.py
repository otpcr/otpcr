# This file is placed in the Public Domain.


"engine"


import unittest


from otpcr.handler import Handler
from otpcr.message import Message


buffer = []


def hello(event):
    event.reply(event.text)
    event.ready()


class TestHandler(unittest.TestCase):

    hdl = Handler()

    def setUp(self):
        self.hdl.register("hello", hello)
        self.hdl.start()

    def shutDown(self):
        self.hdl.stop()

    def test_callback(self):
        evt = Message()
        evt.kind = "hello"
        evt.text = "hello"
        self.hdl.callback(evt)
        evt.wait()
        self.assertTrue("hello" in evt.result)

    def test_loop(self):
        evt = Message()
        evt.kind = "hello"
        evt.text = "hello"
        self.hdl.put(evt)
        evt.wait()
        self.assertTrue(evt._ready.is_set())

    def test_loop2(self):
        evt = Message()
        evt.kind = "hello"
        evt.text = "hello bot"
        self.hdl.put(evt)
        evt.wait()
        self.assertTrue("hello bot" in evt.result)

    def test_put(self):
        hdl = Handler()
        evt = Message()
        evt.kind = "hello"
        hdl.put(evt)
        event = hdl.queue.get()
        self.assertTrue(event is evt)

    def test_register(self):
        self.hdl.register("hlo", hello)
        self.assertTrue(hello in self.hdl.cbs.values())

    def test_start(self):
        hdl = Handler()
        hdl.start()
        self.assertTrue(not hdl.stopped.is_set())

    def test_stop(self):
        self.hdl.stop()
        self.assertTrue(self.hdl.stopped.is_set())
