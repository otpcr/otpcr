# This file is placed in the Public Domain.


"disk"


import unittest


from otpcr.persist import Disk


class TestStorage(unittest.TestCase):

    def test_disk(self):
        disk = Disk()
        self.assertTrue(disk)
