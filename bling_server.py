#
# This module contains the overall bling service that accepts command
# requests received from the FRC robot via the NetworkTables. This module
# instantiates the Bling instance, configures it based on a set of command
# arguments, and sets up the NetworkTables client.
#

import sys
import time
from networktables import NetworkTables
from optparse import OptionParser

import bling


# To see messages from networktables, you must setup logging
import logging
logging.basicConfig(level=logging.DEBUG)

# command line options handling
parser = OptionParser()

parser.add_option(
    "-i","--ipaddress",dest="ipaddress", default='10.10.73.2', 
    help='IP Address of the network tables server')
parser.add_option(
    "-l","--num_leds",dest="num_leds", default='48', 
    help='Total number of LEDs in the strip')
parser.add_option(
    "-s","--num_segments",dest="num_segments", default=None, 
    help='Number of LED segments in the strip')

# Parse the command line arguments
(options,args) = parser.parse_args()

# create the bling server object, specifying the number of LEDs in the strip
# for now, we will assume that we have a left and a right segment, with half
# the LEDs on the left and half on the right. we can change this if we come up
# with more segments (e.g. front/back/left/right)
if options.num_segments is not None:
    num_segments = int(options.num_segments)
else:
    num_segments = None

bling_server = bling.Bling(int(options.num_leds), num_segments)

# initialize the network tables and connect to the specified server
NetworkTables.initialize(server=options.ipaddress)

# define some helper and callback functions 
def valueChanged(table, key, value, isNew):
    bling_server.process_cmd(value)
    
def connectionListener(connected, info):
    print(info, '; Connected=%s' % connected)

NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)

bling_table = NetworkTables.getTable('Bling')
bling_table.addTableListener(valueChanged)

# start things off with a base pattern to indicate that the bling application is
# running
bling_server.process_cmd('Pattern=ColorWipe,Color=YELLOW,Speed=MEDIUM')

done = False
while not done:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        bling_server.stop_animation()
        done = True


