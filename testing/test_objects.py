# This file is placed in the Public Domain.


"obejcts tests"


import unittest


from otpcr.objects import Dict, Methods, Object


import otpcr.objects


TARGET = otpcr.objects
VALIDJSON = '{"test": "bla"}'


class TestObject(unittest.TestCase):

    def test_constructor(self):
        obj = Object()
        self.assertTrue(type(obj), Object)

    def test_class(self):
        obj = Object()
        clz = obj.__class__()
        self.assertTrue("Object" in str(type(clz)))

    def test_contains(self):
        obj = Object()
        obj.key = "value"
        self.assertTrue("key" in obj)

    def test_delattr(self):
        obj = Object()
        obj.key = "value"
        del obj.key
        self.assertTrue("key" not in obj)

    def test_dict(self):
        obj = Object()
        self.assertEqual(obj.__dict__, {})

    def test_doc(self):
        obj = Object()
        self.assertEqual(obj.__doc__, None)

    def test_format(self):
        obj = Object()
        self.assertEqual(format(obj, ""), "{}")

    def test_getattribute(self):
        obj = Object()
        obj.key = "value"
        self.assertEqual(getattr(obj, "key", None), "value")

    def test_hash__(self):
        obj = Object()
        hsj = hash(obj)
        self.assertTrue(isinstance(hsj, int))

    def test_init(self):
        obj = Object()
        self.assertTrue(type(Object.__init__(obj)), Dict)

    def test_iter(self):
        obj = Object()
        obj.key = "value"
        self.assertTrue(list(iter(obj)), ["key",])

    def test_getattr(self):
        obj = Object()
        obj.key = "value"
        self.assertEqual(getattr(obj, "key"), "value")

    def test_keys(self):
        obj = Object()
        obj.key = "value"
        self.assertEqual(list(Dict.keys(obj)), ["key"])

    def test_len(self):
        obj = Object()
        self.assertEqual(len(obj), 0)

    def test_items(self):
        obj = Object()
        obj.key = "value"
        self.assertEqual(list(Dict.items(obj)), [("key", "value")])

    def test_register(self):
        obj = Object()
        setattr(obj, "key", "value")
        self.assertEqual(obj.key, "value")

    def test_repr(self):
        self.assertTrue(
                        repr(Dict.update(Object(), {"key": "value"})),
                        {"key": "value"}
                       )

    def test_setattr(self):
        obj = Object()
        setattr(obj, "key", "value")
        self.assertTrue(obj.key, "value")

    def test_str(self):
        obj = Object()
        self.assertEqual(str(obj), "{}")

    def test_update(self):
        obj = Object()
        obj.key = "value"
        oobj = Object()
        Dict.update(oobj, obj)
        self.assertTrue(oobj.key, "value")

    def test_values(self):
        obj = Object()
        obj.key = "value"
        self.assertEqual(list(Dict.values(obj)), ["value"])


class TestComposite(unittest.TestCase):

    def testcomposite(self):
        obj = Object()
        obj.obj = Object()
        obj.obj.a = "test"
        self.assertEqual(obj.obj.a, "test")


class TestMethods(unittest.TestCase):

    def testformat(self):
        o = Object()
        o.a = "b"
        self.assertEqual(Methods.fmt(o), 'a="b"')
