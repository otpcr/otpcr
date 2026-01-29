# This file is placed in the Public Domain.


"engine"


import unittest


from otpcr.handler import Client, Handler
from otpcr.message import Message
from otpcr.methods import parse


buffer = []


class MyClient(Client):

    def raw(self, text):
        buffer.append(text)


def hello(event):
    event.reply(event.text)
    event.ready()


def output(self, txt):
    buffer.append(txt)


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
        print(evt)
        self.assertTrue("hello" in evt.result.values())

    def test_loop(self):
        evt = Message()
        evt.kind = "hello"
        self.hdl.put(evt)
        evt.wait()
        self.assertTrue(evt._ready.is_set())

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
        self.assertTrue(hdl.running.is_set())
    
    def test_stop(self):
        self.hdl.stop()
        self.assertTrue(not self.hdl.running.is_set())


class TestClient(unittest.TestCase):

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
    
    def test_loop(self):
        evt = Message()
        evt.kind = "hello"
        evt.text = "hello bot"
        self.clt.put(evt)
        evt.wait()
        self.assertTrue("hello bot" in evt.result.values())
    
    def test_poll(self):
         clt = Client()
         evt = Message()
         evt.text = "okdan"
         clt.iqueue.put(evt)
         event = clt.poll()
         self.assertTrue(event is evt)
     
    def test_put(self):
         evt = Message()
         evt.type = "hello"
         self.clt.put(evt)
                      