# This file is placed in the Public Domain.


"threading"


import unittest


from otpcr.threads import Task


def func():
    return "ok"


class TestThread(unittest.TestCase):

    def test_task(self):
        task = Task(func)
        task.start()
        result = task.join()
        self.assertEqual(result, "ok")
