from functools import wraps
from itertools import chain


def pack(subscribe=False, skip_grab_check=False, *args):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            result = fn(*args, **kwargs)

            if isinstance(result, dict):
                return result

            names = [el.get("name", None) for el in chain(*result)]

            for i, el in enumerate(chain(*result)) if not skip_grab_check else []:
                for name in el.get("grab", []):
                    if name not in names:
                        raise ValueError("Element {} can't grab '{}' - no such name!".format(el["name"] or "#"+str(i), name))
            return {"type": "ui", 
                    "subscribe": subscribe,
                    "data": result, }
        return wrapper

    return decorator


def update(**kwargs):
    return {"type": "ui_update",
            "data": kwargs, }


def set(**kwargs):
    return kwargs


def append(**kwargs):
    kwargs.update({"__method": "append", })
    return kwargs
