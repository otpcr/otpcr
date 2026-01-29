# This file is placed in the Public Domain.


"utilities"


import unittest

import otpcr.utility as TARGET


class TestUtilities(unittest.TestCase):

    def test_interface(self):
        print(dir(TARGET))
        self.assertTrue(True)
