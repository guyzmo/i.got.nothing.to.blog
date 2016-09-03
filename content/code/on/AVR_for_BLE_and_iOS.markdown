---
type: post
categories: code
tags: [ avr, arduino, hack, ble, bluetooth ]
title: "AVR for BLE and iOS"
date: 2014-04-06T17:44:58+02:00
summary: "For a project, I've been assigned the task to access the ANCS from an AVR using Nordic's nRF8001. Even though it's mostly integration work of Apple's specifications and Nordic's ones, it end up being way harder to build than expected, and couldn't have been done without the help of the Nordic's support team."
lang: english
logo: "/img/bluetooth.jpg"
header_background: /img/nrf8001.png
aliases:
 - /code/on/avr-for-ble-and-ios/
---

For a project I've been assigned the task to access the ANCS from an AVR using Nordic's nRF8001.
Even though it's mostly integration work of Apple's specifications and Nordic's ones, it end up
being way harder to build than expected, and couldn't have been done without the help of the 
Nordic's support team.

First tests
-----------

The first tests were quite easy and gave the false feeling that using BLE is straightforward. But
when digging into Apple's specification and home made stuff, the path has many pitfalls.

So everything started when I bought the [Red Bear Lab Shield][1] to explore the BLE protocol. I
downloaded a few test applications on the iPhone to find out how things work. First tests were
impressive, basically compile, flash, plug and play!

Then, on the iOS side (or MacOS), you can use the really nice [Light Blue][2] application, that is
simple but enables to show how BLE work: you can navigate through your device's services, access
the characteristics and read from or send data to the characteristics. That App is definitely a
must have to discover the BLE protocol. On the FLOSS side, you have the gatt-tool that achieves
the same, on the command line.

So now, what I want is to get the phone's notifications and be able to use them. And that's where
the real fun starts. For those who missed it, I'm being ironic.

RTFM
----

The starting point for all that has been the WWDC videos that talk about Core Bluetooth and the
new BLE and Bluetooth 4 features. How can a device wake up an application, how can it subscribe
to the notifications sent by the ANCS, and what the ANCS actually is.

Then it leads to the Core Bluetooth specification pages, and more exactly to the [ANCS specification page][3]

There we learn many useful things, the services' values, how to handle exchanges between
the device and the phone, how shall we deal with datagram fragmentation... That's so cool.

