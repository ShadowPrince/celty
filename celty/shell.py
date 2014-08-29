import celty

from celty.log import i, e


def init():
    print("mode: shell")


def loop():
    while True:
        try:
            x = input("[ ")
            out = celty.call(x.strip())
            print(out)
        except celty.CommandNotRegisteredError:
            print("! sorry, no such command")
        except (EOFError, KeyboardInterrupt):
            print("\ngood bye!")
            break
