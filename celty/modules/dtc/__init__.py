from celty.modules import api

from datetime import datetime


@api.command()
def now():
    return str(datetime.now())
