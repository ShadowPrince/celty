import helmet
from helmet import elements as els
from celty.modules import api

import subprocess


def sh(*args):
    try:
        return subprocess.check_output(args).decode("utf-8")
    except IndexError:
        raise TypeError("required argument")
    except Exception, e:
        return str(e)


@api.command()
@api.ui()
@helmet.pack()
def sh_main(c, line=None):
    if line:
        out = sh(*line.split())
    else:
        out = ""

    return ([els.label(out)],
            [els.input("sh"), els.button("exec", "sh_main", ("sh", )), els.button("back", "main") ])
