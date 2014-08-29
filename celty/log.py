LEVEL = 0

ERROR = 1
INFO = 2


def _stringlevel(lvl):
    return {1: "ERROR",
            2: "INFO",}.get(lvl, lvl)


def log(level, msg, *args, **kwargs):
    if level >= LEVEL:
        print("[{}] {}".format(_stringlevel(level), msg.format(*args, **kwargs)))


def i(*args, **kwargs):
    log(INFO, *args, **kwargs)


def e(*args, **kwargs):
    log(ERROR, *args, **kwargs)
