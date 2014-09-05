import helmet
from helmet import check as ck
from helmet import elements as els

import celty
from celty.modules import api

from subprocess import check_output


FIELDS="pcpu,pmem,pid,user,args".split(",")


def auth(c, s):
    s.lines = 7
    s.fields = "pcpu,pmem,pid,user,args"
    s.sort = "pcpu"


@api.command(main_menu="configure system module")
@helmet.ui()
def configure(c, s, **data):
    submit = els.button("save", configure, ("lines", "fields", "sort"))

    cdata, err = ck.check(
            submit, 
            data,
            validators={
                "fields": [
                    ck.not_empty(),
                    lambda x: None if [True for a in x.split(",")] == [x in FIELDS for x in x.split(",")] else "invalid value!",
                    ],
                "lines": ck.integer(),
                "sort": ck.value_in(FIELDS),
                },
            translators={
                "lines": [ck.to_integer(), lambda x: x+1, ]
                }, )

    if not err:
        s.lines = cdata["lines"]
        s.fields = cdata["fields"]
        s.sort = cdata["sort"]

        return helmet.update(status=dict(text="success"), errors=dict(text=""))
    elif not data:
        data = {"lines": s.lines,
                "fields": s.fields,
                "sort": s.sort, }
    else:
        return helmet.update(status=helmet.set(text=""), errors=helmet.set(text="\n".join(ck.errorlines(err))))

    return ([els.label(name="errors"), ],
            [els.label("lines to show: "), els.input("lines", data["lines"])],
            [els.label("fields: "), els.input("fields", data["fields"])],
            [els.label("sort (one of fields): "), els.input("sort", data["sort"])],
            [submit, els.label(name="status")], )


@api.widget()
def uptime(c, s):
    return [(check_output("uptime").decode("utf-8").strip()), ]


@api.command()
def refresh_ps(c, s):
    celty.reset_widget_time(c, "system:ps")


@api.widget(timeout=3)
def ps(c, s):
    top = check_output((
        "sh",
        "-c", "ps -eo {} | sort -k {} -r".format(s.fields, s.fields.split(",").index(s.sort) + 1)))
    out = top.decode("utf-8").strip().splitlines()[:s.lines]

    return out
