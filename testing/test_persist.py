# This file is placed in the Public Domain.


"persist tests"


import os
import sys
import unittest


sys.path.insert(0, ".")


from otpcr.configs import Main
from otpcr.objects import Base
from otpcr.persist import Cfg, Disk


Main.wdr = '.test'


class TestPersist(unittest.TestCase):

    def test_loadcfg(self):
        Main.a = "b"
        Cfg.load(Main)
        self.assertEqual(Main.a, "b")

    def test_save(self):
        obj = Base()
        opath = Disk.write(obj)
        self.assertTrue(os.path.exists(os.path.join(
                                                    Main.wdr,
                                                    "store",
                                                    opath
                                                   )))

    def test_writecfg(self):
        Main.a = "b"
        Cfg.save(Main, "main")
        self.assertTrue(os.path.exists(os.path.join(
                                                    Main.wdr,
                                                    "config",
                                                    "main"
                                                   )))
