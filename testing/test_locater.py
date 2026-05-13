# This file is placed in the Public Domain.


"logging tests"


import unittest


from otpcr.persist import Locate


class TestLocater(unittest.TestCase):

    def test_construct(self):
        lct = Locate()
        self.assertTrue(lct)
