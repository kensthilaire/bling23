
from bibliopixel.drivers.LPD8806 import *
from bibliopixel import LEDStrip
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
from BiblioPixelAnimations.strip import hexclock
from BiblioPixelAnimations.strip import LarsonScanners
from BiblioPixelAnimations.strip import LinearRainbow
from BiblioPixelAnimations.strip import PartyMode
from BiblioPixelAnimations.strip import PixelPingPong
from BiblioPixelAnimations.strip import Searchlights
from BiblioPixelAnimations.strip import Wave

class Bling(object):

    def __init__(self):
        self.num_leds = 36

        #init driver with the type and count of LEDs you're using
        self.driver = DriverLPD8806(num=self.num_leds, c_order = ChannelOrder.GRB, SPISpeed=2, use_py_spi=True, dev='/dev/spidev0.0')

        #init controller
        self.led = LEDStrip(self.driver)

        # the frames per second is used to control how fast the animation runs. some of the animations
        # work better when run at a low frames per second
        self.fps = None

        # animation object containing pattern to apply to the LEDs
        self.anim = None

        # flag to indicate whether the selected mode requires animation. Displaying a solid color across all or a range
        # of LEDs does not require animation
        self.animate = True

    def num_leds(self):
        return self.num_leds

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

    def set_blinking_anim(self, speed, segment):
        fps_params = { 'SLOW': 2,
                       'MEDIUM': 4,
                       'FAST':8 }
        segment_params = { 'ALL': (0,self.num_leds),
                           'LEFT': (0, (self.num_leds/2)-1),
                           'RIGHT': (self.num_leds/2, self.num_leds) }
        color = [colors.Green]
        segment_leds = segment_params[segment]
        self.fps = fps_params[speed]
        self.anim = PartyMode.PartyMode(self.led, colors=color, 
                                        start=segment_leds[0], end=segment_leds[1])

    def stop_animation(self):
        self.anim.stopThread(wait=True)
        self.led.all_off()
        self.led.update()

    def menu_select( self, menu_selection ):
        result = 'OK'
        self.animate = True

        if menu_selection == 1:
            # Alternates
            self.fps = 5
            self.anim = Alternates.Alternates(self.led, color1=colors.Blue, color2=colors.Orange)
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
            self.fps = 10
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
            self.animate = False
            self.led.fill(colors.Red)
        elif menu_selection == 18:
            # Solid Yellow
            self.animate = False
            self.led.fill(colors.Yellow)
        elif menu_selection == 19:
            # Solid Green
            self.animate = False
            self.led.fill(colors.Green)
        elif menu_selection == 20:
            # Test Pattern
            # This animation is used to test the strip and the color order
            self.anim = StripChannelTest(self.led)
        elif menu_selection == 21:
            self.set_blinking_anim('SLOW', 'ALL')
        elif menu_selection == 22:
            self.set_blinking_anim('MEDIUM', 'ALL')
        elif menu_selection == 23:
            self.set_blinking_anim('FAST', 'ALL')
        elif menu_selection == 24:
            self.set_blinking_anim('MEDIUM', 'LEFT')
        elif menu_selection == 25:
            self.set_blinking_anim('MEDIUM', 'RIGHT')
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

