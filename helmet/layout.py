from functools import wraps
from itertools import chain


def pack(skip_grab_check=False, *args):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            result = fn(*args, **kwargs)
            names = [el.get("name", None) for el in chain(*result)]

            for i, el in enumerate(chain(*result)) if not skip_grab_check else []:
                for name in el.get("grab", []):
                    if name not in names:
                        raise RuntimeError("Element {} can't grab '{}' - no such name!".format(el["name"] or "#"+str(i), name))
            return result
        return wrapper

    return decorator
