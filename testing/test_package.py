# This file is placed in the Public Domain.


"package"


import unittest


from otpcr.package import Mods, initmods


class TestPackage(unittest.TestCase):

    def test_init(self):
        initmods("mod", "mod")
        self.assertTrue("mod" in Mods.dirs)
