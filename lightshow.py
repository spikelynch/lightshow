#!/usr/bin/env python
# encoding: utf-8

from spectrum import SpectrumAnalyser
from holiday import Holiday

# arguments
# - holiday:
#   - IP
# - spectrumAnalyzer
#   - audio device, etc
#
#
# - config:

parser = argparse.ArgumentParser()
parser.add_argument("-l", "--lights",  type=str, default=None, help="IP of the Holiday lights")
parser.add_argument("-m", "--mode", type=str, default="levels" help="Display mode (levels|spectrum)", choices=["levels", "spectrum"])
parser.add_argument("-d", "--device", type=int, help="Audio device")
                        
args = parser.parse_args()
holiday = Holiday(args.lights, args.mode)
spec = SpectrumAnalyser(args.device)

spec.run(holiday)

