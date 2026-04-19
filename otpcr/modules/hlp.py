# This file is placed in the Public Domain.


"help"


from otpcr.configs import Main


def hlp(event):
    event.reply(HELP % (Main.name, Main.name))


hlp.skip = "irc"


HELP = """%s [-c|d|h|s] [-a] [-b] [-n] [-r] [-u] [-v] [-w] [key=value] [key==value]

options:

-h       show this help message and exit
-a       load all modules
-b       read config on boot
-c       start console
-d       start background daemon
-n       disable ignore
-r       read modules on start
-s       start service
-u       use local mods directory
-v       enable verbose
-w       wait for services to start

keys:

default,ignore,init,level,mods,name,version,wdr

example:

%s -cvw level=debug mods=irc,rss"""
