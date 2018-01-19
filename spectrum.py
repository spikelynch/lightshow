#!/usr/bin/env python
# encoding: utf-8

# FFT code adapted from
# https://gist.github.com/hyperconcerto/950bbb9d9d4014d893e5


import numpy as np
import pyaudio, math


class SpectrumAnalyser:
    FORMAT = pyaudio.paFloat32
    CHANNELS = 2
    DEVICE = 0
    RATE = 48000
    CHUNK = 2048 
    START = 0
    DEFAULT_BINS = 100
    DEFAULT_USE = 25 
    EXPECT_MAX = 3.0 
    data = []
    spectrum = []

    def __init__(self, device=None, scale=EXPECT_MAX, nbins=DEFAULT_BINS, nfreq=DEFAULT_USE):
        self.pa = pyaudio.PyAudio()
        self.device = device
        if not device:
            self.device = self.DEVICE
        self.nfreq = nfreq
        self.nbins = nbins
        self.max = 0
        self.scale = 1.0 / scale
        self.stream = self.pa.open(
            input_device_index=device,
            format = self.FORMAT,
            channels = self.CHANNELS, 
            rate = self.RATE, 
            input = True,
            output = False,
            frames_per_buffer = self.CHUNK)

    def run(self, renderers):
        print("Listening on device {}".format(self.device))
        try:
            while True:
                self.data = self.audioinput()
                self.fft()
                for r in renderers:
                    r.render(self.spectrum)
        except KeyboardInterrupt:
            self.stream.close()
            self.pa.terminate()

        print("Done.")

    def audioinput(self):
        ret = self.stream.read(self.CHUNK)
        ret = np.fromstring(ret, np.float32)
        return ret

    def fft(self):
        interleaved = self.data[self.START:self.START + self.nbins * 2]
        stereo = np.reshape(interleaved, (self.nbins, 2))
  
        left = np.fft.fft(stereo[:,1])
        right = np.fft.fft(stereo[:,0])
        
        left = left[:self.nfreq]
        right = right[:self.nfreq]    
        lspec = [ np.sqrt(c.real ** 2 + c.imag ** 2) for c in left ]
        rspec = [ np.sqrt(c.real ** 2 + c.imag ** 2) for c in right ]
        lspec.reverse()
        self.spectrum = [ self.scale * v for v in lspec + rspec ]
        m = max(self.spectrum)
        if m > self.max:
            self.max = m




        
