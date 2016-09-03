---
type: post
categories: hack
tags: [ C, code, msp430, electronics, macosx ]
title: "Hack to work with msp430 on macosx" 
date: 2012-05-18T17:08:41+02:00
summary: "I got my hands on a msp430 launchpad to play around with it, and unluckily, the launchpad does not play nice with MacOSX 10.6. After the break, you'll get my tutorial to make it work."
lang: english
logo: /img/ti_launchpad_t.jpeg
header_background: /img/msp430_bg.jpeg
aliases:
 - /hack/on/hack-to-work-with-msp430-on-macosx/
---
I got my hands on a msp430 launchpad to play around with it,
and unluckily, the launchpad does not play nice with macosx.

So as every manual states it, you begin by getting the toolchain :

    % sudo port install msp430-gcc msp430-binutils msp430-gdb msp430-libc msp430mcu

you can also do it using brew :

    % cd `brew --prefix`
    % git pull http://github.com/reid/homebrew.git
    % brew install mspdebug llvm-msp430

then, if you run ``mspdebug rf2500`` to connect to the launchpad, you'll get a
``permission denied error``. And no, that's not a matter of permissions. OSX
does not have the damn good USB module installed.

So here's my quick and dirty solution to get something that just works :

On [TI's official driver's page](http://e2e.ti.com/support/interface/digital_interface/m/videos__files/198722.aspx) 
you can download the last compiled module ([source code over here](http://e2e.ti.com/support/interface/digital_interface/m/videos__files/198719.aspx). 
You can download [it](http://e2e.ti.com/support/interface/digital_interface/m/videos__files/198722/download.aspx) and unzip it :

    % wget http://e2e.ti.com/support/interface/digital_interface/m/videos__files/198722/download.aspx -O TIVCP_bin_2D00_1.2.1.zip
    % unzip TIVCP_bin_2D00_1.2.1.zip TIVCP-OSX_binaries-1.2.1.dmg
    % open TIVCP-OSX_binaries-1.2.1.dmg
    % sudo cp -r /Volumes/TIVCP-OSX_binaries-1.2.1/TIVCPSerial.kext/ /System/Library/Extensions
    % sudo touch /System/Library/Extensions
    % sudo chown -R root:wheel /System/Library/Extensions/TIVCPSerial.kext/
    % sudo chmod -R 755  /System/Library/Extensions/TIVCPSerial.kext/

Then you have to edit with your favorite editor the following file :

    % vim /System/Library/Extensions/TIVCPSerial.kext/Contents/Info.plist

and insert into it :

         <key>ComIntf</key>
         <dict>
             <key>CFBundleIdentifier</key>
             <string>com.apple.kernel.iokit</string>
             <key>IOClass</key>
             <string>IOService</string>
             <key>IOProviderClass</key>
             <string>IOUSBInterface</string>
             <key>bConfigurationValue</key>
             <integer>1</integer>
             <key>bInterfaceNumber</key>
             <integer>0</integer>
             <key>idProduct</key>
             <integer>62514</integer>
             <key>idVendor</key>
             <integer>1105</integer>
         </dict>
         <key>DebugIntf</key>
         <dict>
             <key>CFBundleIdentifier</key>
             <string>com.apple.kernel.iokit</string>
             <key>IOClass</key>
             <string>IOService</string>
             <key>IOProviderClass</key>
             <string>IOUSBInterface</string>
             <key>bConfigurationValue</key>
             <integer>1</integer>
             <key>bInterfaceNumber</key>
             <integer>1</integer>
             <key>idProduct</key>
             <integer>62514</integer>
             <key>idVendor</key>
             <integer>1105</integer>
         </dict>
         <key>DeviceDriver</key>
         <dict>
             <key>CFBundleIdentifier</key>
             <string>com.apple.kernel.iokit</string>
             <key>IOClass</key>
             <string>IOService</string>
             <key>IOProviderClass</key>
             <string>IOUSBDevice</string>
             <key>bcdDevice</key>
             <integer>256</integer>
             <key>idProduct</key>
             <integer>62514</integer>
             <key>idVendor</key>
             <integer>1105</integer>
         </dict>

just before (note that it has to be inside the big <dict></dict> that has IOKitPersonalities as key !) :

     </dict>
     <key>OSBundleLibraries</key>
     <dict>
         <key>com.apple.iokit.IOSerialFamily</key>
         <string>1.0.4</string>
         <key>com.apple.iokit.IOUSBFamily</key>
         <string>1.8</string>
         <key>com.apple.kpi.bsd</key>
         <string>8.0</string>
         <key>com.apple.kpi.iokit</key>
         <string>8.0</string>
         <key>com.apple.kpi.libkern</key>
         <string>8.0</string>
         <key>com.apple.kpi.mach</key>
         <string>8.0</string>
         <key>com.apple.kpi.unsupported</key>
         <string>8.0</string>
     </dict>
 </dict>
 </plist>

for older OSX systems (less than 10.4) you'll have to do the following 
(but it won't hurt if you do it anyway), but on newer systems, changing
the date of a file inside /System/Library/Extensions will trigger it:

    % kextcache -e

And then you're done ! It worked for me directly without rebooting, 
but the other tutorials say you'd better reboot to get it work.

This hackish tutorial is mixing informations from two tutorials :

 * [The first at TI](http://processors.wiki.ti.com/index.php/MSP430_LaunchPad_Mac_OS_X)
 * [The second on mspdebug's wiki](http://mspdebug.sourceforge.net/faq.html#rf2500_osx)
