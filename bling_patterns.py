'''
Created on Feb 5, 2017

@author: ksthilaire
'''
#
# import all the animations that are provided by the BiblioPixel animation library
#
from bibliopixel.animation import StripChannelTest
from bibliopixel.animation import BaseStripAnim

import bibliopixel.colors as colors


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

# Modified Larson Scanner class to handle multiple segments within a LED strip. This
# class will display the same pattern on each of the segments
class SegmentLarsonScanner(BaseStripAnim):
    def __init__(self, led, num_segments, segment_size, color, tail=2, start=0, end=-1):
        super(SegmentLarsonScanner, self).__init__(led, start, end)
        self._color = color
        self._num_segments = num_segments
        self._segment_size = segment_size

        self._tail = tail + 1  # makes tail math later easier
        if self._tail >= self._size / 2:
            self._tail = (self._size / 2) - 1

        self._direction = -1
        self._last = 0
        self._fadeAmt = 256 / self._tail

    def step(self, amt = 1):
        self._led.all_off()

        self._last = self._start + self._step

        for j in range(0,self._num_segments):
            self._led.set((j*self._segment_size)+self._last, self._color)

        for i in range(self._tail):
            for j in range(0,self._num_segments):
                base_led = j*self._segment_size
                top_led = (j+1)*self._segment_size
                lower_led = base_led+self._last - i
                if lower_led >= base_led:
                    self._led.set(lower_led, colors.color_scale(self._color, 255 - (self._fadeAmt * i)))
                upper_led = base_led+self._last + i
                if upper_led < top_led:
                    self._led.set(upper_led, colors.color_scale(self._color, 255 - (self._fadeAmt * i)))

        if self._start + self._step >= self._segment_size-1:
            self._direction = -self._direction
        elif self._step <= 0:
            self._direction = -self._direction

        self._step += self._direction * amt

class SegmentColorWipe(BaseStripAnim):
    """Fill the dots progressively along the strip."""
    def __init__(self, led, num_segments, segment_size, color, start=0, end=-1):
        super(SegmentColorWipe, self).__init__(led, start, end)
        self._color = color
        self._num_segments = num_segments
        self._segment_size = segment_size

    def step(self, amt = 1):
        if self._step == 0:
            self._led.all_off()

        for i in range(amt):
            for j in range(0,self._num_segments):
                self._led.set((j*self._segment_size)+self._start + self._step - i, self._color)

        self._step += amt
        overflow = (self._start + self._step) - (self._segment_size)
        if overflow >= 0:
            self._step = overflow

class SegmentColorChase(BaseStripAnim):
    """Chase one pixel down the strip."""

    def __init__(self, led, num_segments, segment_size, color, width=1, start=0, end=-1):
        super(SegmentColorChase, self).__init__(led, start, end)
        self._color = color
        self._width = width
        self._num_segments = num_segments
        self._segment_size = segment_size

    def step(self, amt = 1):
        self._led.all_off() #because I am lazy

        for i in range(self._width):
            for j in range(0,self._num_segments):
                self._led.set((j*self._segment_size)+self._start + self._step - i, self._color)

        self._step += amt
        overflow = (self._start + self._step) - (self._segment_size)
        if overflow >= 0:
            self._step = overflow


class SegmentRainbow(BaseStripAnim):
    """Display the rainbow across multiple segments"""

    def __init__(self, led, num_segments, segment_size, max_led=-1, centre_out=True, rainbow_inc=4):
        super(SegmentRainbow, self).__init__(led, 0, max_led)
        self._centerOut = centre_out
        self._rainbowInc = rainbow_inc
        self._num_segments = num_segments
        self._segment_size = segment_size
        self._color_step = 0

    def step(self, amt = 1):

        for j in range(0,self._num_segments):
            led_index = (j*self._segment_size)+self._start + self._step
            self._led.fill( colors.hue2rgb_rainbow(self._color_step), led_index, led_index )

        self._step += amt
        overflow = (self._start + self._step) - (self._segment_size)
        if overflow >= 0:
            self._step = overflow

        if self._color_step == len(colors.hue_rainbow)-1:
            self._color_step = 0
        else:
            self._color_step += amt + self._rainbowInc
            if self._color_step > len(colors.hue_rainbow)-1:
                self._color_step = 0

