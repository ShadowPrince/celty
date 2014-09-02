import json
import time

from twisted.protocols.basic import LineReceiver


class JSONReceiver(LineReceiver):
    def jsonReceived(self, data):
        pass

    def sendJson(self, data):
        self.sendLine(json.dumps(data).encode("utf-8"))

    def lineReceived(self, line):
        self.jsonReceived(json.loads(line.decode("utf-8")))
