# This file is placed in the Public Domain.


import unittest


from otpcr.objects import Object
from otpcr.serials import dumps


VALIDJSON = '{"test": "bla"}'


class TestEncoder(unittest.TestCase):

    def test_dumps(self):
        obj = Object()
        obj.test = "bla"
        self.assertEqual(dumps(obj), VALIDJSON)
