---
type: post
categories: hack
tags: [ code, electronics, hack, openlightdimmer, triac ]
title: "The Open Light Project: Next Step"
date: 2012-10-13T18:52:42+02:00
summary: "Two years after the first try, I have worked on a few other electronic prototypes and now I think I have the experience I missed a few years back to put the prototype together."
lang: english
filters: markdown,lightbox
header_background: /img/concert-lights.jpeg
aliases:
 - /hack/on/the-open-light-project:-next-step/
---

The goal of that project is to create cheap and efficient
wireless devices to control professional lightning products,
traditional analogical ones using a controlled Triac and DMX
ones, by using a transceiver to DMX.

For the wireless part, the best option is using the zigbee, 
which is light, cheap, yet meshable.

The first step, here, is to test the designs exposed, then
prototype it using the DIP designs showed in images here,
and finally rebuild it using SMD components only. Once I'm
sure things I've done works, It'll be published.


The DMX Chapter
===============

First step, let's put a MAX485 and control a LED projector
from an Arduino. To work it out, I wired up a [MAX485"](http://octopart.com/max485cpa%2B-dallas+semiconductor-504827)
on a breadboard.

To talk to the board, I found out the [DMXSimple project](http://code.google.com/p/tinkerit/wiki/DmxSimple)
from tinker.it, which is pretty neat because the protocol 
has been implemented close to the assembly, and run by a 
timer so you won't get timing issues.

But sadly, my first attempt has been unsuccessful…

For the time being, here is a first look at a possible implementation
of the DMX to zigbee board. The overall cost of this design is about
30 euros without connectors and casing.

![Image of schematic of Open Light DMX](/img/open_light_dmx-schema.png "Image of schematic of DMX")
![Image of layout of Open Light DMX](/img/open_light_dmx-layout.png "Image of layout of DMX")


The TRIAC Chapter
=================

And now, let's have a look at the Triac schematic. I finally
found out a really neat [cheap and efficient design of a Triac](http://www-user.tu-chemnitz.de/~heha/Mikrocontroller/Triac8/index.htm.en)
on the Intertubes.

But I changed a few things from this design, first of all I
want to change the old ATTiny2313 to the better ATTiny85 to
control the triacs, and change the very (too?) simple alimentation
to a more usual one.

Here is a first design attempt I built

![Image of schematic of Open Light Triac](/img/open_light_triac-schema.png "Image of schematic of Triac")
![Image of layout of Open Light Triac](/img/open_light_triac-layout.png "Image of layout of Triac")

And here is the first prototype. Once it's built, I'll write
a code to test it.

![Picture of the Open Light Triac prototype](/img/open_light_triac_proto.png "Picture of the Open Light Triac prototype")
![Picture of the Open Light Triac prototype (split up)](/img/open_light_triac_proto2.png "Picture of the Open Light Triac prototype, split up")


The XBee Chapter
================

I just found out about the XBee SMT, which is as cheap as
€14.40, wih a µFL connector. I have worked on a footprint
for eagle, and I found out the written package specification
are inconsistent:

![Inconsistent XBee SMT Package dimensions...](/img/component_size_problem.png "Failing XBee SMT Package...")

Thus, I used the given DXF file and imported it in eagle,
but I have yet to verify it against the real chip once I'll
buy one.

![XBee SMT Package](/img/xbee_smt_package.png "XBee SMT Package")

I'm going to put my own Eagle library on my github soon, including
that package.

