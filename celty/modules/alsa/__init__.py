import celty
from celty.modules import api

import helmet
from helmet import elements as els


import re

from subprocess import check_output


def auth(c, s):
    s.step = 5
    s.channel = 'Master'



@api.command(main_menu=True)
@helmet.ui(subscribe='alsa:updater')
def alsa(c, s):
    @api.inline()
    def vol_up():
        check_output(['amixer', 'set', s.channel, str(s.step)+'+'])

    @api.inline()
    def vol_down():
        check_output(['amixer', 'set', s.channel, str(s.step)+'-'])

    @api.inline()
    def updater():
        c = check_output(['amixer', 'get', s.channel]).splitlines()[-1]
        return helmet.update(vol=helmet.set(
            text="Volume of {}: {}%".format(
                s.channel,
                re.findall(r'\[(\d+)\%\]', c)[0]
            ),
        ))

    return (
        [els.label(name='vol'), ],
        [els.button("/\\", vol_up),
         els.button("\\/", vol_down), ], )
