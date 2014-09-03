from helmet import elements
import helmet

from celty.modules import api
import celty


@api.command()
def subscribe(c, s, *args, **kwargs):
    try:
        celty.subscribe(c, *args, **kwargs)
        return {"type": "subscribe",
                "result": "success", }
    except celty.CommandNotRegisteredError:
        return {"type": "subscribe",
                "result": "error",
                "error": "command not registered!"}


@api.command()
def unsubscribe(c, s, command):
    celty.unsubscribe(c, command)
    return {"type": "unsubscribe",
            "result": "success", }


@api.command()
def widgets(c, s):
    data = {"type": "widgets", "data": {}}
    for name, out in celty.updated_widgets(c):
        data["data"][name] = out

    return data


@api.ui()
@helmet.pack()
def main(c, s):
    menu = [[elements.button(*x)] for x in celty._main_menu]
    return [[elements.label(*["celty main menu", "pick something:"]), ], ] + menu


@api.widget(timeout=1)
def celty_status(c, s):
    return ["celty {}, clients: {}".format("0.1", len(celty.get_connected())),
            "commands: {}, widgets: {}".format(len(celty._commands), len(celty._widgets)), ]
