# Lightshow

A quick frequency-spectrum analyser for Holiday programmable LED lights, or the command line, or anything else you care to add.

Uses the PyAudio package to read data from an audio input, and runs numpy's
FFT to generate frequency spectrum data, which it then sends to an object
implementing a method render().

This package includes two renderers:

* AsciiSpectrum writes an ascii-art spectrum to the command line as a debugging aid
* HolidaySpectrum sends colours to a set of Holiday lights over your wifi

## How to run it

./lightshow.py -i INPUT -l LIGHTS -m MODE -d DECAY -a

INPUT is the index number of the input channel. I use a USB audio
adaptor on my Pi which shows up as index # 2, but it may not be the
same on whatever device you use. I've included a little script called
devices.py which scans all the audio devices with PyAudio and dumps
them out with their index numbers to help find it

LIGHTS is the  IP address of your Holiday lights

MODE is the visualisation mode, either 'levels' or 'spectrum'. In
either mode, each light is assigned one of 50 frequency bins. For
'level' mode, the level of each frequency is mapped to a colour on the
colour gradient. In 'spectrum' mode, each light has a colour mapped
from its frequency, and the levels are used to control the light's
value (from dark to 100% bright). I think 'levels' is better.

DECAY lets you smooth out the visualisation by making lights decay
exponentially from a peak value, instead of just going dark. It's a
value between 0 and 1: the larger, the slower and smoother. Values
from 0.2 to 0.5 look good to me. If you leave it off, it's equivalent
to DECAY = 0 (ie a light goes dark as soon as its level drops)

The -a flag sends an ASCII-art visualisation of the spectrum to the
command line: it's useful for debugging if you haven't got the lights
working yet.


## Installation

The dependencies are:

* argparse
* PyAudio
* NumPy

I run the code on my Raspberry Pi and installed the dependencies using
the Raspbian packages python-pyaudio and python-numpy. I've put a
setup.py in this repo with the dependencies, but haven't tested it
yet.

# To Do

Right now it just takes input from one stereo channel. It should take
both, and give you the option of taking the average or visualising
both channels.

Keep a rolling average and adjust the scaling to the level of the
input signals

Detect pauses between songs and switch in new gradients.

Throw away some of the higher frequencies
