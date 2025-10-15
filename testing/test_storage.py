# This file is placed in the Public Domain.


import os
import sys
import unittest


sys.path.insert(0, ".")


from otpcr.objects import Object
from otpcr.caching import Cache, write
from otpcr.workdir import Workdir, store


import otpcr.caching


Workdir.wdr = '.test'


ATTRS1 = (
          'Cache',
          'find',
          'last',
          'read',
          'write'
         )


class TestStorage(unittest.TestCase):

    def test_constructor(self):
        obj = Cache()
        self.assertTrue(type(obj), Cache)

    def test__class(self):
        obj = Cache()
        clz = obj.__class__()
        self.assertTrue('Cache' in str(type(clz)))

    def test_dirmodule(self):
        self.assertEqual(
                         dir(otpcr.caching),
                         list(ATTRS1)
                        )

    def test_module(self):
        self.assertTrue(Cache().__module__, 'Cache')

    def test_save(self):
        obj = Object()
        opath = write(obj)
        print(opath)
        self.assertTrue(os.path.exists(opath))
