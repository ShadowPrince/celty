import celty


def command(_name=None, _namespace=None):
    def cb(x):
        if not _name:
            name = x.__name__
        else:
            name = _name

        celty.register(name, x, namespace=_namespace)
        return x

    return cb
