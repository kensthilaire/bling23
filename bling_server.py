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

if len(sys.argv) < 2:
    print 'Usage: python bling_listener.py <IP address> [number of LEDs]'
    exit(0)

ip = sys.argv[1]
try:
    num_leds = int(sys.argv[2])
except:
    num_leds = 36


# create the bling server object, specifying the number of LEDs in the strip
# for now, we will assume that we have a left and a right segment, with half
# the LEDs on the left and half on the right. we can change this if we come up
# with more segments (e.g. front/back/left/right)
bling_server = bling.Bling(num_leds)

# initialize the network tables and connect to the specified server
NetworkTables.initialize(server=ip)

def valueChanged(table, key, value, isNew):
    bling_server.process_cmd(value)
    
def connectionListener(connected, info):
    print(info, '; Connected=%s' % connected)

NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)

bling_table = NetworkTables.getTable('Bling')
bling_table.addTableListener(valueChanged)

done = False
while not done:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        bling_server.stop_animation()
        done = True


