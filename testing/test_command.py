# This file is placed in the Public Domain.


"commands"


import os
import unittest


from otpcr.command import Commands
from otpcr.handler import Event, Handler
from otpcr.package import Mods


def cmnd(event):
    event.reply("yo!")


class TestCommands(unittest.TestCase):

    def test_construct(self):
        cmds = Commands()
        self.assertEqual(type(cmds), Commands)

    def test_add(self):
        Commands.add(cmnd)
        self.assertTrue("cmnd" in Commands.cmds)

    def test_get(self):
        Commands.add(cmnd)
        self.assertTrue(Commands.get("cmnd"))

    def test_command(self):
        clt = Handler()
        Commands.add(cmnd)
        evt = Event()
        evt.text = "cmnd"
        evt.orig = repr(clt)
        Commands.command(evt)
        self.assertTrue("yo!" in evt.result)


class TestPackage(unittest.TestCase):

    def test_add(self):
        if os.path.exists("mods"):
            Mods.add("mods", "mods")
            self.assertTrue("mods" in Mods.dirs)
