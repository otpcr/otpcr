# This file is placed in the Public Domain.


"engine"


import unittest


from otpcr.handler import Client, Event, Handler, Polled


buffer = []


class MyClient(Client):

    def raw(self, text):
        buffer.append(text)


def hello(event):
    print("hello")
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
        evt = Event()
        evt.kind = "hello"
        evt.text = "hello"
        self.hdl.callback(evt)
        evt.wait()
        self.assertTrue("hello" in evt.result)

    def test_loop(self):
        evt = Event()
        evt.kind = "hello"
        evt.text = "hello"
        self.hdl.put(evt)
        evt.wait()
        self.assertTrue(evt._ready.is_set())

    def test_loop2(self):
        evt = Event()
        evt.kind = "hello"
        evt.text = "hello bot"
        self.hdl.put(evt)
        evt.wait()
        self.assertTrue("hello bot" in evt.result)

    def test_put(self):
        hdl = Handler()
        evt = Event()
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
        evt = Event()
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
        clt = Polled()
        evt = Event()
        evt.text = "okdan"
        clt.iqueue.put(evt)
        event = clt.poll()
        self.assertTrue(event is evt)

    def test_put(self):
        evt = Event()
        evt.type = "hello"
        self.clt.put(evt)


class TestMessage(unittest.TestCase):

    def test_ready(self):
        msg = Event()
        msg.ready()  # pylint: disable=E1102
        self.assertTrue(msg._ready.is_set())

    def test_reply(self):
        msg = Event()
        msg.reply("test")
        self.assertTrue("test" in msg.result)

    def test_wait(self):
        msg = Event()
        msg.ready()  # pylint: disable=E1102
        msg.wait()
        self.assertTrue(msg._ready.is_set())