So after looking at [nordic's documentation][4], we learn that we need to setup "*Pipes*"
that matches the "*Characteristics*" we then need to broadcast along with the "*Services*".
But the good thing is that all can be done using a tool called "*nRFGo Studio*".

Since my work on the topic, a really interesting resource has been published by [Adafruit][9] that gets
into details on how BLE actually works... What are the GAP, GATT things, what are characteristics, what
are services... So I won't cover that in this post.

Getting hands dirty
-------------------

So let's download and try "*nRFGo Studio*". It obvious that's a Qt application, but they
did not port it [because there are platform specific stuff][5] that are not needed for
the nRF8001. But the good news, though, is that it works perfectly well with wine, either
on Linux and MacOSX! So no need to bring your pirate windows VM up.

Then you need to go in the `nRF8001 Setup` menu, and select `Edit 128 bits UUID`. There
you can click on `Add new`, get to the bottom of the list and change the name `Custom base XX`
and change the base UUID using the values given on Apple's website:

![Base UUIDs](/img/nrfgo-studio-uuid.png)

Then you need to create a new service, by clicking on `New Service`:

Choosing the `ANCS` name, and using the `ANCS` base we created. Then we need to create
the characteristics for ANCS: Control Point, Data Source and Notification Source. And
don't forget to complete the missing UUID part.

There, we need to click on `New characteristic template`, add the name, use the matching
base and the missing UUID part:

 * Notification Source
  * `9FBF` *120d* `6301` `42D9` `8C58` `25E699A21DBD`
  * Properties: **Notify**
 * Data Source
  * `22EA` *C6E9* `24D6` `4BB5` `BE44` `B36ACE7C7BFB`
  * Propertiens: **Notify**
 * Control Point
  * `69D1` *D8F3* `45E1` `49A8` `9821` `9BBDFDAAD9D9`
  * Properties: **Write**

And then once the characteristics templates are done, you drag them and drop them over
the `Mandatory` view. And you're ok to validate the newly created service. Finally, you
need to add the service to your nrf8001 profile, by drag'n droping the `ANCS` from `service
templates` over the `Remote` column of the `GATT Services` Area.

Then, you can save your profile into your project's directory, and generate the `services.h`
file using `nRF8001 Setup` menu, select `Generate Source File` and `Generate only services.h`.
The other option, `Generate services.h and services.c` is only adding boilerplate we don't
really need as they are already defined by nrf framework (or RedBearLab's if you're using theirs) ;
so in the end, it will only take more memory for no real use.

Let's hack!
-----------

At the time I started hacking on this (it was last september), all the frameworks were
not stable enough, and lacking most of the features I needed. So I decided to start upon
the most complete code around, that has been published by a Nordic Engineer on the Bluetooth
forum on a link that is now dead, as follow up of a very [interesting Webinar that has been recorded][7].

For reference, here is a part of that [web page][6], and here's [the library][7] as it has 
been posted on the original page.

My first try has been with a random example to see it working ― I think
it was the `ble_my_project_template` one, though it does not really matter, and add to 
that example the ANCS services from the `services.h` and tried to open them by adding
some testing within the `ACI_EVT_PIPE_STATUS`:

            case ACI_EVT_PIPE_STATUS:
                // ...
                // Detection of ANCS pipes
                if (lib_aci_is_discovery_finished(&aci_state)) {
                    Serial.println(F(" Service Discovery is over."));
                    // Test ANCS Pipes availability
                    if (!lib_aci_is_pipe_closed(&aci_state, PIPE_ANCS_NOTIFICATION_SOURCE_RX)) {
                        Serial.println(F("  -> ANCS Notification Source not available"));
                    } else {
                        Serial.println(F("  -> ANCS Notification Source available!"));
                        if (!lib_aci_open_remote_pipe(&aci_state, PIPE_ANCS_NOTIFICATION_SOURCE_RX)) {
                            Serial.println(F("  -> ANCS Notification Source Pipe: Failure opening!"));
                        } else {
                            Serial.println(F("  -> ANCS Notification Source Pipe: Success opening!"));
                        }
                    }
                } else {
                    Serial.println(F(" Service Discovery is still going on."));
                }
                // ...

But that has been a huge FAIL! I'm only getting `ANCS Notification Source not available`, 
and I did not understand why. So I posted a message on [Nordic's public forum][10], and Nordic's
support forum. And there, Nordic's engineer really helped me understand THAT thing that is not
in documentations elsewhere that otherwise won't make the ANCS services available.

The undocumented
----------------

In order to get the ANCS services to show up, you need to *force* a bonding between
your nrf8001 device and your iPhone. Only then, the ANCS services will show up. That's
not in the WWDC conferences, that's not in the documentation... So much fun.

So we need to bring the `nRFStudio` up again, and modify the device's profile, by
switching to the `Security` tab, and set up:

 * `Device security`: `Security required`
 * `Required level of security`: `Authenticated (Passkey)`
 * `I/O capabilities`: `Display only`

Then you in your code you need to add:

            case ACI_EVT_DISPLAY_PASSKEY:
                Serial.println(F("Evt Display Passkey: [ "));
                for (uint8_t i=0; i<6; ++i) {
                    Serial.print((char)aci_evt->params.display_passkey.passkey[i]);
                    Serial.print(F(" "));
                }
                Serial.println(" ]");

                break;

Though, one of the good advices I've been given was to start from the `proximity` example
of the library, to add bonding and key handling.

The lookup for ANCS services shall only be done when the local services are up and when
the bonding is a success, so, here's the new code for the pipe status event:

            case ACI_EVT_PIPE_STATUS:
                if ((ACI_BOND_STATUS_SUCCESS == aci_state.bonded) && 
                        (lib_aci_is_pipe_available(&aci_state, PIPE_BATTERY_BATTERY_LEVEL_TX)))
                {
                    // Detection of ANCS pipes
                    if (lib_aci_is_discovery_finished(&aci_state)) {
                        Serial.println(F(" Service Discovery is over."));
                        // Test ANCS Pipes availability
                        if (!lib_aci_is_pipe_closed(&aci_state, PIPE_ANCS_CONTROL_POINT_TX_ACK))
                            Serial.println(F("  -> ANCS Control Point not available."));
                        else {
                            Serial.println(F("  -> ANCS Control Point available!"));
                            if (!lib_aci_open_remote_pipe(&aci_state, PIPE_ANCS_CONTROL_POINT_TX_ACK))
                                Serial.println(F("  -> ANCS Control Point Pipe: Failure opening!"));
                            else
                                Serial.println(F("  -> ANCS Control Point Pipe: Success opening!"));
                        }
                        if (!lib_aci_is_pipe_closed(&aci_state, PIPE_ANCS_DATA_SOURCE_RX))
                            Serial.println(F("  -> ANCS Data Source not available."));
                        else {
                            Serial.println(F("  -> ANCS Data Source available!"));
                            if (!lib_aci_open_remote_pipe(&aci_state, PIPE_ANCS_DATA_SOURCE_RX))
                                Serial.println(F("  -> ANCS Data Source Pipe: Failure opening!"));
                            else {
                                Serial.println(F("  -> ANCS Data Source Pipe: Success opening!"));
                            }
                        }
                        if (!lib_aci_is_pipe_closed(&aci_state, PIPE_ANCS_NOTIFICATION_SOURCE_RX)) {
                            Serial.println(F("  -> ANCS Notification Source not available."));
                        } else {
                            Serial.println(F("  -> ANCS Notification Source available!"));
                            if (!lib_aci_open_remote_pipe(&aci_state, PIPE_ANCS_NOTIFICATION_SOURCE_RX)) {
                                Serial.println(F("  -> ANCS Notification Source Pipe: Failure opening!"));
                            } else {
                                Serial.println(F("  -> ANCS Notification Source Pipe: Success opening!"));
                            }
                        }
                    } else {
                        Serial.println(F(" Service Discovery is still going on."));
                    }
                }
                break;

And now, it's working...

...well at least it should...

...only if you turn the bluetooth off and on again on the iPhone. Come on...

that's what the Nordic engineers tell:

> *After bonding is successful the ANCS pipes will still NOT be seen.
> 
> Disconnect
> 
> Wait for a few mins
> 
> Re-connect to the iPhone, make sure that some apps are using the ANCS.*

Get it to work. For real. Every times
-------------------------------------

So, here come my little "hack", to make it work:

            case ACI_EVT_TIMING:
                Serail.println(F("Evt link connection interval changed"));
                //Disconnect as soon as we are bonded and required pipes are available
                //This is used to store the bonding info on disconnect and
                //then re-connect to verify the bond
                if((ACI_BOND_STATUS_SUCCESS == aci_state.bonded) &&
                        (true == bonded_first_time) &&
                        (GAP_PPCP_MAX_CONN_INT >= aci_state.connection_interval) && 
                        //Timing change already done: Provide time for the the peer to finish
                        (GAP_PPCP_MIN_CONN_INT <= aci_state.connection_interval) &&
                        (lib_aci_is_pipe_available(&aci_state, PIPE_BATTERY_BATTERY_LEVEL_TX))) {
                    lib_aci_disconnect(&aci_state, ACI_REASON_TERMINATE);
                }
                break;

basically, it comes at the timing negociation state of the communication with the radio.
Instead of forcing a disconnect from the phone, we force a reset on the radio from the
firmware.

The full ANCS library
---------------------

I'm not getting in much further length about how to implement the communication with
the ANCS, because Apple's specifications are pretty well made on that part and there's
no need to get much further.

Basically, the library's algorithm is building a full notification object by merging
successive datagrams, as BLE has a limit to up to 20 byte per datagram. It gets data
from the Notification Source, as well as from the Data Source for more details.

You have to write two hook functions:

    void ancs_notifications_use_hook(ancs_notification_t* notif);
    void ancs_notifications_remove_hook(ancs_notification_t* notif);

the first being triggered just when the notification has been added and fully
retrieved and the second one when a notification gets deleted (by iOS). Those
functions is where you need to plug your actions on new and delete of notifications.

You'll find the full library over:

[`https://github.com/guyzmo/avr_nrf_ancs_library`][11]

Final words
-----------

This has been an unexpectidely challenging project, to make the nrf8001 radio to
communicate properly with iOS' ANCS. It would have helped a lot if Apple had used
headers in front of each notification packet sent through the `source` services to
make the merging algorithm smaller and easier to write.

On Nordic's side, I do not understand the reason why the `ACI` protocol, which is just
a special case of `SPI` with a handshake instead of a single pin select uses a `SPI` setup
totally different from other `SPI` devices, forcing the reconfiguration of the `SPI` if we
want to share the `SPI` bus with other devices.

`</rant>`

I finally would love to thank a lot Nordic's support team, particularly *Runar* and *David*
who have been really patient and helped me get through most of those problems with clever
advices and ideas.

Post Scriptum
-------------

The Support engineers asked me to make an update, the latest BLE library made by Nordic
is available now on github:

 * https://github.com/NordicSemiconductor/ble-sdk-arduino/releases

and other useful resources are on their devzone:

 * https://devzone.nordicsemi.com/arduino

Finally, on a [question on Stack Overflow][12] I've been told about an alternative way
to bring the ANCS up *without* bonding. In [that article][13], the author says (sic):
> '*You can either advertise a specific payload or require your devices to bond. This
> is required or your iOS device will not allow you to read and write the ANCS service
> characteristics. You can check Apple forums for information on the specific payload 
> you can use to bypass the bonding process.*

[1]:http://redbearlab.com/bleshield/
[2]:http://blog.punchthrough.com/post/46285311872/testing-bluetooth-low-energy-devices
[3]:https://developer.apple.com/library/ios/documentation/CoreBluetooth/Reference/AppleNotificationCenterServiceSpecification/Introduction/Introduction.html
[4]:http://www.nordicsemi.com/eng/nordic/download_resource/17534/14/69433804
[5]:https://devzone.nordicsemi.com/index.php/nrfgo-studio-port-to-macosx-and-linux#reply-1579
[6]:https://developer.bluetooth.org/DevelopmentResources/Documents/Answers%20for%20the%20Webinar%20at%20Bluetooth%20SIG.pdf
[7]:https://developer.bluetooth.org/DevelopmentResources/Pages/Webinars.aspx
[8]:https://developer.bluetooth.org/Community/SiteAssets/SitePages/Topic/Bluetooth_low_energy_for_Arduino_0_5_0_0_RC2.zip
[9]:https://learn.adafruit.com/introduction-to-bluetooth-low-energy/
[10]:https://devzone.nordicsemi.com/index.php/how-to-setup-a-pipe-to-access-ios7-s-ancs
[11]:https://github.com/guyzmo/avr_nrf_ancs_library
[12]:http://stackoverflow.com/questions/22873155/ble-shield-used-for-ancs-iphone/22892262?noredirect=1#comment35016186_22892262
[13]:http://mbientlab.com/blog/ancs-on-ti2541-in-an-afternoon/
