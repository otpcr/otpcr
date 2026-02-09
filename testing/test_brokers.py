# This file is placed in the Public Domain.


import unittest


from otpcr.brokers import Broker
from otpcr.clients import Client
from otpcr.decoder import Json
from otpcr.objects import Dict, Object


class TestBroker(unittest.TestCase):

    def test_add(self):
        clt = Client()
        self.assertTrue(Broker.has(clt))

    def test_addobj(self):
        obj = Object()
        Broker.add(obj)
        self.assertTrue(Broker.has(obj))
    
    def test_getobj(self):
        obj = Object()
        Broker.add(obj)
        oobj = Broker.get(repr(obj))
        self.assertTrue(oobj is obj)

    def test_objs(self):
        clt = Client()
        objs = Broker.objs("announce")
        self.assertTrue(clt in objs)

    def test_has(self):
        obj = Object()
        Broker.add(obj)
        self.assertTrue(Broker.has(obj))

    def test_like(self):
        obj = Object()
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
        Dict.update(Broker, o)
        self.assertEqual(Broker.a, "b")
