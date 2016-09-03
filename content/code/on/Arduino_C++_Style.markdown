---
type: post
categories: code
tags: [ hack, bootloader, avr ]
title: "Arduino: C++ Style"
date: 2014-04-08T13:37:53+02:00
summary: "Here's a tip that will make C coders yell and cry, but will make C++ coders happy: how to implement C++ stream syntax for Arduino."
lang: english
header_background: /img/ArduinoUnoBack.jpeg
logo: "/img/arduino.jpeg"
aliases:
    - /code/on/arduino:-c++-style/
---

Here's a simple tip that will make C coders cry and yell, but will definitely make C++ codes happy: how
to implement C++ stream syntax for Arduino.

Based on the [following tip](http://playground.arduino.cc/Main/StreamingOutput) from the Arduino Playground,
I added a few things to make it more compatible with C++, so one can test a library on his computer, before
running on the microcontroller:

    static uint8_t base=0;
    inline Print &operator <<(Print &obj, unsigned long arg)
    {  
        switch (base) {
            case HEX: obj.print(F("0x")); break;
            case BIN: obj.print(F("0b")); break;
        }
        obj.print(arg, (int)base);
        base = 0;
        return obj; 
    }
    template<class T>
    inline Print &operator <<(Print &obj, T arg) {  
        obj.print(arg); 
        return obj; 
    }
    inline unsigned long hex(unsigned long arg) {  
        base = HEX;
        return arg; 
    }
    inline unsigned long bin(unsigned long arg) {  
        base = BIN;
        return arg; 
    }

    #define endl F("\n")
    #define cout Serial

N.B.: I know there can be some improvement, mostly about the `base` variable, but at least
that hack does the job of almost mimicking C++ like operators.

The idea is to be able to mimick the following syntax:

    cout << "This is an address 0x" << hex << n << endl;

so it can work in both STL and Arduino frameworks. But at the time being all it does is

    cout << "This is an address 0x" << hex(n) << endl;

It was a quick and dirty hack, and if you can suggest improvement on that, I'd be happy to
hear! Don't hesitate to comment and criticize that on Twitter!

