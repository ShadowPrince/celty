from celty.log import e, i
from celty.server.reactor import CertyFactory


from twisted.internet import reactor


PORT = 23589  # C-E-L-T-Y


def init():
    reactor.listenTCP(PORT, CertyFactory())
    i("Started twisted server at {}:{}", "localhost", PORT)


def loop(state):
    reactor.run()
