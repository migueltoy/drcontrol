## DESCRIPTION ##

DRControl is Python script that controls the USB Relay board from Denkovi http://www.denkovi.com.

## REQUIREMENTS ##

  * Python 2.6+
  * Tested on Raspberry Pi with Python 2.6
  * Tested on Mac OSX 10.8.2 with Python 2.7.2
  * Tested on Ubuntu 12.04 Desktop (via VMWare)
  * Denkovi 4 USB Relay Board, product code DAE-CB/Ro4-USB

## NOTES ##

  * The DRControl will always show all 8 relays even if the connected board is an 4 USB Relay Board. There is no way at the current time to identify if the board is 4 or 8 USB Relay Board.

## DRCONTROL.PY ##

Options;

|-d|Device|
|:-|:-----|
|-r|Relay number|
|-s|Relay state|
|-l|List all available FTDI devices|
|-v|Verbose, print status and information on stdout|

### Device (-d) ###

---

```
option -d <device serial number>
```

Address the relay board with the serial number of the FTDI device, this can be listed with the "-l" (list) switch.

Example below is two devices listed, the "FT245R USB FIFO" is the relay board (4 x USB Board) which is then used the serial "A6VV5PHY" to show the state of the relay 1.

```
$ ./drcontrol.py -l
Vendor		Product			Serial
RFXCOM		RFXtrx433		03VHG0NE
FTDI		FT245R USB FIFO		A6VV5PHY
$ ./drcontrol.py -d A6VV5PHY -r 1 -c state
ON
$
```

### Relay (-r) ###

---

```
option -r <1..8|all>
```

Needed in to address which relay is going to be commanded.

"ALL" can be used to send the command to all relays. Command is not case sensitive.

Example;

```
$ ./drcontrol.py -d A6VV5PHY -r ALL -c state -v
DRControl 0.12
Device:		A6VV5PHY
Send command:	Relay all (0xFF) to STATE
Relay 1 state:	ON (2)
Relay 2 state:	ON (8)
Relay 3 state:	ON (32)
Relay 4 state:	ON (128)
Relay 5 state:	ON (4)
Relay 6 state:	ON (16)
Relay 7 state:	ON (64)
$
```

### Relay Command (-c) ###

---

```
option -c <on|off|state>
```

Options: on, off, state

ON = To set the relay ON

OFF = To set the relay OFF

STATE = To show the current state of the relay

Command is not case sensitive

Examples;

```
$ ./drcontrol.py -d A6VV5PHY -r 1 -c state
ON
$ ./drcontrol.py -d A6VV5PHY -r 1 -c off
$ ./drcontrol.py -d A6VV5PHY -r 1 -c state
OFF
$ ./drcontrol.py -d A6VV5PHY -r 1 -c on
$ ./drcontrol.py -d A6VV5PHY -r 1 -c state
ON
$
```

### List devices (-l) ###

---

```
option -l
```

List all FTDI devices on the system.

Example;

```
$ ./drcontrol.py -l
Vendor		Product			Serial
RFXCOM		RFXtrx433		03VHG0NE
FTDI		FT245R USB FIFO		A6VV5PHY
$
```

### Verbose (-v) ###

---

```
option -v
```

Give verbose printouts of all commands.

Example;

```
$ ./drcontrol.py -d A6VV5PHY -r 1 -c state -v
DRControl 0.11
Device:		A6VV5PHY
Send command:	Relay 1 (0x2) to STATE
Relay 1 state:	ON (2)
$ ./drcontrol.py -d A6VV5PHY -r 1 -c off -v
DRControl 0.11
Device:		A6VV5PHY
Send command:	Relay 1 (0x2) to OFF
Relay 1 to OFF
$ ./drcontrol.py -d A6VV5PHY -r 1 -c state -v
DRControl 0.11
Device:		A6VV5PHY
Send command:	Relay 1 (0x2) to STATE
Relay 1 state:	OFF (0)
$
```


---

## INFO ##

The USB 4 relay board is a product from [Denkovi Assembly Electronics ltd](http://denkovi.com/)


---

## COPYRIGHT ##

Copyright (C) 2012 Sebastian Sjoholm

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.