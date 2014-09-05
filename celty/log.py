LEVEL = 0

ERROR = 1
INFO = 2


def _stringlevel(lvl):
    """
    Turn integer level into string one.

    lvl -- level
    Return string level.
    """
    return {1: "e",
            2: "i",}.get(lvl, lvl)


def log(level, msg, *args, **kwargs):
    """
    Log message. Message formatted with *args and **kwargs

    level -- level (one of UPPER CONSTANT ones in this module)
    msg -- message
    """
    if level >= LEVEL:
        print("[{}] {}".format(_stringlevel(level), msg.format(*args, **kwargs)))


def i(*args, **kwargs):
    """
    Log INFO-level message.
    """
    log(INFO, *args, **kwargs)


def e(*args, **kwargs):
    """
    Log ERROR-level message.
    """
    log(ERROR, *args, **kwargs)
