---
type: post
categories: hack
tags: [ python, hack, arduino ]
title: "Pyaler release: RESTful interface for arduinos"
date: 2010-07-24T19:44:00+02:00
summary: "After a colleague pointed out the Yaler project, that aims to control an arduino using a RESTful interface, he challenged us to do the same, but simpler and in python. That's how we started the Pyaler project"
lang: english
logo: /img/pyaler.ico
aliases:
 - /hack/on/pyaler-release:-restful-interface-for-arduinos/
---
After a colleague pointed out the [Yaler project](http://yaler.org), 
that aims to control an arduino using a RESTful interface, he challenged us to do the same,
but simpler and in python. That's how we started the Pyaler project and how I started to
have some interest about Arduinos.

Pyaler has not been long to code, so at first, it enabled me to control a green-LED using
REST queries. That was fun, but not that much.

Then at the [RMLL2010](http://2010.rmll.info), John from [Hackable:Devices](http://hackable-devices.org)
gave me an RGB LED, that I made to work with Arduino and Pyaler. I put a demo on the
stand so anybody could come and change the light using the public IP address of my 
laptop. 

Still at the RMLL, [Jimmie P. Rodgers](http://www.jimmieprodgers.com)
gave me a LOLShield so I can test Pyaler with something funnier. Sadly, the
Lolshield could only display static strings, then I recoded the library so it
supports dynamic strings taken from the serial line (see my
[previous post](http://i.got.nothing.to/post/2010/07/13/Hacking-the-arduino-s-LoLshield)).

We finally released today [Pyaler](http://www.pyaler.org), now available 
on [Pypi](http://pypi.python.org/pypi/pyaler). And a live demo is
online at [play.pyaler.org](http://play.pyaler.org) so you can change
the displayed string and watch it change in a live video broadcast.
