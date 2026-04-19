# This file is placed in the Public Domain.


"""**NAME**

| ``%s`` - %s
|


**SYNOPSIS**

| ``%s [-h] [-a] [-c] [-d] [-l LEVEL] [-m MODS] [-n] [-s] [-t] [-v] [-w] [-u] [-x][--wdr WDR]``
|
| ``%s <cmd> [key=val] [key==val]``
| ``%s -cvaw [mods=mod1,mod2]``
|

**DESCRIPTION**

``%s`` has all you need to program a unix cli program, such as disk
perisistence for configuration files, event handler to handle the
client/server connection, deferred exception handling to not crash
on an error, etc.

``%s`` contains python3 code to program objects in a functional way.
it provides an "clean namespace" Object class that only has dunder
methods, so the namespace is not cluttered with method names. This
makes storing and reading to/from json possible.

``%s`` is a python3 IRC bot, it can connect to IRC, fetch and
display RSS feeds, take todo notes, keep a shopping list and log
text. You can run it under systemd for 24/7 presence in a IRC channel.

``%s`` is Public Domain.


**INSTALL**


installation is done with pipx

| ``$ pipx install %s``
| ``$ pipx ensurepath``
|
| <new terminal>
|
| ``$ %s srv > %s.service``
| ``$ sudo mv %s.service /etc/systemd/system/``
| ``$ sudo systemctl enable %s --now``
|
| joins ``#%s`` on localhost
|


**USAGE**


use ``%s`` to control the program, default it does nothing

| ``$ %s``
| ``$``
|

the -h option will show you possible options

| ``$ %s -h``
|
| options:
|
| ``-h,--help          show this help message and exit``
| ``-a,--all           load all modules``
| ``-c,--console       start console``
| ``-d,--daemon        start background daemon``
| ``-l,--level LEVEL   set loglevel``
| ``-m,--mods MODS     modules to load``
| ``-n,--noignore      disable ignore``
| ``-r, --read         read modules on start``
| ``-s,--service       start service``
| ``-t,--threaded      enable multiple workers``
| ``-v,--verbose       enable verbose``
| ``-w,--wait          wait for services to start``
| ``-u,--user          use local mods directory``
| ``-x,--admin         use admin mode``
| ``--wdr <WDR>        set working directory``
|

see list of commands

| ``$ %s cmd``
| ``cfg,cmd,dne,dpl,err,exp,imp,log,mod,mre,nme,``
| ``pwd,rem,req,res,rss,srv,syn,tdo,thr,upt``
|

start console

| ``$ %s -c``
|

start console and run irc and rss clients

| ``$ %s -c init=irc,rss``
|

list available modules

| ``$ %s mod``
| ``err,flt,fnd,irc,llm,log,mbx,mdl,mod,req,rss,``
| ``rst,slg,tdo,thr,tmr,udp,upt``
|

start daemon

| ``$ %s -d``
| ``$``
|

start service

| ``$ %s -s``
| ``<runs until ctrl-c>``
|


**COMMANDS**


here is a list of available commands

| ``cfg`` - irc configuration
| ``cmd`` - commands
| ``dpl`` - sets display items
| ``err`` - show errors
| ``exp`` - export opml (stdout)
| ``imp`` - import opml
| ``log`` - log text
| ``mre`` - display cached output
| ``pwd`` - sasl nickserv name/pass
| ``rem`` - removes a rss feed
| ``res`` - restore deleted feeds
| ``req`` - reconsider
| ``rss`` - add a feed
| ``syn`` - sync rss feeds
| ``tdo`` - add todo item
| ``thr`` - show running threads
| ``upt`` - show uptime
|

**CONFIGURATION**


irc

| ``$ %s cfg irc server=<server>``
| ``$ %s cfg irc hannel=<channel>``
| ``$ %s cfg irc nick=<nick>``
|

sasl

| ``$ %s pwd <nsnick> <nspass>``
| ``$ %s cfg irc password=<frompwd>``
|

rss

| ``$ %s rss <url>``
| ``$ %s dpl <url> <item1,item2>``
| ``$ %s rem <url>``
| ``$ %s nme <url> <name>``
|

opml

| ``$ %s exp``
| ``$ %s imp <filename>``
|


**PROGRAMMING**

| %s has it's user modules in the ~/.%s/mods directory so for a
| hello world command you would  edit a file in ~/.%s/mods/hello.py
| and add the following
|

::

    def hello(event):
        event.reply("hello world !!")


|
| typing the hello command would result into a nice hello world !!
|

::

    $ %s hello
    hello world !!


|
| commands run in their own thread and the program borks on exit to enable a
| short debug cycle, output gets flushed on print so exceptions appear in the
| systemd logs. modules can contain your own written python3 code.
|


**FILES**

|
| ``~/.%s``
| ``~/.local/bin/%s``
| ``~/.local/share/pipx/venvs/%s/*``
|

**AUTHOR**

|
| ``%s`` <``%s``>
|

**COPYRIGHT**

|
| ``%s`` is Public Domain.
|
"""


def man(event):
    args = event.args
    try:
        name, email, author = args[0], args[1], " ".join(args[2:])
    except (ValueError, IndexError):
        event.reply("man <name> <email> <author>")
        return
    event.reply(__doc__ % (
        name,
        name.upper(),
        *(name,) * 3,
        *(name.upper(),) * 4,
        *(name,) * 33,
        author,
        email,
        name.upper()
    ))


man.skip = "irc"
