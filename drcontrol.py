#!/usr/bin/python
# coding=UTF-8

# ----------------------------------------------------------------------------
#   
#   DRCONTROL.PY
#   
#   Copyright (C) 2012 Sebastian Sjoholm, sebastian.sjoholm@gmail.com
#   
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#   
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#   
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#   
#   Version history can be found at 
#   http://code.google.com/p/drcontrol/wiki/VersionHistory
#
#   $Rev$
#   $Date$
#
# ----------------------------------------------------------------------------

from optparse import OptionParser

from pylibftdi import Driver
from pylibftdi import BitBangDevice

import sys
import time

# ----------------------------------------------------------------------------
# VARIABLE CLASSS
# ----------------------------------------------------------------------------

class app_data:
    def __init__(
        self,
        name = "DRControl",
        version = "0.1",
        date = "$Date$",
        rev = "$Rev$",
        author = "Sebastian Sjoholm"
        ):

        self.name = name
        self.version = version
        self.build = date
        self.rev = rev
        self.author = author

class cmdarg_data:
    def __init__(
        self,
        device = "",
        relay = "",
        state = "",
        verbose = False
        ):

        self.device = device
        self.relay = relay
        self.state = state
        self.verbose = verbose

class relay_data(dict):

    address = {
            "1":"2",
            "2":"8",
            "3":"20",
            "4":"80",
            "5":"1",
            "6":"4",
            "7":"10",
            "8":"40"
            }

    def __getitem__(self, key): return self[key]
    def keys(self): return self.keys()

# ----------------------------------------------------------------------------
# LIST_DEVICES()
#
# Routine modified from the original pylibftdi example by Ben Bass
# ----------------------------------------------------------------------------

def list_devices():
    print "Vendor\t\tProduct\t\t\tSerial"
    dev_list = []
    for device in Driver().list_devices():
        device = map(lambda x: x.decode('latin1'), device)
        vendor, product, serial = device
        print "%s\t\t%s\t\t%s" % (vendor, product, serial)

# ----------------------------------------------------------------------------
# SET_RELAY()
#
# Set specified relay to chosen state
# ----------------------------------------------------------------------------

def set_relay():

    if cmdarg.verbose:
        print "Device: " + cmdarg.device
        print "Relay: " + cmdarg.relay + " (0x" + relay.address[cmdarg.relay] + ")"
        print "State: " + cmdarg.state

    try:
        with BitBangDevice(cmdarg.device) as bb:

            if cmdarg.verbose:
                print "Current state: " + bb.port

            if cmdarg.state == "on":
                bb.port |= int(relay.address[cmdarg.relay], 16)
            elif cmdarg.state == "off":
                bb.port &= ~int(relay.address[cmdarg.relay], 16)

            if cmdarg.verbose:
                print "Current state: " + bb.port

    except Exception:
        print "Error: Problem with device, or device not exists"
        sys.exit(1)

def check():

    # Check python version
    if sys.hexversion < 0x02060000:
        print "Error: Your Python need to be 2.6 or newer"
        sys.exit(1)

    # Check availability on library


if __name__ == '__main__':

    # Init objects    
    cmdarg = cmdarg_data()
    relay = relay_data()
    app = app_data()

    # Do system check
    check()

    parser = OptionParser()
    parser.add_option("-d", "--device", action="store", type="string", dest="device", help="The device serial, example A6VV5PHY")
    parser.add_option("-l", "--list", action="store_true", dest="list", default=False, help="List all devices")
    parser.add_option("-r", "--relay", action="store", type="string", dest="relay", help="Relay to command by number")
    parser.add_option("-s", "--state", action="store", type="string", dest="state", help="State: on or off")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="Verbose, print all info on screen")

    (options, args) = parser.parse_args()

    if options.verbose:
        cmdarg.verbose = options.verbose
        print app.name + " " + app.version

    if options.list:
        list_devices()
        sys.exit(0)

    if options.device:
        if not options.relay:
            print "Error: Need to state which relay"
            sys.exit(1)
        if not options.state:
            print "Error: Need to specify which relay state"
            sys.exit(1)

        cmdarg.device = options.device
        cmdarg.relay = options.relay
        cmdarg.state = options.state

        set_relay()
        sys.exit(0)





