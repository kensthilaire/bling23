'''
Created on Feb 5, 2017

@author: ksthilaire
'''

#
# import all the animations that are provided by the BiblioPixel animation library
#
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

# import the bling color map that defines all of our supported color schemes
import bling_colors

#
# Base class for the Bling patterns. This class contains the base behavior that is required for each of 
# the patterns. The individual patterns will derive from this base class and override the 
# appropriate functions
#
class BlingPatternBase(object):
    def __init__(self, name, animated=False):
        self.name = name
        self.animated = animated
        self.speed_params = { 'SLOW': 0, 'MEDIUM': 0, 'FAST':0 }
        self.animation = None
        self.fps = 0
    
    def is_animated(self):
        return self.animated
    def set_fps(self, speed_str):
        self.fps = self.speed_params[speed_str.upper()]
        return self.fps
    def setup(self):
        print 'Setup Not Implemented!!!'
        raise
    def clear(self):
        self.animation = None
    
    def run(self):
        if self.animated is True:
            if self.animation is None:
                print 'Animation is NOT Setup'
                raise
            
            #run the animation
            self.animation.run(fps=self.fps, threaded=True)
        else:
            # no animation, just update the LEDs
            self.led.update()

    def stop(self):
        if self.animation is not None:
            self.animation.stopThread(wait=True)
        self.led.all_off()
        self.led.update()

    def get_animation(self):
        if self.animation is None:
            print 'Pattern is NOT set up!!!'
            raise
        return self.animation

#
# Class that will be used to catch any errors in the implementation of the other patterns. The
# error pattern will be generated if an error is encountered while processing the other patterns
# so that the error can be quickly exposed.
#
class ErrorPattern(BlingPatternBase):
    def __init__(self):
        super(ErrorPattern,self).__init__('Error', animated=True)
        self.fps = 25
        
    def setup(self, led, color_str='RED', speed_str='MEDIUM', min_led=0, max_led=-1):
        # for the error pattern, we will ignore all settings and just blink the color red on
        # all LEDs at a super fast rate
        self.led = led
        colors = bling_colors.get_colors(color_str)
        self.animation = PartyMode.PartyMode(led, colors=colors)
    
#
# Class that implements the solid color pattern. This class doesn't use any animation
# and supports only a single color.
#    
class SolidPattern(BlingPatternBase):
    def __init__(self):
        super(SolidPattern,self).__init__('Solid')
        
    def setup(self, led, color_str, speed_str='MEDIUM', min_led=0, max_led=-1):
        self.led = led
        color = bling_colors.get_first_color(color_str)
        self.led.fill(color, start=min_led, end=max_led)
        print 'Setup Solid Params: color=%s, min=%d, max=%d' % (color, min_led, max_led)

#
# Class that implements the blinking pattern. This class uses the PartyMode animation, slowing
# it down so that the blinking pattern is obtained.
#    
class BlinkingPattern(BlingPatternBase):
    def __init__(self):
        super(BlinkingPattern,self).__init__('Blinking', animated=True)
        self.speed_params = { 'SLOW': 2, 'MEDIUM': 4, 'FAST':8 }
        
    def setup(self, led, color_str, speed_str='MEDIUM', min_led=0, max_led=-1):
        self.led = led
        self.set_fps(speed_str)
        print 'color: %s, speed: %s, min: %d, max: %d' % (color_str,speed_str,min_led,max_led)
        colors = bling_colors.get_colors(color_str)
        self.animation = PartyMode.PartyMode(led, colors=colors, start=min_led, end=max_led)
        print 'Setup BlinkingPattern Params: color=%s, min=%d, max=%d' % (colors, min_led, max_led)

        
#
# Helper functions to retrieve the dictionary of bling patterns or to retrieve a single pattern 
# from the set of supported patterns
#
def get_patterns():
    return patterns
def get_pattern( pattern_str ):
    return patterns[pattern_str]

patterns = {
    'Solid': SolidPattern(),
    'Blinking': BlinkingPattern(),
    
    'Error': ErrorPattern()
    }



if __name__ == '__main__':
    pass
