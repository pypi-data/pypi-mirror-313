# This file is in the Public Domain.
# pylint: disable=C0116,C0415,E0402


"service"


from .persist import Config, pidfile, pidname
from .runtime import errors, forever, privileges, scan, wrap


def service():
    privileges()
    pidfile(pidname(Config.name))
    from .modules import face as mods
    scan(mods, init=True)
    forever()


def wrapped():
    wrap(service)
    for line in errors():
        print(line)


if __name__ == "__main__":
    wrapped()
