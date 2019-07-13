#!/usr/bin/env python
# encoding: utf-8

import sys, argparse, json, re
import gradient
from spectrum import SpectrumAnalyser
from holiday import HolidaySpectrum
from text import TextSpectrum
from color_ansi_rgb import ColorANSIRGB


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
parser.add_argument("-o", "--output",  type=str, default='ansi', help="IP of Holiday lights, 'ascii' or 'ansi' for text mode")
parser.add_argument('-c', '--config', type=str, default='holiday_conf.json', help="Holiday config settings")
parser.add_argument("-m", "--mode",  type=str, default=None, help="Mode (levels/spectrum/wave)")
parser.add_argument("-g", "--gradient",  type=str, default=None, help="Colour gradient")
parser.add_argument("-d", "--demo", action="store_true", default=False, help="Demo mode: render the gradient with the map")
                        
args = parser.parse_args()

spec = SpectrumAnalyser(args.input, args.scale, NBINS, NFREQ)

config = None

with open(args.config) as gf:
    config = json.load(gf)
    if args.mode:
        config['mode'] = args.mode
    if args.gradient:
        config['gradient'] = args.gradient

if re.compile('^\d\.\d\.\d\.\d$').match(args.output):
    target = 'holiday'
else:
    target = args.output

grad = None
renderer = None

ansi = ColorANSIRGB()
 
if target == 'holiday' or target == 'ansi':
    graddef = config['gradients'][config['gradient']]
    if config['mode'] == 'spectrum':
        grad = gradient.makeGradient(target, 25, graddef)
        grad = grad[::-1] + grad
    else:    
        grad = gradient.makeGradient(target, 50, graddef)
if args.output == 'ascii' or args.output == 'ansi':
    if args.output == 'ansi':
        grad = [ ansi.rgb(c) + '█' for c in grad ]
    renderer = TextSpectrum(grad)
else:
    renderer = HolidaySpectrum(args.output, config, grad)


if args.demo:
    renderer.demo()
    if target == 'ansi':
       print(ansi.reset())
else:
    # trap keyboard interrupts and reset ANSI
    spec.run([ renderer ])

