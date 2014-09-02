from log import e, i
import time


_commands = {}
_keywords = {}
_widgets = {}
_modules = {}
_connections = []


class ExitError(Exception):
    pass


class CommandNotRegisteredError(Exception):
    def __init__(self, name):
        super(Exception, self).__init__("Command \"{}\" not registered!".format(name))


class CommandWrongUsageError(Exception):
    pass


class Client:
    def __init__(self, protocol):
        self.widgets = dict([(n, {"last_time": 0}) for n in (x["name"] for x in _widgets.values())])
        self.subscriptions = {}
        self.proto = protocol

    def subscribe(self, cmd, *args, **kwargs):
        self.subscriptions[cmd] = (args, kwargs, )

    def unsubscribe(self, cmd):
        del self.subscriptions[cmd]


def register_command(name, fn, namespace=None):
    _commands["{}{}".format(namespace+":" if namespace else "", name)] = fn


def register_widget(fn, name=None, timeout=1000, *args):
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


def updated_widgets(c):
    for fn, opts in _widgets.items():
        try:
            copts = c.widgets[opts["name"]]
        except KeyError:
            continue

        if copts["last_time"] + opts["timeout"] < time.time():
            c.widgets[opts["name"]]["last_time"] = time.time()
            yield opts["name"], fn(c)


def call(cl, name, *args, **kwargs):
    try:
        return _commands[name](cl, *args, **kwargs)
    except TypeError as ex:
        raise CommandWrongUsageError(str(ex))
    except KeyError:
        raise CommandNotRegisteredError(name)


def process_subscriptions():
    for c in _connections:
        for sub, (args, kwargs) in c.subscriptions.items():
            c.proto.send_subscription(call(c, sub, *args, **kwargs))


def auth(protocol, token):
    if token == "1":
        cl = Client(protocol)
        for m in _modules.values():
            if hasattr(m, "auth"):
                m.auth(cl)

        return cl
    else:
        return None


def subscribe(c, *args, **kwargs):
    c.subscribe(*args, **kwargs)


def unsubscribe(c, cmd):
    c.unsubscribe(cmd)


def connection_made(protocol):
    _connections.append(protocol.client)


def connection_lost(protocol):
    _connections.remove(protocol.client)


def get_connected():
    return _connections
