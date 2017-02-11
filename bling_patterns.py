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

# a constant specifying the number of LEDs for a default width. We may want to expose the width 
# as a parameter in the interface from the robot code, too
DEFAULT_WIDTH=3
DEFAULT_CYCLES=5

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
        colors = bling_colors.get_colors(color_str)
        self.animation = PartyMode.PartyMode(led, colors=colors, start=min_led, end=max_led)

        
class AlternatesPattern(BlingPatternBase):
    def __init__(self):
        super(AlternatesPattern,self).__init__('Alternates', animated=True)
        self.speed_params = { 'SLOW': 2, 'MEDIUM': 5, 'FAST':10 }
        
    def setup(self, led, color_str, speed_str='MEDIUM', min_led=0, max_led=-1):
        self.led = led
        self.set_fps(speed_str)
        colors = bling_colors.get_colors(color_str)
        self.animation = Christmas.Christmas(led, max_led=max_led, color1=colors[0],color2=colors[1])
        
class ColorChasePattern(BlingPatternBase):
    def __init__(self):
        super(ColorChasePattern,self).__init__('ColorChase', animated=True)
        self.speed_params = { 'SLOW': 5, 'MEDIUM': 10, 'FAST':20 }
        
    def setup(self, led, color_str, speed_str='MEDIUM', min_led=0, max_led=-1):
        self.led = led
        self.set_fps(speed_str)
        color = bling_colors.get_first_color(color_str)
        self.animation = ColorChase.ColorChase(led, color=color, width=DEFAULT_WIDTH, start=min_led, end=max_led)

class ColorFadePattern(BlingPatternBase):
    def __init__(self):
        super(ColorFadePattern,self).__init__('ColorFade', animated=True)
        self.speed_params = { 'SLOW': 20, 'MEDIUM': 40, 'FAST':80 }
        
    def setup(self, led, color_str, speed_str='MEDIUM', min_led=0, max_led=-1):
        self.led = led
        self.set_fps(speed_str)
        colors = bling_colors.get_colors(color_str)
        self.animation = ColorFade.ColorFade(led, colors=colors, start=min_led, end=max_led)
        
class ColorsPattern(BlingPatternBase):
    def __init__(self):
        super(ColorsPattern,self).__init__('ColorsPattern', animated=True)
        self.speed_params = { 'SLOW': 5, 'MEDIUM': 15, 'FAST':25 }
        
    def setup(self, led, color_str, speed_str='MEDIUM', min_led=0, max_led=-1):
        self.led = led
        self.set_fps(speed_str)
        colors = bling_colors.get_colors(color_str)
        self.animation = ColorPattern.ColorPattern(led, colors=colors, width=DEFAULT_WIDTH, dir=True, start=min_led, end=max_led)
        
class ColorWipePattern(BlingPatternBase):
    def __init__(self):
        super(ColorWipePattern,self).__init__('ColorWipe', animated=True)
        self.speed_params = { 'SLOW': 5, 'MEDIUM': 15, 'FAST':25 }
        
    def setup(self, led, color_str, speed_str='MEDIUM', min_led=0, max_led=-1):
        self.led = led
        self.set_fps(speed_str)
        color = bling_colors.get_first_color(color_str)
        self.animation = ColorWipe.ColorWipe(led, color=color, start=min_led, end=max_led)
        
class FireFliesPattern(BlingPatternBase):
    def __init__(self):
        super(FireFliesPattern,self).__init__('FireFlies', animated=True)
        self.speed_params = { 'SLOW': 20, 'MEDIUM': 40, 'FAST':80 }
        
    def setup(self, led, color_str, speed_str='MEDIUM', min_led=0, max_led=-1):
        self.led = led
        self.set_fps(speed_str)
        colors = bling_colors.get_colors(color_str)
        self.animation = FireFlies.FireFlies(led, colors=colors, start=min_led, end=max_led)
        
