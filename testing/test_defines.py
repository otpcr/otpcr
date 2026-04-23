# This file is placed in the Public Domain.


"definition tests"


import unittest


from otpcr.configs import Main


class TestDefines(unittest.TestCase):

    def test_main(self):
        main = Main()
        self.assertEqual(type(main), Main)
