from log import e, i


commands = {}


class CommandNotRegisteredError(Exception):
    def __init__(self, name):
        super(Exception, self).__init__("Command \"{}\" not registered!".format(name))


def register(name, fn, namespace=None):
    i("Registered command {} in ns {}", name, namespace)
    commands["{}{}".format(namespace+":" if namespace else "", name)] = fn


def call(name, *args, **kwargs):
    try:
        return commands[name](*args, **kwargs)
    except KeyError:
        raise CommandNotRegisteredError(name)
