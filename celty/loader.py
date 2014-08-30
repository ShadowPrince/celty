import celty
from celty import server as ui

from log import e, i


if __name__ == "__main__":
    print("celty 0.1")

    print("--------------------modules-loading-log:----------------")
    celty.register_module("celty")
    celty.register_module("dtc")
    celty.register_module("shell")
    celty.register_module("systemd")
    print("--------------------------------------------------------")

    env = ui.init()

    while True:
        ui.loop(env)
