---
type: post
categories: hack
tags: [ arduino, C, C++, python, sensor, pollution ]
title: "Pollux'NZ City goes opensourced!"
date: 2013-03-15T16:47:54+02:00
summary: "The pollux project has been a project I've worked on for two years with my friend and colleague Kasey. Today, that project has been released as FLOSS/OSHW with all sources on github. And it is also featured on hackaday. And that rocks!"
lang: english
logo: "/img/pollux_in_the_city_small.png"
header_background: "/img/pollux_in_the_city_bg.png"
aliases:
 - /hack/on/pollux'nz-city-goes-opensourced!/
---

Today, the decision has been taken to give the Pollux'NZ City project a second breath:
it is being published as opensource and libre. We are really thrilled to share the project's
technologies we have developped over the last two years, with my friend and colleague [Kasey](http://kasey.fr)
at [CKAB](http://ckab.com/uncategorized/polluxnz-city-open-source).

The origins
===========

At first, it began as a simple implementation based on Adafruit's sensor shield, as a Proof 
of Concept. We could show off the fact that it is possible to create a simple arduino-based
solution that interact with the environment. But that was far from being a correct solution
for autonomous measurement. It used a 6 battery pack, couldn't go into sleep mode between
measures and the sensors weren't reliable enough.

![Pollux'NZ City Proof of Concept](/img/citypulse-station-nice.jpg)

A new design
============

So we decided to go for a design from scratch. We designed the overall architecture so
we can create a cluster of autonomous sensors modules that are interrogated by a gateway
module that pushes the values over Internet on datastores.

And for more flexibility, we decided to make each measuring module independant, operated
by a simple microcontroller working on a bus.

Finally, on the Gateway module, we decided that it should be agnostic of any datastores,
so it could push on any platform that exists, or will exist.

The prototype
=============

Then, begun the new implementation. To be able to work with clusters of modules, we chose
the zigbee technology, that can create secure and reliable communications between nodes,
and can create mesh networks. We used the XBee modules for their ease of use and position
on the market.

For the autonomous sensor module prototype, we implemented an Arduino with a XBee shield,
and master of an I2C bus. On that I2C bus, all sensors are implemented with a microcontroller
(an ATTiny85) that controls each sensor and format the returned values for transfer over the
I2C bus and XBee radio.

![Pollux'NZ City prototypes](/img/polluxnzcity_prototypes.png)

The gateway is actually the brain of the whole system. It knows every autonomous module on
the network, and every measuring sensor on each of them. On a regular basis (about 15min
interval) it will query each sensor of each module, and push them to configured datastores.
That's why we implemented a web UI frontend on the beaglebone that enables the users to
configure the topology of their network and configure the datastores addon.

Basically, a datastore addon is a simple python script that gets a list of all the values
measured, so it can format them (in JSON, XML, CSV…) and send them to the chosen web service.

And finally…
============

Today, the project is being on field testing with the help of the INRIA laboratory, and
we hope it will give a frame for future designs of pollution sensors.

![Pollux'NZ City… in the city](/img/pollux_in_the_city.png)

And today our project has been featured on [hackaday](http://hackaday.com/2013/03/15/deploying-an-open-source-pollution-monitoring-network/)!

