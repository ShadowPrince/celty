import celty
from celty.log import e, i
from celty.server.reactor import CeltyProtocol, CeltyFactory
from txsockjs.factory import SockJSFactory

import sys
from twisted.internet import reactor, task, error
from twisted.internet.protocol import Factory


PORT = 23589  # C-E-L-T-Y
UPDATE_TIME = 0.3

datetimes = {}


def celtyLoop():
    """
    Loop for subscriptions and stuff.
    """
    celty.process_subscriptions()


def init():
    """
    Init reactor and events.
    """
    reactor.listenTCP(PORT+1, CeltyFactory())
    reactor.listenTCP(PORT, SockJSFactory(Factory.forProtocol(CeltyProtocol)))
    i("Started twisted server at {}:{}", "localhost", PORT)


def run():
    """
    Run reactor.
    """
    loop = task.LoopingCall(celtyLoop)
    loop.start(UPDATE_TIME)

    try:
        reactor.run()
    except error.ReactorNotRestartable:
        e("reactor halted!")
        sys.exit(1)
