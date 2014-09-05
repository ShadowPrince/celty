from functools import wraps


RESERVED_NAMES = ["c", "s", ]


def element(t=None):
    """
    Decorator for element functions.
    Deals with some kwargs (like name), checks if names is not reserver and setups type argument from wrapped function name.

    Keyword arguments:
    t -- set type manually
    """

    def decorator(fn):
        if not t:
            _t = fn.__name__
        else:
            _t = t

        @wraps(fn)
        def wrap(*args, **kwargs):
            result = fn(*args, **kwargs)

            if "name" not in result:
                result["name"] = kwargs.get("name")

            if result["name"] in RESERVED_NAMES:
                raise ValueError("{} is in reserved names({}), so you can't use it!".format(result["name"], RESERVED_NAMES))

            if "type" not in result:
                result["type"] = _t

            delkeys = []
            for k, v in result.items():
                if v == None:
                    delkeys.append(k)

            for k in delkeys:
                del result[k]

            return result
        return wrap

    return decorator


@element()
def label(*lines, **kw):
    """
    Label.

    lines -- lines to show (joined with \n). Notice: this attribute supports "append" update query.
    Keyword arguments:
    max_lines -- max lines to show (cliend-side)
    """
    return {"text": "\n".join(lines), 
            "max_lines": kw.get("max_lines"), }


@element()
def input(name, value=None, **kw):
    """
    Input.

    name -- name of element (unique)
    value -- default value
    """
    return {"name": name,
            "value": value if value else "", }


@element()
def button(caption, command, grab=(), **kw):
    """
    Button.

    caption -- caption of element
    command -- command string or function, which lookups with celty
    grab -- tuple of element's names, values of which will pass as arguments to command
    """
    return {"caption": caption,
            "command": command,
            "grab": grab, }


@element()
def progressbar(name, progress=0, **kw):
    """
    Progressbar.

    name -- name of element
    progress -- progress (from 0 to 100)
    """
    return {"name": name,
            "progress": progress, }


@element()
def select(name, choices, selected=None, **kw):
    """
    Select.

    name -- name of element
    choices -- dict (key => value)
    selected -- selected key
    """
    return {"name": name,
            "choices": choices,
            "selected": selected if selected else "", }
