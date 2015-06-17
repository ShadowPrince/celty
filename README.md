# Celty

Celty is server-client-kit for dedicated server administration or monitoring. Designed for devices lacking keyboard (goodbye, ssh) and screen space (goodbye, various admin panels), it offers unified way to deal with various tasks for all-kind of client platforms.

## Usage

Since Celty is an only server-kit it's not quite usefull by itself. But, since Celty is an server-kit, it can be powered with easy-to-write modules, that can perform all kind of tasks. 

## Modules

Module is a just python package placed in a right place. It can register widgets (for monitoring various stuff) and command (for any interaction with users) with a simplified, but unified gui.

## GUI

The main goal was about moving GUI code to server and creating an unified and minimalistic iterface protocol over the network.
It's just like a sweet combination of HTML and JavaScript, except for hugeness of HTML and complexity of JS. Overall transfer data is much smaller than a web site, and it's not lacking that much of interactivity like mobile browsers (like OperaMini) do.


## Kit parts

* celty - celty server itself
* shooter - help celty server to run
* helmet - GUI layout markup library (server-side)
* webhelmet - implementation of client-side helmet library in javascript

## Client apps

* [webcelty](https://github.com/ShadowPrince/celty/tree/master/webcelty) - basic HTML/JS implementation using **webhelmet**
* [iCelty](http://github.com/shadowprince/iCelty) - cocoa implementation
