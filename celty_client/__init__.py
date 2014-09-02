from threading import Thread
import socket
import json
import time

widgets = {}


def send(c, data):
    client.send("{}\r\n".format(json.dumps(data)).encode("utf-8"))


def dispatch(data):
    if data["type"] == "auth":
        print("auth: " + data["state"])
    elif data["type"] == "widgets":
        for k, v in data["data"].items():
            widgets[k] = v
    elif data["type"] == "commands":
        print(data)


class WidgetsThread(Thread):
    def run(self):
        buffer = b""
        while 1:
            chunk = self.s.recv(1)
            buffer += chunk

            if buffer.decode("utf-8").endswith("\r\n"):
                dispatch(json.loads(buffer.decode("utf-8").strip()))
                buffer = b""

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 23590))

th = WidgetsThread()
th.s = client
th.start()

print("auth...")
send(client, {"token": "1", })
send(client, {"command": "help", })

while 1:
    print()
    print()
    print()
    print()
    print()
    for k, v in widgets.items():
        print("/{}-------------------".format(k))
        print("|{}".format("\n|".join(v)))
        print("\---------------------")

    try:
        send(client, {"command": "widgets", })
        pass
    except KeyboardInterrupt:
        break
    except IndexError:
        pass

    time.sleep(1)

client.shutdown(1)
client.close()
