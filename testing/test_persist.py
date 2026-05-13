# This file is placed in the Public Domain.


"persist tests"


import sys
import unittest


sys.path.insert(0, ".")


from otpcr.defines import Disk, Main, Object, Workdir, e, j


Workdir.wdr = '.test'


class TestPersist(unittest.TestCase):

    def test_loadcfg(self):
        Main.a = "b"
        Disk.read(Main, "main", "config")
        self.assertEqual(Main.a, "b")

    def test_save(self):
        obj = Object()
        opath = Disk.write(obj)
        self.assertTrue(e(j(Workdir.wdr, "store", opath)))

    def test_writecfg(self):
        Main.a = "b"
        Disk.write(Main, "main", "config")
        self.assertTrue(e(j(Workdir.wdr, "config", "main")))
