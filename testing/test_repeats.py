# This file is placed in the Public Domain.


"if it repeats it's important"


import unittest


from otpcr.repeats import Repeater


def hello(event):
    event.reply("hoi!")


class TestRepeater(unittest.TestCase):

    def test_construct(self):
        rpt = Repeater(60, hello)
        self.assertTrue(rpt)
