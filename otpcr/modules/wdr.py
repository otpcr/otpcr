# This file is placed in the Public Domain.


"working directory"


from otpcr.persist import workdir


def wdr(event):
    event.reply(workdir())