class ScannerPattern(BlingPatternBase):
    def __init__(self):
        super(ScannerPattern,self).__init__('Scanner', animated=True)
        self.speed_params = { 'SLOW': 5, 'MEDIUM': 10, 'FAST':25 }
        
    def setup(self, led, color_str, speed_str='MEDIUM', min_led=0, max_led=-1):
        self.led = led
        self.set_fps(speed_str)
        color = bling_colors.get_first_color(color_str)
        self.animation = LarsonScanners.LarsonScanner(led, color=color, start=min_led, end=max_led)
        
class RainbowScannerPattern(BlingPatternBase):
    def __init__(self):
        super(RainbowScannerPattern,self).__init__('RainbowScanner', animated=True)
        self.speed_params = { 'SLOW': 10, 'MEDIUM': 20, 'FAST':40 }
        
    def setup(self, led, color_str, speed_str='MEDIUM', min_led=0, max_led=-1):
        self.led = led
        self.set_fps(speed_str)
        # The rainbow scanner doesn't actually let us set the colors...
        colors = bling_colors.get_colors(color_str)
        self.animation = LarsonScanners.LarsonRainbow(led, start=min_led, end=max_led)
        
class PingPongPattern(BlingPatternBase):
    def __init__(self):
        super(PingPongPattern,self).__init__('PingPong', animated=True)
        self.speed_params = { 'SLOW': 10, 'MEDIUM': 20, 'FAST':40 }
        
    def setup(self, led, color_str, speed_str='MEDIUM', min_led=0, max_led=-1):
        self.led = led
        self.set_fps(speed_str)
        color = bling_colors.get_first_color(color_str)
        # The PingPong animation doesn't let us set the range of LEDs, just the max number
        self.animation = PixelPingPong.PixelPingPong(led, color=color, max_led=max_led)
        
class PartyModePattern(BlingPatternBase):
    def __init__(self):
        super(PartyModePattern,self).__init__('PartyMode', animated=True)
        self.speed_params = { 'SLOW': 5, 'MEDIUM': 12, 'FAST':30 }
        
    def setup(self, led, color_str, speed_str='MEDIUM', min_led=0, max_led=-1):
        self.led = led
        self.set_fps(speed_str)
        colors = bling_colors.get_colors(color_str)
        self.animation = PartyMode.PartyMode(led, colors=colors, start=min_led, end=max_led)
        
class RainbowHalvesPattern(BlingPatternBase):
    def __init__(self):
        super(RainbowHalvesPattern,self).__init__('RainbowHalves', animated=True)
        self.speed_params = { 'SLOW': 10, 'MEDIUM': 20, 'FAST':40 }
        
    def setup(self, led, color_str, speed_str='MEDIUM', min_led=0, max_led=-1):
        self.led = led
        self.set_fps(speed_str)
        colors = bling_colors.get_colors(color_str)
        self.animation = HalvesRainbow.HalvesRainbow(led, max_led=max_led, centre_out=True)
        
class RainbowPattern(BlingPatternBase):
    def __init__(self):
        super(RainbowPattern,self).__init__('Rainbow', animated=True)
        self.speed_params = { 'SLOW': 50, 'MEDIUM': 100, 'FAST':200 }
        
    def setup(self, led, color_str, speed_str='MEDIUM', min_led=0, max_led=-1):
        self.led = led
        self.set_fps(speed_str)
        # The Rainbow pattern doesn't let us set the colors...
        colors = bling_colors.get_colors(color_str)
        self.animation = Rainbows.Rainbow(led, start=min_led, end=max_led)
        
class RainbowCyclePattern(BlingPatternBase):
    def __init__(self):
        super(RainbowCyclePattern,self).__init__('RainbowCycle', animated=True)
        self.speed_params = { 'SLOW': 100, 'MEDIUM': 200, 'FAST':400 }
        
    def setup(self, led, color_str, speed_str='MEDIUM', min_led=0, max_led=-1):
        self.led = led
        self.set_fps(speed_str)
        # The Rainbow pattern doesn't let us set the colors...
        colors = bling_colors.get_colors(color_str)
        self.animation = Rainbows.RainbowCycle(led, start=min_led, end=max_led)
        
