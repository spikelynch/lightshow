#!/usr/bin/env python
# encoding: utf-8

import sys, argparse
from spectrum import SpectrumAnalyser
from holiday import HolidaySpectrum
from ascii import AsciiSpectrum


# TODO: make it easier to drop renderers into a directory without having
# to add them manually

# arguments
# - holiday:
#   - IP
# - spectrumAnalyzer
#   - audio device, etc
#
#
# - config:

NFREQ = 50


parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", type=int, help="Audio input device")
parser.add_argument("-l", "--lights",  type=str, default=None, help="IP of Holiday lights")
parser.add_argument("-m", "--mode", type=str, default="levels", help="Holiday render mode", choices=[ "levels", "spectrum" ])
parser.add_argument("-d", "--decay", type=float, default=0, help="Decay rate")
parser.add_argument("-a", "--ascii", action="store_true", default=False, help="Send ASCII spectrum visualisation to stdout")
                        
args = parser.parse_args()

spec = SpectrumAnalyser(args.input, NFREQ)

renderers = []

if args.lights:
    renderers.append(HolidaySpectrum(spec.nfreq, args.lights, args.mode, args.decay))
if args.ascii:
    renderers.append(AsciiSpectrum(spec.nfreq))

if not renderers:
    print("You need to select at least one of --lights / --ascii")
    sys.exit(-1)
    
spec.run(renderers)

