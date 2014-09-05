from functools import wraps

import time
import os
import subprocess


def to_dict(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        return dict(fn(*args, **kwargs))
    return wrapper


@to_dict
def get_stamps():
    dirs = ["./celty", "./helmet",]
    for path, directories, files in os.walk("."):
        if not list(filter(lambda x: x, [path.startswith(x) for x in dirs])):
            continue


        for f in filter(lambda x: not x.startswith(".") and not x.endswith("pyc") and not x.endswith("pyo"), files):
            fp = os.path.join(path, f)
            yield fp, os.path.getmtime(fp)


def start():
    return subprocess.Popen(["python2", "./celty/loader.py"])

stamps = get_stamps()
p = start()

while True:
    try:
        new_stamps = get_stamps()
        if new_stamps != stamps:
            stamps = new_stamps

            p.terminate()
            p.wait()
            print("============================== Changes made, restarting server... ========================")
            p = start()

        time.sleep(3)
    except:
        p.terminate()
        break