class SegmentLinearRainbow(BaseStripAnim):

    def __init__(self, led, num_segments, segment_size, individual_pixel=False, max_led=-1):
        super(SegmentLinearRainbow, self).__init__(led, 0, -1)
        self._step = 0
        self._current = 0
        self._minLed = 0
        self._maxLed = max_led
        if self._maxLed < 0 or self._maxLed < self._minLed:
            self._maxLed = self._led.lastIndex
        self._num_segments = num_segments
        self._segment_size = segment_size

        self._individualPixel = individual_pixel

    def step(self, amt=1):
        for j in range(0,self._num_segments):
            led_index = (j*self._segment_size)+self._current
            if self._individualPixel:
                # This setting will change the colour of each pixel on each cycle
                self._led.fill( colors.hue2rgb_rainbow(self._step), led_index, led_index)
            else:
                # This setting will change the colour of all pixels on each cycle
                self._led.fill(colors.wheel_color(self._step), 0, led_index)

        if self._step == len(colors.hue_rainbow) - 1:
            self._step = 0
        else:
            self._step += amt

        if self._current == self._segment_size-1:
            self._current = self._minLed
        else:
            self._current += amt

class SegmentColorPattern(BaseStripAnim):
    """Fill the dots progressively along the strip with alternating colors."""

    def __init__(self, led, num_segments, segment_size, colors, width, dir = True, start=0, end=-1):
        super(SegmentColorPattern, self).__init__(led, start, end)
        self._colors = colors
        self._colorCount = len(colors)
        self._width = width
        self._total_width = self._width * self._colorCount;
        self._dir = dir
        self._num_segments = num_segments
        self._segment_size = segment_size

    def step(self, amt = 1):

        for i in range(self._size):
            cIndex = ((i+self._step) % self._total_width) / self._width;
            for j in range(0,self._num_segments):
                led_index = (j*self._segment_size)+(i % self._segment_size)
                self._led.set(led_index, self._colors[cIndex])

        if self._dir:
            self._step += amt
            overflow = (self._start + self._step) - self._end
            if overflow >= 0:
                self._step = overflow
        else:
            self._step -= amt
            if self._step < 0:
                self._step = self._end + self._step



#
# Base class for the Bling patterns. This class contains the base behavior that is required for each of 
# the patterns. The individual patterns will derive from this base class and override the 
# appropriate functions
#
class BlingPatternBase(object):
    def __init__(self, name, bling_mgr, animated=False):
        self.name = name
        self.bling = bling_mgr
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
    def __init__(self, bling_mgr):
        super(ErrorPattern,self).__init__('Error', bling_mgr, animated=True)
        self.fps = 25
        
    def setup(self, led, color_str='RED', speed_str='MEDIUM', min_led=0, max_led=-1, segment_ctrl=None):
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
    def __init__(self, bling_mgr):
        super(SolidPattern,self).__init__('Solid', bling_mgr)
        
    def setup(self, led, color_str, speed_str='MEDIUM', min_led=0, max_led=-1, segment_ctrl=None):
        self.led = led
        color = bling_colors.get_first_color(color_str)
        self.led.fill(color, start=min_led, end=max_led)

#
# Class that implements the blinking pattern. This class uses the PartyMode animation, slowing
# it down so that the blinking pattern is obtained.
#    
class BlinkingPattern(BlingPatternBase):
    def __init__(self, bling_mgr):
        super(BlinkingPattern,self).__init__('Blinking', bling_mgr, animated=True)
        self.speed_params = { 'SLOW': 2, 'MEDIUM': 4, 'FAST':8 }
        
    def setup(self, led, color_str, speed_str='MEDIUM', min_led=0, max_led=-1, segment_ctrl=None):
        self.led = led
        self.set_fps(speed_str)
        colors = bling_colors.get_colors(color_str)
        self.animation = PartyMode.PartyMode(led, colors=colors, start=min_led, end=max_led)

        
class AlternatesPattern(BlingPatternBase):
    def __init__(self, bling_mgr):
        super(AlternatesPattern,self).__init__('Alternates', bling_mgr, animated=True)
        self.speed_params = { 'SLOW': 2, 'MEDIUM': 5, 'FAST':10 }
        
    def setup(self, led, color_str, speed_str='MEDIUM', min_led=0, max_led=-1, segment_ctrl=None):
        self.led = led
        self.set_fps(speed_str)
        colors = bling_colors.get_colors(color_str)
        if len(colors) < 2:
            colors.extend(bling_colors.get_colors('YELLOW'))
        self.animation = Alternates.Alternates(led, max_led=max_led, color1=colors[0],color2=colors[1])
        
