# This file is placed in the Public Domain.


"logging tests"


import unittest


from otpcr.objects import Base
from otpcr.parsers import Parse


class TestParse(unittest.TestCase):

    def test_parse(self):
        obj = Base()
        obj.cmd = ""
        Parse.parse(obj, "cmd")
        print(obj)
        self.assertEqual(obj.cmd, "cmd")
