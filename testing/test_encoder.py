# This file is placed in the Public Domain.


import unittest


from otpcr.encoder import *
from otpcr.objects import *


VALIDJSON = '{"test": "bla"}'


class TestEncoder(unittest.TestCase):

    def test_dumps(self):
        obj = Object()
        obj.test = "bla"
        self.assertEqual(Json.dumps(obj), VALIDJSON)


class TestDecoder(unittest.TestCase):

    def test_loads(self):
        obj = Object()
        obj.test = "bla"
        oobj = Json.loads(Json.dumps(obj))
        self.assertEqual(oobj["test"], "bla")


class TestTypes(unittest.TestCase):

    def test_dict(self):
        obj = Json.loads(Json.dumps({"a": "b"}))
        self.assertEqual(obj, {"a": "b"})

    def test_integer(self):
        obj = Json.loads(Json.dumps(1))
        self.assertEqual(obj, 1)

    def test_float(self):
        obj = Json.loads(Json.dumps(1.0))
        self.assertEqual(obj, 1.0)

    def test_string(self):
        obj = Json.loads(Json.dumps("test"))
        self.assertEqual(obj, "test")

    def test_true(self):
        obj = Json.loads(Json.dumps(True))
        self.assertEqual(obj, True)

    def test_false(self):
        obj = Json.loads(Json.dumps(False))
        self.assertEqual(obj, False)

    def test_object(self):
        ooo = Object()
        ooo.a = "b"
        obj = Object()
        Dict.update(obj, Json.loads(Json.dumps(ooo)))
        self.assertEqual(obj.a, "b")
