# This file is placed in the Public Domain.


"commands"


import unittest


from otpcr.command import *
from otpcr.handler import Client
from otpcr.message import Message
from otpcr.objects import values


def cmnd(event):
    event.reply("yo!")


class TestCommands(unittest.TestCase):

    def test_construct(self):
        cmds = Commands()
        self.assertEqual(type(cmds), Commands)

    def test_addcmd(self):
        addcmd(cmnd)
        self.assertTrue(hascmd("cmnd"))
    
    def test_getcmd(self):
        addcmd(cmnd)
        self.assertTrue(getcmd("cmnd"))

    def test_hascmd(self):
        addcmd(cmnd)
        self.assertTrue(hascmd("cmnd"))
    
    def test_scancmd(self):
        from testing import dbg
        scancmd(dbg)
        self.assertTrue("dbg" in Commands.cmds)

    def test_command(self):
        clt = Client()
        addcmd(cmnd)
        evt = Message()
        evt.text = "cmnd"
        evt.orig = repr(clt)
        command(evt)
        print(evt)
        self.assertTrue("yo!" in values(evt.result))
