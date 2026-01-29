# This file is placed in the Public Domain.


"write your own commands"


import inspect


from .brokers import getobj
from .message import Message
from .methods import parse


class Commands:

    cmds = {}
    names = {}


def addcmd(*args):
    "add functions to commands."
    for func in args:
        name = func.__name__
        Commands.cmds[name] = func
        Commands.names[name] = func.__module__.split(".")[-1]


def getcmd(cmd):
    "get function for command."
    return Commands.cmds.get(cmd, None)
        

def hascmd(cmd):
    "whether cmd is registered."
    return cmd in Commands.cmds


def scancmd(module):
    "scan a module for functions with event as argument."
    for key, cmdz in inspect.getmembers(module, inspect.isfunction):
        if 'event' not in inspect.signature(cmdz).parameters:
            continue
        addcmd(cmdz)


"utility"


def command(evt):
    "command callback."
    parse(evt, evt.text)
    func = getcmd(evt.cmd)
    if func:
        func(evt)
        bot = getobj(evt.orig)
        if bot:
            bot.display(evt)
    evt.ready()


def docmd(text):
    "parse text for command and run it."
    for txt in text.split(" ! "):
        evt = Message()
        evt.text = txt
        evt.type = "command"
        command(evt)
        evt.wait()
    return evt


"interface"


def __dir__():
    return (
        'Config',
        'Commands',
        'addcmd',
        'command',
        'docmd',
        'getcmd',
        'scancmd'
    )
