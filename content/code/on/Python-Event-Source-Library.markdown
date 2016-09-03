---
type: post
categories: code
tags: [ code, github, python ]
title: "Python Event Source Library"
date: 2012-05-29T15:38:12+02:00
summary: "For a project, I needed to have a simple way to make a central software be able to send commands to several slaves appliances that are on the internets, i.e. they can either be on Internet with a public IP address, or be behind a proxyfied-firewalled private network that can only communicate through port 80. That's how I came across a W3C working paper about a very simple technology based on HTTP/1.1 long-polling, called EventSource. The full story and real code after the break..."
lang: english
logo: /img/python-logo.png
header_background: /img/python-logo.png
aliases:
 - /hack/on/python-event-source-library/
---
After looking at a lot of different technologies, it rapidly seemed obvious 
that HTTP 1.1's long polling methods are what I was looking for. But when I
tried to find client/server implementation, I rapidly found out websockets 
implementation that are über-sophisticated  and with only the server-side 
(the client side being javascript) or other very obscure technologies I 
won't list.


To help me through this whole mess of technologies, I asked my colleagues 
and the community on [stackoverflow](http://stackoverflow.com/questions/10665569/websocket-event-source-implementation-to-expose-a-two-way-rpc-to-a-python-dj).


That's how [Athoune](http://blog.garambrogne.net/) gave me a good hint 
about a technology I had never head about: [W3C's Eventsource](http://dev.w3.org/html5/eventsource/).


It is basically a really simple one way communication scheme, initiated 
by the client, where the talking channel is from server to client. The
protocol is really simple, basically it is made of several ``field: value``, 
separated by two carriage return, where the field can be ``id``, ``event`` or ``data``.


So I took python [Tornado](http://tornadoweb.org) library, and cooked a
very simple, yet almost complete, client-server eventsource library in python:


It's on my [github](https://github.com/guyzmo/event-source-library/)


It comes in three components:

 * the server which opens a port and wait for new clients (GET) or for commands (POST), 
 * the client which connects to the server and wait for commands, and that can be extended by giving it a callback to do "things"
 * the request client, that posts commands and values to the server, which forwards them to the client.


It's already in [Pipy](http://pypi.python.org/pypi/eventsource/) and [documentation is over here](http://packages.python.org/eventsource/index.html). 


Try it, and don't hesitate to give me feedback !