class LinearRainbowPattern(BlingPatternBase):
    def __init__(self):
        super(LinearRainbowPattern,self).__init__('LinearRainbow', animated=True)
        self.speed_params = { 'SLOW': 25, 'MEDIUM': 50, 'FAST':100 }
        
    def setup(self, led, color_str, speed_str='MEDIUM', min_led=0, max_led=-1):
        self.led = led
        self.set_fps(speed_str)
        colors = bling_colors.get_colors(color_str)
        # LinearRainbow doesn't let us set the colors or the LED range.
        self.animation = LinearRainbow.LinearRainbow(led, individual_pixel=True, max_led=max_led)
        
class SearchLightsPattern(BlingPatternBase):
    def __init__(self):
        super(SearchLightsPattern,self).__init__('SearchLights', animated=True)
        self.speed_params = { 'SLOW': 10, 'MEDIUM': 20, 'FAST':40 }
        
    def setup(self, led, color_str, speed_str='MEDIUM', min_led=0, max_led=-1):
        self.led = led
        self.set_fps(speed_str)
        colors = bling_colors.get_colors(color_str)
        self.animation = Searchlights.Searchlights(led, colors=colors, start=min_led, end=max_led)
        
class WavePattern(BlingPatternBase):
    def __init__(self):
        super(WavePattern,self).__init__('Wave', animated=True)
        self.speed_params = { 'SLOW': 3, 'MEDIUM': 6, 'FAST':12 }
        
    def setup(self, led, color_str, speed_str='MEDIUM', min_led=0, max_led=-1):
        self.led = led
        self.set_fps(speed_str)
        color = bling_colors.get_first_color(color_str)
        self.animation = Wave.Wave(led, color=color, cycles=DEFAULT_CYCLES, start=min_led, end=max_led)
        

        
class TestPattern(BlingPatternBase):
    def __init__(self):
        super(TestPattern,self).__init__('Test', animated=True)
        self.speed_params = { 'SLOW': 2, 'MEDIUM': 4, 'FAST':8 }
        
    def setup(self, led, color_str, speed_str='MEDIUM', min_led=0, max_led=-1):
        self.led = led
        self.set_fps(speed_str)
        colors = bling_colors.get_colors(color_str)
        self.animation = StripChannelTest(led)

#
# Helper functions to retrieve the dictionary of bling patterns or to retrieve a single pattern 
# from the set of supported patterns
#
def get_patterns():
    return patterns
def get_pattern( pattern_str ):
    return patterns[pattern_str]

patterns = {
    'SOLID': SolidPattern(),
    'BLINKING': BlinkingPattern(),
    'ALTERNATES': AlternatesPattern(),
    'COLORCHASE': ColorChasePattern(),
    'COLORFADE': ColorFadePattern (),
    'COLORPATTERN': ColorsPattern(),
    'COLORWIPE': ColorWipePattern(),
    'FIREFLIES': FireFliesPattern(),
    'SCANNER': ScannerPattern(),
    'RAINBOWSCANNER': RainbowScannerPattern(),
    'PINGPONG': PingPongPattern(),
    'PARTYMODE': PartyModePattern(),
    'RAINBOWHALVES': RainbowHalvesPattern(),
    'RAINBOW': RainbowPattern(),
    'RAINBOWCYCLE': RainbowCyclePattern(),
    'LINEARRAINBOW': LinearRainbowPattern(),
    'SEARCHLIGHTS': SearchLightsPattern(),
    'WAVE': WavePattern(),
    
    'TEST': TestPattern(),
    'ERROR': ErrorPattern()
    }



if __name__ == '__main__':
    pass
