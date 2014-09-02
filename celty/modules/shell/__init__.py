import helmet
from helmet import elements as els
from celty.modules import api

import subprocess


def execute(*args):
    try:
        return subprocess.check_output(args).decode("utf-8")
    except IndexError:
        raise TypeError("required argument")
    except Exception, e:
        return str(e)


def auth(c):
    c.history = []


@api.command()
@api.ui()
@helmet.pack()
def main(c, sh=None):
    if sh:
        out = execute(*sh.split())
    else:
        out = ""

    c.history.append("$ " + str(sh))
    c.history += out.splitlines()
    out = c.history[-50:]

    return ([els.label(*out)],
            [els.input("sh"), els.button("exec", "shell:main", ("sh", )), ])
