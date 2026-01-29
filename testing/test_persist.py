# This file is placed in the Public Domain.


import os
import sys
import unittest


sys.path.insert(0, ".")


from otpcr.objects import Object
from otpcr.persist import Cache, Workdir, write


Workdir.wdr = '.test'


class TestPersist(unittest.TestCase):

    def test_constructor(self):
        obj = Cache()
        self.assertTrue(type(obj), Cache)

    def test_save(self):
        obj = Object()
        opath = write(obj)
        self.assertTrue(os.path.exists(os.path.join(Workdir.wdr, "store", opath)))
