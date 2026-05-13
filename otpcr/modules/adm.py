# This file is placed in the Public Domain.


"administrator"


import inspect
import os


from otpcr.defines import Commands, Json, Main, Mods, Utils, Workdir, d, j


dumps = Json.dumps


def srv(event):
    "generate systemd service file."
    import getpass
    name = getpass.getuser()
    event.reply(SYSTEMD % (
                           Main.name.upper(),
                           name,
                           name,
                           name,
                           Main.name
                          ))


def tbl(event):
    "create table."
    core = {}
    md5s = {}
    for name, module in Mods.all():
        md5s[name] = Utils.md5(module.__file__)
        Commands.scan(module)
    corepath = d(inspect.getsourcefile(Commands))
    for path in os.listdir(corepath):
        if path.startswith("__") or not path.endswith(".py") or "statics" in path:
            continue
        name = path[:-3]
        core[name] = Utils.md5(j(corepath, path))
    event.reply("# This file is placed in the Public Domain.")
    event.reply("\n")
    event.reply('"tables"')
    event.reply("\n")
    event.reply(f"NAMES = {dumps(Commands.names, indent=4, sort_keys=True)}")
    event.reply("\n")
    event.reply(f"CORE = {dumps(core, indent=4, sort_keys=True)}")
    event.reply("\n")
    event.reply(f"MD5 = {dumps(md5s, indent=4, sort_keys=True)}")


def wdr(event):
    "show working directory."
    event.reply(Workdir.workdir())


SYSTEMD = """[Unit]
Description=%s
After=multi-user.target

[Service]
Type=simple
User=%s
Group=%s
ExecStart=/home/%s/.local/bin/%s -s

[Install]
WantedBy=multi-user.target"""
