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

from ctypes.util import find_library

import sys
import time
import serial
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())

# ----------------------------------------------------------------------------
# VARIABLE CLASSS
# ----------------------------------------------------------------------------

class app_data:
    def __init__(
        self,
        name = "DRControl",
        version = "0.12",
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
        command = "",
        type = "",
        verbose = False
        ):

        self.device = device
        self.relay = relay
        self.command = command
        self.type = type
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
            "8":"40",
            "all":"FF"
            }

    def __getitem__(self, key): return self[key]
    def keys(self): return self.keys()

# ----------------------------------------------------------------------------

def init_logger(loglevel):

	formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s')
	handler = logging.StreamHandler()
	handler.setFormatter(formatter)
	logger = logging.getLogger('DRControl')
	logger.setLevel(loglevel)
	logger.addHandler(handler)
			
	return logger
	
# ----------------------------------------------------------------------------
# testBit() returns a nonzero result, 2**offset, if the bit at 'offset' is one.
# http://wiki.python.org/moin/BitManipulation
# ----------------------------------------------------------------------------

def testBit(int_type, offset):
    mask = 1 << offset
    return(int_type & mask)

# ----------------------------------------------------------------------------

def get_relay_state( data, relay ):
    if relay == "1":
        return testBit(data, 1)
    if relay == "2":
        return testBit(data, 3)
    if relay == "3":
        return testBit(data, 5)
    if relay == "4":
        return testBit(data, 7)
    if relay == "5":
        return testBit(data, 2)
    if relay == "6":
        return testBit(data, 4)
    if relay == "7":
        return testBit(data, 6)
    if relay == "8":
        return testBit(data, 8)

# ----------------------------------------------------------------------------
#
# USB4/8 RELAY 
#
# These functions are only valid for relays that uses bitbanging interface
#
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
#
# USB16 RELAY 
#
# These functions are only valid for relays that uses serial terminal interface
#
# ----------------------------------------------------------------------------

def usb16_statetext(data, relay):

	if relay == 1:
		if testBit(int(data), 7):
			return "ON"
		else:
			return "OFF"
	elif relay == 2:
		if testBit(int(data), 6):
			return "ON"
		else:
			return "OFF"
	elif relay == 3:
		if testBit(int(data), 5):
			return "ON"
		else:
			return "OFF"
	elif relay == 4:
		if testBit(int(data), 4):
			return "ON"
		else:
			return "OFF"
	elif relay == 5:
		if testBit(int(data), 3):
			return "ON"
		else:
			return "OFF"
	elif relay == 6:
		if testBit(int(data), 2):
			return "ON"
		else:
			return "OFF"
	elif relay == 7:
		if testBit(int(data), 1):
			return "ON"
		else:
			return "OFF"
	elif relay == 8:
		if testBit(int(data), 0):
			return "ON"
		else:
			return "OFF"
	else:
		return "n/a"
		
def usb16_relay(device, relay, command):
	"""

	Set state on one or all relays
	
	Input:
		device = the serial device handler
		relay = relay number or all
		command = command on or off
	
	Output:
		none
		
	"""
	logger.debug("USB16_relay")
	logger.debug("Device: " + device)
	logger.debug("Relay: " + relay)
	logger.debug("Command: " + command)
	
	if relay == 'all':
		if command == 'on':
			command_string = 'on'
		else:
			command_string = 'off'
		
	elif int(relay) >= 1 or int(relay) <= 16:
		if len(relay) == 1:
			relay = "0" + relay
			logger.debug("Fixed leading zero to relay: " + relay)
			
		if command == "on":
			command_string = str(relay) + "+"
		else:
			command_string = str(relay) + "-"
	else:
		logger.error("Relay number out of range")
		sys.exit(1)

	# Open serial
	logger.debug("Open serial port")
	comport = open_serialport(device)
	
	command_string = command_string + "//\r\n"
	logger.debug("Command string: " + command_string.strip())
	
	comport.flushOutput()
	comport.flushInput()
	logger.debug("Write command to serial port")
	comport.write(command_string)
	time.sleep(0.5)
	
	logger.debug("Read serial port")
	logger.debug("Data waiting: " + str(comport.inWaiting()))
		
