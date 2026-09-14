# F1 25 UDP Telemetry Setup --- MetaRacing Reference

## Purpose

Future reference for connecting **F1 25 live telemetry** to MetaRacing
or another telemetry/dashboard application.

## In-Game Telemetry Settings

Open:

**Options → Settings → Telemetry Settings**

  -----------------------------------------------------------------------
  Setting                             Reference
  ----------------------------------- -----------------------------------
  UDP Telemetry                       **On**

  UDP Broadcast Mode                  **Off**, unless general network
                                      broadcasting is required

  UDP IP Address                      `127.0.0.1` when the receiver is on
                                      the same PC; otherwise use the
                                      target device's local IP

  UDP Port                            `20777`

  UDP Send / Update Rate              `30Hz` or `60Hz`

  UDP Format                          Match the telemetry tool/game year,
                                      e.g. `2025`
  -----------------------------------------------------------------------

## Same-PC Setup

If F1 25 and MetaRacing's telemetry receiver run on the same computer:

``` text
UDP Telemetry       = ON
UDP Broadcast Mode  = OFF
UDP IP Address      = 127.0.0.1
UDP Port             = 20777
UDP Update Rate      = 30Hz or 60Hz
UDP Format           = 2025
```

`127.0.0.1` means the local computer itself.

## Telemetry Flow for MetaRacing

``` text
F1 25
  |
  | UDP Telemetry
  v
127.0.0.1 : 20777
  |
  v
Telemetry Receiver
  |
  v
MetaRacing Telemetry / Race Control
```

The receiver must listen on the same UDP port configured in F1 25.

## What External Tools Can Receive

The reference mentions external telemetry/dashboard applications such
as:

-   Sim Racing Telemetry
-   Victory

Telemetry can provide live information such as:

-   Lap times
-   Tire wear
-   ERS
-   Car status
-   Other racing telemetry

## Troubleshooting Checklist

If MetaRacing does not receive telemetry:

1.  Confirm **UDP Telemetry = On**.
2.  Confirm the UDP IP address.
3.  Confirm the UDP port is `20777`.
4.  Confirm the UDP format matches the expected F1 25 format.
5.  Try `30Hz` or `60Hz` update rate.
6.  Check Windows Firewall for blocked UDP traffic.
7.  Check whether another application is interfering with the UDP
    stream.

## Quick Reference

``` text
GAME:       F1 25
PROTOCOL:   UDP
PORT:       20777
LOCAL IP:   127.0.0.1
TELEMETRY:  ON
BROADCAST:  OFF
RATE:       30Hz / 60Hz
FORMAT:     2025
```

## Source Note

This document is based on the F1 25 telemetry setup information visible
in the screenshot provided on **14 September 2026**. It is intended as a
project memory/reference for future MetaRacing telemetry integration.
