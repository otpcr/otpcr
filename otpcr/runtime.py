# This file is put into the Public Domain.


"place your runtime code here"


from .objects import Default


class Config(Default):

    pass


Cfg = Config()


"interface"


def __dir__():
    return (
        'Cfg',
    )
