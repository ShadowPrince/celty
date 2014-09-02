import helmet
from helmet import elements as els
from celty.modules import api

from subprocess import check_output


def auth(c):
    c.lines = 7
    c.fields = "pcpu,pmem,pid,user,args"
    c.sort = "pcpu"


@api.command(ns="system")
@api.ui()
@helmet.pack()
def configure(c, **data):
    if not data:
        data = {"lines": c.lines,
                "fields": c.fields,
                "sort": c.sort, }
        result = ""
    else:
        c.lines = int(data["lines"])
        c.fields = data["fields"]
        c.sort = data["sort"]
        result = "success"

    return ([els.label("lines to show"), els.input("lines", data["lines"])],
            [els.label("fields"), els.input("fields", data["fields"])],
            [els.label("sort (one of fields)"), els.input("sort", data["sort"])],
            [els.button("save", "system:configure", ("lines", "fields", "sort")), els.label(result)], )


@api.widget()
def uptime(c):
    return [check_output("uptime").decode("utf-8").strip()]


@api.widget(timeout=3)
def ps(c):
    top = check_output((
        "sh",
        "-c", "ps -eo {} | sort -k {} -r".format(c.fields, c.fields.split(",").index(c.sort) + 1)))
    out = top.decode("utf-8").strip().splitlines()[:c.lines]

    return out
