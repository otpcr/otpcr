# This file is placed in the Public Domain.


"silence"


from otpcr.brokers import Broker


def sil(event):
    bot = Broker.get(event.orig)
    if not bot:
        event.reply("no bot in fleet.")
        return
    bot.silent = True
    event.reply("ok")


def lou(event):
    bot = Broker.get(event.orig)
    if not bot:
        event.reply("no bot in fleet.")
        return
    bot.silent = False
    event.reply("ok")
