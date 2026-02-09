# This file is placed in the Public Domain.


import gc as garbage
import sys


def gc(event):
    garbage.collect(0)
    garbage.collect(1)
    garbage.collect(2)
    event.reply(str(garbage.get_count()))


def obj(event):
    for obj in garbage.get_objects():
        if 'copyright' in str(obj).lower():
            continue
        if 'all rights' in str(obj).lower():
            continue
        if event.rest and event.rest not in str(obj):
            continue
        event.reply(f'{type(obj)} {sys.getrefcount(obj)} {[str(type(x)) for x in garbage.get_referents(obj)]}')
