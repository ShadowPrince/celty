import celty

from functools import wraps
from itertools import chain


def prep_ui(layout, subscribe=False, skip_grab_check=False):
    """
    Prepare layout to be sended to client.
    Checks if names from button's grab exists, sets element's command argument to celty command if its has been passed like python functions.

    Return celty dict with "ui" type, subscribe function (if exists) and "data" with gui layout.
    """
    if isinstance(layout, dict):
        return layout

    names = []
    for i, el in enumerate(chain(*layout)):
        if type(el) is not dict:
            raise ValueError("Layout value {} is not an helmet element!".format(el));

        names.append(el.get("name", None))

    for i, el in enumerate(chain(*layout)):
        for name in el.get("grab", []):
            if name not in names:
                raise ValueError("Element {} can't grab '{}' - no such name!".format(el["name"] or "#"+str(i), name))

        if el["type"] == "button":
            if not isinstance(el["command"], basestring):
                el["command"] = celty.find_command(el["command"])

    if not isinstance(subscribe, basestring):
        _subscribe = celty.find_command(subscribe)
    else:
        _subscribe = subscribe

    return {"type": "ui",
            "subscribe": _subscribe,
            "data": layout, }


def update(fb=None, **kwargs):
    """
    Prepare update query.
    Updates passed trough kwargs (element name => action).

    Arguments:
    fb - dict that represents framebuffer
    kwargs - update actions dictionary

    Return celty dict with "ui_update" type, and "data" with update data.
    """
    if fb:
        for k, v in kwargs.items():
            if fb.get(k, None) != v:
                fb[k] = v
            else:
                del kwargs[k]

    return {"type": "ui_update",
            "data": kwargs, }


def set(**kwargs):
    """
    Action of helmet.update function.
    Sets element attributes, which passed in kwargs.
    """
    return kwargs


def append(**kwargs):
    """
    Action of helmet.update function.
    Appends data (passed in kwargs) to elements attributes.
    Notice: not any element support that query.
    """
    kwargs.update({"__method": "append", })
    return kwargs


def ui(subscribe=False, skip_grab_check=False):
    """
    Decorator for celty's command.
    Wraps function call with helmet.prep_ui function.
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            return prep_ui(fn(*args, **kwargs), subscribe=subscribe, skip_grab_check=skip_grab_check)
        return wrapper

    return decorator


def updater():
    """
    Decorator for celty's command.
    Wraps function call with helmet.update function.
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            return update(**fn(*args, **kwargs))
        return wrapper
    return decorator
