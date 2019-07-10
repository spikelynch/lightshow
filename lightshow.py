#!/usr/bin/env python
# encoding: utf-8

import sys, argparse, json
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

NBINS = 100 
NFREQ = 25 

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", type=int, help="Audio input device")
parser.add_argument("-s", "--scale", type=float, default=2.0, help="Scale input")
parser.add_argument("-l", "--lights",  type=str, default=None, help="IP of Holiday lights")
parser.add_argument('-c', '--config', type=str, default='holiday_conf.json', help="Holiday config settings")
parser.add_argument("-m", "--mode",  type=str, default=None, help="Mode (levels/spectrum/wave)")
parser.add_argument("-g", "--gradient",  type=str, default=None, help="Colour gradient")
parser.add_argument("-d", "--demo", action="store_true", default=False, help="Demo mode: render the gradient with the map")
parser.add_argument("-a", "--ascii", action="store_true", default=False, help="Send ASCII spectrum visualisation to stdout")
                        
args = parser.parse_args()

spec = SpectrumAnalyser(args.input, args.scale, NBINS, NFREQ)

renderers = []

if args.lights:
    with open(args.config) as gf:
        config = json.load(gf)
        if args.mode:
            config['mode'] = args.mode
        if args.gradient:
            config['gradient'] = args.gradient
        hs = HolidaySpectrum(args.lights, config)
        if args.demo:
            hs.demo(range(50))
            sys.exit(-1)
        else:
            renderers.append(hs)
if args.ascii:
    renderers.append(AsciiSpectrum())

if not renderers:
    print("You need to select at least one of --lights / --ascii")
    sys.exit(-1)
    
spec.run(renderers)

