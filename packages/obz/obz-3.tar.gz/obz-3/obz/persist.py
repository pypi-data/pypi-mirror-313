# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,R0903,W0105,W0719,E1101,E0402


"persistence"


import datetime
import json
import os
import pathlib
import time
import uuid
import _thread


from obx import Object, dump, load, search, update


cachelock = _thread.allocate_lock()
disklock  = _thread.allocate_lock()
findlock  = _thread.allocate_lock()
lock      = _thread.allocate_lock()
p         = os.path.join


class Obj(Object):

    def __getattr__(self, key):
        return self.__dict__.get(key, "")


class Config(Obj):

    fqns = []
    name = "obz"
    wdr  = os.path.expanduser("~/.{Config.name}")


def long(name):
    split = name.split(".")[-1].lower()
    res = name
    for names in types():
        if split == names.split(".")[-1].lower():
            res = names
            break
    return res


def modname():
    return p(Config.wdr, "mods")


def pidname(name):
    return p(Config.wdr, f"{name}.pid")


def store(pth=""):
    stor = p(Config.wdr, "store", "")
    if not os.path.exists(stor):
        skel()
    return p(Config.wdr, "store", pth)


class Cache:

    objs = {}

    @staticmethod
    def add(path, obj):
        with cachelock:
            Cache.objs[path] = obj

    @staticmethod
    def get(path):
        with cachelock:
            return Cache.objs.get(path)

    @staticmethod
    def typed(match):
        with cachelock:
            for key in Cache.objs:
                if match not in key:
                    continue
                yield Cache.objs.get(key)


"utilities"


def cdir(pth):
    path = pathlib.Path(pth)
    path.parent.mkdir(parents=True, exist_ok=True)


def find(mtc, selector=None, index=None, deleted=False, matching=False):
    clz = long(mtc)
    nrs = -1
    with findlock:
        for fnm in sorted(fns(clz), key=fntime):
            obj = Cache.get(fnm)
            if obj:
                yield (fnm, obj)
                continue
            obj = Object()
            read(obj, fnm)
            if not deleted and '__deleted__' in dir(obj) and obj.__deleted__:
                continue
            if selector and not search(obj, selector, matching):
                continue
            nrs += 1
            if index is not None and nrs != int(index):
                continue
            Cache.add(fnm, obj)
            yield (fnm, obj)


def fns(mtc=""):
    dname = ''
    with disklock:
        pth = store(mtc)
        for rootdir, dirs, _files in os.walk(pth, topdown=False):
            if dirs:
                for dname in sorted(dirs):
                    if dname.count('-') == 2:
                        ddd = p(rootdir, dname)
                        for fll in os.scandir(ddd):
                            yield strip(p(ddd, fll))


def fntime(daystr):
    daystr = daystr.replace('_', ':')
    datestr = ' '.join(daystr.split(os.sep)[-2:])
    if '.' in datestr:
        datestr, rest = datestr.rsplit('.', 1)
    else:
        rest = ''
    timed = time.mktime(time.strptime(datestr, '%Y-%m-%d %H:%M:%S'))
    if rest:
        timed += float('.' + rest)
    return timed


def laps(seconds, short=True):
    txt = ""
    nsec = float(seconds)
    if nsec < 1:
        return f"{nsec:.2f}s"
    yea = 365*24*60*60
    week = 7*24*60*60
    nday = 24*60*60
    hour = 60*60
    minute = 60
    yeas = int(nsec/yea)
    nsec -= yeas*yea
    weeks = int(nsec/week)
    nsec -= weeks*week
    nrdays = int(nsec/nday)
    nsec -= nrdays*nday
    hours = int(nsec/hour)
    nsec -= hours*hour
    minutes = int(nsec/minute)
    nsec -= int(minute*minutes)
    sec = int(nsec)
    if yeas:
        txt += f"{yeas}y"
    if weeks:
        nrdays += weeks * 7
    if nrdays:
        txt += f"{nrdays}d"
    if short and txt:
        return txt.strip()
    if hours:
        txt += f"{hours}h"
    if minutes:
        txt += f"{minutes}m"
    if sec:
        txt += f"{sec}s"
    txt = txt.strip()
    return txt


def pidfile(filename):
    if os.path.exists(filename):
        os.unlink(filename)
    path2 = pathlib.Path(filename)
    path2.parent.mkdir(parents=True, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as fds:
        fds.write(str(os.getpid()))


def skel():
    stor = p(Config.wdr, "store", "")
    path = pathlib.Path(stor)
    path.mkdir(parents=True, exist_ok=True)
    return path


def shortid():
    return str(uuid.uuid4())[:8]


def spl(txt):
    try:
        result = txt.split(',')
    except (TypeError, ValueError):
        result = txt
    return [x for x in result if x]


def strip(pth, nmr=3):
    return os.sep.join(pth.split(os.sep)[-nmr:])


def types():
    return os.listdir(store())


"methods"


def read(obj, pth):
    with disklock:
        pth2 = store(pth)
        fetch(obj, pth2)
        return os.sep.join(pth.split(os.sep)[-3:])


def fqn(obj):
    kin = str(type(obj)).split()[-1][1:-2]
    if kin == "type":
        kin = f"{obj.__module__}.{obj.__name__}"
    return kin


def ident(obj):
    return p(fqn(obj), *str(datetime.datetime.now()).split())


def last(obj, selector=None):
    if selector is None:
        selector = {}
    result = sorted(
                    find(fqn(obj), selector),
                    key=lambda x: fntime(x[0])
                   )
    res = None
    if result:
        inp = result[-1]
        update(obj, inp[-1])
        res = inp[0]
    return res


def fetch(obj, pth):
    with lock:
        with open(pth, 'r', encoding='utf-8') as ofile:
            try:
                update(obj, load(ofile))
            except json.decoder.JSONDecodeError as ex:
                raise Exception(pth) from ex


def write(obj, pth=None):
    if pth is None:
        pth = ident(obj)
    with disklock:
        pth2 = store(pth)
        sync(obj, pth2)
        return pth


def sync(obj, pth):
    with lock:
        cdir(pth)
        with open(pth, 'w', encoding='utf-8') as ofile:
            dump(obj, ofile, indent=4)


"interface"


def __dir__():
    return (
        'Config',
        'Obj',
        'find',
        'fetch',
        'last',
        'read',
        'sync',
        'write'
    )