class ColorChasePattern(BlingPatternBase):
    def __init__(self, bling_mgr):
        super(ColorChasePattern,self).__init__('ColorChase', bling_mgr, animated=True)
        self.speed_params = { 'SLOW': 5, 'MEDIUM': 10, 'FAST':20 }
        
    def setup(self, led, color_str, speed_str='MEDIUM', min_led=0, max_led=-1, segment_ctrl=None):
        self.led = led
        self.set_fps(speed_str)
        color = bling_colors.get_first_color(color_str)
        if segment_ctrl is not None:
            num_segments = self.bling.get_num_segments()
            segment_size = self.bling.get_segment_size()
            self.animation = SegmentColorChase(led, num_segments=num_segments, segment_size=segment_size,
                                              color=color, width=DEFAULT_WIDTH, start=min_led, end=max_led)
        else:
            self.animation = ColorChase.ColorChase(led, color=color, width=DEFAULT_WIDTH, start=min_led, end=max_led)

class ColorFadePattern(BlingPatternBase):
    def __init__(self, bling_mgr):
        super(ColorFadePattern,self).__init__('ColorFade', bling_mgr, animated=True)
        self.speed_params = { 'SLOW': 20, 'MEDIUM': 40, 'FAST':80 }
        
    def setup(self, led, color_str, speed_str='MEDIUM', min_led=0, max_led=-1, segment_ctrl=None):
        self.led = led
        self.set_fps(speed_str)
        colors = bling_colors.get_colors(color_str)
        self.animation = ColorFade.ColorFade(led, colors=colors, start=min_led, end=max_led)
        
class ColorsPattern(BlingPatternBase):
    def __init__(self, bling_mgr):
        super(ColorsPattern,self).__init__('ColorsPattern', bling_mgr, animated=True)
        self.speed_params = { 'SLOW': 5, 'MEDIUM': 15, 'FAST':25 }
        
    def setup(self, led, color_str, speed_str='MEDIUM', min_led=0, max_led=-1, segment_ctrl=None):
        self.led = led
        self.set_fps(speed_str)
        colors = bling_colors.get_colors(color_str)
        if segment_ctrl is not None:
            num_segments = self.bling.get_num_segments()
            segment_size = self.bling.get_segment_size()
            self.animation = SegmentColorPattern(led, num_segments=num_segments, segment_size=segment_size,
                                                 colors=colors, width=DEFAULT_WIDTH, dir=True, start=min_led, end=max_led)
        else:
            self.animation = ColorPattern.ColorPattern(led, colors=colors, width=DEFAULT_WIDTH, dir=True, start=min_led, end=max_led)
        
class ColorWipePattern(BlingPatternBase):
    def __init__(self, bling_mgr):
        super(ColorWipePattern,self).__init__('ColorWipe', bling_mgr, animated=True)
        self.speed_params = { 'SLOW': 5, 'MEDIUM': 15, 'FAST':25 }
        
    def setup(self, led, color_str, speed_str='MEDIUM', min_led=0, max_led=-1, segment_ctrl=None):
        self.led = led
        self.set_fps(speed_str)
        color = bling_colors.get_first_color(color_str)
        if segment_ctrl is not None:
            num_segments = self.bling.get_num_segments()
            segment_size = self.bling.get_segment_size()
            self.animation = SegmentColorWipe(led, num_segments=num_segments, segment_size=segment_size, 
                                              color=color, start=min_led, end=max_led)
        else:
            self.animation = ColorWipe.ColorWipe(led, color=color, start=min_led, end=max_led)
        
class FireFliesPattern(BlingPatternBase):
    def __init__(self, bling_mgr):
        super(FireFliesPattern,self).__init__('FireFlies', bling_mgr, animated=True)
        self.speed_params = { 'SLOW': 20, 'MEDIUM': 40, 'FAST':80 }
        
    def setup(self, led, color_str, speed_str='MEDIUM', min_led=0, max_led=-1, segment_ctrl=None):
        self.led = led
        self.set_fps(speed_str)
        colors = bling_colors.get_colors(color_str)
        self.animation = FireFlies.FireFlies(led, colors=colors, start=min_led, end=max_led)
        
class ScannerPattern(BlingPatternBase):
    def __init__(self, bling_mgr):
        super(ScannerPattern,self).__init__('Scanner', bling_mgr, animated=True)
        self.speed_params = { 'SLOW': 5, 'MEDIUM': 10, 'FAST':25 }
        
    def setup(self, led, color_str, speed_str='MEDIUM', min_led=0, max_led=-1, segment_ctrl=None):
        self.led = led
        self.set_fps(speed_str)
        color = bling_colors.get_first_color(color_str)
        if segment_ctrl is not None:
            num_segments = self.bling.get_num_segments()
            segment_size = self.bling.get_segment_size()
            self.animation = SegmentLarsonScanner(led, num_segments=num_segments, segment_size=segment_size, 
                                                  color=color, start=min_led, end=max_led)
        else:
            self.animation = LarsonScanners.LarsonScanner(led, color=color, start=min_led, end=max_led)
        
