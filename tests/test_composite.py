# This file is placed in the Public Domain.


"composite"


import unittest


from otpcr.object import Object


class TestComposite(unittest.TestCase):

    "TestComposite"

    def testcomposite(self):
        "test composition."
        obj = Object()
        obj.obj = Object()
        obj.obj.abc = "test"
        self.assertEqual(obj.obj.abc, "test")
