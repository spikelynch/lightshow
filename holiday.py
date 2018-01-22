import gradient
from holidaysecretapi import HolidaySecretAPI
import sys


# a renderer needs to have a method 'render' which accepts a single
# list of values as an argument

class HolidaySpectrum:

    def __init__(self, addr, mode, gradients, decay):
        self.DECAY = decay
        self.WAVELET = 10 
        self.WAVEMULT = 100 // self.WAVELET
        print("{} {}".format(self.WAVELET, self.WAVEMULT))
        self.holiday = HolidaySecretAPI(addr=addr)
        self.levels = [ 0.0 ] * 50
        self.buffer = [ ( 0, 0, 0 ) ] * 50
        self.mode = mode
        self.gradient = gradient.json(gradients[self.mode])
        if self.mode == 'spectrum':
            self.gradient = self.gradient[::-1] + self.gradient
        self.ngrad = len(self.gradient)
        if self.mode == 'wave':
            self.render = self.render_wave
        else:
            self.render = self.render_spectrum
            if self.mode == 'levels':
                self.f_col = self.f_col_levels
            else:
                self.f_col = self.f_col_spectrum

    def f_col_levels(self, i, level):
        k = int(level * self.ngrad)
        if k > self.ngrad - 1:
            k = self.ngrad - 1
        return self.gradient[k]

    def f_col_spectrum(self, i, level):
        k = level;
        if k > 1.0:
            k = 1.0
        ( r, g, b ) = self.gradient[i]
        return ( int(r * k), int(g * k), int(b * k) )

    def decay(self, i, level):
        if not self.DECAY:
            return level
        else:
            dl = self.levels[i] * self.DECAY
            if level > dl:
		self.levels[i] = level
	    else:
                self.levels[i] = dl
            return self.levels[i]	
        
    def render_spectrum(self, analyzer):
        """Render a frequency spectrum"""
        for i in range(50):
            l = self.decay(i, analyzer.spectrum[i])
            ( r, g, b ) = self.f_col(i, l) 
            self.holiday.setglobe(i, r, g, b)
        self.holiday.render() 

    def render_wave(self, analyzer):
        """Render the raw waveform"""
        self.buffer = self.buffer[self.WAVELET:]
        for i in range(self.WAVELET):
            v = int(self.ngrad * abs( analyzer.left[self.WAVEMULT * i] + analyzer.right[self.WAVEMULT * i] ))
            if v > self.ngrad - 1:
                v = self.ngrad - 1
            ( r, g, b ) = self.gradient[v]
            self.buffer.append(( r, g, b ))
        for i in range(50):
            self.holiday.setglobe(i, *self.buffer[i])
        self.holiday.render() 

    def demo(self):
        for i in range(50):
            ( r, g, b ) = self.gradient[i]
            self.holiday.setglobe(i, r, g, b)
        self.holiday.render() 
        sys.exit(-1)

