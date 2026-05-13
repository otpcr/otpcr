# This file is placed in the Public Domain.


"logging tests"


import unittest


from otpcr.objects import Base, Object


class TestObject(unittest.TestCase):

    def test_clear(self):
        obj = Base()
        obj.a = "b"
        Object.clear(obj)
        self.assertEqual(str(obj), "{}")
