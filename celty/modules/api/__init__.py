from functools import wraps
import celty


def command(name=None, ns=None, main_menu=False):
    def cb(x):
        if not name:
            _name = x.__name__
        else:
            _name = name

        if not ns:
            _ns = x.__module__.split(".")[-1]
        else:
            _ns = ns

        celty.register_command(_name, x, namespace=_ns, main_menu=main_menu)
        return x

    return cb


def widget(*args, **kwargs):
    def cb(x):
        celty.register_widget(x, *args, **kwargs)

        return x

    return cb


def ui(_name=None, ns=None, main_menu=False):
    def decorator(fn):
        @command(_name, ns, main_menu)
        @wraps(fn)
        def wrapper(*args, **kwargs):
            return {"type": "ui",
                    "data": fn(*args, **kwargs)}

        return wrapper
    return decorator
