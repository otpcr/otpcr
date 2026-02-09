# This file is placed in the Public Domain.


"commands"


import unittest


from otpcr.clients import Client
from otpcr.command import Commands
from otpcr.objects import Dict, Object
from otpcr.message import Message


def cmnd(event):
    event.reply("yo!")


class TestCommands(unittest.TestCase):

    def test_construct(self):
        cmds = Commands()
        self.assertEqual(type(cmds), Commands)

    def test_addcmd(self):
        Commands.add(cmnd)
        self.assertTrue(Commands.has("cmnd"))
    
    def test_getcmd(self):
        Commands.add(cmnd)
        self.assertTrue(Commands.get("cmnd"))

    def test_hascmd(self):
        Commands.add(cmnd)
        self.assertTrue(Commands.get("cmnd"))
    
    def test_scancmd(self):
        from testing import dbg
        Commands.scan(dbg)
        self.assertTrue("dbg" in Commands.cmds)

    def test_command(self):
        clt = Client()
        Commands.add(cmnd)
        evt = Message()
        evt.text = "cmnd"
        evt.orig = repr(clt)
        Commands.command(evt)
        self.assertTrue("yo!" in Dict.values(evt.result))
