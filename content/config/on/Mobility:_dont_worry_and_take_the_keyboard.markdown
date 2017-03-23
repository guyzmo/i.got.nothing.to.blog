---
type: post
categories: hack
tags: [ linux, tinc, setup, laptop, workstation, ssh ]
title: "How I achieve full mobility with simple linux tools"
date: 2017-03-24T23:12:14+01:00
summary: "Over the years, I've tried many ways to make it possible to switch between my
laptop and my workstation in the most seamless way possible. After the break, I'll share
my mobile epiphany…"
lang: english
logo: "/img/syncthing.jpeg"
header_background: /img/laptop_coffee.png
tweet: 845061462817198080
---

I spent most of my life doing *stuff* with computers. Originally, I was only working
on static workstations, and as I grew up, I had my hands on a few crappy laptops. Then
I've bought my first mac (about 12 years ago, and it was a powerbook) and stuck with 
Apple.

But I never abondonned using a workstation. Because it's where I can store a
lot of data (because terabytes are cheap!), which I can connect to from anywhere in
the world, on which I got my mechanical keyboard connected, got 22 USB inputs, have
got some hifi speakers on etc.

# The frustration

Though, I always had that frustration when starting a work on a device, I have to keep
on working on that same device, because I won't be able to start over where I left at
on the other device.

<center>
![](/img/trollface_frustration.png)
</center>

The issue here, is that keeping my work in sync between two devices is tough, and does
not work well, and I gave many shots at that. There are a few good cloud based tools
out there that might do the job. But I prefer to stay frustrated than use a tool that
I cannot trust and stores my data in places I don't know.

So I tried many tools. I first used SVN to sync my home and my configuration, but ended
up in a nightmare having my work SVN repositories mixed up with my home one… And years
later when I upgraded to Git things did not go better on that side. So version control
was not a good idea ☹

I then tried using rsync, the unix utility that can do whatever you want when it comes
to syncing your files. I tried unison on top of that, but it fell too easily out of sync,
I had a few conflicts, or with other parameters it was just too slow… In the end it
was always too painful.

The following years, I tried bittorrent-sync (non-free, but not keeping your files)
which lost me some files, a dual way configuration of lsyncd (which ended up in a weird
file copy feedback loop), and even lurked at orifs, which is a great concept if only it
worked!

But file syncing is not the only thing, there's also network configuration. Wherever
I am, I want to be able to have my workstation↔laptop connections stay up and working.
And I've tried many different VPNs that were working so-so, but were a nightmare to
configure and keep in shape.

# The Solutions

Then in the recent months, I switched back from Apple laptops to a linux-based lenovo
laptop. Doing so, I tried again to work a solution to have real mobility between my
devices. And finally, there was an epiphany 🙌

## Private network

I have discovered [`tinc`][tinc] as advised by a good friend, and found out that it's
the first time I got a tunnel that can be setup in a couple of minutes, while being
relatively safe.
The great thing of tinc is that it's supporting the full IP stack, including UDP.

To create a new network, you've got to create three files, generate a key and start
the service:

``` bash
% mkdir /etc/tinc/myprivatenetwork
% cat > /etc/tinc/myprivatenetwork/tinc.conf
Name = MyWorkstation
ConnectTo = MyLaptop

% cat > /etc/tinc/myprivatenetwork/tinc-up
#!/bin/sh

ip link set $INTERFACE up
ip addr add 192.168.254.10/32 dev $INTERFACE
ip route add 192.168.254.0/24 dev $INTERFACE

% cat > /etc/tinc/myprivatenetwork/tinc-down
#!/bin/sh
ip route del 192.168.42.0/24 dev $INTERFACE
ip addr del 192.168.42.10/32 dev $INTERFACE
ip link set $INTERFACE down        

% tincd -n myprivatenetwork -K
% sudo systemctl start tincd@myprivatenetwork
```

Then when you're adding new hosts to the network, you need to copy the public
key of that host in `/etc/tinc/myprivatenetwork/hosts` of your other hosts. 

And you're set!

Then, everytime I restart or get my laptop out of sleep, I have my connections
to my workstation back on, and I can keep working seamlessly. I can also switch
from wifi to the network cable at home, without having to restart synergy or other
local network apps!

[tinc]:http://tinc-vpn.org

## File syncing

I have found greatness in a tool called [syncthing]. It's packaged on all the
distributions, and has been designed to be the bittorrent-sync (and dropbox)
killer. And I have to admit, not only it is FLOSS, but it definitely sets a new
standard in syncing files. I've been using it for a few months, and I almost
feel like I'm having the same drive shared on NFS on both computers — without
the slow.

Once installed, syncthing comes with a WebUI, though a GTK app also exists. You
need to pair your computers together, sets up the volumes you want to share, and
start sharing. From then on, you just forget about it, it'll do the job.

As a side effect, I'm also having my work (as it is) being duplicated between two
storing units (laptop and workstation), making it a great real time backup helping
me to never loose any minute of my work even when if I break my laptop. If you add
a duplicity backup of my work onto another storage drive, my work is pretty safe!

[syncthing]:https://syncthing.net/

## Working over slow connections

I'm an heavy IRC user, and I still read my mail in the shell, on an SSH connection.
But as I also have been taking the train a lot, I've started to use [mosh] to make
it friendly to work on very slow connections.

Though, because of it's heavy use of UDP ports (and it's coded in [Perl 🔥](https://youtu.be/yp_l5ntikaU?t=59)), I prefer
to keep the session opened inside tinc!

[mosh]:http://mosh.org

# Finally…

…I'm happy with my new setup, and even though I know I can do better (like syncing my mails
between my laptop and my workstation, but that's for another article), it's doing a great
job at optimising my productivity and keep my mind at rest in terms of backup.

What are your solutions to keep your data in sync? And your network connections?

