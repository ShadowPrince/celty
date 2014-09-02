from helmet import elements
import helmet

from celty.modules import api
import celty


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


@api.ui()
@helmet.pack()
def main(c):
    return ([elements.label(*["celty main menu", "pick something:"]), ],
            [elements.button("system config", "system:configure"), ],
            [elements.button("sh", "shell:main"), ],)


@api.widget(timeout=1)
def celty_status(c):
    return ["celty 0.1", "i'm okay!", "connected: {}".format(len(celty.get_connected()))]
