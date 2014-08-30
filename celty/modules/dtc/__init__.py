from celty.modules import api

from datetime import datetime
from subprocess import check_output


@api.command()
def now(cl):
    result = {
        "now": str(datetime.now()),
    }
    return result


@api.command()
def calendar(cl):
    return check_output("cal").decode("utf-8")


@api.widget(timeout=1)
def dtc(cl):
    return [now(cl)["now"], ]
