# This file is placed in the Public Domain.


"configuration"


from otpcr.defines import Base, Disk, Mods, Object


def cfg(event):
    "configure."
    if not event.args:
        mods = f"{'main,' + Mods.has('Config')}"
        if mods.endswith(","):
            mods = mods[:-1]
        event.reply(f"cfg <{mods}>")
        return
    name = event.args[0]
    config = Base()
    Disk.read(config, name, "config")
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
            Object.fmt(
                config,
                Object.keys(config),
                skip=["word",]
            )
        )
        return
    Object.edit(config, event.sets)
    Disk.write(config, name, "config")
    event.ok()
