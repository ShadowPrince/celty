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

        if isinstance(main_menu, bool) and main_menu == True:
            _main_menu = _name
        else:
            _main_menu = main_menu

        celty.register_command(_name, x, namespace=_ns, main_menu=_main_menu)
        return x

    return cb


def widget(name=None, ns=None, timeout=3):
    def cb(x):
        if not name:
            _name = x.__name__
        else:
            _name = name

        if not ns:
            _ns = x.__module__.split(".")[-1]
        else:
            _ns = ns

        celty.register_widget(x, name=_name, namespace=_ns, timeout=timeout)

        return x

    return cb
