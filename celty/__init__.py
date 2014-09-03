from celty.log import e, i
import time


_commands = {}
_main_menu = []
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


class ClientStorage:
    pass


class Client:
    def __init__(self, protocol):
        self.widgets = dict([(n, {"last_time": 0}) for n in (x["name"] for x in _widgets.values())])
        self.subscriptions = {}
        self.proto = protocol
        self.storages = {}

    def subscribe(self, cmd, *args, **kwargs):
        self.subscriptions[cmd] = (args, kwargs, )

    def unsubscribe(self, cmd):
        del self.subscriptions[cmd]

    def storage_for(self, m):
        if m in self.storages:
            return self.storages[m]
        else:
            o = ClientStorage()
            self.storages[m] = o
            return o


def register_command(name, fn, namespace=None, main_menu=False):
    fullname = "{}{}".format(namespace+":" if namespace else "", name)
    _commands[fullname] = fn
    if main_menu:
        _main_menu.append([main_menu, fullname])


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
        "_": lambda x: x.__package__,
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
            yield opts["name"], fn(c, c.storage_for(fn.__module__))


def call(cl, name, *args, **kwargs):
    try:
        fn = _commands[name]
        return fn(cl, cl.storage_for(fn.__module__), *args, **kwargs)
    #@TODO: except invalid arguments number TypeError 
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
                m.auth(cl, cl.storage_for(m.__name__))

        return cl
    else:
        return None


def reset_widget_time(c, name):
    c.widgets[name]["last_time"] = 0


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
