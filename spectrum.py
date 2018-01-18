#!/usr/bin/env python
# encoding: utf-8

# FFT code adapted from
# https://gist.github.com/hyperconcerto/950bbb9d9d4014d893e5


import numpy as np
import pyaudio


class SpectrumAnalyser:
    FORMAT = pyaudio.paFloat32
    CHANNELS = 1
    DEVICE = 0
    RATE = 48000
    CHUNK = 2048 
    START = 0
    DEFAULT_NFREQ = 50 
    wave_x = 0
    wave_y = 0
    spec_x = 0
    spec_y = 0
    data = []

    def __init__(self, device, nfreq=DEFAULT_NFREQ):
        self.pa = pyaudio.PyAudio()
        if not device:
            device = self.DEVICE
        self.nfreq = nfreq
        self.stream = self.pa.open(
            input_device_index=device,
            format = self.FORMAT,
            channels = self.CHANNELS, 
            rate = self.RATE, 
            input = True,
            output = False,
            frames_per_buffer = self.CHUNK)

    def run(self, renderers):
        print("Listening on device {}".format(self.DEVICE))
        try:
            while True:
                self.data = self.audioinput()
                self.fft()
                for r in renderers:
                    r.render(self.spec_y)
        except KeyboardInterrupt:
            self.stream.close()
            self.pa.terminate()

        print("Done.")

    def audioinput(self):
        ret = self.stream.read(self.CHUNK)
        ret = np.fromstring(ret, np.float32)
        return ret

    def fft(self):
        self.wave_x = range(self.START, self.START + self.nfreq)
        self.wave_y = self.data[self.START:self.START + self.nfreq]
        self.spec_x = np.fft.fftfreq(self.nfreq, d = 1.0 / self.RATE)  
        y = np.fft.fft(self.data[self.START:self.START + self.nfreq])    
        self.spec_y = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in y]




        
