# This file is placed in the Public Domain.


"broker tests"


import types
import unittest


from otpcr.brokers import Broker
from otpcr.encoder import Json
from otpcr.handler import Client
from otpcr.objects import Base, Object


class TestBroker(unittest.TestCase):

    def test_ismethod(self):
        self.assertEqual(type(Broker.add), types.MethodType)

    def test_asinstance(self):
        broker = Broker()
        self.assertTrue(isinstance(broker, Broker))

    def test_functioninginstance(self):
        broker = Broker()
        obj = Base()
        broker.add(obj)
        self.assertTrue(Broker.has(obj))

    def test_add(self):
        clt = Client()
        self.assertTrue(Broker.has(clt))

    def test_addobj(self):
        obj = Base()
        Broker.add(obj)
        self.assertTrue(Broker.has(obj))

    def test_getobj(self):
        obj = Base()
        Broker.add(obj)
        oobj = Broker.get(repr(obj))
        self.assertTrue(oobj is obj)

    def test_objs(self):
        clt = Client()
        objs = Broker.objs("announce")
        self.assertTrue(clt in objs)

    def test_has(self):
        obj = Base()
        Broker.add(obj)
        self.assertTrue(Broker.has(obj))

    def test_like(self):
        obj = Base()
        Broker.add(obj)
        self.assertTrue(Broker.like(repr(obj)))

    def test_json(self):
        Broker.a = "b"
        s = Json.dumps(Broker)
        o = Json.loads(s)
        self.assertEqual(o["a"], "b")

    def test_update(self):
        o = {}
        o["a"] = "b"
        Object.update(Broker, o)
        self.assertEqual(Broker.a, "b")
