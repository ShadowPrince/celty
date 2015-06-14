# -*- coding: utf-8 -*-
import helmet
from helmet import check as ck
from helmet import elements as els

import celty
from celty.modules import api


from time import sleep
from math import floor
from mpd import (MPDClient, CommandError, PendingCommandError)


def auth(c, s):
    s.c = MPDClient()
    s.c.connect(host="localhost", port=6600)
    s.show = 10
    s.anim = 0


@api.command(main_menu=True)
@helmet.ui(subscribe='mpd:updater')
def mpd(c, s):
    @api.inline()
    def control_prev():
        s.c.send_prev()

    @api.inline()
    def control_next():
        s.c.send_next()

    @api.inline()
    def control_pp():
        s.c.send_pause()

    @api.inline()
    def play(id):
        s.c.send_playid(id)

    @api.inline()
    def updater():
        status = _status(s)

        pi = s.c.playlistinfo()
        try:
            song = pi[int(status.get('song', 0))]
        except IndexError:
            song = {}

        ppos = int(status.get('song', 0)) - s.show/2
        if ppos < 0:
            ppos = 0
        elif ppos + s.show > len(pi):
            ppos = len(pi) - s.show

        current = _trackline(song, "ui", status)
        viewport = 20
        # shure it should be done in frontend
        if len(current) > viewport:
            if s.anim >= len(current):
                s.anim = -3
            else:
                s.anim += 1
            overflow = viewport + s.anim - len(current)
            f = s.anim if s.anim > 0 else 0
            current = current[f:f+viewport] + ((" :: " + current)[:overflow] if overflow > 0 else "")

        update = dict()
        for i, p in enumerate(pi[ppos:ppos+s.show]):
            update["playlist_{}".format(i)] = helmet.set(text=_trackline(p, "playlist", status))
            cap = "•"
            if status.get('song') == p.get('pos'):
                cap += ">"
            update["play_{}".format(i)] = helmet.set(caption=cap, args={"id": p.get('id')})

        update.update(dict(
            state=helmet.set(text='{}'.format(status['state'])),
            time=helmet.set(text='{}/{}'.format(*map(_parse_time, status.get('time', '0:0').split(':')))),
            track=helmet.set(text=current),
            control_pp=helmet.set(caption=_pp_char(status, True)),
        ))

        return helmet.update(s.get_or_set('mpd_fb', {}), **update)

    return [
        [els.label('['),
         els.label(name='state'),
         els.label('] '),
         els.label(name='track'),
         els.label(' '),
         els.label(name='time')],
        [els.button('<<', control_prev),
         els.button('', control_pp, name='control_pp'),
         els.button('>>', control_next),
         els.label(' | '), 
         els.button('settings', configure)], ]\
        +\
        [(els.button("*", play, name='play_{}'.format(i)),
          els.label(name='playlist_{}'.format(i)), )for i in range(s.show)]

@api.command()
@helmet.ui()
def configure(c, s):
    @api.inline()
    def save(show):
        upd = {"show_errors": helmet.set(text=""), "state": helmet.set(text="")}
        try:
            s.show = int(show)
            upd["state"] = helmet.set(text="saved!")
        except ValueError:
            upd["show_errors"] = helmet.set(text="should be number!")
        return helmet.update(**upd)

    return ([els.label("Visible items in playlist: "), 
             els.input("show", s.show),
             els.label(name="show_errors")],
            [els.button("Save", save, ("show", )),
             els.button("Back", mpd),
             els.label(name="state")], )

@api.widget(timeout=1)
def widget(c, s):
    status = _status(s)
    try:
        song = s.c.playlistinfo()[int(status.get('song', 0))]
        next = s.c.playlistinfo()[int(status.get('nextsong', 0))]
    except IndexError:
        song = {}
        next = {}
    return [
            _trackline(song, "widget_1", status),
            _trackline(next, "widget_n", status),
        ]


def _status(s):
    return s.c.status()


def _trackline(song, f, kwargs={}):
    if f == "playlist":
        return "{}. {}: {}".format(
                song.get('pos'),
                song.get('artist'),
                song.get('title'),
            )
    elif f == "widget_1":
        times = "[{0[0]}/{0[1]}]".format(
                map(_parse_time, kwargs.get('time', '0:0').split(':')), )
        return '{} {}. {}: {}'.format(
            times,
            kwargs.get('song'),
            song.get('artist'),
            song.get('title'), )
    elif f == "widget_n":
        times = "[{0[0]}/{0[1]}]".format(
                map(_parse_time, kwargs.get('time', '0:0').split(':')), )
        return '[{}]{}next: {}. {}: {} (next)'.format(
            kwargs['state'],
            ' ' * (len(times) - len(kwargs['state']) - 2 - 5),
            song.get('pos'),
            song.get('artist'),
            song.get('title'), )
    elif f == "ui":
        return "{} - {}".format(song.get("artist"), song.get("title"))


def _pp_char(status, reverse=False):
    if status['state'] == 'pause':
        return '||' if not reverse else '|>'
    elif status['state'] == 'play':
        return '|>' if not reverse else '||'
    elif status['state'] == 'stop':
        return '[]'


def _parse_time(t):
    t = int(t)
    m = floor(t/60)
    return "{:02.0f}:{:02.0f}".format(m, t-m*60)