def usb16_state(device, relay):
	
	logger.debug("USB16_state")
	
	comport = open_serialport(device)
	comport.flushOutput()
	comport.flushInput()
	comport.write('ask//\r\n')
	time.sleep(1)
	
	data1 = 0
	data2 = 0
	
	if comport.inWaiting() == 2:
		data1 = ord(comport.read(1))
		data2 = ord(comport.read(1))
	else:
		print "Error: Not expected reply from serial port"
			
	close_serialport(comport)

	# Process data
	if relay == 'all':
		print "Relay states"
		print "Relay #1\t" + usb16_statetext(data1, 1)
		print "Relay #2\t" + usb16_statetext(data1, 2)
		print "Relay #3\t" + usb16_statetext(data1, 3)
		print "Relay #4\t" + usb16_statetext(data1, 4)
		print "Relay #5\t" + usb16_statetext(data1, 5)
		print "Relay #6\t" + usb16_statetext(data1, 6)
		print "Relay #7\t" + usb16_statetext(data1, 7)
		print "Relay #8\t" + usb16_statetext(data1, 8)
		print "Relay #9\t" + usb16_statetext(data2, 1)
		print "Relay #10\t" + usb16_statetext(data2, 2)
		print "Relay #11\t" + usb16_statetext(data2, 3)
		print "Relay #12\t" + usb16_statetext(data2, 4)
		print "Relay #13\t" + usb16_statetext(data2, 5)
		print "Relay #14\t" + usb16_statetext(data2, 6)
		print "Relay #15\t" + usb16_statetext(data2, 7)
		print "Relay #16\t" + usb16_statetext(data2, 8)
		
	elif int(relay) >= 1 and int(relay) <= 8:
		print "Relay #" + relay + "\t" + usb16_statetext(data1, int(relay))
		
	elif int(relay) >= 9 and int(relay) <= 16:
		print "Relay #" + relay + "\t" + usb16_statetext(data2, int(relay))
		
	else:
		print "Error: Invalid relay number"
		sys.exit(1)

# ----------------------------------------------------------------------------

def open_serialport(device):
	"""
	Open serial port for communication to the relay board.
	Only relay type: 16USB
	"""

	try:  
		comport = serial.Serial(device, 9600, timeout=5)
	except serial.SerialException, e:
		print "Error: Failed to connect on device " + device
		print "Error: " + str(e)
		sys.exit(1)

	if not comport.isOpen():
		comport.open()
		
	return comport

# ----------------------------------------------------------------------------

def close_serialport(device):
	"""
	Close serial port.
	"""

	try:
		device.close()
	except:
		print "Error: Failed to close the port " + device
		sys.exit(1)

# ----------------------------------------------------------------------------

def readbytes(number):
	"""
	Read x amount of bytes from serial port. 
	Credit: Boris Smus http://smus.com
	"""
	buf = ''
	for i in range(number):
		try:
			byte = serial_param.port.read()
		except IOError, e:
			print "Error: %s" % e
		buf += byte

	return buf

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
        print "Device:\t\t" + cmdarg.device
        print "Send command:\tRelay " + cmdarg.relay + " (0x" + relay.address[cmdarg.relay] + ") to " + cmdarg.command.upper()

    try:
        with BitBangDevice(cmdarg.device) as bb:
			
            # Action towards specific relay
            if cmdarg.relay.isdigit():
				
                if int(cmdarg.relay) >= 1 and int(cmdarg.relay) <= 8:

                    # Turn relay ON
                    if cmdarg.command == "on":
                        if cmdarg.verbose:
                            print "Relay " + str(cmdarg.relay) + " to ON"
                        bb.port |= int(relay.address[cmdarg.relay], 16)

                    # Turn relay OFF
                    elif cmdarg.command == "off":
                        if cmdarg.verbose:
                            print "Relay "  + str(cmdarg.relay) + " to OFF"
                        bb.port &= ~int(relay.address[cmdarg.relay], 16)

                    # Print relay status
                    elif cmdarg.command == "state":
                        state = get_relay_state( bb.port, cmdarg.relay )
                        if state == 0:
                            if cmdarg.verbose:
                                print "Relay " + cmdarg.relay + " state:\tOFF (" + str(state) + ")"
                            else:
                                print "OFF"
                        else:
                            if cmdarg.verbose:
                                print "Relay " + cmdarg.relay + " state:\tON (" + str(state) + ")"
                            else:
                                print "ON"

            # Action towards all relays
            elif cmdarg.relay == "all":

                if cmdarg.command == "on":
                    if cmdarg.verbose:
                        print "Relay " + str(cmdarg.relay) + " to ON"
                    bb.port |= int(relay.address[cmdarg.relay], 16)

                elif cmdarg.command == "off":
                    if cmdarg.verbose:
                        print "Relay "  + str(cmdarg.relay) + " to OFF"
                    bb.port &= ~int(relay.address[cmdarg.relay], 16)

                elif cmdarg.command == "state":
                    for i in range(1,8):
                        state = get_relay_state( bb.port, str(i) )
                        if state == 0:
                            if cmdarg.verbose:
                                print "Relay " + str(i) + " state:\tOFF (" + str(state) + ")"
                            else:
                                print "OFF"
                        else:
                            if cmdarg.verbose:
                                print "Relay " + str(i) + " state:\tON (" + str(state) + ")"
                            else:
                                print "ON"

                else:
                    print "Error: Unknown command"

            else:
                print "Error: Unknown relay number"
                sys.exit(1)

    except Exception, err:
        print "Error: " + str(err)
        sys.exit(1)

