# This file is placed in the Public Domain


"debug"


import time


from ..fleet import Fleet


def dbg(event):
    event.reply("raising exception")
    raise Exception("yo!")


def brk(event):
    event.reply("borking")
    for bot in Fleet.bots.values():
        if "sock" in dir(bot):
            event.reply("shutdown on {bot.cfg.server}")
            time.sleep(2.0)
            bot.sock.shutdown(2)
