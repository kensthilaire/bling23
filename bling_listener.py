#
# This is a NetworkTables client (eg, the DriverStation/coprocessor side).
# You need to tell it the IP address of the NetworkTables server (the
# robot or simulator).
#
# This shows how to use a listener to listen for all changes in NetworkTables
# values, which prints out all changes. Note that the keys are full paths, and
# not just individual key values.
#

import sys
import time
from networktables import NetworkTables

import bling


# To see messages from networktables, you must setup logging
import logging
logging.basicConfig(level=logging.DEBUG)

#
bling_server = bling.Bling(num_leds=36)

# initialize the network tables and connect to the specified server
NetworkTables.initialize(server='192.168.1.13')

def valueChanged(table, key, value, isNew):
    bling_server.process_cmd(value)
    
    #print("valueChanged: key: '%s'; value: %s; isNew: %s" % (key, value, isNew))
    #print 'Command Received: %s' % value
    #tokens=value.split(',')
    #for token in tokens:
    #    key,token_value=token.split('=')
    #    print 'name=%s value=%s' % (key,token_value)

def connectionListener(connected, info):
    print(info, '; Connected=%s' % connected)

NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)

bling_table = NetworkTables.getTable('Bling')
bling_table.addTableListener(valueChanged)

while True:
    time.sleep(1)

