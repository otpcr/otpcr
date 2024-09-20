# This file is placed in the Public Domain.
# pylint: disable=W0719


"debug"


from ..client import Commands


def dbg(event):
    "raise exception"
    raise Exception("yo!")


Commands.add(dbg)
