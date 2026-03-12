# This file is placed in the Public Domain.


"utilities"


import time
import unittest


from otpcr.utility import Utils


class TestUtilities(unittest.TestCase):

    def test_pkgname(self):
        self.assertEqual(Utils.pkgname(Utils), "otpcr")

    def test_strptime(self):
        date = time.strptime("2019-3-4 22:22", "%Y-%m-%d %H:%M")
        self.assertTrue(date is not None)
