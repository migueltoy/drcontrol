# Introduction #

Instructions how to install the needed libraries and test DRControl utility to control Denkovi USB Relay board.

# Tested on #

  * [Raspberry Pi with Raspbian 3.2.27+](http://www.raspberrypi.org/downloads)
  * Ubuntu 12.04 Desktop via VMWare (on Mac OSX)
  * [Denkovi 4 USB Relay Board](http://denkovi.com/product/44/usb-four-4-relay-output-module-board-for-home-automation.html)

# Python Libraries #

There are two libraries that are needed to interface the relay board.

  * Python-FTDI
  * PyLibFTDI, version 0.11 and later

## Library install ##

Install Python-FTDI library, and Python-pip package is needed to install the pyLibFTDI

```
# sudo apt-get install python-ftdi python-pip
```

Install the FTDI wrapper PyLibFTDI usinf PIP.

```
# sudo pip install pylibftdi
```

## Library Test ##

If you have the relay board connected, then you can run a quick test by entering following command. Note, when you run this after installation and under normal user you might get a error instead of printout.

```
# python -m pylibftdi.examples.list_devices
```

Example printout

```
pi@raspberrypi:~# python -m pylibftdi.examples.list_devices
FTDI:FT245R USB FIFO:A6VV5PHY
pi@raspberrypi:~# 
```

Note that this command will list all FTDI devices, so if you have more of them, then it will be listed as well.

## Errors ##

Do you only get following printout when you list the devices;

```
pi@raspberrypi /opt/drcontrol $ python -m pylibftdi.examples.list_devices
::
pi@raspberrypi /opt/drcontrol $
```

Or if you get Python exception like;

```
pi@raspberrypi ~ $ python -m pylibftdi.examples.list_devices
Traceback (most recent call last):
  File "/usr/lib/python2.7/runpy.py", line 162, in _run_module_as_main
    "__main__", fname, loader, pkg_name)
  File "/usr/lib/python2.7/runpy.py", line 72, in _run_code
    exec code in run_globals
  File "/usr/local/lib/python2.7/dist-packages/pylibftdi/examples/list_devices.py", line 42, in <module>
    for device in get_ftdi_device_list():
  File "/usr/local/lib/python2.7/dist-packages/pylibftdi/examples/list_devices.py", line 33, in get_ftdi_device_list
    for device in Driver().list_devices():
  File "/usr/local/lib/python2.7/dist-packages/pylibftdi/driver.py", line 158, in list_devices
    raise FtdiError(self.fdll.ftdi_get_error_string(byref(ctx)))
pylibftdi._base.FtdiError: error sending control message: Operation not permitted
pi@raspberrypi ~ $
```

You can try to run with sudo, and if that works, then you know it is a permission thing.

```
pi@raspberrypi ~ $ sudo python -m pylibftdi.examples.list_devices
FTDI:FT245R USB FIFO:A6VV5PHY
pi@raspberrypi ~ $
```

Then the normal user (if you are not as root) does not have access to the device, to give access to the device you need to add UDEV rules. Ben Bass has a great instructions regarding this here: [https://pylibftdi.readthedocs.org/en/latest/installation.html](https://pylibftdi.readthedocs.org/en/latest/installation.html)

Here is in short what needs to be done. Note, that I have changed the MODE to 0666, this gives write permission to everyone, this is needed if the script is to be executed via PHP/Apache. At Ben Bass page this is 0660.

```
pi@raspberrypi ~ $ sudo nano /etc/udev/rules.d/99-libftdi.rules
```

Add following line to the file and save.

```
SUBSYSTEMS=="usb", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6001", GROUP="dialout", MODE="0666"
```

Check that the file is OK

```
pi@raspberrypi ~ $ cat /etc/udev/rules.d/99-libftdi.rules
SUBSYSTEMS=="usb", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6001", GROUP="dialout", MODE="0666"
pi@raspberrypi ~ $
```

Do a reboot.

# DRControl install #

The DRControl does not need that much installation, as it is only one python file that can be executed from user chosen directory. It can be downloaded from download page here, or then fetched directly from the SVN repository.

Download from download page

```
# mkdir drcontrol
# cd drcontrol
# wget http://drcontrol.googlecode.com/files/drcontrol.0.12c.zip
# unzip drcontrol.0.12c.zip
```

Example of printing out relay device, and status on all relays

```
pi@raspberrypi ~/drcontrol $ ./drcontrol.py -l
Vendor		Product			Serial
FTDI		FT245R USB FIFO		A6VV5PHY
pi@raspberrypi ~/drcontrol $ ./drcontrol.py -d A6VV5PHY -c state -r all -v
DRControl 0.12
Device:		A6VV5PHY
Send command:	Relay all (0xFF) to STATE
Relay 1 state:	OFF (0)
Relay 2 state:	OFF (0)
Relay 3 state:	OFF (0)
Relay 4 state:	OFF (0)
Relay 5 state:	OFF (0)
Relay 6 state:	OFF (0)
Relay 7 state:	OFF (0)
pi@raspberrypi ~/drcontrol $
```

Or from the SVN directly (Note, that this version might not be fully tested or working)

```
# wget http://drcontrol.googlecode.com/svn/trunk/drcontrol.py
```