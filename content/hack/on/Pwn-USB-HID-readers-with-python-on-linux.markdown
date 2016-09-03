---
type: post
categories: hack
tags: [ code, geek, github, magnetic, python, pyusb, tmsr33 ]
title: "Pwn USB HID readers with python on linux"
date: 2011-12-23T20:28:24+02:00
summary:"For a work's project I needed to use two magnetic card readers ; our usage was depending on which one is used and the card's ID. So I sourced a magnetic card reader that outputs the Id through a TTL serial line and then I could manage using an arduino both serial lines and get them to work how we needed. But what was my surprise to get USB HID readers once I receipt the package ! So I plug them in, and well, they worked out of the box... but both of them output Ids on the console the same way. We were on a rush on the project, so we had no time to send them back. So my challenge was : How can we differenciate USB HID readers that act as keyboards ?" 
lang: english
logo: /img/msr001.jpg
header_background: /img/magnetic-cards.jpeg
aliases:
 - /hack/on/pwn-usb-hid-readers-with-python-on-linux/
---
For a work's project I needed to use two magnetic card readers ;
our usage was depending on which one is used and the card's ID.
So I sourced a magnetic card reader that outputs the Id through
a TTL serial line and then I could manage using an arduino both
serial lines and get them to work how we needed. But what was my
surprise to get USB HID readers once I receipt the package !

So I plug them in, and well, they worked out of the box...
but both of them output Ids on the console the same way. We were
on a rush on the project, so we had no time to send them back.


So my challenge was : How can we differenciate USB HID readers
that act as keyboards ?

## Challenge accepted !

So I've look on the great Internet how people managed to work out with USB HID
magnetic card readers, and after lots of useless reading I finally found on <a
href="http://www.micahcarrick.com/credit-card-reader-pyusb.html"
hreflang="en">Micah Carrick's site</a> how he managed to use a MagTek reader to
work with python.

Good news was that at first I could easily differentiate both readers by using PyUSB 1.0 :

    import usb.core
    import usb.util

    VENDOR_ID = 0x1130
    PRODUCT_ID = 0x0001
    DATA_SIZE = 167

    device = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)

And to connect two readers, nothing is easier ! Just add the parameter `find_all` to `usb.core.find()`:

    device = usb.core.find(find_all=True, idVendor=VENDOR_ID, idProduct=PRODUCT_ID)

*device is a list of all device with same vendor and product id connected to
the system, so you can differentiate `device[0]` and `device[1]`!*

Then, to unload the kernel driver, so it does not output anymore the Ids on the
console (and thus have access to the reader).

    if device.is_kernel_driver_active(0):
        try:
            device.detach_kernel_driver(0)
            except usb.core.USBError as e:
            sys.exit("Could not detatch kernel driver: %s" % str(e))
            …

And finally, we have to get the endpoint, which is the mapping to the actual
device :

    endpoint = device[0][(0,0)][0]

To read the output, the following is what you need :

    endpoint.read(self._endpoint.wMaxPacketSize)

*(the whole actual loop is in the source)*

But, once I've been able to read things from the card... what was my surprise
to only get garbage ! The data was totally messed up.

So I started to look around on Internet, and nothing was to be found, seems I
was the only one who wanted to read directly on such a device.

## What can be done then ?

well, get back to what I know :

 * get the datasheet of the reader
 * learn what the kernel does to get something out of that

After some searching, I finally found [it](http://www.barcode-manufacturer.com/magnetic_card/portable_magstripe/msr-swipe_card_reader.html). 
But nothing very helpful over there

So my last luck was reverse engineering the kernel. So I started with the USB
protocol specification :

* http://www.usb.org/developers/devclass_docs/Hut1_12v2.pdf

after reading some, I was quite afraid, because it has been hard to actually
communicate actively with the reader. But after turning around with digging in
the protocol, I chose to dig in the kernel's code, and what was my luck was to
stumble on the following code :

* http://git.kernel.org/?p=linux/kernel/git/torvalds/linux.git;a=blob;f=drivers/hid/usbhid/usbkbd.c;hb=HEAD

Finally I found the structure of what the HID device outputs : the first byte
is the modifier keycode, and the following byte is the actual character
keycode. Then, the keycode is matched to the `usb_kbd_keycode` array, and again
to a layout array (in another module) which matches your country's keyboard.

After some matching, I got the following mapping that works out of the box with
my reader:

    key_pages = [
        '', '', '', '',
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
        'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '\n', '^]', '^H',
        '^I', ' ', '-', '=', '[', ']', '\\', '&gt;', ';', "'", '`', ',', '.',
        '/', 'CapsLock', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12',
        'PS', 'SL', 'Pause', 'Ins', 'Home', 'PU', '^D', 'End', 'PD', '-&gt;', '&lt;-', '-v', '-^', 'NL',
        'KP/', 'KP*', 'KP-', 'KP+', 'KPE', 'KP1', 'KP2', 'KP3', 'KP4', 'KP5', 'KP6', 'KP7', 'KP8',
        'KP9', 'KP0', '\\', 'App', 'Pow', 'KP=', 'F13', 'F14' 
    ]

A lot of thanks to [Micah Carrick](http://www.micahcarrick.com/credit-card-reader-pyusb.html) for his blog post and his code.

* full source code is on [my github's page](https://github.com/guyzmo/tmsr33-pyusb/blob/master/tmsr33_pyusb.py)

