import sys
from bling import Bling
from optparse import OptionParser


# command line options handling
parser = OptionParser()

parser.add_option(
    "-l","--num_leds",dest="num_leds", default='48',
    help='Total number of LEDs in the strip')
parser.add_option(
    "-s","--num_segments",dest="num_segments", default=None,
    help='Number of LED segments in the strip')

# Parse the command line arguments
(options,args) = parser.parse_args()

if options.num_segments is not None:
    num_segments = int(options.num_segments)
else:
    num_segments = None

bling = Bling(int(options.num_leds), num_segments)

print bling.menu()

done = False
while not done:
    try:
        input = raw_input('Enter your selection: ')
        if input == '?':
            print bling.menu()
        elif input == '':
            bling.stop_animation()
        elif input.lower() == 'q':
            done = True
        else:
            try:
                result = bling.menu_select(int(input))
                print result
            except ValueError:
                print 'Invalid input choose a number: %s' % input

    except KeyboardInterrupt:
        done = True

print '\nDone!'
