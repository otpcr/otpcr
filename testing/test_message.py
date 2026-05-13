# This file is placed in the Public Domain.


"logging tests"


import unittest


from otpcr.message import Message


class TestMessage(unittest.TestCase):

    def test_ready(self):
        msg = Message()
        msg.ready()  # pylint: disable=E1102
        self.assertTrue(msg._ready.is_set())

    def test_reply(self):
        msg = Message()
        msg.reply("test")
        self.assertTrue("test" in msg.result)

    def test_wait(self):
        msg = Message()
        msg.ready()  # pylint: disable=E1102
        msg.wait()
        self.assertTrue(msg._ready.is_set())
