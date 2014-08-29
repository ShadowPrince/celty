import celty
from celty import shell

from log import e, i


def register(module_name):
    i("loading module {}", module_name)
    from modules import dtc as m
    setup(m)


def setup(module):
    i("set-upping module {}", module.__name__)
    for k, v in  {
        "name": lambda x: x.__name__.split(".")[-1],
    }.items():
        try:
            getattr(module, k)
        except AttributeError:
            setattr(module, k, v(module))


if __name__ == "__main__":
    print("celty 0.1")

    i("-----------------")
    register("dtc")
    i("-----------------")

    shell.init()
    shell.loop()
