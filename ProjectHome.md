# DRControl #

DRControl is a command utility written in Python and uses the pylibftdi. You can control the Denkovi 4 USB Relay board to set relay on or off.

The 4 USB relay board (DAE-CB/Ro4-USB) uses a FT245RL chipset that uses Synchronous Bit-Bang Mode protocol.

## Info ##

  * The pylibftdi version 0.11 or later is needed, otherwise the previous relay states does go to off when new state is issued.
  * The only relay board that has been tested is the 4 USB Relay board. Support for the 8 USB Board Relay is added, but not tested.

## News ##

4-JAN-2013

Release 0.12c, small bug fixed with the "ALL" option.

3-JAN-2013

Release 0.12, Fixes to 8 USB Board, and the "ALL" action now works for ON, OFF and STATE.
Update, version 0.12b replaces the version 0.12 with a important fix.

2-JAN-2013

Small fixes and 0.11 release available.

27-DEC-2012

Release 0.1 is now downloadable, still working on the documentation.

## Latest Release ##

[Version 0.12c (4-JAN-2013)](http://drcontrol.googlecode.com/files/drcontrol.0.12c.zip)
  * Version 0.12c fixes a bug with the "ALL" option

[Version 0.12b (3-JAN-2013)](http://drcontrol.googlecode.com/files/drcontrol.0.12b.zip)
  * Version 0.12b fixes a critical bug with checking the correct relay number
  * Fixes to 8 USB Relay Board
  * All relays can be adressed with "ALL" for ON, OFF and STATE

## Credits ##

  * Ben Bass (pylibftdi)

## Resources ##

  * USB relay boards from Denkovi [http://denkovi.com](http://denkovi.com)
  * Python-FTDI from [http://www.ohloh.net/p/python-ftdi](http://www.ohloh.net/p/python-ftdi)
  * pyLibFTDI wrapper for Python-FTDI [https://bitbucket.org/codedstructure/pylibftdi](https://bitbucket.org/codedstructure/pylibftdi)

## Other Projects ##

  * [RFXCMD](http://code.google.com/p/rfxcmd/), an command line utility to receive and send messages with RFXtrx433 transceiver.
  * [TempSensor](http://code.google.com/p/usb-sensors-linux/), an utility to read data from Lascar EL-USB-RT temperature/humidity USB sensor.