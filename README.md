# Celty

Celty is server-kit for various tasks at dedicated server, like administration or assistance. Designed for devices lack of keyboard (goodbye, ssh) and screen space (goodbye, various admin panels), it offers unified modules for all-kind of client platforms with GUI, over the network connection.

## Usage

Since Celty is an server-kit it's not usage by itself. But, since Celty is an server-kit, it can be powered with easy-to-write and connect modules, that can perform all kind of tasks. 

## Modules

Module is a just python package placed in a right place. It can register widgets (for monitoring various stuff) and command (for any interaction with users) with a simplified, but unified gui.

## GUI

The main goal was about moving GUI to server and creating an unified interface protocol over the network, so client developers don't has to implement GUI to every module, but implement one layout markup protocol named `helmet`. 

Its just like a sweet combination of HTML and JavaScript, except for hugeness of HTML and complexity of JS. Overall transfer data is much smaller than a web site, and its not lacking that much of interactivity like mobile browsers (like OperaMini) do.


## Kit parts

* celty - celty server itself
* shooter - help celty server to run
* helmet - GUI layout markup library (server-side)
* webhelmet - implementation of client-side helmet library in javascript
* webcelty - basic implementation of client app in form of web app
