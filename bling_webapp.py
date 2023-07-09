# requests received from the a web client. This module
# instantiates the Bling instance, configures it based on a set of command
# arguments, and sets up the web application.
#

import os
import sys
import time
import web
import json
from networktables import NetworkTables
from optparse import OptionParser
from threading import Thread, Event

import bling
import bling_patterns
import bling_colors

speed_opts = [ 'SLOW', 'MEDIUM', 'FAST' ]

current_pattern = 'RainbowHalves'
current_color = 'RAINBOW'
current_speed = speed_opts[1]

urls = (
    '/', 'Index',

    '/stop',        'Stop',
    '/pattern',     'Pattern',
    '/colors',      'Colors',
    '/patterns',    'Patterns',
    '/speeds',      'Speeds'
)

class Index:
    def GET(self):
        return render_page( 'main' )

class Pattern:
    def GET(self):
        bling_pattern = { 'pattern':current_pattern, 'color':current_color, 'speed':current_speed }
        return json.dumps( bling_pattern )
    def POST(self):
        params = web.input()
        set_bling_pattern( pattern=params.pattern, color=params.color, speed=params.speed )

class Stop:
    def POST(self):
        bling.stop_animation()

class Patterns:
    def GET(self):
        pattern_dict = bling_patterns.BlingPatterns(bling.get_bling_server()).patterns
        return json.dumps( list(pattern_dict.keys()) )

class Colors:
    def GET(self):
        color_dict = bling_colors.color_map
        return json.dumps( list(color_dict.keys()) )

class Speeds:
    def GET(self):
        return json.dumps( speed_opts )


# simple HTML page render function that will read the page specified by the 
# file prefix
def render_page( html_file_prefix ):
    filename = './html/%s.html' % html_file_prefix
    fd = open( filename, 'r' )
    file_content = fd.read()

    return file_content

def set_bling_pattern( pattern=None, color=None, speed=None ):
    global current_pattern
    global current_color
    global current_speed
    
    if pattern is None:
        pattern = current_pattern
    else:
        current_pattern = pattern

    if color is None:
        color = current_color
    else:
        current_color = color

    if speed is None:
        speed = current_speed
    else:
        current_speed = speed

    bling.process_cmd('Pattern=%s,Color=%s,Speed=%s' % (pattern,color,speed))

#
# define the network table connection and bling table value listener
#
def network_table_connection_listener(connected, info):
    print(info, '; Connected=%s' % connected)

def network_table_value_listener(table, key, value, isNew):

    # mark that we have received a command from the network tables
    if network_table_cmd_check is not None:
        network_table_cmd_check.cmd_received()

    bling.process_cmd(value)

class NetworkTableCmdRcvdCheck(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stop_flag = event
        self.cmd_received = False
        self.is_finished = False

    def run(self):
        counter = 0
        while not self.stop_flag.wait(1.0) and self.is_finished is False:
            counter += 1
            if counter == 30 and self.cmd_received is False:
                # timeout waiting to receive an initial command through
                # the network tables
                print( 'Timeout waiting for Network Table commands...' )
                self.is_finished = True
                set_bling_pattern( pattern='BLINKING', color='RED', speed='FAST' )
                
                print( 'Delaying a bit to allow things to settle' )
                time.sleep(2)
                os.system('sudo shutdown -r now')
                
    def cmd_received(self):
        # cancel the timer and mark the command as being received
        self.is_finished = True
        self.cmd_received = True

    def cancel(self):
        print( 'Canceling network table cmd check...' )
        self.is_finished = True

network_table_cmd_check = None

if __name__ == "__main__":

    # set up the logging service
    import logging
    logging.basicConfig(level=logging.DEBUG)

    # command line options handling
    parser = OptionParser()

    parser.add_option(
        "-i","--ipaddress",dest="ipaddress", default='10.10.73.2', 
        help='IP Address of the network tables server')
    parser.add_option(
        "-l","--leds",dest="leds", default='48', 
        help='Total number of LEDs in the strip')
    parser.add_option(
        "-s","--segments",dest="segments", default=None, 
        help='Number of LED segments in the strip')
    parser.add_option(
        "-b","--brightness",dest="brightness", default='255', 
        help='Overall brightness of the LEDs from 0-255, with 255 being the brightest')
    parser.add_option(
        "-n","--ntcheck",dest="ntcheck", action="store_true", default=False, 
        help='Enable the Network Table command check')

    # Parse the command line arguments
    (options,args) = parser.parse_args()

    # Strip off the command line arguments
    sys.argv[1:] = args

    # create the bling server object, specifying the number of LEDs in the strip
    # for now, we will assume that we have a left and a right segment, with half
    # the LEDs on the left and half on the right. we can change this if we come up
    # with more segments (e.g. front/back/left/right)
    if options.segments is not None:
        num_segments = int(options.segments)
    else:
        num_segments = None

    try:
        bling.create_bling_server(int(options.leds), num_segments, int(options.brightness))
    except ValueError:
        sys.exit('ERROR: Invalid Brightness Level: %s, must be 0-255' % options.brightness)

    # start things off with a base pattern to indicate that the bling application is
    # running
    set_bling_pattern()

    # initialize the network tables and connect to the specified server
    NetworkTables.initialize(server=options.ipaddress)
    NetworkTables.addConnectionListener(network_table_connection_listener, immediateNotify=True)

    # and create the bling table instance and install the table listener
    bling_table = NetworkTables.getTable('Bling')
    bling_table.addTableListener(network_table_value_listener)

    # start the thread which will check for commands being received from the network tables
    if options.ntcheck:
        network_table_event = Event()
        network_table_cmd_check = NetworkTableCmdRcvdCheck(network_table_event)
        network_table_cmd_check.start()

    # and launch the web server
    app = web.application(urls, globals())
    app.run()

    bling.stop_animation()

    if network_table_cmd_check is not None:
        network_table_cmd_check.cancel()
        network_table_cmd_check.join()

