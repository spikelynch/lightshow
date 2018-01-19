import gradient
from holidaysecretapi import HolidaySecretAPI

# a renderer needs to have a method 'render' which accepts a single
# list of values as an argument

class HolidaySpectrum:

    def __init__(self, addr, mode, gradients, decay):
        self.DECAY = decay
        self.holiday = HolidaySecretAPI(addr=addr)
        self.levels = [ 0.0 ] * 50
        self.mode = mode
        self.gradient = gradient.json(gradients[self.mode])
        if self.mode == 'spectrum':
            self.gradient = self.gradient[::-1] + self.gradient
        self.ngrad = len(self.gradient)
    
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
        
    def render(self, spectrum):
        """Render a frequency spectrum on the Holiday lights"""
        for i in range(50):
            l = self.decay(i, spectrum[i])
            ( r, g, b ) = self.f_col(i, l) 
            self.holiday.setglobe(i, r, g, b)
        self.holiday.render() 

    def demo(self):
        for i in range(50):
            ( r, g, b ) = self.gradient[i]
            self.holiday.setglobe(i, r, g, b)
        self.holiday.render() 

