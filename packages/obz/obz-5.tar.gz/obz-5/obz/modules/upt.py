# This file is placed in the Public Domain.
# pylint: disable=C,E0402


"uptime"


import time


from ..persist import laps


STARTTIME = time.time()


def upt(event):
    event.reply(laps(time.time()-STARTTIME))
