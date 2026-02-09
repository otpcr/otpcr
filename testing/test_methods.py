# This file is placed in the Public Domain.


"methods"


import unittest


from otpcr.objects import Methods, Object


class TestMethods(unittest.TestCase):

    def testformat(self):
        o = Object()
        o.a = "b"
        self.assertEqual(Methods.fmt(o), 'a="b"')
