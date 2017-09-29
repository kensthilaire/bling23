# requests received from the a web client. This module
# instantiates the Bling instance, configures it based on a set of command
# arguments, and sets up the web application.
#

import sys
import time
import web
import json
from optparse import OptionParser

import bling
import bling_patterns
import bling_colors

speed_opts = [ 'SLOW', 'MEDIUM', 'FAST' ]

current_pattern = 'RainbowHalves'
current_color = 'RAINBOW'
current_speed = speed_opts[1]

urls = (
    '/', 'index',

    '/stop',        'stop',
    '/pattern',     'pattern',
    '/colors',      'colors',
    '/patterns',    'patterns',
    '/speeds',      'speeds'
)

class index:
    def GET(self):
        return render_page( 'main' )

class pattern:
    def GET(self):
        bling_pattern = { 'pattern':current_pattern, 'color':current_color, 'speed':current_speed }
        return json.dumps( bling_pattern )
    def POST(self):
        params = web.input()
        set_bling_pattern( pattern=params.pattern, color=params.color, speed=params.speed )

class stop:
    def POST(self):
        bling.stop_animation()

class patterns:
    def GET(self):
        pattern_dict = bling_patterns.BlingPatterns(bling.get_bling_server()).patterns
        return json.dumps( pattern_dict.keys() )

class colors:
    def GET(self):
        color_dict = bling_colors.color_map
        return json.dumps( color_dict.keys() )

class speeds:
    def GET(self):
        return json.dumps( speed_opts )


# simple HTML page render function that will read the page specified by the 
# file prefix
def render_page( html_file_prefix ):
    filename = './html/%s.html' % html_file_prefix
    try:
        fd = open( filename, 'r' )
        file_content = fd.read()
    except:
        file_content = None

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

    app = web.application(urls, globals())
    app.run()

    bling.stop_animation()

