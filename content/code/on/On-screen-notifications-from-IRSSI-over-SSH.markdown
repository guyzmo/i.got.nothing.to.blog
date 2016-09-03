---
type: post
categories: code
tags: [ code, github, irssi, perl, python, ssh, tunnel ]
title: On-screen notifications from IRSSI over SSH
date: 2010-06-21T15:23:00+02:00
summary: "After years of working with an IRC client inside screen on my server, here is how I managed to get my notifications get through SSH so I won't miss when you highlight me!"
lang: english
aliases:
 - /hack/on/on-screen-notifications-from-irssi-over-ssh/
---
After years of working with an IRC client inside screen on my server to which 
I connect using SSH, I was missing having any kind of notifications when I'm
being highlighted. I don't want to use bouncers or to disconnect/reconnect all
the time. So I prefer to make a ssh tunnel from an IRSSI script to a python 
script I run on localhost, that sends every configured highlight to localhost.
That other script calls libnotify on linux or growl on OSX to display the 
notification.

Source code available on my [github](http://github.com/guyzmo/irssi-over-ssh-notifications)

Contributions are opened to package and make it better.

There's a bug I still can't get rid of : when notifications are sent through
the tunnel, SSH reports almost all the time :

    setsockopt TCP_NODELAY: Invalid argument

if anyone has an idea on how to resolve that, drop me a mail !
