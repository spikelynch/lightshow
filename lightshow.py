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




parser = argparse.ArgumentParser()
parser.add_argument("-d", "--device", type=int, help="Audio input device")
parser.add_argument("-l", "--lights",  type=str, default=None, help="IP of Holiday lights")
parser.add_argument("-m", "--mode", type=str, default="levels", help="Holiday render mode", choices=[ "levels", "spectrum" ])
parser.add_argument("-a", "--ascii", action="store_true", default=False, help="Send ASCII spectrum visualisation to stdout")
                        
args = parser.parse_args()

renderers = []

if args.lights:
    renderers.append(HolidaySpectrum(args.lights, args.mode))
if args.ascii:
    renderers.append(AsciiSpectrum())

if not renderers:
    print("You need to select at least one of --lights / --ascii")
    sys.exit(-1)
    
spec = SpectrumAnalyser(args.device)

spec.run(renderers)

