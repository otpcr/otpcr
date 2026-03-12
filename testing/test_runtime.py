# This file is placed in the Public Domain.


"runtime"


import unittest


from otpcr.defines import Main
from otpcr.runtime import Runtime


class TestRuntime(unittest.TestCase):

    def test_banner(self):
        version = Runtime.banner()
        self.assertTrue(version, Main.version)

    def test_boot(self):
        pass

    def test_daemon(self):
        pass

    def test_init(self):
        pass

    def test_out(self):
        pass

    def test_privileges(self):
        pass

    def test_scanner(self):
        pass

    def test_shutdown(self):
        pass

    def test_wrap(self):
        pass
