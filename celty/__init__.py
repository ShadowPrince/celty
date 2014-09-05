from celty.log import e, i

import importlib
import time


_commands = {}
_main_menu = []
_keywords = {}
_widgets = {}
_modules = {}
_connections = []


class CommandAlreadyRegisteredError(Exception):
    def __init__(self, name):
        super(Exception, self).__init__("Command \"{}\" already registered!".format(name))


class WidgetAlreadyRegisteredError(Exception):
    def __init__(self, name):
        super(Exception, self).__init__("Widget \"{}\" already registered!".format(name))


class CommandNotRegisteredError(Exception):
    def __init__(self, name):
        super(Exception, self).__init__("Command \"{}\" not registered!".format(name))


class CommandWrongUsageError(Exception):
    pass


class ClientStorage:
    """
    Empty class for module per-client storage.
    """
    pass


class Client:
    """
    Class for every client connected to celty. 
    Keeps every per-client data, like subscriptions or module storages.

    widgets -- dict (command => dict of params) of widgets per-client parameters (like last_time)
    subscriptions -- dict (command => (args, kwargs)) of subscriptions
    proto -- protocol
    storages -- dict (module_name => ClientStorage) of storages
    """
    def __init__(self, protocol):
        """
        protocol -- instance of celty.server.reactor.CeltyProtocol
        """
        self.widgets = dict([(n, {"last_time": 0}) for n in (x["name"] for x in _widgets.values())])
        self.subscriptions = {}
        self.proto = protocol
        self.storages = {}

    def subscribe(self, cmd, *args, **kwargs):
        """
        Subscribe this client to command.

        cmd -- command name
        args, kwargs -- command args, kwargs
        """
        self.subscriptions[cmd] = (args, kwargs, )

    def unsubscribe(self, cmd):
        """
        Unsubscribe this client from command.

        cmd -- command name
        """
        try:
            del self.subscriptions[cmd]
        except KeyError:
            pass

    def storage_for(self, m):
        """
        Get storage for module.

        m -- module
        return instance of ClientStorage
        """
        if m in self.storages:
            return self.storages[m]
        else:
            o = ClientStorage()
            self.storages[m] = o
            return o


def register_command(name, fn, namespace=None, main_menu=False):
    """
    Register command to celty.

    name -- name of command
    fn -- function of command

    Kwargs:
    namespace -- namespace of command. Resulting name will be namespace:name
    main_menu -- if presented - name which will represent command in celty's main menu

    Raises CommandAlreadyRegisteredError.
    """
    fullname = "{}{}".format(namespace+":" if namespace else "", name)
    if fullname not in _commands:
        _commands[fullname] = fn
        if main_menu:
            _main_menu.append([main_menu, fullname])
    else:
        raise CommandAlreadyRegisteredError(fullname)


def register_widget(fn, name=None, namespace=None, timeout=1000, *args):
    fullname = "{}{}".format(namespace+":" if namespace else "", name)
    if fullname not in _widgets:
        _widgets[fn] = {
            "name": fullname,
            "priority": args[0] if len(args) > 0 else 0,
            "timeout": timeout,
            "last_time": 0,
        }
    else:
        raise WidgetAlreadyRegisteredError(name)


def register_module(module_name):
    """
    Register module.
    Imports module, so all commands and stuff will be registered by decorators.

    module_name -- string representing module_name
    """
    wgts, cmds = len(_widgets), len(_commands)
    module = importlib.import_module("modules." + module_name)

    _modules[module_name] = module

    wgts, cmds = len(_widgets) - wgts, len(_commands) - cmds
    i("{}: loaded {} commands and {} widgets", module_name, cmds, wgts)


def updated_widgets(c):
    """
    Get iterable trough widgets, that need to be updated for the client.

    c -- Client instance

    Yield tuples of (name, out text) of widgets
    """
    for fn, opts in _widgets.items():
        try:
            copts = c.widgets[opts["name"]]
        except KeyError:
            continue

        if copts["last_time"] + opts["timeout"] < time.time():
            c.widgets[opts["name"]]["last_time"] = time.time()
            yield opts["name"], fn(c, c.storage_for(fn.__module__))


def find_command(fn):
    """
    Find command name by function.

    fn -- function object
    Return command name.
    """
    for k, v in _commands.items():
        if v == fn:
            return k


def call(cl, name, *args, **kwargs):
    """
    Call command.

    cl -- Client
    name -- name of command
    args, kwargs -- args and kwargs used in function call
    Returns result of function call
    """
    fn = _commands[name]
    return fn(cl, cl.storage_for(fn.__module__), *args, **kwargs)


def process_subscriptions():
    """
    Process subscriptions, which means - call all subscripted commands for all clients and send them corresponding data.
    """
    for c in _connections:
        for sub, (args, kwargs) in c.subscriptions.items():
            c.proto.send_subscription(call(c, sub, *args, **kwargs))


def auth(protocol, token):
    """
    Auth client.

    protocol -- instance of CeltyProtocol
    token -- string of token
    Returns Client if successfull or None
    """
    if token == "1":
        cl = Client(protocol)
        for m in _modules.values():
            if hasattr(m, "auth"):
                m.auth(cl, cl.storage_for(m.__name__))

        return cl
    else:
        return None


def connection_made(protocol):
    """
    Add connection to internal connections list.
    """
    _connections.append(protocol.client)


def connection_lost(protocol):
    """
    Remove connection from internal connections list.
    """
    _connections.remove(protocol.client)


def get_connected():
    """
    Get connected protocols list.
    """
    return _connections
