
import numpy as np

class TextSpectrum:
    """
Visualises a spectrum by mapping it onto strings, either single ASCII characters
or ANSI sequences for colour
"""


    ASCII = " .:-=+*#%@"
    
    def __init__(self, gradient):
        if gradient:
            self.gradient = gradient
            self.ansi = True
        else:
            self.gradient = self.ASCII
            self.ansi = False
        self.max = len(self.gradient) - 1

    def ascify(self, level):
        if np.isnan(level):
            k = 0
        else:
            k = int(self.max * level)
        if k > self.max:
            k = self.max
        if self.ansi:
            return self.gradient[k]
        else:
            return self.gradient[k]

    def render(self, spec):
        print(''.join([ self.ascify(l) for l in spec.spectrum ]))

    def demo(self):
        print("".join(self.gradient))


