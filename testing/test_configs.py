# This file is placed in the Public Domain.


"logging tests"


import unittest


from otpcr.configs import Main


class TestConfig(unittest.TestCase):

    def test_construct(self):
        config = Main()
        self.assertTrue(config)
