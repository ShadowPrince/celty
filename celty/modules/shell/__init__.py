import helmet
from helmet import check as ck
from helmet import elements as els
from celty.modules import api

import subprocess


def _execute(*args):
    try:
        return subprocess.check_output(["sh", "-c", " ".join(args)]).decode("utf-8")
    except IndexError:
        raise TypeError("required argument")
    except Exception, e:
        return str(e) + "\n"


def auth(c, s):
    s.default(
            history=[],
            history_lines=300,
            lines=50, )


@api.command()
@helmet.ui()
def configure(c, s, **data):
    submit = els.button("save", "shell:configure", ("lines", ))
    cdata, err = ck.check(
        submit,
        data,
        validators={
            "lines": ck.integer(),
        },
        translators={
            "lines": ck.to_integer(),
        })

    if not err:
        s.lines = cdata["lines"]
        return helmet.update(status=helmet.set(text="success"))
    elif not data:
        data = {"lines": s.lines, }
    else:
        return helmet.update(status=helmet.set(text=""), err=helmet.set(text=ck.errortext(err)))
    
    return ([els.label(name="err"), ],
            [els.label("lines to show: "), els.input("lines", data["lines"])],
            [submit, els.button("back", "shell:main"), els.label(name="status")], )


@api.command(main_menu="shell")
@helmet.ui()
def main(c, s, sh=None):
    if sh:
        out = _execute(*sh.split())
        s.history.append("$ " + str(sh))
        s.history += out.splitlines()

        if len(s.history) > s.history_lines:
            s.history = s.history[-s.history_lines:]
        
        return helmet.update(
                history=helmet.append(text="$ {}\n{}".format(sh, out)),
                sh=helmet.set(value=""))

    return ([els.label(*s.history[-s.lines:], name="history", max_lines=s.lines)],
            [els.input("sh"), els.button("exec", "shell:main", ("sh", )), els.button("config", "shell:configure")], )
