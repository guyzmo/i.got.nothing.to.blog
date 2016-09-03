---
type: post
categories: code
header_background: /img/atmega32u4_closeup.jpeg
tags: [ bootloader, avr ]
title: "AVR bootloaders: reboot into bootloader"
date: 2014-01-15T10:42:53+02:00
summary: "I needed to tweak the bootloader to get a working reboot into bootloader feature. With help from the AVRFreaks community, I thought it'd be a good idea to share my experience working with AVR bootloaders."
lang: english
logo: "/img/avr.png"
aliases:
 - /code/on/avr-for-ble-and-ios/
---

When dealing with firmware updates, you need to make the AVR reboot into bootloader. And
there are lots of solution when you try to do that:

 - either you force a reboot using the 'reset' button, and try to launch the avrdude command
   just 42ms after hitting the switch, or
 - you can use the not always wired up and not always working properly DTR line pushed down, or
 - you can wire a pin to the reset button — which is the worst solution, as avr pins are in an undefined state
    at startup time) or
 - you can use the watchdog reset to reboot.

My preferred solution would be the DTR line pulled down, though it's mostly an electronic
solution and it does not work with newer atmega USB MCUs. So, let's have fun hacking the
bootloader.

As I hacked this on the stk500 bootloader from Peter Fleury, I'm going to show the modifications
based on that bootloader, which is known to work on all AVR from the atmega168 to the 2560. But
that kind of hack could be easily patched on optiboot, the newer smaller (less than 1k) bootloader.

In that latest version of the firmware, patched by Mark Sproul, he fixed an issue with the watchdog
timer, which we can thank him for, as we won't have to do write it. Indeed, when you set up a watchdog
in your firmware for something like 1 second, that for a reason your code gets reboot, and then you
have a 2 seconds timeout in bootloader mode, the watchdog will get triggered during boot time and
won't be reset unless you hard reset the AVR.

So his code in the `_FIX_ISSUE_181_` preprocessor block fixes that:

	uint8_t	mcuStatusReg;
	mcuStatusReg	=	MCUSR;

	__asm__ __volatile__ ("cli");
	__asm__ __volatile__ ("wdr");
	MCUSR	=	0;
	WDTCSR	|=	_BV(WDCE) | _BV(WDE);
	WDTCSR	=	0;
	__asm__ __volatile__ ("sei");
	// check if WDT generated the reset, if so, go straight to app
    if (mcuStatusReg & _BV(WDRF))
    {
        app_start();
    }

This code stores the reboot status register in `mcuStatusReg`, clears the watchdog reset
registers, and if a watchdog caused the reboot, jump straight to address `0x00` (which
`app_start()` points to).

Though the only minor modification we need to do here is:

	if (mcuStatusReg & _BV(WDRF))
	{
        boot_timeout =  200000; // sixteen LED blinks
	} else {
        boot_timeout =  50000; // four LED blinks
    }

So there's a really long timeout at boot time in order for the flashing to be done. 

And voila `\o/`

Don't forget to merge the bootloader with your firmware before uploading using your
favorite flasher and now you can reboot into bootloader using the following code in
your firmware:

    #include <avr/wdt.h>

    void reboot_into_bootloader(void) {
        wdt_enable(WDTO_15MS);
        for(;;);
    }

