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


def auth(c, s):
    s.history = []


@api.ui(main_menu="shell")
@helmet.pack()
def main(c, s, sh=None):
    if sh:
        out = execute(*sh.split())
    else:
        out = ""

    s.history.append("$ " + str(sh))
    s.history += out.splitlines()
    out = s.history[-50:]

    return ([els.label(*out)],
            [els.input("sh"), els.button("exec", "shell:main", ("sh", )), ])
