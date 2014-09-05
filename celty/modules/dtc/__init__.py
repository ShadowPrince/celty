from celty.modules import api
from celty.modules import celty

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
        return celty.main(c, s)

    return helmet.update(p=helmet.set(progress=s.p))


@api.command()
@helmet.pack()
def test_data(c, s, ss):
    return helmet.update(b=helmet.set(caption=ss))


@api.command(main_menu=True)
@helmet.pack(subscribe="dtc:test_updater")
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
                els.button("set caption!", "dtc:test_data", ("ss", ), name="b")
            ], )
