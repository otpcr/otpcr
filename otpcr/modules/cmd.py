# This file is placed in the Public Domain.


"availalbe commands."


from ..command import Commands
from ..object    import keys


def cmd(event):
    "list commands."
    event.reply(",".join(sorted(keys(Commands.cmds))))
