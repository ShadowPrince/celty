from celty.modules import api
import celty

import subprocess


@api.command()
def exit(c):
    raise celty.ExitError("good bye!")


@api.command()
def widgets(c):
    data = {}
    for name, out in celty.widgets(c):
        data[name] = out

    return data


@api.widget(timeout=10)
def celty_status(c):
    return ["celty 0.1" "i'm okay!", ]


@api.widget(timeout=30)
def fortune(c):
    return [subprocess.check_output("fortune").decode("utf-8").strip(), ]
