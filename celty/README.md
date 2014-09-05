# Celty server

This is the server for celty. To be honest, there is two servers powered by twisted: one in plain sockets, and second in web- ones. 

## Installation

No additional configuration needed.  Server depends on `twisted`, `txsockjs`, `pyopenssl`, `service_identity`.
You can set port in `server/__init__.py` file.


## Running 

Server starts with execution of `loader.py`.
Time, in which celty checks and sends subscriptions and widgets, configures in `server/reactor.py` file. 
