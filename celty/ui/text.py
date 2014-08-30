import celty
import readline

from celty.log import i, e


def _strip(text):
    return text.strip()
    

def init():
    print("mode: text")


def loop():
    try:
        fn, args = celty.findout(_strip(input("{ ")))
        print(fn(*args))
    except celty.NotObviousFindoutError:
        print("! sorry, not obvious")
    except celty.FindoutFailedError:
        print("! sorry, I dunno anything 'bout this")
    except celty.FindoutEmptyQueryError:
        pass
    except (EOFError, KeyboardInterrupt):
        raise celty.ExitError("\ngood bye!")
