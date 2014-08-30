import celty

from twisted.internet.protocol import Factory
from celty.server.helpers import JSONReceiver


class CeltyClient(JSONReceiver):
    def __init__(self):
        self.mode = self.auth

    def jsonReceived(self, data):
        self.sendJson(self.mode(data))

    def auth(self, data):
        self.client = celty.auth(data["token"])
        if self.client:
            self.mode = self.command
            return "success"
        else:
            return "failed"

    def command(self, data):
        try:
            out = celty.call(self.client, data["command"], *data.get("args", []))
        except celty.CommandNotRegisteredError:
            out = "404"
        except celty.CommandWrongUsageError as ex:
            out = str(ex)

        return out


class CertyFactory(Factory):
    def buildProtocol(self, addr):
        return CeltyClient()
