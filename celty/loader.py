import celty
from celty import server

from log import e, i

import os


if __name__ == "__main__":
    print("celty 0.1")

    print("--------------------modules-loading-log:----------------")
    base = os.path.join(os.path.dirname(__file__), "modules")
    for dir in filter(lambda x: not x.startswith("__"), os.listdir(base)):
        if os.path.isdir(os.path.join(base, dir)):
            celty.register_module(dir)
    print("--------------------------------------------------------")

    server.init()
    server.run()
