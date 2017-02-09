
from bibliopixel.drivers.LPD8806 import *
from bibliopixel import LEDStrip

import bling_patterns

# TODO: Remove all these imports once we convert this module to use the bling patterns
# rather than the direct calls to the BiblioPixel animation objects
import bibliopixel.colors as colors
from bibliopixel.animation import StripChannelTest

from BiblioPixelAnimations.strip import Alternates
from BiblioPixelAnimations.strip import Rainbows
from BiblioPixelAnimations.strip import ColorChase
from BiblioPixelAnimations.strip import ColorFade
from BiblioPixelAnimations.strip import ColorPattern
from BiblioPixelAnimations.strip import ColorWipe
from BiblioPixelAnimations.strip import FireFlies
from BiblioPixelAnimations.strip import HalvesRainbow
from BiblioPixelAnimations.strip import LarsonScanners
from BiblioPixelAnimations.strip import LinearRainbow
from BiblioPixelAnimations.strip import PartyMode
from BiblioPixelAnimations.strip import PixelPingPong
from BiblioPixelAnimations.strip import Searchlights
from BiblioPixelAnimations.strip import Wave

class Bling(object):

    def __init__(self, num_leds):
        # set the total number of LEDs in the strip
        self.num_leds = num_leds
        
        # initialize the list of segments to include all, left and right
        # these segment settings can be overwritten dynamically if we want to define
        # additional segments, like all, left, right, front, back, etc...
        self.segments = { 'ALL':   ( 0, self.num_leds ),
                          'LEFT':  ( 0, int((self.num_leds/2)-1) ),
                          'RIGHT': ( int(self.num_leds/2), int(self.num_leds) ) }

        # initialize the driver with the type and count of LEDs that we are using
        # also, define the correct RGB channel order once you have run the test pattern
        # the other parameters are set based on the controlling application. We're using
        # the RaspberryPi as the controller with the SPI port
        self.driver = DriverLPD8806(num=self.num_leds, c_order = ChannelOrder.GRB, SPISpeed=2, use_py_spi=True, dev='/dev/spidev0.0')

        # we are using the LED strip configuration, other available configurations include an LED matrix,
        # but we have only a single strip at this time
        self.led = LEDStrip(self.driver)

        # the frames per second is used to control how fast the animation runs. some of the animations
        # work better when run at a low frames per second
        self.fps = None

        # the pattern variable contains the most recent bling pattern that has been assigned
        self.pattern = None
        
        # initialize the bling command parameters to provide reasonable default values for each
        # setting
        self.params = {}
        self.init_params()
        
        ###### TODO: remove these variables after converting the menu processing to use #####
        ######       the new patterns                                                   #####
        # animation object containing pattern to apply to the LEDs
        self.anim = None

        # flag to indicate whether the selected mode requires animation. Displaying a solid color across all or a range
        # of LEDs does not require animation
        self.animate = True

    def num_leds(self):
        return self.num_leds

    def stop_animation(self):
        if self.pattern is not None:
            self.pattern.stop()
        else:
            if self.anim is not None:
                self.anim.stopThread(wait=True)
            self.led.all_off()
            self.led.update()

    def get_leds_from_segment(self, segment_str):
        segment_leds = [0,-1]
        try:
            segment_def = self.segments[segment_str]
            segment_leds[0] = segment_def[0]
            segment_leds[1] = segment_def[1]
        except:
            # if the specified segment doesn't exist, return all LEDs
            pass
            segment_leds = [0,-1]
        return segment_leds

    def init_params(self):
        self.params['Pattern'] = 'Error'
        self.params['Segment'] = 'All'
        self.params['Color'] = 'Error'
        self.params['Speed'] = 'Medium'
        self.params['Min'] = '0'
        self.params['Max'] = '100'

    def apply_min_max_params(self, leds):
        # Re-calculate the minimum and maximum LED values by applying any
        # specified min/max percentage parameter setting
        min_param = int(self.params['Min'])
        max_param = int(self.params['Max'])
        if min_param > 100:
            print 'Invalid  Minimum Setting: %d, Must be 0-100' % min_param
            min_param = 0
        if max_param > 100:
            print 'Invalid  Maximum Setting: %d, Must be 0-100' % max_param
            max_param = 100
        led_range = leds[1]-leds[0]
        min_adjust=0
        max_adjust=0
        if min_param is not 0:
            min_adjust = int((float(led_range)*(min_param)/100)+1)
            #min_adjust = int(float((min_param/led_range)*100))
            leds[0] += min_adjust
        if max_param is not 100:
            max_adjust = int((float(led_range)*(100-max_param)/100)+1)
            leds[1] -= max_adjust
        print 'Min:%d, Max:%d, MinAdjust:%d, MaxAdjust:%d' % (min_param,max_param,min_adjust,max_adjust)
        print 'Adjusted Min:%d, Max:%d' % (leds[0],leds[1])
        return leds
    
    def process_cmd(self, cmd_str):
        result = 'OK'

        # start by starting any animation that is already running
        self.stop_animation()

        # re-initialize the animation parameters to the default settings
        self.init_params()
        
        try:
            # Parse command string into parameter list
            print 'Command: %s' % cmd_str
            cmd_params=cmd_str.split(',')
            for param in cmd_params:
                name,value=param.split('=')
                self.params[name.title()] = value.upper()
                print 'Setting param: %s to: %s' % (name,self.params[name.title()])
    
            if self.params['Pattern'] == 'OFF':
                # if the patter is OFF, then simply return. we have already turned off
                # the LEDs
                return result

            # process the command based on the provided parameters
            # first get the specified pattern
            print 'Getting Pattern: %s' % self.params['Pattern']
            self.pattern = bling_patterns.get_pattern(self.params['Pattern'].title())
            
            # process the segment parameter, getting the list of LEDs that will be
            # controlled by this command
            leds = self.get_leds_from_segment( self.params['Segment'])
            leds = self.apply_min_max_params( leds )
            print 'LED Range: %d-%d' % (leds[0], leds[1])
            
            self.pattern.setup( self.led, self.params['Color'], self.params['Speed'], leds[0], leds[1] )
            self.pattern.run()
        except:
            raise
            # catch any thrown exceptions and generate the error pattern
            print 'Error processing command: %s' % cmd_str
            self.pattern = bling_patterns.get_pattern('Error')
            self.pattern.setup(self.led, 'RED')
            self.pattern.run()

            result = 'ERROR'

 
    # TODO: Most of the following code will be removed once we complete the implementation of the pattern
    # classes and convert the menu over to using the pattern classes insead
    def menu(self):
        menu_str  = '\n'
        menu_str += '                              Available Bling Patterns\n\n'
        menu_str += '(1)  Alternates (two alternating colors)        '
        menu_str += '(14) Linear Rainbow (another variation)\n'
        menu_str += '(2)  Color Chase (one LED moving end to end)    '
        menu_str += '(15) Search Lights (colors moving up/down)\n'
        menu_str += '(3)  Color Fade (one color fading in/out)       '
        menu_str += '(16) Wave (colors moving up/down)\n'
        menu_str += '(4)  Color Pattern ()                           '
        menu_str += '(17) Solid Red (one color on all LEDs)\n'
        menu_str += '(5)  Color Wipe (one color moving up/down)      '
        menu_str += '(18) Solid Yellow (one color on all LEDs)\n'
        menu_str += '(6)  Fire Flies (colors randomly blinking)      '
        menu_str += '(19) Solid Green (one color on all LEDs)\n'
        menu_str += '(7)  Scanner (one color moving up/down)         '
        menu_str += '(20) Test Strip (test pattern for RGB cal.)\n'
        menu_str += '(8)  Rainbow Scanner (colors moving up/down)    '
        menu_str += '(21) Blinking Green (slow on all LEDs)\n'
        menu_str += '(9)  Ping Pong (colors bouncing around)         '
        menu_str += '(22) Blinking Green (medium on all LEDs)\n'
        menu_str += '(10) Party Mode (colors blinking on/off)        '
        menu_str += '(23) Blinking Green (fast on all LEDs)\n'
        menu_str += '(11) Rainbow Halves (strand divided in two      '
        menu_str += '(24) Blinking Green (medium on left LEDs)\n'
        menu_str += '(12) Rainbow (set of colors moving end to end)  '
        menu_str += '(25) Blinking Green (medium on right LEDs)\n'
        menu_str += '(13) Rainbow Cycles (variation of above)        '
        menu_str += '\n'
        menu_str += '\n'
        menu_str += '\n'
    
        return menu_str


    def menu_select( self, menu_selection ):
        result = 'OK'
        self.animate = True

        if menu_selection == 1:
            # Alternates
            self.process_cmd('Pattern=Alternates,Color=TEAMCOLORS,Speed=MEDIUM,Segment=RIGHT')
            return
        elif menu_selection == 2:
            # Color Chase
            self.fps = 10
            self.anim = ColorChase.ColorChase(self.led, colors.Green)
        elif menu_selection == 3:
            # Color Fade
            self.fps = 40
            self.anim = ColorFade.ColorFade(self.led, colors=ColorFade.rainbow)
        elif menu_selection == 4:
            # Color Pattern
            self.fps = 15
            self.anim = ColorPattern.ColorPattern(self.led, colors=ColorPattern.rainbow, width=3)
        elif menu_selection == 5:
            # Color Wipe
            self.fps = 15
            self.anim = ColorWipe.ColorWipe(self.led, colors.Green)
        elif menu_selection == 6:
            # Fire Flies
            self.fps = 40
            self.anim = FireFlies.FireFlies(self.led, colors=FireFlies.rainbow)
        elif menu_selection == 7:
            # Scanner
            self.fps = 10
            self.anim = LarsonScanners.LarsonScanner(self.led, color=colors.Blue)
        elif menu_selection == 8:
            # Rainbow Scanner
            self.fps = 20
            self.anim = LarsonScanners.LarsonRainbow(self.led)
        elif menu_selection == 9:
            # Ping Pong
            self.fps = 20
            #self.anim = PixelPingPong.PixelPingPong(self.led, color=colors.Blue)
            self.anim = PixelPingPong.PixelPingPong(self.led, color=colors.Blue, total_pixels=4,fade_delay=4)
        elif menu_selection == 10:
            # Party Mode
            self.fps = 10
            self.anim = PartyMode.PartyMode(self.led, colors=PartyMode.rainbow)
        elif menu_selection == 11:
            # Rainbow Halves
            self.fps = 20
            self.anim = HalvesRainbow.HalvesRainbow(self.led)
        elif menu_selection == 12:
            # Rainbow
            self.fps = 100
            self.anim = Rainbows.Rainbow(self.led)
        elif menu_selection == 13:
            # Rainbow Cycle
            self.fps = 200
            self.anim = Rainbows.RainbowCycle(self.led)
        elif menu_selection == 14:
            # Linear Rainbow
            self.fps = 50
            self.anim = LinearRainbow.LinearRainbow(self.led, individual_pixel=True)
        elif menu_selection == 15:
            # Search Lights
            self.fps = 20
            self.anim = Searchlights.Searchlights(self.led) 
        elif menu_selection == 16:
            # Wave
            self.fps = 5
            self.anim = Wave.Wave(self.led, color=colors.Blue, cycles=5) 
        elif menu_selection == 17:
            # Solid Red
            self.process_cmd('Pattern=Solid,Color=RED')
            return
        elif menu_selection == 18:
            # Solid Yellow
            self.process_cmd('Pattern=Solid,Color=YELLOW')
            return
        elif menu_selection == 19:
            # Solid Green
            self.process_cmd('Pattern=Solid,Color=GREEN')
            return
        elif menu_selection == 20:
            # Test Pattern
            # This animation is used to test the strip and the color order
            self.anim = StripChannelTest(self.led)
        elif menu_selection == 21:
            self.process_cmd('Pattern=Blinking,Color=PURPLE,Speed=SLOW,Segment=ALL')
            return
        elif menu_selection == 22:
            self.process_cmd('Pattern=Blinking,Color=GREEN,Speed=MEDIUM,Segment=ALL')
            return
        elif menu_selection == 23:
            self.process_cmd('Pattern=Blinking,Color=GREEN,Speed=FAST,Segment=ALL')
            return
        elif menu_selection == 24:
            self.process_cmd('Pattern=Blinking,Color=GREEN,Speed=MEDIUM,Segment=LEFT')
            return
        elif menu_selection == 25:
            self.process_cmd('Pattern=Blinking,Color=GREEN,Speed=MEDIUM,Segment=RIGHT')
            return
        elif menu_selection == 99:
            # All off
            self.animate = False
            self.led.all_off()
        else:
            raise ValueError
            result = 'ERROR'

        self.run()

        return result

    def run(self):
        try:
            if self.animate is True:
                #run the animation
                self.anim.run(fps=self.fps, threaded=True)
            else:
                # no animation, just update the LEDs
                self.led.update()
        except KeyboardInterrupt:
            #Ctrl+C will exit the animation and turn the LEDs offs
            self.led.all_off()
            self.led.update()

           
        
