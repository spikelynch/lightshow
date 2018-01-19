
import numpy as np

class AsciiSpectrum:
    """
Basic visualiser which turns a frequency spectrum into a single line
of ASCII
"""


    ASCII = " .:-=+*#%@"
    
    def __init__(self):
        self.max = max

    def ascify(self, level):
        if np.isnan(level):
            k = 0
        else:
            k = int(10.0 * level)
        if k > 9:
            k = 9
        return self.ASCII[k]

    def render(self, spectrum):
        print(''.join([ self.ascify(l) for l in spectrum ]))
