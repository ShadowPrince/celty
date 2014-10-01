from functools import wraps
import celty


def command(name=None, ns=None, main_menu=False, inline=False):
    """
    Decorator to register the command to celty.
    If name is not presented - it'll be function's __name__.
    If ns is not presented - it'll be function's __module__.

    name -- name of command
    ns -- namespace
    main_menu -- if presented - register command to celty's main menu represented as this argument
    """
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

        celty.register_command(_name, x, namespace=_ns, main_menu=_main_menu, inline=inline)
        return x

    return cb


def widget(name=None, ns=None, timeout=3):
    """
    Decorator to register the widget to celty.
    If name is not presented - it'll be function's __name__.
    If ns is not presented - it'll be function's __module__.

    name -- name of command
    ns -- namespace
    timeout -- time in seconds in which widget will be refreshed
    """
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

def inline(*args, **kwargs):
    """
    Decorator to register inline command to celty. Wrapper around api.command decorator, used for one-time inline defined commands.
    If name is not presented - it'll be function's __name__.
    If ns is not presented - it'll be function's __module__.

    name -- name of command
    ns -- namespace
    main_menu -- if presented - register command to celty's main menu represented as this argument
    """
    return command(*args, inline=True, **kwargs)
