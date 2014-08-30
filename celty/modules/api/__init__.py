import celty


def command(_name=None, ns=None):
    def cb(x):
        if not _name:
            name = x.__name__
        else:
            name = _name

        celty.register_command(name, x, namespace=ns)
        return x

    return cb


def widget(*args, **kwargs):
    def cb(x):
        celty.register_widget(x, *args, **kwargs)

        return x

    return cb