class RainbowScannerPattern(BlingPatternBase):
    def __init__(self, bling_mgr):
        super(RainbowScannerPattern,self).__init__('RainbowScanner', bling_mgr, animated=True)
        self.speed_params = { 'SLOW': 10, 'MEDIUM': 20, 'FAST':40 }
        
    def setup(self, led, color_str, speed_str='MEDIUM', min_led=0, max_led=-1, segment_ctrl=None):
        self.led = led
        self.set_fps(speed_str)
        # The rainbow scanner doesn't actually let us set the colors...
        colors = bling_colors.get_colors(color_str)
        self.animation = LarsonScanners.LarsonRainbow(led, start=min_led, end=max_led)
        
class PingPongPattern(BlingPatternBase):
    def __init__(self, bling_mgr):
        super(PingPongPattern,self).__init__('PingPong', bling_mgr, animated=True)
        self.speed_params = { 'SLOW': 10, 'MEDIUM': 20, 'FAST':40 }
        
    def setup(self, led, color_str, speed_str='MEDIUM', min_led=0, max_led=-1, segment_ctrl=None):
        self.led = led
        self.set_fps(speed_str)
        color = bling_colors.get_first_color(color_str)
        # The PingPong animation doesn't let us set the range of LEDs, just the max number
        self.animation = PixelPingPong.PixelPingPong(led, color=color, max_led=max_led)
        
class PartyModePattern(BlingPatternBase):
    def __init__(self, bling_mgr):
        super(PartyModePattern,self).__init__('PartyMode', bling_mgr, animated=True)
        self.speed_params = { 'SLOW': 5, 'MEDIUM': 10, 'FAST':30 }
        
    def setup(self, led, color_str, speed_str='MEDIUM', min_led=0, max_led=-1, segment_ctrl=None):
        self.led = led
        self.set_fps(speed_str)
        colors = bling_colors.get_colors(color_str)
        self.animation = PartyMode.PartyMode(led, colors=colors, start=min_led, end=max_led)
        
class RainbowHalvesPattern(BlingPatternBase):
    def __init__(self, bling_mgr):
        super(RainbowHalvesPattern,self).__init__('RainbowHalves', bling_mgr, animated=True)
        self.speed_params = { 'SLOW': 10, 'MEDIUM': 20, 'FAST':40 }
        
    def setup(self, led, color_str, speed_str='MEDIUM', min_led=0, max_led=-1, segment_ctrl=None):
        self.led = led
        self.set_fps(speed_str)
        colors = bling_colors.get_colors(color_str)
        if segment_ctrl is not None:
            num_segments = self.bling.get_num_segments()
            segment_size = self.bling.get_segment_size()
            self.animation = SegmentRainbow(led, num_segments=num_segments, segment_size=segment_size, 
                                            max_led=max_led, centre_out=True)
        else:
            self.animation = HalvesRainbow.HalvesRainbow(led, max_led=max_led, centre_out=True)
        
class RainbowPattern(BlingPatternBase):
    def __init__(self, bling_mgr):
        super(RainbowPattern,self).__init__('Rainbow', bling_mgr, animated=True)
        self.speed_params = { 'SLOW': 50, 'MEDIUM': 100, 'FAST':200 }
        
    def setup(self, led, color_str, speed_str='MEDIUM', min_led=0, max_led=-1, segment_ctrl=None):
        self.led = led
        self.set_fps(speed_str)
        # The Rainbow pattern doesn't let us set the colors...
        colors = bling_colors.get_colors(color_str)
        self.animation = Rainbows.Rainbow(led, start=min_led, end=max_led)
        
class RainbowCyclePattern(BlingPatternBase):
    def __init__(self, bling_mgr):
        super(RainbowCyclePattern,self).__init__('RainbowCycle', bling_mgr, animated=True)
        self.speed_params = { 'SLOW': 100, 'MEDIUM': 200, 'FAST':400 }
        
    def setup(self, led, color_str, speed_str='MEDIUM', min_led=0, max_led=-1, segment_ctrl=None):
        self.led = led
        self.set_fps(speed_str)
        # The Rainbow pattern doesn't let us set the colors...
        colors = bling_colors.get_colors(color_str)
        self.animation = Rainbows.RainbowCycle(led, start=min_led, end=max_led)
        
