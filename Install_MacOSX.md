# Introduction #

Instructions how to install the needed libraries and test DRControl utility to control Denkovi USB Relay board.

# Tested on #

  * Mac OSX 10.8+
  * [Denkovi 4 USB Relay Board](http://denkovi.com/product/44/usb-four-4-relay-output-module-board-for-home-automation.html)

# Be aware #

  * It seems that only way to get the library to communicate with the device is to unload the FTDI kernel extension, it can cause issues if the user have other FTDI devices connected to the system that uses this extension.

# Python Libraries #

There are two libraries that are needed to interface the relay board.

  * Python-FTDI
  * PyLibFTDI

## Library install ##

To install the additional software I have used [MacPort](http://www.macports.org/), but I guess alternatives like [HomeBrew](http://mxcl.github.com/homebrew/) could be used as well.

Install libFTDI

```
# sudo port install libftdi
```

To install the pylibftdi with PIP, if you have PIP already installed you can skip first line.

```
# sudo easy_install pip
# sudo pip install pylibftdi
```

## Library Test ##

To test that the python software is properly installed following command should give you a printout.

```
# python -m pylibftdi.examples.list_devices
```

It should list all FTDI devices you have on the system.

Example;
```
$ python -m pylibftdi.examples.list_devices
RFXCOM:RFXtrx433:03VHG0NE
FTDI:FT245R USB FIFO:A6VV5PHY
```

## Errors ##

### Error: libftdi library not found ###

[MacPort](http://www.macports.org/) will install the library to the directory /opt/local/lib/ for some reason the Python will not look here for the library. Therefor the system variable DYLD\_LIBRARY\_PATH need to point to this library path for the scripts to work properly.

```
echo $DYLD_LIBRARY_PATH 
export DYLD_LIBRARY_PATH=/opt/local/lib/
```

### Error: device not found (-3) ###

If following error occur when the device is accessed

```
pylibftdi._base.FtdiError: device not found (-3)
```

It means that the only solution (what I know of) is to unload the FTDI kernel extension, by executing following command;

```
# sudo kextunload /System/Library/Extensions/FTDIUSBSerialDriver.kext
```

How to reload the FTDI kernel

```
# sudo kextload /System/Library/Extensions/FTDIUSBSerialDriver.kext
```

# DRControl install #

The DRControl does not need that much installation, as it is only one python file that can be executed from user chosen directory. It can be downloaded from download page here, or then fetched directly from the SVN repository.

Download from download page

```
# wget http://drcontrol.googlecode.com/files/drcontrol.0.1.zip
# unzip drcontrol.0.1.zip
```

Or from the SVN directly (Note, that this version might not ve fully tested or working)

```
# wget http://drcontrol.googlecode.com/svn/trunk/drcontrol.py
```