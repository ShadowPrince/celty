import celty

from twisted.internet.protocol import Factory
from celty.server.helpers import JSONReceiver


class CeltyProtocol(JSONReceiver):
    """
    Celty protocol.

    mode -- function to call when message received.
    """
    def __init__(self):
        self.mode = self.auth

    def connectionMade(self):
        pass

    def connectionLost(self, reason):
        celty.connection_lost(self)

    def jsonReceived(self, data):
        self.sendJson(self.mode(data))

    def auth(self, data):
        """
        Auth user.

        data -- dict (token: token)
        Return response dict (type: auth, result: success | error, error: error string)
        """
        self.client = celty.auth(self, data["token"])
        if self.client:
            self.mode = self.command
            celty.connection_made(self)
            return {"type": "auth",
                    "result": "success"}
        else:
            return {"type": "auth",
                    "result": "error",
                    "error": "token check failed", }

    def command(self, data):
        """
        Call command and return result or error.

        data -- dict(command: command, args: args)
        Return command result or dict(type: error, error: error)
        """
        try:
            args = data.get("args", [])
            if isinstance(args, list):
                out = celty.call(self.client, data["command"], *args)
            elif isinstance(args, dict):
                out = celty.call(self.client, data["command"], **args)
        except celty.CommandNotRegisteredError:
            out = {"type": "error",
                   "error": "command {} not registered".format(data["command"]), }
        except celty.CommandWrongUsageError as ex:
            out = {"type": "error",
                   "error": str(ex), }

        return out

    def send_subscription(self, data):
        """
        Send subscription data.

        data -- subscription data
        """
        self.sendJson(data)


class CeltyFactory(Factory):
    """
    Celty factory.
    """
    def buildProtocol(self, addr):
        return CeltyProtocol()
