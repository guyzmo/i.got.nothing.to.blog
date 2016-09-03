---
type: post
categories: code
tags: [ multitouch, python, github, kivy ]
title: "KiTT: A Multitouch Gesture Tool based on Kivy"
date: 2013-05-22T16:49:58+02:00
summary: "After having used a multitouch input device for some time on OSX, along with Better Touch Tool, I really missed to be able to switch workspaces or tabs using very simple two or three finger gestures. That's why I got that fixed, and here is KiTT!"
lang: english
logo: "/img/Kitt_Knight_Rider.jpeg"
header_background: "/img/k2000-front.jpeg"
aliases:
 - /code/on/avr-bootloaders:-reboot-into-bootloader/
---

I have now used for several years on my OSX computer the really excellent [BetterTouchTool](http://www.boastr.de/)
by Andreas Hegenberg. When I reconfigured my linux box again, that was something I really missed. Being able to 
move around workspaces or tabs using two/three fingers was just impossible.

I have looked over the intertubes for some gesture management application, and found a few stuff like [Touchègg](https://code.google.com/p/touchegg) that
I couldn't make work on my Debian Wheezy or PyMT based utility that is now abandonned (both PyMT and the utility). I only
found out about [xswipe](https://github.com/iberianpig/xSwipe) after having written KiTT.

So, there's now a new application, [KiTT](https://github.com/guyzmo/kitt.git) that enables a user to define gestures
and associate events to it. You can easily write new plugins for it, associate gestures with events and redefine 
touches for your input device. The application can communicate to the system using `Xlib`, `wnck` and `dbus`.

One could easily create a subprocess plugin, as follows:

    from kivy.logger import Logger
    log = Logger.getChild("KiTT")

    import subprocess

    def exec_proc(*command):
        subprocess.call(command))
        
    ACTIONS = dict(exec_proc=exec_proc)

and to bind that function to a gesture, here is what to add to the actions file:

    "four_swipe_up": [ { "function": "exec_proc", 
                         "parameters: ["xmessage", "hello world"] "]

The plugin file has to be saved in the kitt module directory, and you can send patches
with your own plugins to the main code so I can integrate them.

For future versions of the project, I want :
 * to compile a library of gestures for different input devices that could be detected and selected so the user does not have to care about his device ;
 * add support for pinch in/pinch out gestures and other weird gestures alike ;
 * create a BTT-like GUI, so newbie users can easily manage their gestures and commands

Now, go and `git clone https://github.com/guyzmo/kitt.git`

