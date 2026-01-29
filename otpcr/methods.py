# This file is placed in the Public Domain.


"an object as the first argument"


from .objects import Default, items


def edit(obj, setter={}, skip=False):
    "update object with dict."
    for key, val in items(setter):
        if skip and val == "":
            continue
        typed(obj, key, val)


def fmt(obj, args=[], skip=[], plain=False, empty=False):
    "format object info printable string."
    if args == []:
        args = list(obj.__dict__.keys())
    txt = ""
    for key in args:
        if key.startswith("__"):
            continue
        if key in skip:
            continue
        value = getattr(obj, key, None)
        if value is None:
            continue
        if not empty and not value:
            continue
        if plain:
            txt += f"{value} "
        elif isinstance(value, (int, float, dict, bool, list)):
            txt += f"{key}={value} "
        elif isinstance(value, str):
            txt += f'{key}="{value}" '
        else:
            txt += f"{key}={fqn(value)}((value))"
    if txt == "":
        txt = "{}"
    return txt.strip()


def fqn(obj):
    "full qualified name."
    kin = str(type(obj)).split()[-1][1:-2]
    if kin == "type":
        kin = f"{obj.__module__}.{obj.__name__}"
    return kin


def parse(obj, text):
    "parse text for command."
    data = {
        "args": [],
        "cmd": "",
        "gets": Default(),
        "index": None,
        "init": "",
        "opts": "",
        "otxt": text,
        "rest": "",
        "silent": Default(),
        "sets": Default(),
        "text": text
    }
    for k, v in data.items():
        setattr(obj, k, getattr(obj, k, v) or v)
    args = []
    nr = -1
    for spli in text.split():
        if spli.startswith("-"):
            try:
                obj.index = int(spli[1:])
            except ValueError:
                obj.opts += spli[1:]
            continue
        if "-=" in spli:
            key, value = spli.split("-=", maxsplit=1)
            typed(obj.silent, key, value)
            typed(obj.gets, key, value)
            continue
        if "==" in spli:
            key, value = spli.split("==", maxsplit=1)
            typed(obj.gets, key, value)
            continue
        if "=" in spli:
            key, value = spli.split("=", maxsplit=1)
            typed(obj.sets, key, value)
            continue
        nr += 1
        if nr == 0:
            obj.cmd = spli
            continue
        args.append(spli)
    if args:
        obj.args = args
        obj.text  = obj.cmd or ""
        obj.rest = " ".join(obj.args)
        obj.text  = obj.cmd + " " + obj.rest
    else:
        obj.text = obj.cmd or ""


def skip(obj, chars="_"):
    "skip keys containing chars."
    res = {}
    for key, value in items(obj):
        next = False
        for char in chars:
            if char in key:
                next = True
        if next:
            continue
        res[key] = value
    return res


def typed(obj, key, val):
    "assign proper types."
    try:
        setattr(obj, key, int(val))
        return
    except ValueError:
        pass
    try:
        setattr(obj, key, float(val))
        return
    except ValueError:
        pass
    if val in ["True", "true", True]:
        setattr(obj, key, True)
    elif val in ["False", "false", False]:
        setattr(obj, key, False)
    else:
        setattr(obj, key, val)


"interface"


def __dir__():
    return (
        'edit',
        'fmt',
        'fqn',
        'parse',
        'skip',
        'typed'
    )
