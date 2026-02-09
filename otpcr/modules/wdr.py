# This file is placed in the Public Domain.


"working directory"


from otpcr.persist import Workdir


def wdr(event):
    event.reply(Workdir.workdir())
