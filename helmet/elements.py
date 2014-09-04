from functools import wraps


RESERVED_NAMES = ["c", "s", ]


def element(t=None):
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
    return {"text": "\n".join(lines), 
            "max_lines": kw.get("max_lines"), }


@element()
def input(name, value=None, **kw):
    return {"name": name,
            "value": value if value else "", }


@element()
def button(caption, command, grab=(), **kw):
    return {"caption": caption,
            "command": command,
            "grab": grab, }


@element()
def progressbar(name, progress=0, **kw):
    return {"name": name,
            "progress": progress, }


@element()
def select(name, choices, selected=None, **kw):
    return {"name": name,
            "choices": choices,
            "selected": selected if selected else "", }
