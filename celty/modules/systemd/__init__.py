from celty.modules import api

from subprocess import check_output


@api.widget()
def uptime(c):
    return [check_output("uptime").decode("utf-8").strip()]
