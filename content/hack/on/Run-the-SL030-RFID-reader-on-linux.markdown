---
type: post
categories: hack
tags: [ arduino, beaglebone, C, code, hack, rfid ]
title: "Run the SL030 RFID reader on linux"
date: 2012-06-02T15:21:32+02:00
summary: "I need to use the SL030 RFID reader on linux (on a beaglebone with i2c support enabled, of course). But when I tried to communicate with the device using i2cget, the device failed and disappeared from the detected devices... After the break, we'll see why and how I solved it."
lang: english
logo: /img/sl030.jpg
header_background: /img/sl030-bg.jpg
aliases:
 - /hack/on/run-the-sl030-rfid-reader-on-linux
---

I needed to use the SL030 RFID reader on linux (on a beaglebone
with i2c support enabled, of course). But when I tried to
communicate with the device using ``i2cget``, the device failed
and disappeared from the detected devices... After the break,
we'll see why and how I solved it.

My first contact with the SL030 has been using [arduino](https://github.com/guyzmo/LeLoopRFID),
using the SL018 library and everything worked __really__ fine.

So given the really low price of the product, it has been quite
obvious to me that I would use again the [SL030](http://www.stronglink-rfid.com/en/rfid-modules/sl030.html|en] for another [beaglebone](http://beagleboard.org/bone/)
based project.

So, I plugged the SL030 in the matching ``/dev/i2c-3`` device,
which is wired per default on the beaglebone. Then I ran :

    % i2cdetect -r -y 3
        0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
    00:          -- -- -- -- -- -- -- -- -- -- -- -- -- 
    10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    50: 50 -- -- -- UU UU UU UU -- -- -- -- -- -- -- -- 
    60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    70: -- -- -- -- -- -- -- --                         

and found my device is lying on the address 50. And then, I tried
to get a full dump of the device using ``i2cdump``, and that not only
did not work (only ``XX`` values for every register), but when I ran again
``i2cdetect`` the device disappeared !

So, I read the documentation thoroughly and found out that the 
SL030 is not a register-based i2c device, but it is using a
command scheme :

    write:
    [ADDRESS|REGISTER|LENGTH|COMMAND|DATA]
    
    read:
    [ADDRESS|REGISTER|LENGTH|COMMAND|STATUS|DATA]

So I made a little C code that reads a tag when one is present:

    // under WTFPL license

    #include <errno.h>
    #include <string.h>
    #include <stdio.h>
    #include <stdlib.h>
    #include <unistd.h>
    #include <linux/i2c-dev.h>
    #include <sys/ioctl.h>
    #include <sys/types.h>
    #include <sys/stat.h>
    #include <fcntl.h>
    #include <time.h>


    const char STATUS[][32] = {
        /*0x00*/ "Operation succeed",
        /*0x01*/ "No tag",
        /*0x02*/ "Login succeed",
        /*0x03*/ "Login fail",
        /*0x04*/ "Read fail",
        /*0x05*/ "Write fail",
        /*0x06*/ "Unable to read after write",
        /*0x08*/ "Address overflow",
        /*0x09*/ "Download Key fail",
        /*0x0A*/ "Collision occur",
        /*0x0C*/ "Load key fail",
        /*0x0D*/ "Not authenticate",
        /*0x0E*/ "Not a value block"
    };

    int main(void) {
        int file;
        char filename[40];
        const char *buffer;
        int addr = 0x50; // Addr of SL030

        sprintf(filename,"/dev/i2c-3");
        if ((file = open(filename,O_RDWR)) < 0) {
            printf("Failed to open the bus.");
            exit(1);
        }

        if (ioctl(file,I2C_SLAVE,addr) < 0) {
            printf("Failed to acquire bus access and/or talk to slave.\n");
            exit(1);
        }
        char buf[128] = {0};
        for (int i=0;i<128;++i) buf[i] = 0;

        // ------------ WRITE COMMAND ------------------
        unsigned char reg = 0x01; // Device register to access
        buf[0] = 1;
        buf[1] = reg;

        if (write(file,buf,2) != 2) {
            // ERROR HANDLING: i2c transaction failed
            printf("Failed to write to the i2c bus.\n");
            buffer = strerror(errno);
            printf(buffer);
            printf("\n\n");
        } else {
            printf("write success\n\n");
        }

        for (int i=0;i<128;++i) buf[i] = 0;

        struct timespec tim, tim2;
        tim.tv_sec = 0;
        tim.tv_nsec = 20000000;
        nanosleep(&tim,&tim2);

        // ------------ READ CARD STATUS ------------------
        unsigned short len=0;
        unsigned short cmd=0;
        unsigned short sta=0;
        // Using I2C Read
        if (read(file,buf,128) <= 0) {
            // ERROR HANDLING: i2c transaction failed
            printf("Failed to read from the i2c bus.\n");
            buffer = strerror(errno);
            printf(buffer);
            printf("\n\n");
            return 1;
        }
        len = (unsigned short)buf[0];
        cmd = (unsigned short)buf[1];
        sta = (unsigned short)buf[2];

        printf("Length:  %d\n",len);
        printf("Command: 0x%02X\n",cmd);
        printf("Status:  %s\n",STATUS[sta]);
        printf("Data: ");
        for (int i=3;i<len;++i)
            printf("%02X;", buf[i]);

        printf("\n\n");

        return 0;
    }

use it, share it, improve it ! 

this code is actually based on [this one](http://elinux.org/Interfacing_with_I2C_Devices#Completed_Code).

this code can be downloaded as a [gist as well](https://gist.github.com/guyzmo/10118958)
