# This file is placed in the Public Domain.
# pylint: disable=C


"service"


from .main    import forever, privileges, scanner, wrap
from .modules import face
from .persist import NAME, pidfile, pidname


scan = scanner


def wrapped():
    wrap(main)


def main():
    privileges()
    pidfile(pidname(NAME))
    scan(face, init=True)
    forever()


if __name__ == "__main__":
    wrapped()
