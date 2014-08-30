import celty

from celty.log import i, e


def init():
    print("mode: shell")


def loop():
    try:
        x = input("[ ")
        out = celty.call(x.strip())
        print(out)
    except celty.CommandNotRegisteredError:
        print("! sorry, no such command")
    except (EOFError, KeyboardInterrupt):
        raise celty.ExitError("\ngood bye!")
