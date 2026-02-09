# This file is placed in the Public Domain.


"show prodess stats"


def ps(event):
    try:
        import psutil
    except ModuleNotFoundError:
        event.reply("psutil is not installed.")
        return
    proc = psutil.Process()
    txt = ' '.join(str(proc.memory_info()).split('(')[1:])
    txt2 = ""
    for value in txt.split():
        name, nrs = value.split('=')
        txt2 += " " + f'{name.upper()}: {float(int(nrs[:-1])/1000000):.2f}M'
    event.reply(txt2.strip())
