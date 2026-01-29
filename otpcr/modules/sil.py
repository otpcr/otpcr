# This file is placed in the Public Domain.


from otpcr.brokers import getobj


def sil(event):
    bot = getobj(event.orig)
    bot.silent = True
    event.reply("ok")


def lou(event):
    bot = getobj(event.orig)
    bot.silent = False
    event.reply("ok")
