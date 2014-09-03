import helmet
from helmet import check
from helmet import elements as els

from celty.modules import api

from subprocess import check_output


FIELDS="pcpu,pmem,pid,user,args".split(",")


def auth(c, s):
    s.lines = 7
    s.fields = "pcpu,pmem,pid,user,args"
    s.sort = "pcpu"


@api.ui(main_menu="configure system module")
@helmet.pack()
def configure(c, s, **data):
    submit = els.button("save", "system:configure", ("lines", "fields", "sort"))

    cdata, err = check.check(
            submit, 
            data,
            validators={
                "fields": [
                    check.not_empty(),
                    lambda x: None if [True for a in x.split(",")] == [x in FIELDS for x in x.split(",")] else "invalid value!", 
                    ],
                "lines": check.integer(),
                "sort": check.value_in(FIELDS),
                },
            translators={
                "lines": [check.to_integer(), lambda x: x+1, ]
                }, )

    if not err:
        s.lines = cdata["lines"]
        s.fields = cdata["fields"]
        s.sort = cdata["sort"]
    elif not data:
        data = {"lines": s.lines,
                "fields": s.fields,
                "sort": s.sort, }

    return ([els.label(*check.errorlines(err)), ],
            [els.label("lines to show: "), els.input("lines", data["lines"])],
            [els.label("fields: "), els.input("fields", data["fields"])],
            [els.label("sort (one of fields): "), els.input("sort", data["sort"])],
            [submit, ], )


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
