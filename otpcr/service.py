# This file is placed in the Public Domain.
# pylint: disable=C,W0105


"service"


from .command import NAME, forever, privileges, scanner, wrap
from .modules import face
from .persist import pidfile, pidname
from .runtime import errors


def wrapped():
    wrap(main)
    for text in errors():
        print(text)


def main():
    privileges()
    pidfile(pidname(NAME))
    scanner(face, init=True)
    forever()


if __name__ == "__main__":
    wrap(main)
    for txt in errors():
        print(txt)
