# This file is placed in the Public Domain.


"obejcts tests"


import unittest


from otpcr.encoder import Json
from otpcr.objects import Base, Object, Methods
from otpcr.persist import Disk


import otpcr.objects


TARGET = otpcr.objects
VALIDJSON = '{"test": "bla"}'


class TestObject(unittest.TestCase):

    def test_constructor(self):
        obj = Base()
        self.assertTrue(type(obj), Base)

    def test_class(self):
        obj = Base()
        clz = obj.__class__()
        self.assertTrue("Base" in str(type(clz)))

    def test_contains(self):
        obj = Base()
        obj.key = "value"
        self.assertTrue("key" in obj)

    def test_delattr(self):
        obj = Base()
        obj.key = "value"
        del obj.key
        self.assertTrue("key" not in obj)

    def test_dict(self):
        obj = Base()
        self.assertEqual(obj.__dict__, {})

    def test_doc(self):
        obj = Base()
        self.assertEqual(obj.__doc__, None)

    def test_format(self):
        obj = Base()
        self.assertEqual(format(obj, ""), "{}")

    def test_getattribute(self):
        obj = Base()
        obj.key = "value"
        self.assertEqual(getattr(obj, "key", None), "value")

    def test_hash__(self):
        obj = Base()
        hsj = hash(obj)
        self.assertTrue(isinstance(hsj, int))

    def test_init(self):
        obj = Base()
        self.assertTrue(type(Base.__init__(obj)), Base)

    def test_iter(self):
        obj = Base()
        obj.key = "value"
        self.assertTrue(list(iter(obj)), ["key",])

    def test_getattr(self):
        obj = Base()
        obj.key = "value"
        self.assertEqual(getattr(obj, "key"), "value")

    def test_keys(self):
        obj = Base()
        obj.key = "value"
        self.assertEqual(list(Object.keys(obj)), ["key"])

    def test_len(self):
        obj = Base()
        self.assertEqual(len(obj), 0)

    def test_items(self):
        obj = Base()
        obj.key = "value"
        self.assertEqual(list(Object.items(obj)), [("key", "value")])

    def test_read(self):
        obj = Base()
        Disk.read(obj, "bla")
        res = {}
        Object.update(res, obj)
        self.assertEqual(res, {})

    def test_register(self):
        obj = Base()
        setattr(obj, "key", "value")
        self.assertEqual(obj.key, "value")

    def test_repr(self):
        self.assertTrue(
                        repr(Object.update(Base(), {"key": "value"})),
                        {"key": "value"}
                       )

    def test_setattr(self):
        obj = Base()
        setattr(obj, "key", "value")
        self.assertTrue(obj.key, "value")

    def test_str(self):
        obj = Base()
        self.assertEqual(str(obj), "{}")

    def test_update(self):
        obj = Base()
        obj.key = "value"
        oobj = Base()
        Object.update(oobj, obj)
        self.assertTrue(oobj.key, "value")

    def test_values(self):
        obj = Base()
        obj.key = "value"
        self.assertEqual(list(Object.values(obj)), ["value"])


class TestComposite(unittest.TestCase):

    def testcomposite(self):
        obj = Base()
        obj.obj = Base()
        obj.obj.a = "test"
        self.assertEqual(obj.obj.a, "test")


class TestMethods(unittest.TestCase):

    def testformat(self):
        o = Base()
        o.a = "b"
        self.assertEqual(Methods.fmt(o), 'a="b"')


VALIDJSON = '{"test": "bla"}'


class TestEncoder(unittest.TestCase):

    def test_dumps(self):
        obj = Base()
        obj.test = "bla"
        self.assertEqual(Json.dumps(obj), VALIDJSON)


class TestDecoder(unittest.TestCase):

    def test_loads(self):
        obj = Base()
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
        ooo = Base()
        ooo.a = "b"
        obj = Base()
        Object.update(obj, Json.loads(Json.dumps(ooo)))
        self.assertEqual(obj.a, "b")
