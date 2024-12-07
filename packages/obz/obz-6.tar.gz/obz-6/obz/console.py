# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,C0415,R0903,R0912,R0915,W0105,W0718,E0402


"main"


import sys
import termios
import time

from .persist import Config
from .runtime import Client, Commands, Event
from .runtime import command, errors, forever, later, parse, scan, wrap


cfg = Config()


class Console(Client):

    def announce(self, txt):
        self.raw(txt)

    def callback(self, evt):
        Client.callback(self, evt)
        evt.wait()

    def poll(self):
        evt = Event()
        evt.txt = input("> ")
        evt.type = "command"
        return evt

    def raw(self, txt):
        print(txt)
        sys.stdout.flush()


def banner():
    tme = time.ctime(time.time()).replace("  ", " ")
    print(f"{cfg.name.upper()} since {tme}")


def wrap(func):
    old = None
    try:
        old = termios.tcgetattr(sys.stdin.fileno())
    except termios.error:
        pass
    try:
        func()
    except (KeyboardInterrupt, EOFError):
        print("")
    except Exception as ex:
        later(ex)
    finally:
        if old:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old)


def wrapped():
    wrap(main)
    for line in errors():
        print(line)


def main():
    parse(cfg, " ".join(sys.argv[1:]))
    if "v" in cfg.opts:
        banner()
    from .modules import face
    for mod, thr in scan(face, init="i" in cfg.opts, disable=cfg.sets.dis):
        if "v" in cfg.opts and "output" in dir(mod):
            mod.output = print
        if thr and "w" in cfg.opts:
            thr.join()
    csl = Console()
    csl.start()
    forever()


if __name__ == "__main__":
    wrapped()
