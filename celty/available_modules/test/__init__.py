import celty
from celty.modules import api

import helmet
from helmet import elements as els


def auth(c, s):
    s.p = 0


@api.command()
def test_updater(c, s):
    s.p += 1
    if s.p > 100:
        s.p = 0
        # ain't fast enough!
        return celty.call("celty:main_menu")

    return helmet.update(p=helmet.set(progress=s.p))


@api.command()
@helmet.updater()
def test_data(c, s, ss):
    s.p = 0
    return dict(b=helmet.set(caption=ss))


@api.command(main_menu=True)
@helmet.ui(subscribe=test_updater)
def test(c, s):
    return ([
                els.label("time to decide: "),
                els.progressbar("p"),
            ], [
                els.label("select button caption: "),
                els.select(
                    "ss",
                    dict(AAA="I like AAA", BBB="BBB is better!"), selected="a")
            ], [
                els.button("set caption!", test_data, ("ss", ), name="b")
            ], )
