import celty
from celty.log import e, i
from celty.server.reactor import CeltyClient, CeltyFactory
from txsockjs.factory import SockJSFactory

import sys
from twisted.internet import reactor, task, error
from twisted.internet.protocol import Factory


PORT = 23589  # C-E-L-T-Y

datetimes = {}


def celtyLoop():
    celty.process_subscriptions()


def init():
    reactor.listenTCP(PORT+1, CeltyFactory())
    reactor.listenTCP(PORT, SockJSFactory(Factory.forProtocol(CeltyClient)))
    i("Started twisted server at {}:{}", "localhost", PORT)

    loop = task.LoopingCall(celtyLoop)
    loop.start(0.3)


def loop(state):
    try:
        reactor.run()
    except error.ReactorNotRestartable:
        e("reactor halted!")
        sys.exit(1)
