# This file is placed in the Public Domain.


"show path to otpcr docs"


import os


d = os.path.dirname


def pth(event):
    path = d(d(__file__))
    path = os.path.join(path, "network", "index.html")
    event.reply(f"file://{path}")
