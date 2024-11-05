# This file is placed in the Public Domain.
# pylint: disable=C


"list of commands"


from ..command import Commands
from ..object  import keys


def cmd(event):
    event.reply(",".join(sorted(keys(Commands.cmds))))