class LinearRainbowPattern(BlingPatternBase):
    def __init__(self, bling_mgr):
        super(LinearRainbowPattern,self).__init__('LinearRainbow', bling_mgr, animated=True)
        self.speed_params = { 'SLOW': 25, 'MEDIUM': 50, 'FAST':100 }
        
    def setup(self, led, color_str, speed_str='MEDIUM', min_led=0, max_led=-1, segment_ctrl=None):
        self.led = led
        self.set_fps(speed_str)
        colors = bling_colors.get_colors(color_str)
        # LinearRainbow doesn't let us set the colors or the LED range.
        if segment_ctrl is not None:
            num_segments = self.bling.get_num_segments()
            segment_size = self.bling.get_segment_size()
            self.animation = SegmentLinearRainbow(led, num_segments=num_segments, segment_size=segment_size, 
                                                  individual_pixel=True, max_led=max_led)
        else:
            self.animation = LinearRainbow.LinearRainbow(led, individual_pixel=True, max_led=max_led)
        
class SearchLightsPattern(BlingPatternBase):
    def __init__(self, bling_mgr):
        self.bling = bling_mgr
        super(SearchLightsPattern,self).__init__('SearchLights', bling_mgr, animated=True)
        self.speed_params = { 'SLOW': 10, 'MEDIUM': 20, 'FAST':40 }
        
    def setup(self, led, color_str, speed_str='MEDIUM', min_led=0, max_led=-1, segment_ctrl=None):
        self.led = led
        self.set_fps(speed_str)
        colors = bling_colors.get_colors(color_str)
        self.animation = Searchlights.Searchlights(led, colors=colors, start=min_led, end=max_led)
        
class WavePattern(BlingPatternBase):
    def __init__(self, bling_mgr):
        super(WavePattern,self).__init__('Wave', bling_mgr, animated=True)
        self.speed_params = { 'SLOW': 3, 'MEDIUM': 6, 'FAST':12 }
        
    def setup(self, led, color_str, speed_str='MEDIUM', min_led=0, max_led=-1, segment_ctrl=None):
        self.led = led
        self.set_fps(speed_str)
        color = bling_colors.get_first_color(color_str)
        self.animation = Wave.Wave(led, color=color, cycles=DEFAULT_CYCLES, start=min_led, end=max_led)
        

        
class TestPattern(BlingPatternBase):
    def __init__(self, bling_mgr):
        super(TestPattern,self).__init__('Test', bling_mgr, animated=True)
        self.speed_params = { 'SLOW': 2, 'MEDIUM': 4, 'FAST':8 }
        
    def setup(self, led, color_str, speed_str='MEDIUM', min_led=0, max_led=-1, segment_ctrl=None):
        self.led = led
        self.set_fps(speed_str)
        colors = bling_colors.get_colors(color_str)
        self.animation = StripChannelTest(led)

class BlingPatterns(object):
    def __init__(self, bling_mgr):

        self.patterns = {
            'SOLID': SolidPattern(bling_mgr),
            'BLINKING': BlinkingPattern(bling_mgr),
            'ALTERNATES': AlternatesPattern(bling_mgr),
            'COLORCHASE': ColorChasePattern(bling_mgr),
            'COLORFADE': ColorFadePattern (bling_mgr),
            'COLORPATTERN': ColorsPattern(bling_mgr),
            'COLORWIPE': ColorWipePattern(bling_mgr),
            'FIREFLIES': FireFliesPattern(bling_mgr),
            'SCANNER': ScannerPattern(bling_mgr),
            'RAINBOWSCANNER': RainbowScannerPattern(bling_mgr),
            'PINGPONG': PingPongPattern(bling_mgr),
            'PARTYMODE': PartyModePattern(bling_mgr),
            'RAINBOWHALVES': RainbowHalvesPattern(bling_mgr),
            'RAINBOW': RainbowPattern(bling_mgr),
            'RAINBOWCYCLE': RainbowCyclePattern(bling_mgr),
            'LINEARRAINBOW': LinearRainbowPattern(bling_mgr),
            'SEARCHLIGHTS': SearchLightsPattern(bling_mgr),
            'WAVE': WavePattern(bling_mgr),

            'TEST': TestPattern(bling_mgr),
            'ERROR': ErrorPattern(bling_mgr)
        }

    #
    # Helper functions to retrieve the dictionary of bling patterns or to retrieve a single pattern 
    # from the set of supported patterns
    #
    def get_patterns(self):
        return self.patterns
    def get_pattern(self, pattern_str):
        return self.patterns[pattern_str]



if __name__ == '__main__':
    pass