def check():

    # Check python version
    if sys.hexversion < 0x02060000:
        print "Error: Your Python need to be 2.6 or newer"
        sys.exit(1)

    # Check availability on library, this check is also done in pylibftdi
    ftdi_lib = find_library('ftdi')
    if ftdi_lib is None:
        print "Error: The pylibftdi library not found"
        sys.exit(1)

if __name__ == '__main__':

	# Init objects
	cmdarg = cmdarg_data()
	relay = relay_data()
	app = app_data()

	# Do system check
	check()

	parser = OptionParser()
	parser.add_option("-d", "--device", action="store", type="string", dest="device", help="The device serial, example A6VV5PHY")
	parser.add_option("-t", "--type", action="store", type="string", dest="type", help="Relay type: 4USB, 8USB, 16USB")
	parser.add_option("-l", "--list", action="store_true", dest="list", default=False, help="List all devices")
	parser.add_option("-r", "--relay", action="store", type="string", dest="relay", help="Relay to command by number: 1...16 or all")
	parser.add_option("-c", "--command", action="store", type="string", dest="command", help="State: on, off, state")
	parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="Verbose, print all info on screen")
	parser.add_option("-L", "--loglevel", action="store", type="string", dest="loglevel", help="Loglevel, ERROR, INFO or DEBUG")
	
	(options, args) = parser.parse_args()

	if options.verbose:
		cmdarg.verbose = options.verbose
		print app.name + " " + app.version
	else:
		cmdarg.verbose = False

	if options.loglevel:
		logger = init_logger(options.loglevel.upper())
	else:
		logger = init_logger('ERROR')
		logger.disabled = True

	if options.list:
		list_devices()
		sys.exit(0)

	if not options.device:
		print "Error: Device missing"
		sys.exit(1)
		
	if not options.command:
		print "Error: Command missing"
		sys.exit(1)
		
	if not options.type:
		print "Error: Relay type missing"
		sys.exit(1)
	elif options.type <> '4USB' and options.type <> '8USB' and options.type <> '16USB':
		print "Error: Invalid relay type"
		sys.exit(1)
	else:
		cmdarg.type = options.type

	if options.device:
		if not options.relay:
			print "Error: Need to state which relay"
			sys.exit(1)
		if not options.command:
			print "Error: Need to specify which relay state"
			sys.exit(1)

		cmdarg.device = options.device
		cmdarg.relay = options.relay.lower()
		cmdarg.command = options.command.lower()

		#set_relay()
	
	if cmdarg.verbose:
		print "Device:\t\t" + cmdarg.device
		print "Relay type:\t" + cmdarg.type
		print "Relay #:\t" + cmdarg.relay
		print "Command:\t" + cmdarg.command
	
	# GET STATE
	if cmdarg.command == "state":
		if cmdarg.type.lower() == "16usb":
			usb16_state(cmdarg.device, cmdarg.relay)
	
	# SET ON/OFF
	if cmdarg.command == "on" or cmdarg.command == "off":
		if cmdarg.type.lower() == "16usb":
			usb16_relay(cmdarg.device, cmdarg.relay, cmdarg.command)
	
	logger.debug("Exit 0")
	sys.exit(0)





