from log import e, i
import time


_commands = {}
_keywords = {}
_widgets = {}
_modules = {}


class ExitError(Exception):
    pass


class CommandNotRegisteredError(Exception):
    def __init__(self, name):
        super(Exception, self).__init__("Command \"{}\" not registered!".format(name))


class CommandWrongUsageError(Exception):
    pass


class Client:
    def __init__(self):
        pass


def register_command(name, fn, namespace=None):
    _commands["{}{}".format(namespace+":" if namespace else "", name)] = fn


def register_widget(fn, *args, name=None, timeout=1000):
    _widgets[fn] = {
        "name": fn.__name__ if not name else name,
        "priority": args[0] if len(args) > 0 else 0,
        "timeout": timeout,
        "last_time": 0,
    }


def register_module(module_name):
    wgts, cmds = len(_widgets), len(_commands)
    m = __import__("modules." + module_name)

    setup_module(getattr(m, module_name))

    wgts, cmds = len(_widgets) - wgts, len(_commands) - cmds
    i("{}: loaded {} commands and {} widgets", module_name, cmds, wgts)


def setup_module(module):
    for k, v in {
        "name": lambda x: x.__name__.split(".")[-1],
    }.items():
        try:
            getattr(module, k)
        except AttributeError:
            setattr(module, k, v(module))

    _modules[module.name] = module


def widgets(c):
    for fn, opts in _widgets.items():
        if opts["last_time"] + opts["timeout"] < time.time():
            _widgets[fn]["last_time"] = time.time()
            yield opts["name"], fn(c)


def call(cl, name, *args, **kwargs):
    try:
        return _commands[name](cl, *args, **kwargs)
    except TypeError as ex:
        raise CommandWrongUsageError(str(ex))
    except KeyError:
        raise CommandNotRegisteredError(name)


def auth(token):
    if token == "1":
        cl = Client()
        for m in _modules.values():
            if hasattr(m, "auth"):
                m.auth(cl)

        return cl
    else:
        return None
