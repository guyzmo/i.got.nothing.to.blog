---
type: post
categories: hack
tags: [ code, electronics, hack, openlightdimmer, triac ]
title: "Open Light Dimmer: First try"
date: 2010-08-05T16:24:42+02:00
summary: "Back in high school, I had the luck to get some experience and learn many things about stage lightnings. But, as I was already computer-litterate at that time I was amazed to discover that at the ethernet era, the protocol used for controlling lights was still DMX-512 based on RS485 serial line over a 3 points XLR. Because the DMX network configuration is a daisy chain, it looked to me a lot like BNC-based 10 base-T computer networks... with cable length, line terminals... being one's worst nightmare."
lang: english
aliases:
 - /hack/on/open-light-dimmer:-first-try/
---
Back in high school, I had the luck to get some experience and learn many things
about stage lightnings. But, as I was already computer-litterate at that time I
was amazed to discover that at the ethernet era, the protocol used for controlling
lights was still DMX-512 based on RS485 serial line over a 3 points XLR. Because
the DMX network configuration is a daisy chain, it looked to me a lot like BNC-based
10 base-T computer networks... with cable length, line terminals... being one's
worst nightmare.

At the same time, back in 2000-2002, it was the beginning of the WiFi-aera. That's
why, I imagined we simply could encapsulate a DMX packet in TCP packets (or even a
UDP datagram, as DMX is a broadcast-only protocol) sent over WiFi and receive them 
through a dongle attached at the back of the DMX-enabled projectors (and have Triac
based system to control analogical projectors).

But as I was a poor high-school guy with not much money, I contacted people with a 
white paper describing this with no success.

Then time went on, I passed university and I discovered the Hacklab movement. Almost
10 years later, you have many dmx over RF solutions on the market, big shows and
theatres with plenty of projectors use Martin-labeled cisco routers with 
RJ45/Ethernet connections all over, and connected to the Grand MA console.
But because the whole point of the Hacklab movement is DIY, I decided to try to find
all my electronics skills (burried deep in my memory) and finally build that system...
It's never too late ;) And I also have a perfect playground to test my system once 
done, as I'm often doing the lightning on 'alternative' stages in Paris.

The design of such a project is not very sophisticated, main design is :

 * have a computer that can send packets over RF
 * create two kinds of dongle
    * a analogical dongle, that will receive messages telling the brightness percent the projector shall lighten
    * a digital dongle, that will receive messages containing the channel and the value to send to the projector(s)

For economical reasons, I prefer to choose zigbee components (actually the xBee dongle
that is $20) to do the wireless. The digital dongle consist of a very basic design :

 * the microcontroller receives the RF message
    * it de-encapsulates the channel/value information
    * add the correct DMX-512 timings (header, seperator and ending)
    * sends it to the RS485 line, using a TTL2RS485 converter component (like the MAX485, but I've heard there are cheaper ones)

The analogical dongle is a bit more complex (at least to me, as I'm a ex-electronic
student doing mostly software-level stuff today) :

 * the micontroller receives the RF message
    * it de-encapsulates the brightness level (a value between 0 and 255)
    * and sets its DAC to the matching value between 0 and +Vcc
    * That voltage is then used by the Triac schematic to phaseshift correctly and manage the brightness of the light.

Easy to say, harder to do.

I started with that last part : *the Triac module*. For two reasons it's the harder to do
for me : I haven't done analogical electronics for 10 years and I'm afraid of high 
currents/voltages... (more than 10V 10mA is enormous !). As a friend gave me a few
components to start with, I tried to build my own schematic using the other schematics 
found on Internet. So I bought the missing parts, used a prototype board... and it end
up being an epic failure. Did not even have smoke or sparkles, neither did the surge 
protection break.

Some time have passed since then, it's hard to face my own inaptitude... 
But I decided to choose a schematic from [there (where the source is Elektor mag)](http://www.epanorama.net/documents/lights/lightdimmer.html)
and try again. So the following is to come...


