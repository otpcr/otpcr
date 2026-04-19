# This file is placed in the Public Domain.


"configuration"


from otpcr.objects import Base, Methods, Object
from otpcr.package import Mods
from otpcr.persist import Cfg


def cfg(event):
    if not event.args:
        mods = f"{Mods.has('Config') + ',main'}"
        if mods.startswith(","):
            mods = mods[1:]
        event.reply(f"cfg <{mods}>")
        return
    name = event.args[0]
    config = Base()
    Cfg.load(config, name)
    if name != "main" and not config:
        mod = Mods.get(name)
        if not mod:
            event.reply(f"no {name} module found.")
            return
        config = getattr(mod, "Config", None)
        if not config:
            event.reply("no configuration found.")
            return
    if not event.sets:
        event.reply(
            Methods.fmt(
                config,
                Object.keys(config),
                skip=["word",]
            )
        )
        return
    Methods.edit(config, event.sets)
    Cfg.save(config, name)
    mod = Mods.get(name)
    if mod and "configure" in dir(mod):
        mod.configure()
    event.ok()


cfg.skip = "irc"
