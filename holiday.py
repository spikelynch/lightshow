import gradient
from holidaysecretapi import HolidaySecretAPI

# a renderer needs to have a method 'render' which accepts a single
# list of values as an argument

class Holiday:

    def __init__(self, addr, mode):
        self.GRAD = 50
        self.holiday = HolidaySecretAPI(addr=addr)
        self.levels = [ 0.0 ] * 50
        self.mode = mode
        if self.mode == 'levels':
            self.gradient = gradient.hsvgrad(16, .66, 1, 0, .66, 1, .5)
            self.gradient += gradient.hsvgrad(17, .66, 1, 1, .33, 1, 1)
            self.gradient += gradient.hsvgrad(17, .33, 1, 1, 0, 1, 1)
            self.f_col = self.f_col_levels
        else:
            self.gradient = gradient.hsvgrad(16, 0, 1, 1, .33, 1, 1)
            self.gradient += gradient.hsvgrad(17, .33, 1, 1, .66, 1, 1)
            self.gradient += gradient.hsvgrad(17, .66, 1, 1, 1, 1, 1)
            self.f_col = self.f_col_spectrum

    def f_col_levels(self, i, level):
        k = int(level * 0.2 * self.GRAD)
        if k > self.GRAD - 1:
            k = self.GRAD - 1
        return self.gradient[k]

    def f_col_spectrum(self, i, level):
        k = level * 0.2;
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
        
    def render(self, spectrum):
        """Render a frequency spectrum on the Holiday lights"""
        for i in range(50):
            if i < 25:
                j = i + 25
            else:
                j = i - 25
            l = self.decay(i, spectrum[j])
            ( r, g, b ) = self.f_col(i, l) 
            self.holiday.setglobe(i, r, g, b)
        self.holiday.render() 

    def demo(self):
        for i in range(50):
            ( r, g, b ) = self.gradient[i]
            self.holiday.setglobe(i, r, g, b)
        self.holiday.render() 

