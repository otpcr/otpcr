# This file is placed in the Public Domain.
# pylint: disable=C,W0105


"list of commands"


from ..command import Commands
from ..object import keys


"commands"


def cmd(event):
    event.reply(",".join(sorted(keys(Commands.cmds))))
