from helmet import elements
import helmet

from celty.modules import api
import celty

import subprocess


@api.command()
def subscribe(*args, **kwargs):
    try:
        celty.subscribe(*args, **kwargs)
        return {"type": "subscribe",
                "result": "success", }
    except celty.CommandNotRegisteredError:
        return {"type": "subscribe",
                "result": "error",
                "error": "command not registered!"}


@api.command()
def unsubscribe(c, command):
    celty.unsubscribe(c, command)
    return {"type": "unsubscribe",
            "result": "success", }


@api.command()
def widgets(c):
    data = {"type": "widgets", "data": {}}
    for name, out in celty.updated_widgets(c):
        data["data"][name] = out

    return data


@api.command()
@api.ui()
@helmet.pack()
def main(c):
    return ([elements.label("celty main menu"), ],
            [elements.button("fortune", "fortune_cookie"), ],
            [elements.button("sh", "sh_main"), ],)


@api.command()
@api.ui()
@helmet.pack()
def fortune_cookie(c):
    return ([elements.label(subprocess.check_output("fortune").decode("utf-8").strip())], 
            [elements.button("get another", "fortune_cookie"), elements.button("main menu", "main")], )


@api.widget(timeout=1)
def celty_status(c):
    return ["celty 0.1", "i'm okay!", "connected: {}".format(len(celty.get_connected()))]


@api.widget(timeout=30)
def fortune(c):
    return [subprocess.check_output("fortune").decode("utf-8").strip(), ]
