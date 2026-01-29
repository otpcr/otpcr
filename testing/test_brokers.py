# This file is placed in the Public Domain.


import unittest


from otpcr.brokers import *
from otpcr.encoder import dumps, loads
from otpcr.handler import Client
from otpcr.objects import Object, update, values


class TestBroker(unittest.TestCase):

    def test_add(self):
        clt = Client()
        self.assertTrue(hasobj(clt))

    def test_addobj(self):
        obj = Object()
        addobj(obj)
        self.assertTrue(hasobj(obj))
    
    def test_getobj(self):
        obj = Object()
        addobj(obj)
        oobj = getobj(repr(obj))
        self.assertTrue(oobj is obj)

    def getobjs(self):
        clt = Client()
        objs = getobjs("announce")
        self.assertTrue(clt in objs)

    def hasobj(self):
        obj = Object()
        addobj(obj)
        self.assertTrue(hasobj(obj))

    def likeobj(self):
        obj = Object()
        addobj(obj)
        self.assertTrue(likeobj(repr(obj)))

    def test_json(self):
        Broker.a = "b"
        s = dumps(Broker)
        o = loads(s)
        self.assertEqual(o["a"], "b")
        
    def test_update(self):
        o = {}
        o["a"] = "b"
        update(Broker, o)
        self.assertEqual(Broker.a, "b")
