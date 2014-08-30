from celty.modules import api

import subprocess

@api.command()
def sh(*args):
    try:
        return subprocess.check_output(args).decode("utf-8")
    except IndexError:
        raise TypeError("required argument")
    except FileNotFoundError:
        return "command not found!"
    except subprocess.SubprocessError:
        return "sub error!"
    

